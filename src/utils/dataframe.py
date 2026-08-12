import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Literal

import pandas as pd


def filter_df(
    df: pd.DataFrame,
    filters: dict[str, Any],
    global_combine: Literal["and", "or"] = "and",
) -> pd.DataFrame:
    """
    Filtra un DataFrame calculando las máscaras por bloque (include, exclude, contains)
    y permitiendo lógica AND/OR tanto a nivel de bloque (local) como entre bloques (global).
    """

    def __is_iterable(value: Any) -> bool:

        return isinstance(value, Iterable) and not isinstance(value, str)

    def __combine_masks(mask1: Any, mask2: Any, combine_method: str) -> Any:

        if mask1 is None:
            return mask2

        return mask1 & mask2 if combine_method == "and" else mask1 | mask2

    def __validate_column(field: str) -> None:

        if field not in df.columns:
            raise KeyError(f"Error crítico en filtro: La columna '{field}' no existe.")

    final_mask = None

    # Procesar cada categoría de filtro admitida
    for filter_type in ["include", "exclude", "contains"]:
        if filter_type not in filters:
            continue

        block_data = filters[filter_type]

        # Soportar la nueva estructura con 'fields' y 'combine'
        if isinstance(block_data, dict) and "fields" in block_data:
            fields = block_data["fields"]
            local_combine = block_data.get("combine", "and")
        else:
            # Fallback por si envían el dict plano (retrocompatibilidad)
            fields = block_data
            local_combine = "and"

        block_mask = None

        for field, value in fields.items():
            __validate_column(field)

            if filter_type == "include":
                if __is_iterable(value):  # noqa
                    mask = df[field].isin(value)
                else:
                    mask = df[field] == value
            elif filter_type == "exclude":
                if __is_iterable(value):  # noqa
                    mask = ~df[field].isin(value)
                else:
                    mask = df[field] != value
            elif filter_type == "contains":
                series = df[field].astype("string")
                if __is_iterable(value):
                    # Un array en 'contains' siempre debería ser evaluado como un OR interno
                    mask = None
                    for v in value:
                        v_mask = series.str.contains(str(v), regex=False, na=False)
                        mask = v_mask if mask is None else mask | v_mask
                else:
                    mask = series.str.contains(str(value), regex=False, na=False)

            # Combinamos la máscara generada con la máscara acumulada del bloque
            block_mask = __combine_masks(block_mask, mask, local_combine)  # type: ignore

        # Si el bloque generó una máscara, la combinamos con la máscara final del DF
        if block_mask is not None:
            final_mask = __combine_masks(final_mask, block_mask, global_combine)

    # Si no se aplicó ningún filtro válido, retornar el DF original
    if final_mask is None:
        return df

    return df[final_mask]  # type: ignore


def drop_duplicate_columns(
    df: pd.DataFrame,
    target_column: str,
    *,
    treat_empty_strings: bool = True,
    consider_empty_spaces: bool = True,
    inplace: bool = False,
) -> pd.DataFrame:

    if not inplace:
        df = df.copy()

    pattern = re.compile(rf"^{re.escape(target_column)}(?:\.(\d+))?$")
    family = [c for c in df.columns if pattern.fullmatch(c)]

    if not family:
        return df

    def __column_is_empty(serie: pd.Series) -> bool:
        s = serie

        if treat_empty_strings and s.dtype == "object":
            if consider_empty_spaces:
                s = s.replace(r"^\s*$", pd.NA, regex=True)
            else:
                s = s.replace("", pd.NA)

        return not s.notna().any()

    # 1) Identificar vacías y no vacías.
    empty_columns = [c for c in family if __column_is_empty(serie=df[c])]
    not_empty_columns = [c for c in family if c not in empty_columns]

    # 2) Eliminar columnas vacías.
    if empty_columns:
        df.drop(columns=empty_columns, inplace=True)

    # 3) Si la columna restante en su nombre tiene sufijo, renombrar al base.
    if len(not_empty_columns) == 1:
        remaining_column = not_empty_columns[0]

        if remaining_column != target_column:
            if target_column not in df.columns:
                df.rename(columns={remaining_column: target_column}, inplace=True)
            else:
                # Por seguridad, evitamos sobreescribir una columna existente.
                pass

    return df


def normalize_date(df: pd.DataFrame, column: str, input_format: str) -> pd.DataFrame:
    """
    Normaliza una columna de fechas según el formato de entrada y devuelve el
    DataFrame con:
    - La columna `column` en formato `dd/mm/yyyy`.
    """

    df = df.copy()

    # Limpieza ligera si es texto
    if pd.api.types.is_string_dtype(df[column]):
        df[column] = df[column].str.strip()

    # Mapear a strptime
    fmt_map = {
        "dd/mm/yy": "%d/%m/%y",
        "mm/dd/yy": "%m/%d/%y",
        "dd/mm/yyyy": "%d/%m/%Y",
        "mm/dd/yyyy": "%m/%d/%Y",
    }
    key = (input_format or "").strip().lower()

    if key not in fmt_map:
        allowed = ", ".join(fmt_map.keys())

        raise ValueError(f"input_format inválido: '{input_format}'. Use uno de: {allowed}")

    in_fmt = fmt_map[key]

    # Parseo a datetime
    if pd.api.types.is_datetime64_any_dtype(df[column]):
        dates = pd.to_datetime(df[column], errors="coerce")
    else:
        dates = pd.to_datetime(df[column], format=in_fmt, errors="coerce")

    # Formateo estándar de salida dd/mm/yyyy (texto)
    df[column] = dates.dt.strftime("%d/%m/%Y")

    return df


def create_file(df: pd.DataFrame, path: Path, datetime_format: str | None = None) -> None:
    # 1. Dimensiones del DataFrame
    num_rows, num_columns = df.shape

    # Lista de nombres de columnas para los encabezados de la tabla
    columns = [{"header": col} for col in df.columns]

    with pd.ExcelWriter(
        path=path,
        engine="xlsxwriter",
        datetime_format=datetime_format,
    ) as writer:
        sheet_name = "DATOS"

        # 2. Volcamos los datos empezando en la fila 1 (dejamos la 0 para el encabezado)
        df.to_excel(
            excel_writer=writer,
            sheet_name=sheet_name,
            index=False,
            header=False,
            startrow=1,
        )

        # 3. Accedemos a los objetos internos de XlsxWriter
        worksheet = writer.sheets[sheet_name]

        # 4. Creamos la tabla sobre el rango de datos
        worksheet.add_table(
            0,
            0,
            num_rows,
            num_columns - 1,
            {
                "name": "Datos",
                "columns": columns,
                "style": None,
            },
        )


def reorder_columns(df: pd.DataFrame, order: list[str]) -> pd.DataFrame:

    return df.loc[:, order]
