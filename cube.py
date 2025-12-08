# cube.py
import random

FACE_NAMES = ["U", "D", "F", "B", "L", "R"]

DEFAULT_COLORS = {
    "U": "W",  # white
    "D": "Y",  # yellow
    "F": "G",  # green
    "B": "B",  # blue
    "L": "O",  # orange
    "R": "R",  # red
}

COLOR_MAP = {
    "W": "\033[97mW\033[0m",
    "Y": "\033[93mY\033[0m",
    "G": "\033[92mG\033[0m",
    "B": "\033[94mB\033[0m",
    "O": "\033[38;5;208mO\033[0m",
    "R": "\033[91mR\033[0m",
}


class Cube:
    def __init__(self):
        self.faces = {
            name: [DEFAULT_COLORS[name]] * 9
            for name in FACE_NAMES
        }

    def copy(self):
        new = Cube.__new__(Cube)
        new.faces = {f: stickers[:] for f, stickers in self.faces.items()}
        return new

    def reset(self):
        self.faces = {
            name: [DEFAULT_COLORS[name]] * 9
            for name in FACE_NAMES
        }

    def is_solved(self) -> bool:
        return all(len(set(face)) == 1 for face in self.faces.values())

    def to_dict(self) -> dict:
        return {name: stickers[:] for name, stickers in self.faces.items()}

    def load_from_dict(self, data: dict) -> None:
        for name in FACE_NAMES:
            if name not in data:
                raise ValueError(f"Missing face {name} in data")
            if len(data[name]) != 9:
                raise ValueError(f"Face {name} must have 9 stickers")
        self.faces = {name: list(data[name]) for name in FACE_NAMES}

    def _rotate_face_cw(self, face_name: str):
        f = self.faces[face_name]
        self.faces[face_name] = [
            f[6], f[3], f[0],
            f[7], f[4], f[1],
            f[8], f[5], f[2],
        ]

    # U moves

    def move_U(self):
        self._rotate_face_cw("U")

        F = self.faces["F"]
        R = self.faces["R"]
        B = self.faces["B"]
        L = self.faces["L"]

        temp = F[0:3]
        F[0:3] = R[0:3]
        R[0:3] = B[0:3]
        B[0:3] = L[0:3]
        L[0:3] = temp

    def move_U_prime(self):
        for _ in range(3):
            self.move_U()

    def move_U2(self):
        self.move_U()
        self.move_U()

    # D moves

    def move_D(self):
        self._rotate_face_cw("D")

        F = self.faces["F"]
        R = self.faces["R"]
        B = self.faces["B"]
        L = self.faces["L"]

        temp = F[6:9]
        F[6:9] = L[6:9]
        L[6:9] = B[6:9]
        B[6:9] = R[6:9]
        R[6:9] = temp

    def move_D_prime(self):
        for _ in range(3):
            self.move_D()

    def move_D2(self):
        self.move_D()
        self.move_D()

    # R moves

    def move_R(self):
        self._rotate_face_cw("R")

        U = self.faces["U"]
        F = self.faces["F"]
        D = self.faces["D"]
        B = self.faces["B"]

        temp = [U[2], U[5], U[8]]
        U[2], U[5], U[8] = F[2], F[5], F[8]
        F[2], F[5], F[8] = D[2], D[5], D[8]
        D[2], D[5], D[8] = B[6], B[3], B[0]
        B[0], B[3], B[6] = temp[2], temp[1], temp[0]

    def move_R_prime(self):
        for _ in range(3):
            self.move_R()

    def move_R2(self):
        self.move_R()
        self.move_R()

    # L moves

    def move_L(self):
        self._rotate_face_cw("L")

        U = self.faces["U"]
        F = self.faces["F"]
        D = self.faces["D"]
        B = self.faces["B"]

        temp = [U[0], U[3], U[6]]
        U[0], U[3], U[6] = B[8], B[5], B[2]
        B[2], B[5], B[8] = D[6], D[3], D[0]
        D[0], D[3], D[6] = F[0], F[3], F[6]
        F[0], F[3], F[6] = temp

    def move_L_prime(self):
        for _ in range(3):
            self.move_L()

    def move_L2(self):
        self.move_L()
        self.move_L()

    # F moves

    def move_F(self):
        self._rotate_face_cw("F")

        U = self.faces["U"]
        L = self.faces["L"]
        D = self.faces["D"]
        R = self.faces["R"]

        temp = [U[6], U[7], U[8]]
        U[6], U[7], U[8] = L[8], L[5], L[2]
        L[2], L[5], L[8] = D[0], D[1], D[2]
        D[0], D[1], D[2] = R[6], R[3], R[0]
        R[0], R[3], R[6] = temp

    def move_F_prime(self):
        for _ in range(3):
            self.move_F()

    def move_F2(self):
        self.move_F()
        self.move_F()

    # B moves

    def move_B(self):
        self._rotate_face_cw("B")

        U = self.faces["U"]
        R = self.faces["R"]
        D = self.faces["D"]
        L = self.faces["L"]

        temp = [U[0], U[1], U[2]]
        U[0], U[1], U[2] = R[2], R[5], R[8]
        R[2], R[5], R[8] = D[8], D[7], D[6]
        D[6], D[7], D[8] = L[0], L[3], L[6]
        L[0], L[3], L[6] = temp[2], temp[1], temp[0]

    def move_B_prime(self):
        for _ in range(3):
            self.move_B()

    def move_B2(self):
        self.move_B()
        self.move_B()

    # whole cube y rotations

    def move_Y(self):
        f = self.faces
        self.faces = {
            "U": f["U"][:],
            "D": f["D"][:],
            "F": f["R"][:],
            "R": f["B"][:],
            "B": f["L"][:],
            "L": f["F"][:],
        }

    def move_Y_prime(self):
        for _ in range(3):
            self.move_Y()

    def move_Y2(self):
        self.move_Y()
        self.move_Y()

    def apply_move(self, move: str):
        if move == "U":
            self.move_U()
        elif move in ("U'", "U’"):
            self.move_U_prime()
        elif move == "U2":
            self.move_U2()
        elif move == "D":
            self.move_D()
        elif move in ("D'", "D’"):
            self.move_D_prime()
        elif move == "D2":
            self.move_D2()
        elif move == "R":
            self.move_R()
        elif move in ("R'", "R’"):
            self.move_R_prime()
        elif move == "R2":
            self.move_R2()
        elif move == "L":
            self.move_L()
        elif move in ("L'", "L’"):
            self.move_L_prime()
        elif move == "L2":
            self.move_L2()
        elif move == "F":
            self.move_F()
        elif move in ("F'", "F’"):
            self.move_F_prime()
        elif move == "F2":
            self.move_F2()
        elif move == "B":
            self.move_B()
        elif move in ("B'", "B’"):
            self.move_B_prime()
        elif move == "B2":
            self.move_B2()
        elif move == "Y":
            self.move_Y()
        elif move in ("Y'", "Y’"):
            self.move_Y_prime()
        elif move == "Y2":
            self.move_Y2()
        elif move.strip() == "":
            return
        else:
            raise ValueError(f"Move not implemented: {move!r}")

    def apply_alg(self, alg: str):
        moves = alg.split()
        for m in moves:
            self.apply_move(m)

    def random_scramble(self, length: int = 20) -> str:
        moves = [
            "U", "U'", "U2",
            "D", "D'", "D2",
            "F", "F'", "F2",
            "B", "B'", "B2",
            "L", "L'", "L2",
            "R", "R'", "R2",
        ]
        alg = " ".join(random.choice(moves) for _ in range(length))
        self.apply_alg(alg)
        return alg

    def __str__(self) -> str:
        def color(c: str) -> str:
            return COLOR_MAP.get(c, c)

        def face_rows(face):
            return [
                " ".join(color(x) for x in face[0:3]),
                " ".join(color(x) for x in face[3:6]),
                " ".join(color(x) for x in face[6:9]),
            ]

        U = face_rows(self.faces["U"])
        D = face_rows(self.faces["D"])
        F = face_rows(self.faces["F"])
        B = face_rows(self.faces["B"])
        L = face_rows(self.faces["L"])
        R = face_rows(self.faces["R"])

        lines = []
        indent = " " * 6

        for row in U:
            lines.append(indent + row)

        for i in range(3):
            lines.append(" ".join([L[i], F[i], R[i], B[i]]))

        for row in D:
            lines.append(indent + row)

        return "\n".join(lines)
