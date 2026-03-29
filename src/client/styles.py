"""
Renk paleti ve QSS stil tanımları — WhatsApp tarzı koyu yeşil tema.
"""

C = {
    "bg":       "#111B21",
    "panel":    "#111B21",
    "header":   "#202C33",
    "chat_bg":  "#0B141A",
    "input_bg": "#202C33",
    "sent":     "#005C4B",
    "recv":     "#202C33",
    "text":     "#E9EDEF",
    "dim":      "#8696A0",
    "green":    "#00A884",
    "hover":    "#202C33",
    "sel":      "#2A3942",
    "blue":     "#53BDEB",
    "border":   "#2A3942",
    "red":      "#FF6B6B",
}

LOGIN_QSS = f"""
QWidget {{
    background: {C['bg']};
    color: {C['text']};
    font-family: "Segoe UI", sans-serif;
}}
QLabel#title {{
    font-size: 22px;
    font-weight: bold;
    color: {C['text']};
}}
QLabel#subtitle {{
    font-size: 13px;
    color: {C['dim']};
}}
QLabel.field {{
    font-size: 12px;
    color: {C['dim']};
}}
QLineEdit {{
    background: {C['input_bg']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 6px;
    padding: 10px 12px;
    font-size: 14px;
}}
QLineEdit:focus {{ border-color: {C['green']}; }}
QPushButton#btn_primary {{
    background: {C['green']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 12px;
    font-size: 15px;
    font-weight: bold;
}}
QPushButton#btn_primary:hover  {{ background: #00C49A; }}
QPushButton#btn_primary:disabled {{ background: #374045; color: {C['dim']}; }}
QPushButton#btn_secondary {{
    background: transparent;
    color: {C['green']};
    border: 1px solid {C['green']};
    border-radius: 6px;
    padding: 11px;
    font-size: 14px;
}}
QPushButton#btn_secondary:hover {{ background: rgba(0,168,132,0.12); }}
QPushButton#btn_secondary:disabled {{ color: {C['dim']}; border-color: {C['dim']}; }}
"""

APP_QSS = f"""
QMainWindow, QWidget {{
    background: {C['bg']};
    color: {C['text']};
    font-family: "Segoe UI", sans-serif;
}}
QScrollBar:vertical {{
    background: transparent; width: 5px; margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #374045; border-radius: 2px; min-height: 24px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QSplitter::handle {{ background: {C['border']}; width: 1px; }}
QLineEdit {{
    background: {C['input_bg']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 14px;
}}
QLineEdit:focus {{ border-color: {C['green']}; }}
QPushButton#btn_send {{
    background: {C['green']};
    border: none;
    border-radius: 20px;
    color: white;
    font-size: 16px;
    font-weight: bold;
    min-width: 44px;
    min-height: 44px;
    max-width: 44px;
    max-height: 44px;
}}
QPushButton#btn_send:hover {{ background: #00C49A; }}
QPushButton#btn_logout {{
    background: transparent;
    border: none;
    color: {C['dim']};
    font-size: 18px;
    padding: 4px;
}}
QPushButton#btn_logout:hover {{ color: {C['red']}; }}
"""
