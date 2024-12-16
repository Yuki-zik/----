from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import hashlib
import json
import os

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.login_attempts = 0
        self.max_attempts = 3
        self.load_users()
        self.initUI()

    def load_users(self):
        """加载用户数据"""
        self.users = {}
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                self.users = json.load(f)

    def save_users(self):
        """保存用户数据"""
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

    def hash_password(self, password):
        """密码加密"""
        return hashlib.sha256(password.encode()).hexdigest()

    def initUI(self):
        self.setWindowTitle('登录验证')
        self.setFixedSize(1000, 1200)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Microsoft YaHei;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 18px;
                margin: 8px 0;
                min-height: 45px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
            QPushButton {
                padding: 12px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 18px;
                min-height: 50px;
                margin: 10px 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
            QLabel {
                font-size: 18px;
                color: #333;
                margin: 8px 0;
            }
        """)

        # 创建布局
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        # 标题
        title = QtWidgets.QLabel('用户登录')
        title.setStyleSheet("""
            font-size: 36px;
            color: #1976D2;
            font-weight: bold;
            margin: 30px 0;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # 用户名输入
        self.username_label = QtWidgets.QLabel('用户名:')
        self.username_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.username_label)
        
        self.username_edit = QtWidgets.QLineEdit()
        self.username_edit.setPlaceholderText('请输入用户名')
        layout.addWidget(self.username_edit)

        # 密码输入
        self.password_label = QtWidgets.QLabel('密码:')
        self.password_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.password_label)
        
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setPlaceholderText('请输入密码')
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_edit.textChanged.connect(self.on_password_changed)
        layout.addWidget(self.password_edit)

        # 按钮区域
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(20)
        
        self.login_button = QtWidgets.QPushButton('登录')
        self.login_button.setFixedHeight(55)
        self.login_button.clicked.connect(self.login)
        button_layout.addWidget(self.login_button)
        
        self.register_button = QtWidgets.QPushButton('注册')
        self.register_button.setFixedHeight(55)
        self.register_button.clicked.connect(self.register)
        button_layout.addWidget(self.register_button)
        
        layout.addLayout(button_layout)

        # 状态提示
        self.status_label = QtWidgets.QLabel()
        self.status_label.setStyleSheet("""
            color: #666;
            font-size: 18px;
            min-height: 60px;
            margin-top: 20px;
            padding: 10px;
        """)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        # 设置主布局
        self.setLayout(layout)

    def on_password_changed(self, text):
        """密码输入变化时的处理"""
        if len(text) > 0:
            displayed_text = text[-1]  # 保留最新输入的字符
            masked_text = '*' * (len(text) - 1) + displayed_text  # 之前的字符用*代替
            self.password_edit.setText(masked_text)
            self.password_edit.setCursorPosition(len(masked_text))

    def login(self):
        """登录处理"""
        if self.login_attempts >= self.max_attempts:
            self.status_label.setText("登录次数超限，请等待30秒后重试")
            self.status_label.setStyleSheet("color: #F44336; font-size: 18px;")
            return

        username = self.username_edit.text()
        password = self.password_edit.text()

        if not username or not password:
            self.status_label.setText("用户名和密码不能为空")
            self.status_label.setStyleSheet("color: #F44336; font-size: 18px;")
            return

        hashed_password = self.hash_password(password)
        if username in self.users and self.users[username] == hashed_password:
            self.status_label.setText("登录成功！")
            self.status_label.setStyleSheet("color: #4CAF50; font-size: 18px;")
            self.login_attempts = 0
        else:
            self.login_attempts += 1
            remaining = self.max_attempts - self.login_attempts
            self.status_label.setText(f"用户名或密码错误，还剩{remaining}次机会")
            self.status_label.setStyleSheet("color: #F44336; font-size: 18px;")
            if remaining == 0:
                self.login_button.setEnabled(False)
                QtCore.QTimer.singleShot(30000, self.reset_attempts)  # 30秒后重置

    def register(self):
        """注册处理"""
        username = self.username_edit.text()
        password = self.password_edit.text()

        if not username or not password:
            self.status_label.setText("用户名和密码不能为空")
            self.status_label.setStyleSheet("color: #F44336; font-size: 18px;")
            return

        if username in self.users:
            self.status_label.setText("用户名已存在")
            self.status_label.setStyleSheet("color: #F44336; font-size: 18px;")
            return

        self.users[username] = self.hash_password(password)
        self.save_users()
        self.status_label.setText("注册成功！")
        self.status_label.setStyleSheet("color: #4CAF50; font-size: 18px;")

    def reset_attempts(self):
        """重置登录尝试次数"""
        self.login_attempts = 0
        self.login_button.setEnabled(True)
        self.status_label.setText("可以重新登录了")
        self.status_label.setStyleSheet("color: #666; font-size: 18px;")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_()) 
