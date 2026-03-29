"""Sunucuyu başlatır.  Kullanım:  python run_server.py"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from server.main import main

if __name__ == "__main__":
    asyncio.run(main())
