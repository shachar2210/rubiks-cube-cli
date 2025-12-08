# main.py
import argparse
import json
import os
from cube import Cube
from PIL import Image, ImageDraw

move_history = []
ALGO_FILE = "algos.json"

def parse_args():
    parser = argparse.ArgumentParser(description="Rubik's Cube 3x3 simulator")
    parser.add_argument(
        "--scramble",
        type=int,
        help="Apply random scramble of given length before starting",
    )
    parser.add_argument(
        "--apply",
        type=str,
        help="Apply an algorithm string like \"R U R' U'\" before starting",
    )
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Do not enter interactive mode, just apply options and exit",
    )
    parser.add_argument(
        "--load",
        type=str,
        help="Load cube state from JSON file",
    )
    parser.add_argument(
        "--save",
        type=str,
        help="Save cube state to JSON file",
    )
    return parser.parse_args()

def load_algos() -> dict:
    if not os.path.exists(ALGO_FILE):
        return {}
    try:
        with open(ALGO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items()}
        return {}
    except Exception:
        return {}

def save_algos(algos: dict) -> None:
    try:
        with open(ALGO_FILE, "w", encoding="utf-8") as f:
            json.dump(algos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to save algorithms: {e}")

def export_cube_image(cube: Cube, filename: str):
    # each sticker is a square
    size = 40
    cols = 12
    rows = 9
    width = cols * size
    height = rows * size
    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)
    color_map = {
        "W": (255, 255, 255),
        "Y": (255, 255, 0),
        "G": (0, 200, 0),
        "B": (0, 100, 255),
        "O": (255, 140, 0),
        "R": (255, 0, 0),
    }
    faces = cube.faces

    def draw_face(face, base_row, base_col):
        for i in range(9):
            r = i // 3
            c = i % 3
            gr = base_row + r  # global row
            gc = base_col + c  # global col
            x1 = gc * size
            y1 = gr * size
            x2 = x1 + size
            y2 = y1 + size
            draw.rectangle([x1, y1, x2, y2], fill=color_map[face[i]])
    # layout (same as text view):
    # U on top, L F R B in the middle row, D at bottom
    draw_face(faces["U"], 0, 3)   # rows 0-2, cols 3-5
    draw_face(faces["L"], 3, 0)   # rows 3-5, cols 0-2
    draw_face(faces["F"], 3, 3)   # rows 3-5, cols 3-5
    draw_face(faces["R"], 3, 6)   # rows 3-5, cols 6-8
    draw_face(faces["B"], 3, 9)   # rows 3-5, cols 9-11
    draw_face(faces["D"], 6, 3)   # rows 6-8, cols 3-5
    img.save(filename)
    print(f"Exported cube image to {filename}")

def invert_alg_string(alg: str) -> str:
    moves = alg.split()
    inv_moves: list[str] = []

    for m in reversed(moves):
        if not m:
            continue
        base = m[0]
        suffix = m[1:]

        if suffix == "2":
            inv_moves.append(m)
        elif suffix in ("'", "’"):
            inv_moves.append(base)
        elif suffix == "":
            inv_moves.append(base + "'")
        else:
            inv_moves.append(m)
    return " ".join(inv_moves)

def print_state(cube: Cube):
    print("\nCurrent cube state:\n")
    print(cube)
    print(f"Solved? {cube.is_solved()}")
    print("-" * 40)

