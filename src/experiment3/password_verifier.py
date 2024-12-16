from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import random
import hashlib
import json
import os

class SliderVerification(QtWidgets.QWidget):
    verified = QtCore.pyqtSignal(bool)  # 验证成功信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.reset()

    def initUI(self):
        self.setFixedSize(300, 200)
        self.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)

        # 创建滑块区域
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setFixedSize(280, 40)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setStyleSheet("""
            QSlider {
                border: none;
            }
            QSlider::groove:horizontal {
                height: 30px;
                background: #f0f0f0;
                border-radius: 15px;
            }
            QSlider::handle:horizontal {
                width: 40px;
                background: #2196F3;
                border-radius: 15px;
                margin: -5px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #1976D2;
            }
        """)

        # 创建图片区域
        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setFixedSize(280, 120)
        self.imageLabel.setStyleSheet("border: 1px solid #ddd; background: #f5f5f5;")

        # 创建提示文本
        self.tipLabel = QtWidgets.QLabel("滑动滑块完成验证")
        self.tipLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tipLabel.setStyleSheet("""
            color: #666;
            font-size: 14px;
            padding: 5px;
        """)

        # 布局
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.imageLabel)
        layout.addWidget(self.slider)
        layout.addWidget(self.tipLabel)
        layout.setContentsMargins(10, 10, 10, 10)

        # 连接信号
        self.slider.sliderPressed.connect(self.onSliderPressed)
        self.slider.sliderReleased.connect(self.onSliderReleased)
        self.slider.valueChanged.connect(self.onSliderMoved)

    def reset(self):
        """重置验证器状态"""
        self.slider.setValue(0)
        self.target_pos = random.randint(30, 70)  # 随机目标位置
        self.verified.emit(False)
        self.tipLabel.setText("滑动滑块完成验证")
        self.tipLabel.setStyleSheet("color: #666;")
        self.drawVerificationImage()

    def drawVerificationImage(self):
        """绘制验证图片"""
        pixmap = QtGui.QPixmap(280, 120)
        pixmap.fill(QtGui.QColor("#f5f5f5"))
        painter = QtGui.QPainter(pixmap)
        
        # 绘制背景图案
        painter.setPen(QtGui.QPen(QtGui.QColor("#ddd"), 1))
        for i in range(0, 280, 20):
            painter.drawLine(i, 0, i, 120)
        for i in range(0, 120, 20):
            painter.drawLine(0, i, 280, i)

        # 绘制目标区域
        target_x = int(280 * self.target_pos / 100)
        painter.fillRect(target_x-20, 40, 40, 40, QtGui.QColor("#2196F3"))
        painter.end()
        
        self.imageLabel.setPixmap(pixmap)

    def onSliderPressed(self):
        """滑块按下时的处理"""
        self.tipLabel.setText("请对准蓝色方块位置...")
        self.tipLabel.setStyleSheet("color: #2196F3;")

    def onSliderReleased(self):
        """滑块释放时的处理"""
        current_pos = self.slider.value()
        if abs(current_pos - self.target_pos) <= 2:  # 允许2%的误差
            self.tipLabel.setText("验证成功！")
            self.tipLabel.setStyleSheet("color: #4CAF50;")
            self.verified.emit(True)
        else:
            self.tipLabel.setText("验证失败，请重试")
            self.tipLabel.setStyleSheet("color: #F44336;")
            QtCore.QTimer.singleShot(1000, self.reset)

    def onSliderMoved(self, value):
        """滑块移动时的处理"""
        if not self.slider.isSliderDown():
            return
        self.tipLabel.setText(f"当前位置: {value}%")

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.login_attempts = 0
        self.max_attempts = 3
        self.load_users()
        self.verification_passed = False

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
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title = QtWidgets.QLabel("用户登录")
        title.setStyleSheet("""
            font-size: 24px;
            color: #1976D2;
            font-weight: bold;
            margin-bottom: 20px;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # 用户名输入
        self.username_edit = QtWidgets.QLineEdit()
        self.username_edit.setPlaceholderText("请输入用户名")
        layout.addWidget(self.username_edit)

        # 密码输入
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setPlaceholderText("请输入密码")
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_edit.textChanged.connect(self.on_password_changed)
        layout.addWidget(self.password_edit)

        # 滑块验证
        self.slider_verification = SliderVerification()
        self.slider_verification.verified.connect(self.on_verification_complete)
        layout.addWidget(self.slider_verification)

        # 登录按钮
        self.login_button = QtWidgets.QPushButton("登录")
        self.login_button.clicked.connect(self.login)
        self.login_button.setEnabled(False)
        layout.addWidget(self.login_button)

        # 注册按钮
        self.register_button = QtWidgets.QPushButton("注册")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        # 状态提示
        self.status_label = QtWidgets.QLabel()
        self.status_label.setStyleSheet("color: #666;")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.status_label)

    def on_password_changed(self, text):
        """密码输入变化时的处理"""
        if len(text) > 0:
            displayed_text = text[-1]
            masked_text = '*' * (len(text) - 1) + displayed_text
            self.password_edit.setText(masked_text)
            self.password_edit.setCursorPosition(len(masked_text))

    def on_verification_complete(self, passed):
        """验证完成的处理"""
        self.verification_passed = passed
        self.login_button.setEnabled(passed)

    def login(self):
        """登录处理"""
        if self.login_attempts >= self.max_attempts:
            self.status_label.setText("登录次数超限，请稍后再试")
            self.status_label.setStyleSheet("color: #F44336;")
            return

        username = self.username_edit.text()
        password = self.password_edit.text()

        if not username or not password:
            self.status_label.setText("用户名和密码不能为空")
            self.status_label.setStyleSheet("color: #F44336;")
            return

        if not self.verification_passed:
            self.status_label.setText("请完成滑块验证")
            self.status_label.setStyleSheet("color: #F44336;")
            return

        hashed_password = self.hash_password(password)
        if username in self.users and self.users[username] == hashed_password:
            self.status_label.setText("登录成功！")
            self.status_label.setStyleSheet("color: #4CAF50;")
            self.login_attempts = 0
        else:
            self.login_attempts += 1
            remaining = self.max_attempts - self.login_attempts
            self.status_label.setText(f"用户名或密码错误，还剩{remaining}次机会")
            self.status_label.setStyleSheet("color: #F44336;")
            if remaining == 0:
                self.login_button.setEnabled(False)
                QtCore.QTimer.singleShot(30000, self.reset_attempts)  # 30秒后重置

    def register(self):
        """注册处理"""
        username = self.username_edit.text()
        password = self.password_edit.text()

        if not username or not password:
            self.status_label.setText("用户名和密码不能为空")
            self.status_label.setStyleSheet("color: #F44336;")
            return

        if username in self.users:
            self.status_label.setText("用户名已存在")
            self.status_label.setStyleSheet("color: #F44336;")
            return

        self.users[username] = self.hash_password(password)
        self.save_users()
        self.status_label.setText("注册成功！")
        self.status_label.setStyleSheet("color: #4CAF50;")

    def reset_attempts(self):
        """重置登录尝试次数"""
        self.login_attempts = 0
        self.login_button.setEnabled(True)
        self.status_label.setText("可以重新登录了")
        self.status_label.setStyleSheet("color: #666;")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login = LoginDialog()
    login.show()
    sys.exit(app.exec_()) 
