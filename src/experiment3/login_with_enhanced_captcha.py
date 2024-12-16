from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import random
import math
import hashlib
import json
import os
class EnhancedSliderCaptcha(QtWidgets.QWidget):
    verified = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        # 基础属性
        self.block_size = 60
        self.image_width = 800
        self.image_height = 300  # 减小验证码区域高度
        
        # 障碍物属性
        self.obstacles = []
        self.obstacle_count = 5
        self.obstacle_size = 30
        
        # 状态属性
        self.is_pressed = False
        self.current_pos = QtCore.QPoint(0, 0)
        self.start_pos = None
        self.gap_pos = None
        
        self.initUI()
        self.reset_captcha()

    def initUI(self):
        self.setFixedSize(1000, 500)  # 减小验证码组件的整体高度
        self.setStyleSheet("background: white;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 图片显示区域
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

        # 提示文本
        self.tip_label = QtWidgets.QLabel("拖动蓝色方块到目标位置，注意避开障碍物")
        self.tip_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tip_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 20px;
                background: transparent;
                font-family: Microsoft YaHei;
                padding: 10px;
            }
        """)
        layout.addWidget(self.tip_label)

    def generate_obstacles(self):
        """生成随机障碍物"""
        self.obstacles = []
        for _ in range(self.obstacle_count):
            x = random.randint(self.block_size * 2, self.image_width - self.block_size * 2)
            y = random.randint(self.block_size * 2, self.image_height - self.block_size * 2)
            self.obstacles.append(QtCore.QPoint(x, y))

    def reset_captcha(self):
        """重置验证码"""
        self.bg_pixmap = QtGui.QPixmap(self.image_width, self.image_height)
        self.bg_pixmap.fill(QtGui.QColor("#f5f5f5"))
        
        # 生成缺口位置
        margin = self.block_size * 2
        self.gap_pos = QtCore.QPoint(
            random.randint(margin, self.image_width - self.block_size - margin),
            random.randint(margin, self.image_height - self.block_size - margin)
        )
        
        # 生成障碍物
        self.generate_obstacles()
        
        # 重置状态
        self.is_pressed = False
        self.current_pos = QtCore.QPoint(self.block_size, self.gap_pos.y())
        self.verified.emit(False)
        
        self.draw_initial_state()

    def draw_initial_state(self):
        """绘制初始状态"""
        painter = QtGui.QPainter(self.bg_pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # 绘制网格背景
        painter.setPen(QtGui.QPen(QtGui.QColor("#e0e0e0"), 1))
        grid_size = 20
        for i in range(0, self.image_width, grid_size):
            painter.drawLine(i, 0, i, self.image_height)
        for i in range(0, self.image_height, grid_size):
            painter.drawLine(0, i, self.image_width, i)
        
        # 绘制障碍物
        painter.setPen(QtGui.QPen(QtGui.QColor("#FF5722"), 2))
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#FF5722")))
        for obstacle in self.obstacles:
            painter.drawEllipse(obstacle, self.obstacle_size, self.obstacle_size)
        
        # 绘制目标位置
        painter.setPen(QtGui.QPen(QtGui.QColor("#2196F3"), 2))
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#fff")))
        painter.drawRoundedRect(
            self.gap_pos.x(), self.gap_pos.y(),
            self.block_size, self.block_size, 4, 4
        )
        
        painter.end()
        self.image_label.setPixmap(self.bg_pixmap)
        self.draw_block(self.current_pos)

    def draw_block(self, pos):
        """绘制可移动方块"""
        pixmap = QtGui.QPixmap(self.bg_pixmap)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # 绘制方块
        painter.setPen(QtGui.QPen(QtGui.QColor("#2196F3"), 2))
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#2196F3")))
        painter.drawRoundedRect(
            int(pos.x()), int(pos.y()),
            self.block_size, self.block_size, 4, 4
        )
        
        painter.end()
        self.image_label.setPixmap(pixmap)

    def check_collision(self, pos):
        """检查是否与障碍物碰撞"""
        for obstacle in self.obstacles:
            distance = math.sqrt((pos.x() - obstacle.x())**2 + (pos.y() - obstacle.y())**2)
            if distance < (self.block_size + self.obstacle_size) / 2:
                return True
        return False

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # 检查是否点击在方块上
            pos = self.image_label.mapFrom(self, event.pos())
            block_rect = QtCore.QRect(
                int(self.current_pos.x()),
                int(self.current_pos.y()),
                self.block_size,
                self.block_size
            )
            if block_rect.contains(pos):
                self.is_pressed = True
                self.start_pos = pos
                self.tip_label.setText("正在移动，注意避开障碍物")
                self.tip_label.setStyleSheet("""
                    QLabel {
                        color: #2196F3;
                        font-size: 20px;
                        background: transparent;
                        font-family: Microsoft YaHei;
                    }
                """)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.is_pressed:
            self.is_pressed = False
            # 检查是否到达目标位置
            if abs(self.current_pos.x() - self.gap_pos.x()) <= 10 and \
               abs(self.current_pos.y() - self.gap_pos.y()) <= 10:
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
                self.tip_label.setText("未到达指定位置，请重试")
                self.tip_label.setStyleSheet("""
                    QLabel {
                        color: #F44336;
                        font-size: 20px;
                        background: transparent;
                        font-family: Microsoft YaHei;
                    }
                """)
                QtCore.QTimer.singleShot(1000, self.reset_captcha)

    def mouseMoveEvent(self, event):
        if self.is_pressed:
            pos = self.image_label.mapFrom(self, event.pos())
            delta = pos - self.start_pos
            new_x = int(max(0, min(self.image_width - self.block_size,
                             self.current_pos.x() + delta.x())))
            new_y = int(max(0, min(self.image_height - self.block_size,
                             self.current_pos.y() + delta.y())))
            
            # 创建新位置
            new_pos = QtCore.QPoint(new_x, new_y)
            
            # 检查碰撞
            if self.check_collision(new_pos):
                self.tip_label.setText("碰到障碍物了，请重试")
                self.tip_label.setStyleSheet("""
                    QLabel {
                        color: #F44336;
                        font-size: 20px;
                        background: transparent;
                        font-family: Microsoft YaHei;
                    }
                """)
                QtCore.QTimer.singleShot(1000, self.reset_captcha)
                return
            
            # 更新位置
            self.current_pos = new_pos
            self.draw_block(self.current_pos)
            self.start_pos = pos

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
        self.setFixedSize(1200, 1000)  # 增加窗口高度
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Microsoft YaHei;
            }
            QLineEdit {
                padding: 15px 15px 15px 50px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 24px;
                min-height: 60px;  # 增加输入框高度
                margin: 10px 0;    # 增加上下边距
                background-repeat: no-repeat;
                background-position: 15px center;
                background-size: 24px 24px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                border-width: 2px;
                background-color: #f8f9fa;
            }
            QLineEdit:hover {
                border-color: #90caf9;
                background-color: #f5f5f5;
            }
            QPushButton {
                padding: 15px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 24px;
                min-height: 60px;  # 增加按钮高度
                font-weight: bold;
                margin: 15px;      # 增加按钮边距
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
                margin: 15px 0;    # 增加标签边距
            }
        """)

        # 创建主布局
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)  # 增加主布局边距
        main_layout.setSpacing(30)  # 增加组件间距

        # 创建中心容器
        center_container = QtWidgets.QWidget()
        center_container.setStyleSheet("border: none;")
        center_layout = QtWidgets.QVBoxLayout(center_container)
        center_layout.setContentsMargins(50, 30, 50, 30)  # 增加内边距
        center_layout.setSpacing(30)  # 增加组件间距

        # 标题
        title = QtWidgets.QLabel('用户登录')
        title.setStyleSheet("""
            font-size: 48px;  # 增加标题字号
            color: #1976D2;
            font-weight: bold;
            margin: 20px 0;   # 增加标题边距
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        center_layout.addWidget(title)

        # 输入区域容器
        input_container = QtWidgets.QWidget()
        input_layout = QtWidgets.QVBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(20)  # 增加输入框间距

        # 用户名输入
        username_label = QtWidgets.QLabel('用户名:')
        username_label.setStyleSheet("""
            font-size: 26px;  # 增加标签字号
            color: #666;
            font-weight: normal;
            margin-bottom: 10px;  # 增加底部边距
        """)
        input_layout.addWidget(username_label)
        
        self.username_edit = QtWidgets.QLineEdit()
        self.username_edit.setPlaceholderText('请输入用户名')
        self.username_edit.setFixedWidth(800)
        self.username_edit.setStyleSheet("""
            QLineEdit {
                background-image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzY2NiI+PHBhdGggZD0iTTEyIDEyYzIuMjEgMCA0LTEuNzkgNC00cy0xLjc5LTQtNC00LTQgMS43OS00IDQgMS43OSA0IDQgNHptMCAyYy0yLjY3IDAtOCAxLjM0LTggNHYyaDE2di0yYzAtMi42Ni01LjMzLTQtOC00eiIvPjwvc3ZnPg==);
                margin: 15px 0;  # 增加输入框边距
            }
        """)
        input_layout.addWidget(self.username_edit)

        # 密码输入
        password_label = QtWidgets.QLabel('密码:')
        password_label.setStyleSheet("""
            font-size: 26px;  # 增加标签字号
            color: #666;
            font-weight: normal;
            margin-bottom: 10px;  # 增加底部边距
        """)
        input_layout.addWidget(password_label)
        
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setPlaceholderText('请输入密码')
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_edit.textChanged.connect(self.on_password_changed)
        self.password_edit.setFixedWidth(800)
        self.password_edit.setStyleSheet("""
            QLineEdit {
                background-image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzY2NiI+PHBhdGggZD0iTTE4IDhoLTFWNmMwLTIuNzYtMi4yNC01LTUtNVM3IDMuMjQgNyA2djJINmMtMS4xIDAtMiAuOS0yIDJ2MTBjMCAxLjEuOSAyIDIgMmgxMmMxLjEgMCAyLS45IDItMlYxMGMwLTEuMS0uOS0yLTItMnptLTYgOWMtMS4xIDAtMi0uOS0yLTJzLjktMiAyLTIgMiAuOSAyIDItLjkgMi0yIDJ6bTMuMS05SDguOVY2YzAtMS43MSAxLjM5LTMuMSAzLjEtMy4xIDEuNzEgMCAzLjEgMS4zOSAzLjEgMy4xdjJ6Ii8+PC9zdmc+);
                margin: 15px 0;  # 增加输入框边距
            }
        """)
        input_layout.addWidget(self.password_edit)

        # 创建输入框容器
        input_frame = QtWidgets.QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                padding: 30px;  # 增加内边距
            }
        """)
        input_frame_layout = QtWidgets.QVBoxLayout(input_frame)
        input_frame_layout.setContentsMargins(40, 40, 40, 40)  # 增加框架内边距
        input_frame_layout.setSpacing(20)  # 增加框架内组件间距
        
        # 将输入区域移动到框架中
        input_frame_layout.addWidget(input_container)
        
        # 将框架添加到中心布局
        center_layout.addWidget(input_frame, alignment=QtCore.Qt.AlignCenter)

        # 验证码区域
        center_layout.addSpacing(20)  # 在验证码前添加间距
        self.captcha = EnhancedSliderCaptcha(self)
        self.captcha.verified.connect(self.on_verification_complete)
        center_layout.addWidget(self.captcha, alignment=QtCore.Qt.AlignCenter)
        center_layout.addSpacing(20)  # 在验证码后添加间距

        # 状态提示
        self.status_label = QtWidgets.QLabel()
        self.status_label.setStyleSheet("""
            color: #666;
            font-size: 24px;  # 增加状态标签字号
            border: none;
            background: transparent;
            font-weight: normal;
            min-height: 40px;  # 增加最小高度
            margin: 10px 0;    # 增加边距
        """)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        center_layout.addWidget(self.status_label)

        # 按钮区域
        button_container = QtWidgets.QWidget()
        button_container.setStyleSheet("border: none;")
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 20, 0, 0)  # 增加按钮区域上边距
        button_layout.setSpacing(30)  # 增加按钮间距
        
        self.login_button = QtWidgets.QPushButton('登录')
        self.login_button.setFixedSize(300, 70)  # 增加按钮尺寸
        self.login_button.clicked.connect(self.login)
        self.login_button.setEnabled(False)
        button_layout.addWidget(self.login_button)
        
        self.register_button = QtWidgets.QPushButton('注册')
        self.register_button.setFixedSize(300, 70)  # 增加按钮尺寸
        self.register_button.clicked.connect(self.register)
        button_layout.addWidget(self.register_button)
        
        center_layout.addWidget(button_container, alignment=QtCore.Qt.AlignCenter)

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
            self.status_label.setStyleSheet("color: #F44336; font-size: 22px;")
            return

        username = self.username_edit.text()
        password = self.password_edit.text()

        if not username or not password:
            self.status_label.setText("用户名和密码不能为空")
            self.status_label.setStyleSheet("color: #F44336; font-size: 22px;")
            return

        if not self.verification_passed:
            self.status_label.setText("请完成验证")
            self.status_label.setStyleSheet("color: #F44336; font-size: 22px;")
            return

        hashed_password = self.hash_password(password)
        if username in self.users and self.users[username] == hashed_password:
            self.status_label.setText("登录成功！")
            self.status_label.setStyleSheet("color: #4CAF50; font-size: 22px;")
            self.login_attempts = 0
        else:
            self.login_attempts += 1
            remaining = self.max_attempts - self.login_attempts
            self.status_label.setText(f"用户名或密码错误，还剩{remaining}次机会")
            self.status_label.setStyleSheet("color: #F44336; font-size: 22px;")
            if remaining == 0:
                self.login_button.setEnabled(False)
                QtCore.QTimer.singleShot(30000, self.reset_attempts)

    def register(self):
        """注册处理"""
        username = self.username_edit.text()
        password = self.password_edit.text()

        if not username or not password:
            self.status_label.setText("用户名和密码不能为空")
            self.status_label.setStyleSheet("color: #F44336; font-size: 22px;")
            return

        if username in self.users:
            self.status_label.setText("用户名已存在")
            self.status_label.setStyleSheet("color: #F44336; font-size: 22px;")
            return

        self.users[username] = self.hash_password(password)
        self.save_users()
        self.status_label.setText("注册成功！")
        self.status_label.setStyleSheet("color: #4CAF50; font-size: 22px;")

    def reset_attempts(self):
        """重置登录尝试次数"""
        self.login_attempts = 0
        self.login_button.setEnabled(True)
        self.status_label.setText("可以重新登录了")
        self.status_label.setStyleSheet("color: #666; font-size: 22px;")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_()) 
