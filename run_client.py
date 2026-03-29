"""İstemciyi başlatır.  Kullanım:  python run_client.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from client.main import main

if __name__ == "__main__":
    main()
