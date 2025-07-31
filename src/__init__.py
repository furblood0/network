"""
BeQuickChat - UDP Tabanlı Çok Kullanıcılı Sohbet Uygulaması

Bu modül, UDP soketleri ve özel protokol kullanarak güvenilir mesajlaşma sağlayan
modern bir sohbet uygulamasıdır.

Modüller:
    client: PyQt5 tabanlı GUI istemcisi
    server: UDP sunucu
    protocol: Mesaj protokolü ve şifreleme
"""

__version__ = "1.0.0"
__author__ = "Beyza Nur Selvi, Furkan Fidan"
__email__ = ""
__license__ = "MIT"

from . import client
from . import server
from . import protocol

__all__ = ["client", "server", "protocol"] 