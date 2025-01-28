from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton
from api_utils import load_api_providers
from chat_app import ChatApp

class StartApp(QMainWindow):
    def __init__(self, providers):
        super().__init__()
        self.setWindowTitle("选择 API 提供方和模型")
        self.setGeometry(100, 100, 400, 300)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        provider_label = QLabel("选择 API 提供方:")
        self.provider_dropdown = QComboBox()
        self.provider_dropdown.addItems([p["name"] for p in providers])
        self.provider_dropdown.currentIndexChanged.connect(self.update_model_dropdown)
        main_layout.addWidget(provider_label)
        main_layout.addWidget(self.provider_dropdown)

        model_label = QLabel("选择模型:")
        self.model_dropdown = QComboBox()
        main_layout.addWidget(model_label)
        main_layout.addWidget(self.model_dropdown)

        prompt_label = QLabel("输入提示词:")
        self.prompt_entry = QLineEdit()
        self.prompt_entry.setText("你是一个AI智能个人助理")
        main_layout.addWidget(prompt_label)
        main_layout.addWidget(self.prompt_entry)

        start_button = QPushButton("启动聊天")
        start_button.clicked.connect(self.start_chat)
        main_layout.addWidget(start_button)

        self.providers = providers  # 保存providers以便后续使用
        self.update_model_dropdown()

    def update_model_dropdown(self):
        selected_provider_name = self.provider_dropdown.currentText()
        selected_provider = next((p for p in self.providers if p["name"] == selected_provider_name), None)

        self.model_dropdown.clear()
        if selected_provider:
            self.model_dropdown.addItems(selected_provider["models"])

    def start_chat(self):
        provider_name = self.provider_dropdown.currentText()
        model_name = self.model_dropdown.currentText()
        prompt = self.prompt_entry.text().strip()

        if not provider_name:
            QMessageBox.warning(self, "错误", "请选择一个 API 提供方")
            return

        if not model_name:
            QMessageBox.warning(self, "错误", "请选择一个模型")
            return

        if not prompt:
            QMessageBox.warning(self, "错误", "提示词不能为空")
            return

        selected_provider = next((p for p in self.providers if p["name"] == provider_name), None)

        if model_name not in selected_provider["models"]:
            QMessageBox.warning(self, "错误", "选择的模型不属于当前 API 提供方")
            return

        self.chat_app = ChatApp(selected_provider, model_name, prompt)
        self.chat_app.show()
        self.close()