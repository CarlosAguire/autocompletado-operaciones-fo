from pathlib import Path

import pandas as pd

from logs_setup import logging
from settings import parameters
from utils.dataframe import create_file, drop_duplicate_columns, filter_df, normalize_date
from utils.files import read_xlsx_file


def __prepare_file_output(df: pd.DataFrame) -> None:

    message = f"Iniciando limpieza: {df.attrs['file_path']}"
    logging(message=message, level="INFO")

    # Filtramos para eliminar filas que no necesitamos
    cleaned_df = filter_df(filters=parameters.FILTERS, df=df)

    if cleaned_df.empty:
        return None

    # Removemos columnas duplicadas
    cleaned_df = drop_duplicate_columns(target_column="Ciudad", df=cleaned_df)

    # Normalizamos la columna de fecha
    cleaned_df = normalize_date(
        df=cleaned_df,
        column="Fecha",
        input_format="mm/dd/yy",
    )

    # Creamos el archivo de salida
    create_file(df=cleaned_df, path=parameters.OUTPUT_FILE_PATH)

    message = f"Archivo creado: {parameters.OUTPUT_FILE_PATH}"
    logging(message=message, level="INFO")


def run(file_path: Path) -> None:
    message = "Preparando limpieza de los archivos"
    logging(message=message, level="INFO")

    # Leemos el archivo
    df = read_xlsx_file(path=file_path, sheet=0, dtype=parameters.FO_TYPES)
    df.attrs["file_path"] = file_path

    # Preparamos y creamos los archivos de salida
    __prepare_file_output(df=df)

    logging(message="Limpieza completada", level="INFO")
