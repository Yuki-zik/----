from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import random
import hashlib
import json
import os

class SliderCaptcha(QtWidgets.QWidget):
    verified = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize attributes first
        self.block_size = 60
        self.image_width = 800
        self.image_height = 400
        self.slider_height = 100
        
        # Then call initUI
        self.initUI()
        
        # Initialize other attributes
        self.is_pressed = False
        self.current_pos = None
        self.start_pos = None
        self.gap_pos = None
        self.reset_captcha()

    def initUI(self):
        self.setFixedSize(1000, 900)
        self.setStyleSheet("""
            QWidget {
                background: white;
                border: none;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 创建图片显示区域
        self.image_label = QtWidgets.QLabel()
        self.image_label.setFixedSize(self.image_width, self.image_height)
        self.image_label.setStyleSheet("""
            QLabel {
                background: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.image_label, 0, QtCore.Qt.AlignCenter)

        # 创建滑块区域
        slider_container = QtWidgets.QWidget()
        slider_container.setFixedSize(self.image_width, self.slider_height)
        slider_container.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                margin-top: 10px;
            }
        """)
        
        slider_layout = QtWidgets.QHBoxLayout(slider_container)
        slider_layout.setContentsMargins(2, 2, 2, 2)
        
        # 创建滑动条背景
        slider_bg = QtWidgets.QWidget()
        slider_bg.setFixedSize(self.image_width - 4, 36)
        slider_bg.setStyleSheet("""
            QWidget {
                background: #f5f5f5;
                border: none;
                border-radius: 18px;
            }
        """)
        slider_layout.addWidget(slider_bg)
        
        # 创建滑块
        self.slider_widget = QtWidgets.QWidget(slider_bg)
        self.slider_widget.setFixedSize(50, 36)
        self.slider_widget.setStyleSheet("""
            QWidget {
                background: #2196F3;
                border: none;
                border-radius: 18px;
            }
            QWidget:hover {
                background: #1976D2;
            }
        """)
        
        layout.addWidget(slider_container, 0, QtCore.Qt.AlignCenter)

        # 创建提示文本
        self.tip_label = QtWidgets.QLabel("按住滑块，拖动完成拼图")
        self.tip_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tip_label.setStyleSheet("""
            QLabel {
                color: #999;
                font-size: 20px;
                background: transparent;
                font-family: Microsoft YaHei;
            }
        """)
        layout.addWidget(self.tip_label)

    def reset_captcha(self):
        """重置验证码"""
        self.bg_pixmap = QtGui.QPixmap(self.image_width, self.image_height)
        self.bg_pixmap.fill(QtGui.QColor("#f5f5f5"))
        
        margin = self.block_size * 2
        self.gap_pos = QtCore.QPoint(
            random.randint(margin, self.image_width - self.block_size - margin),
            random.randint(margin, self.image_height - self.block_size - margin)
        )
        
        painter = QtGui.QPainter(self.bg_pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # 绘制网格背景
        painter.setPen(QtGui.QPen(QtGui.QColor("#e0e0e0"), 1))
        grid_size = 20
        for i in range(0, self.image_width, grid_size):
            painter.drawLine(i, 0, i, self.image_height)
        for i in range(0, self.image_height, grid_size):
            painter.drawLine(0, i, self.image_width, i)
        
        # 绘制滑块缺口
        painter.setPen(QtGui.QPen(QtGui.QColor("#2196F3"), 2))
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#fff")))
        painter.drawRoundedRect(
            self.gap_pos.x(), self.gap_pos.y(),
            self.block_size, self.block_size, 4, 4
        )
        
        painter.end()
        self.image_label.setPixmap(self.bg_pixmap)
        
        self.is_pressed = False
        self.current_pos = QtCore.QPoint(0, self.gap_pos.y())
        self.verified.emit(False)
        self.draw_slider(self.current_pos)

    def draw_slider(self, pos):
        """绘制滑块"""
        pixmap = QtGui.QPixmap(self.bg_pixmap)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # 绘制滑块
        painter.setPen(QtGui.QPen(QtGui.QColor("#2196F3"), 2))
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#2196F3")))
        painter.drawRoundedRect(
            pos.x(), pos.y(),
            self.block_size, self.block_size, 4, 4
        )
        
        painter.end()
        self.image_label.setPixmap(pixmap)
        
        # 更新滑块位置
        relative_x = (pos.x() / (self.image_width - self.block_size)) * (self.image_width - 54)
        self.slider_widget.move(int(relative_x), 0)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            pos = self.image_label.mapFrom(self, event.pos())
            slider_pos = self.slider_widget.mapFrom(self, event.pos())
            
            # 检查是否点击在滑块上
            if self.slider_widget.rect().contains(slider_pos) or \
               (abs(pos.x() - self.current_pos.x()) <= self.block_size and \
                abs(pos.y() - self.current_pos.y()) <= self.block_size):
                self.is_pressed = True
                self.start_pos = pos
                self.tip_label.setText("拖动滑块完成拼图")
                self.tip_label.setStyleSheet("""
                    QLabel {
                        color: #2196F3;
                        font-size: 20px;
                        background: transparent;
                        font-family: Microsoft YaHei;
                    }
                """)

    def mouseMoveEvent(self, event):
        if self.is_pressed:
            pos = self.image_label.mapFrom(self, event.pos())
            delta_x = pos.x() - self.start_pos.x()
            new_x = max(0, min(self.image_width - self.block_size,
                             self.current_pos.x() + delta_x))
            self.current_pos.setX(new_x)
            self.draw_slider(self.current_pos)
            self.start_pos = pos

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.is_pressed:
            self.is_pressed = False
            if abs(self.current_pos.x() - self.gap_pos.x()) <= 10:
                self.tip_label.setText("验证成功！")
                self.tip_label.setStyleSheet("""
                    QLabel {
                        color: #4CAF50;
                        font-size: 20px;
                        background: transparent;
                        font-family: Microsoft YaHei;
                    }
                """)
                self.verified.emit(True)
            else:
                self.tip_label.setText("验证失败，请重试")
                self.tip_label.setStyleSheet("""
                    QLabel {
                        color: #F44336;
                        font-size: 20px;
                        background: transparent;
                        font-family: Microsoft YaHei;
                    }
                """)
                QtCore.QTimer.singleShot(1000, self.reset_captcha)

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.login_attempts = 0
        self.max_attempts = 3
        self.verification_passed = False
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
        self.setFixedSize(1200, 1600)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Microsoft YaHei;
            }
            QLineEdit {
                padding: 15px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 24px;
                min-height: 50px;
                margin: 5px 0;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                border-width: 2px;
            }
            QPushButton {
                padding: 15px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 24px;
                min-height: 50px;
                font-weight: bold;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
            QLabel {
                font-size: 24px;
                color: #333;
                font-weight: bold;
                margin: 10px 0;
            }
        """)

        # 创建主布局
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(50, 70, 50, 70)
        main_layout.setSpacing(40)

        # 创建中心容器
        center_container = QtWidgets.QWidget()
        center_container.setStyleSheet("border: none;")
        center_layout = QtWidgets.QVBoxLayout(center_container)
        center_layout.setContentsMargins(40, 50, 40, 50)
        center_layout.setSpacing(40)

        # 标题
        title = QtWidgets.QLabel('用户登录')
        title.setStyleSheet("""
            font-size: 48px;
            color: #1976D2;
            font-weight: bold;
            margin: 40px 0;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        center_layout.addWidget(title)

        # 用户名输入
        username_label = QtWidgets.QLabel('用户名:')
        username_label.setStyleSheet("""
            font-size: 28px;
            color: #333;
            font-weight: bold;
            margin-top: 20px;
        """)
        center_layout.addWidget(username_label)
        
        self.username_edit = QtWidgets.QLineEdit()
        self.username_edit.setPlaceholderText('请输入用户名')
        self.username_edit.setFixedWidth(800)
        center_layout.addWidget(self.username_edit)

        # 密码输入
        password_label = QtWidgets.QLabel('密码:')
        password_label.setStyleSheet("""
            font-size: 28px;
            color: #333;
            font-weight: bold;
            margin-top: 20px;
        """)
        center_layout.addWidget(password_label)
        
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setPlaceholderText('请输入密码')
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_edit.textChanged.connect(self.on_password_changed)
        self.password_edit.setFixedWidth(800)
        center_layout.addWidget(self.password_edit)

        # 验证区域
        self.captcha = SliderCaptcha(self)
        self.captcha.setFixedSize(800, 500)
        self.captcha.verified.connect(self.on_verification_complete)
        center_layout.addWidget(self.captcha, alignment=QtCore.Qt.AlignCenter)

        # 状态提示
        status_container = QtWidgets.QWidget()
        status_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                margin: 25px 0;
            }
        """)
        status_container.setFixedSize(800, 80)
        status_layout = QtWidgets.QVBoxLayout(status_container)
        status_layout.setContentsMargins(10, 5, 10, 5)
        
        self.status_label = QtWidgets.QLabel()
        self.status_label.setStyleSheet("""
            color: #666;
            font-size: 22px;
            border: none;
            background: transparent;
            font-weight: normal;
        """)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        status_layout.addWidget(self.status_label)
        
        center_layout.addWidget(status_container, alignment=QtCore.Qt.AlignCenter)

        # 登录按钮
        self.login_button = QtWidgets.QPushButton('登录')
        self.login_button.setFixedSize(800, 60)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #CCCCCC;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 24px;
                font-weight: bold;
                margin: 10px 0;
            }
            QPushButton:enabled {
                background-color: #2196F3;
            }
            QPushButton:enabled:hover {
                background-color: #1976D2;
            }
        """)
        self.login_button.clicked.connect(self.login)
        self.login_button.setEnabled(False)
        center_layout.addWidget(self.login_button, alignment=QtCore.Qt.AlignCenter)

        # 分割线
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setStyleSheet("""
            background-color: #ddd;
            margin: 35px 0;
        """)
        separator.setFixedWidth(800)
        center_layout.addWidget(separator, alignment=QtCore.Qt.AlignCenter)

        # 注册按钮
        self.register_button = QtWidgets.QPushButton('注册')
        self.register_button.setFixedSize(800, 60)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2196F3;
                border: 2px solid #2196F3;
                border-radius: 8px;
                font-size: 24px;
                font-weight: bold;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #E3F2FD;
            }
        """)
        self.register_button.clicked.connect(self.register)
        center_layout.addWidget(self.register_button, alignment=QtCore.Qt.AlignCenter)

        # 添加中心容器到主布局
        main_layout.addWidget(center_container, alignment=QtCore.Qt.AlignCenter)

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
            self.status_label.setText("登录次数超限，请等待30秒后重试")
            self.status_label.setStyleSheet("color: #F44336; font-size: 22px; font-weight: normal;")
            return

        username = self.username_edit.text()
        password = self.password_edit.text()

        if not username or not password:
            self.status_label.setText("用户名和密码不能为空")
            self.status_label.setStyleSheet("color: #F44336; font-size: 22px; font-weight: normal;")
            return

        if not self.verification_passed:
            self.status_label.setText("请完成滑块验证")
            self.status_label.setStyleSheet("color: #F44336; font-size: 22px; font-weight: normal;")
            return

        hashed_password = self.hash_password(password)
        if username in self.users and self.users[username] == hashed_password:
            self.status_label.setText("登录成功！")
            self.status_label.setStyleSheet("color: #4CAF50; font-size: 22px; font-weight: normal;")
            self.login_attempts = 0
        else:
            self.login_attempts += 1
            remaining = self.max_attempts - self.login_attempts
            self.status_label.setText(f"用户名或密码错误，还剩{remaining}次机会")
            self.status_label.setStyleSheet("color: #F44336; font-size: 22px; font-weight: normal;")
            if remaining == 0:
                self.login_button.setEnabled(False)
                QtCore.QTimer.singleShot(30000, self.reset_attempts)

    def register(self):
        """注册处理"""
        username = self.username_edit.text()
        password = self.password_edit.text()

        if not username or not password:
            self.status_label.setText("用户名和密码不能为空")
            self.status_label.setStyleSheet("color: #F44336; font-size: 22px; font-weight: normal;")
            return

        if username in self.users:
            self.status_label.setText("用户名已存在")
            self.status_label.setStyleSheet("color: #F44336; font-size: 22px; font-weight: normal;")
            return

        self.users[username] = self.hash_password(password)
        self.save_users()
        self.status_label.setText("注册成功！")
        self.status_label.setStyleSheet("color: #4CAF50; font-size: 22px; font-weight: normal;")

    def reset_attempts(self):
        """重置登录尝试次数"""
        self.login_attempts = 0
        self.login_button.setEnabled(True)
        self.status_label.setText("可以重新登录了")
        self.status_label.setStyleSheet("color: #666; font-size: 22px; font-weight: normal;")

    def mousePressEvent(self, event):
        """添加窗口拖动功能"""
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """窗口拖动实现"""
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_()) 
