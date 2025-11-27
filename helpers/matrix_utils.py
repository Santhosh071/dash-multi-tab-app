import numpy as np


def parse_matrix(text: str):
    """
    Convert textarea input into a 2D NumPy array.

    Input format example:
        1,2,3
        4,5,6.5

    Supports integers and floats with '.' as decimal separator.
    """
    if text is None or text.strip() == "":
        raise ValueError("Matrix is empty.")

    rows = text.strip().split("\n")
    mat = []

    try:
        for row in rows:
            # Split by comma, strip spaces, ignore empty pieces
            parts = [p.strip() for p in row.split(",") if p.strip() != ""]
            if not parts:
                raise ValueError("Empty row detected.")
            mat.append([float(x) for x in parts])

        return np.array(mat)
    except Exception:
        raise ValueError("Invalid matrix format. Use comma-separated numeric values per row.")


def matrix_add(A, B):
    if A.shape != B.shape:
        raise ValueError("A and B must have same shape for addition.")
    return A + B


def matrix_sub(A, B):
    if A.shape != B.shape:
        raise ValueError("A and B must have same shape for subtraction.")
    return A - B


def matrix_mul(A, B):
    try:
        return A @ B
    except Exception:
        raise ValueError("Matrix multiplication shape mismatch.")


def matrix_transpose(M):
    return M.T


def matrix_det(M):
    if M.shape[0] != M.shape[1]:
        raise ValueError("Determinant requires a square matrix.")
    return float(np.linalg.det(M))
