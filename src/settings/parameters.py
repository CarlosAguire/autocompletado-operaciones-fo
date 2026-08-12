from pathlib import Path

# Configuración de ruta raíz del proyecto
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parent.parent.parent


# Configuraciónes y rutas de archivos
DATA_FOLDER = PROJECT_ROOT / "data"


# Columnas y tipos requeridos para cada archivo
FO_TYPES = {
    "Técnico": "string",
    "Estado": "string",
    "Nombre Cliente": "string",
    "Numero OS/oth": "string",
    "Número OP/otp": "string",
    "Tipo de Actividad": "string",
    "Intervalos de tiempo": "string",
    "Fecha": "string",
    "Orden de trabajo": "string",
    "Ciudad": "string",
    "Ciudad.1": "string",
    "Ciudad.2": "string",
    "Ciudad.3": "string",
    "Ciudad.4": "string",
    "Ciudad.5": "string",
    "Subtipo de Cliente (subsegmento)": "string",
    "Compañia": "string",
    "Notas de actividad": "string",
}


# Filtros para el archivo
FILTERS = {
    "exclude": {
        "Tipo de Actividad": ["Almuerzo", "Actividades de Almacen"],
    },
}


# Archivo de salida
OUTPUT_FILE_PATH = PROJECT_ROOT / "data.xlsx"
