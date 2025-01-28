import sys
from PyQt5.QtWidgets import QApplication
from font_utils import setup_font
from start_app import StartApp
from api_utils import load_api_providers

if __name__ == "__main__":
    providers = load_api_providers()

    app = QApplication(sys.argv)

    setup_font()

    start_app = StartApp(providers)  # 传递providers
    start_app.show()
    sys.exit(app.exec_())