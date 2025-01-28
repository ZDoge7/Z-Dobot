from PyQt5.QtGui import QFontDatabase

def setup_font():
    font_db = QFontDatabase()
    font_db.addApplicationFont("C:\\Windows\\Fonts\\simsun.ttc")