def interactive_loop(cube: Cube, algos: dict):
    print_state(cube)

    while True:
        cmd = input(
            "Enter moves (e.g. \"R U R' U2\", 'scramble', 'scramble 30', "
            "'help', or 'quit'): "
        ).strip()

        if not cmd:
            continue

        parts = cmd.split()
        lowered = parts[0].lower()

        if lowered in ("quit", "exit", "q"):
            print("Bye :)")
            break

        elif lowered == "save":
            if len(parts) != 2:
                print("Usage: save <filename>")
            else:
                filename = parts[1]
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(cube.to_dict(), f)
                    print(f"Saved cube state to {filename}")
                except Exception as e:
                    print(f"Failed to save state: {e}")

        elif lowered == "load":
            if len(parts) != 2:
                print("Usage: load <filename>")
            else:
                filename = parts[1]
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    cube.load_from_dict(data)
                    move_history.clear()
                    print(f"Loaded cube state from {filename}")
                except Exception as e:
                    print(f"Failed to load state: {e}")

        elif lowered == "define":
            if len(parts) < 3:
                print("Usage: define <name> <moves...>")
            else:
                name = parts[1]
                alg = " ".join(parts[2:])
                algos[name] = alg
                save_algos(algos)
                print(f"Saved algorithm '{name}': {alg}")

        elif lowered == "run":
            if len(parts) != 2:
                print("Usage: run <name>")
            else:
                name = parts[1]
                if name not in algos:
                    print(f"No algorithm named '{name}'")
                else:
                    alg = algos[name]
                    print(f"Running '{name}': {alg}")
                    try:
                        cube.apply_alg(alg)
                        move_history.extend(alg.split())
                    except ValueError as e:
                        print(e)


        elif lowered in ("algos", "list_algos"):
            if not algos:
                print("No saved algorithms.")
            else:
                print("Saved algorithms:")
                for name, alg in algos.items():
                    print(f"- {name}: {alg}")

        elif lowered == "undef":
            if len(parts) != 2:
                print("Usage: undef <name>")
            else:
                name = parts[1]
                if name in algos:
                    del algos[name]
                    save_algos(algos)
                    print(f"Deleted algorithm '{name}'")
                else:
                    print(f"No algorithm named '{name}'")

        elif lowered == "undo":
            if len(move_history) == 0:
                print("No moves to undo.")
            else:
                last = move_history.pop()
                inv = invert_alg_string(last)
                cube.apply_alg(inv)
                print(f"Undid: {last}")

        elif lowered == "clear":
            cube.reset()
            move_history.clear()
            print("Cube cleared to solved state.")

        elif lowered == "invert":
            if len(parts) < 2:
                print("Usage: invert <moves...> OR invert <saved_name>")
            else:
                # case 1: invert a saved algorithm by name
                if len(parts) == 2 and parts[1] in algos:
                    name = parts[1]
                    orig = algos[name]
                    inv = invert_alg_string(orig)
                    print(f"Inverted '{name}': {inv}")
                else:
                    # case 2: invert raw moves written by the user
                    orig = " ".join(parts[1:])
                    inv = invert_alg_string(orig)
                    print(f"Inverted: {inv}")

        elif lowered == "history":
            if not move_history:
                print("History is empty.")
            else:
                print("Move history:")
                for i, m in enumerate(move_history, 1):
                    print(f"{i}. {m}")

        elif lowered == "export":
            if len(parts) != 2:
                print("Usage: export <filename.png>")
            else:
                export_cube_image(cube, parts[1])

        elif lowered.startswith("scramble"):
            if len(parts) == 2 and parts[1].isdigit():
                length = int(parts[1])
            else:
                length = 20
            alg = cube.random_scramble(length)
            print(f"Scramble: {alg}")
            move_history.extend(alg.split())

        elif lowered == "help":
            print("""
        Available commands:
          MOVE SEQUENCE          Apply moves (e.g. R U R' U2)
          scramble [n]           Scramble cube (default 20)
          define name alg        Save an algorithm
          run name               Run saved algorithm
          algos                  List saved algorithms
          undef name             Delete saved algorithm
          invert <alg|name>      Show inverse of an algorithm
          undo                   Undo last move
          history                Show move history
          clear                  Reset cube to solved state
          save file.json         Save cube state
          load file.json         Load cube state
          export file.png        Export cube as PNG image
          help                   Show this help
          quit                   Exit program
        """)

        else:
            try:
                cube.apply_alg(cmd)
                move_history.extend(cmd.split())
            except ValueError as e:
                print(e)

        print_state(cube)

def main():
    args = parse_args()
    cube = Cube()
    algos = load_algos()

    if args.load:
        try:
            with open(args.load, "r", encoding="utf-8") as f:
                data = json.load(f)
            cube.load_from_dict(data)
            print(f"Loaded cube state from {args.load}")
        except Exception as e:
            print(f"Failed to load state from {args.load}: {e}")

    if args.scramble is not None:
        alg = cube.random_scramble(args.scramble)
        print(f"Initial scramble ({args.scramble} moves): {alg}")

    if args.apply:
        try:
            cube.apply_alg(args.apply)
            print(f"Applied algorithm: {args.apply}")
        except ValueError as e:
            print(e)

    if args.save:
        try:
            with open(args.save, "w", encoding="utf-8") as f:
                json.dump(cube.to_dict(), f)
            print(f"Saved cube state to {args.save}")
        except Exception as e:
            print(f"Failed to save state to {args.save}: {e}")

    if args.no_interactive:
        print_state(cube)
        return

    interactive_loop(cube, algos)


if __name__ == "__main__":
    main()
