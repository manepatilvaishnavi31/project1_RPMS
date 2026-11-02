import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "rpms_user"),
    "password": os.getenv("DB_PASSWORD", "Rpms@12345"),
    "database": os.getenv("DB_NAME", "rpms_db"),
}
