"""
Uygulama genelinde kullanılan sabitler ve yapılandırma değerleri.
"""

from pathlib import Path

HOST = "0.0.0.0"
PORT = 9000
DEFAULT_HOST = "158.180.59.29"

PUBLIC = "__public__"
WINDOW_TITLE = "NetChat"

ASSET_DIR = Path(__file__).parent.parent / "assets"
DB_PATH = Path(__file__).parent.parent / "chat.db"
