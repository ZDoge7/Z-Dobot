import sys
import json
import os
import threading
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTextEdit, QLineEdit, QPushButton, QMessageBox, QFileDialog
from PyQt5.QtGui import QFontDatabase
from openai import OpenAI

# 设置支持中文字体
def setup_font():
    font_db = QFontDatabase()
    font_db.addApplicationFont("C:\\Windows\\Fonts\\simsun.ttc")

# 加载 API 提供方信息
def load_api_providers():
    providers = []
    for file_name in os.listdir("."):
        if file_name.endswith(".json") and file_name != "api_providers.json":
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    provider = json.load(f)
                    providers.append(provider)
            except json.JSONDecodeError as e:
                print(f"解析 JSON 文件 {file_name} 时出错：{e}")
            except Exception as e:
                print(f"读取文件 {file_name} 时出错：{e}")
    return providers

# 调用 API 获取 AI 回复
def get_ai_response(provider, model, prompt, user_message):
    try:
        client = OpenAI(
            api_key=provider["api_key"],
            base_url=provider["base_url"]
        )
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            top_p=0.7,
            temperature=0.9
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"网络错误，请检查您的 API 地址和密钥。错误信息：{e}"

# 启动聊天界面
class ChatApp(QMainWindow):
    def __init__(self, provider, model, prompt):
        super().__init__()
        self.setWindowTitle("AI Chat")
        self.setGeometry(100, 100, 600, 400)

        # 主窗口布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 聊天框
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        main_layout.addWidget(self.chat_history)

        # 输入框和发送按钮
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

        # 初始化 API 客户端
        self.provider = provider
        self.model = model
        self.prompt = prompt

    def send_message(self):
        user_message = self.message_entry.toPlainText().strip()
        if not user_message:
            return
        self.chat_history.append(f"你: {user_message}")
        self.message_entry.clear()

        # 获取 AI 回复
        ai_response = get_ai_response(self.provider, self.model, self.prompt, user_message)
        self.chat_history.append(f"AI: {ai_response}")

    def save_chat_history(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存聊天记录", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.chat_history.toPlainText())
            QMessageBox.information(self, "提示", "聊天记录已保存")

# 启动界面
class StartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("选择 API 提供方和模型")
        self.setGeometry(100, 100, 400, 300)

        # 主窗口布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 提供方选择
        provider_label = QLabel("选择 API 提供方:")
        self.provider_dropdown = QComboBox()
        self.provider_dropdown.addItems([p["name"] for p in providers])
        self.provider_dropdown.currentIndexChanged.connect(self.update_model_dropdown)
        main_layout.addWidget(provider_label)
        main_layout.addWidget(self.provider_dropdown)

        # 模型选择
        model_label = QLabel("选择模型:")
        self.model_dropdown = QComboBox()
        main_layout.addWidget(model_label)
        main_layout.addWidget(self.model_dropdown)

        # 提示词输入
        prompt_label = QLabel("输入提示词:")
        self.prompt_entry = QLineEdit()
        self.prompt_entry.setText("你是一个AI智能个人助理")
        main_layout.addWidget(prompt_label)
        main_layout.addWidget(self.prompt_entry)

        # 启动按钮
        start_button = QPushButton("启动聊天")
        start_button.clicked.connect(self.start_chat)
        main_layout.addWidget(start_button)

        # 确保默认提供方的模型列表正确加载
        self.update_model_dropdown()

    def update_model_dropdown(self):
        # 获取当前选择的提供方
        selected_provider_name = self.provider_dropdown.currentText()
        selected_provider = next((p for p in providers if p["name"] == selected_provider_name), None)

        # 更新模型下拉框
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

        # 获取选定的提供方信息
        selected_provider = next((p for p in providers if p["name"] == provider_name), None)

        # 检查模型是否属于当前提供方
        if model_name not in selected_provider["models"]:
            QMessageBox.warning(self, "错误", "选择的模型不属于当前 API 提供方")
            return

        # 进入聊天界面
        self.chat_app = ChatApp(selected_provider, model_name, prompt)
        self.chat_app.show()
        self.close()

# 主程序
if __name__ == "__main__":
    # 加载 API 提供方信息
    providers = load_api_providers()

    # 创建 QApplication 实例
    app = QApplication(sys.argv)

    # 设置字体
    setup_font()

    # 启动应用
    start_app = StartApp()
    start_app.show()
    sys.exit(app.exec_())
