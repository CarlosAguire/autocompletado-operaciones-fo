import warnings
from pathlib import Path

import pandas as pd


def read_xlsx_file(path: Path, sheet: int | str, dtype: dict[str, str]) -> pd.DataFrame:
    """
    Lee una hoja de Excel.
    - No se recortan espacios.
    - No se cambian mayúsculas/minúsculas.
    - No se normalizan caracteres.
    """

    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message="Data Validation extension is not supported",
    )

    return pd.read_excel(
        io=path,
        sheet_name=sheet,
        engine="openpyxl",
        usecols=list(dtype.keys()),
        dtype=dtype,
    )
