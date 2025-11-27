import base64
import io
import pandas as pd


def parse_contents(contents: str, filename: str) -> pd.DataFrame:
    """
    Decode Dash upload 'contents' and return a pandas DataFrame.

    Supports CSV files. Integers and floats with '.' decimal points
    are parsed automatically by pandas.
    """
    if contents is None:
        raise ValueError("No file contents provided.")

    # contents looks like: "data:text/csv;base64,<base64-data>"
    try:
        content_type, content_string = contents.split(",", 1)
    except ValueError:
        raise ValueError("Could not parse file contents.")

    decoded = base64.b64decode(content_string)
    fname = filename.lower()

    if fname.endswith(".csv"):
        # Try utf-8 first; fall back to raw bytes if needed
        try:
            return pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        except UnicodeDecodeError:
            return pd.read_csv(io.BytesIO(decoded))
    else:
        raise ValueError(f"Unsupported file type: {filename}. Please upload a CSV file.")


def basic_info(df: pd.DataFrame) -> dict:
    """
    Return basic dataset info: number of rows, columns, and total missing values.
    """
    return {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "missing": int(df.isna().sum().sum()),
    }


def split_columns(df: pd.DataFrame):
    """
    Split DataFrame columns into numeric and non-numeric lists.

    Numeric includes int, float, etc. This is what we use for:
    - summary stats
    - correlation heatmap
    - 2D/3D plots
    """
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    other_cols = df.select_dtypes(exclude=["number"]).columns.tolist()
    return numeric_cols, other_cols
