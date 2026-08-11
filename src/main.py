import sys
import traceback
from pathlib import Path

from controllers.process import run
from logs_setup import logging


def __run() -> None:
    """Función principal que ejecuta el flujo de trabajo del proyecto."""

    files_path = Path("path/to/excel_file1.xlsx")
    run(file_path=files_path)


if __name__ == "__main__":
    try:
        # Ejecutamos análisis solicitados
        message = "Preparando archivos para ejecutar los siguientes análisis:"
        logging(message=message, level="INFO")

        __run()

        logging(message="Datos procesados correctamente", level="INFO")
        print("Datos procesados correctamente", flush=True)

        sys.exit(0)
    except Exception as e:
        logging(message="Ocurrió un error:\n", level="ERROR")
        print(f"{e}", flush=True)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
