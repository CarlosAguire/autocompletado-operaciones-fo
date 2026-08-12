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


def get_excel_files(folder_path: Path) -> list[Path]:
    """
    Recibe la ruta de una carpeta y retorna una lista con los
    objetos `Path` de todos los archivos .xlsx que contiene.
    """

    # Validar que la ruta sea realmente una carpeta
    if not folder_path.is_dir():
        raise NotADirectoryError(f"La ruta proporcionada no es una carpeta válida: {folder_path}")

    return list(folder_path.glob("*.xlsx"))
