import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel)
from PyQt5.QtCore import Qt
from poker_game import PokerGame
from texas_holdem import TexasHoldem

class PokerMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        """初始化UI"""
        self.setWindowTitle('扑克牌游戏')
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QLabel {
                color: #323130;
                font-size: 48px;
                font-family: 'Microsoft YaHei';
                font-weight: bold;
            }
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 20px;
                font-size: 24px;
                font-family: 'Microsoft YaHei';
                min-width: 300px;
                min-height: 80px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
            QPushButton:pressed {
                background-color: #005A9E;
            }
        """)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # 标题
        title = QLabel('扑克牌游戏')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 添加一些空间
        layout.addStretch()
        
        # 基础玩法按钮
        basic_button = QPushButton('基础玩法')
        basic_button.clicked.connect(self.start_basic_game)
        layout.addWidget(basic_button, alignment=Qt.AlignCenter)
        
        # 德州扑克按钮
        texas_button = QPushButton('德州扑克')
        texas_button.clicked.connect(self.start_texas_holdem)
        layout.addWidget(texas_button, alignment=Qt.AlignCenter)
        
        # 添加一些空间
        layout.addStretch()
        
    def start_basic_game(self):
        """启动基础玩法"""
        self.basic_game = PokerGame()
        self.basic_game.show()
        self.hide()
        
    def start_texas_holdem(self):
        """启动德州扑克"""
        self.texas_game = TexasHoldem()
        self.texas_game.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = PokerMenu()
    menu.show()
    sys.exit(app.exec_()) 
