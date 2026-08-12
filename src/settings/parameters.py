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
    "Nombre Cliente.1": "string",
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


# Nombre de columnas finales para el archivo
FINAL_COLUMNS = {
    "Numero OS/oth": "Numero OTH",
    "Número OP/otp": "Número OTP",
}


# Orden de columnas para el archivo
COLUMN_ORDER = [
    "Técnico",
    "Tipo de Actividad",
    "Estado",
    "Intervalos de tiempo",
    "Fecha",
    "Orden de trabajo",
    "Compañia",
    "Ciudad",
    "Numero OTH",
    "Número OTP",
    "Nombre Cliente",
    "Subtipo de Cliente (subsegmento)",
    "Notas de actividad",
]


# Archivo de salida
OUTPUT_FILE_PATH = PROJECT_ROOT / "data.xlsx"
