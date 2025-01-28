from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTextEdit, QLineEdit, QPushButton, QMessageBox, QFileDialog
from api_utils import get_ai_response

class ChatApp(QMainWindow):
    def __init__(self, provider, model, prompt):
        super().__init__()
        self.setWindowTitle("AI Chat")
        self.setGeometry(100, 100, 600, 400)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        main_layout.addWidget(self.chat_history)

        input_layout = QHBoxLayout()
        self.message_entry = QTextEdit()
        self.message_entry.setPlaceholderText("输入消息...")
        self.send_button = QPushButton("发送")
        self.send_button.clicked.connect(self.send_message)
        self.save_button = QPushButton("保存聊天记录")
        self.save_button.clicked.connect(self.save_chat_history)
        input_layout.addWidget(self.message_entry)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.save_button)
        main_layout.addLayout(input_layout)

        self.provider = provider
        self.model = model
        self.prompt = prompt

    def send_message(self):
        user_message = self.message_entry.toPlainText().strip()
        if not user_message:
            return
        self.chat_history.append(f"你: {user_message}")
        self.message_entry.clear()

        ai_response = get_ai_response(self.provider, self.model, self.prompt, user_message)
        self.chat_history.append(f"AI: {ai_response}")

    def save_chat_history(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存聊天记录", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.chat_history.toPlainText())
            QMessageBox.information(self, "提示", "聊天记录已保存")