import sys
import traceback

from controllers.process import run
from logs_setup import logging
from settings.parameters import DATA_FOLDER
from utils.files import get_excel_files


def __run() -> None:
    """Función principal que ejecuta el flujo de trabajo del proyecto."""

    file_path = get_excel_files(folder_path=DATA_FOLDER)[0]
    run(file_path=file_path)


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
