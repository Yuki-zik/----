import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, QTextEdit)
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor, QPen, QIcon
from PyQt5.QtCore import Qt, QSize, QRect

class Card:
    """扑克牌类"""
    SUITS = ['S', 'H', 'D', 'C']  # Spades, Hearts, Diamonds, Clubs
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def get_value(self):
        """获取牌的大小值"""
        return Card.RANKS.index(self.rank)
    
    def __str__(self):
        return f"{self.suit}{self.rank}"
    
    def get_card_image(self):
        """获取卡牌图片"""
        pixmap = QPixmap(150, 220)
        pixmap.fill(Qt.white)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制卡牌边框和阴影
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 20))
        painter.drawRoundedRect(5, 5, 146, 216, 8, 8)
        
        # 绘制卡牌主体
        painter.setBrush(QColor("white"))
        painter.setPen(QPen(QColor("#E1DFDD"), 1))
        painter.drawRoundedRect(2, 2, 146, 216, 8, 8)
        
        # 设置字体
        font = QFont('Segoe UI', 12)
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        
        # 设置颜色
        if self.suit in ['H', 'D']:
            painter.setPen(QColor("#E81123"))
        else:
            painter.setPen(QColor("#323130"))
            
        # 绘制点数
        painter.drawText(QRect(15, 15, 45, 45), Qt.AlignCenter, self.rank)
        painter.drawText(QRect(90, 160, 45, 45), Qt.AlignCenter, self.rank)
        
        # 绘制花色
        font.setPointSize(24)
        painter.setFont(font)
        suit_symbol = {
            'S': '♠',
            'H': '♥',
            'D': '♦',
            'C': '♣'
        }[self.suit]
        painter.drawText(QRect(35, 60, 80, 80), Qt.AlignCenter, suit_symbol)
        
        painter.end()
        return pixmap
    
    def get_card_back(self):
        """获取卡牌背面图片"""
        pixmap = QPixmap(150, 220)
        pixmap.fill(Qt.white)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制阴影
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 20))
        painter.drawRoundedRect(5, 5, 146, 216, 8, 8)
        
        # 绘制背景
        painter.setBrush(QColor("#0078D4"))
        painter.setPen(QPen(QColor("#106EBE"), 1))
        painter.drawRoundedRect(2, 2, 146, 216, 8, 8)
        
        # 绘制网格花纹
        pen = QPen(QColor("#106EBE"))
        pen.setWidth(1)
        painter.setPen(pen)
        for i in range(0, 150, 10):
            painter.drawLine(i, 0, i, 220)
        for i in range(0, 220, 10):
            painter.drawLine(0, i, 150, i)
        
        # 绘制中心图案
        painter.setBrush(QColor("white"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(45, 80, 60, 60)
        
        font = QFont('Segoe UI', 32)
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor("#0078D4"))
        painter.drawText(QRect(45, 80, 60, 60), Qt.AlignCenter, "♠")
        
        painter.end()
        return pixmap

class PokerGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initGame()
        
    def initUI(self):
        """初始化UI"""
        self.setWindowTitle('基础扑克')
        self.setFixedSize(1800, 1600)
        
        # 设置窗口背景
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1B5E20;
            }
            QLabel {
                color: white;
                font-size: 24px;
                font-family: 'Microsoft YaHei';
            }
            QTextEdit {
                color: white;
                font-size: 24px;
                font-family: 'Microsoft YaHei';
                padding: 20px;
                background-color: #2E7D32;
                border: 2px solid #1B5E20;
                border-radius: 8px;
                margin: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 20px;
                font-family: 'Microsoft YaHei';
                min-width: 120px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            QPushButton:pressed {
                background-color: #2E7D32;
            }
            QPushButton:disabled {
                background-color: #81C784;
                color: #E8F5E9;
            }
            QFrame#cardArea {
                background-color: #2E7D32;
                border: 2px solid #1B5E20;
                border-radius: 8px;
                margin: 10px;
            }
        """)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # 玩家区域
        self.setup_player_area(main_layout)
        
        # 控制区域
        self.setup_control_area(main_layout)
        
    def setup_player_area(self, main_layout):
        """设置玩家区域"""
        player_container = QWidget()
        player_layout = QHBoxLayout(player_container)
        
        # 玩家1区域
        player1_frame = QFrame()
        player1_frame.setObjectName("cardArea")
        player1_layout = QVBoxLayout(player1_frame)
        
        self.player1_label = QLabel('玩家 1')
        self.player1_score = QLabel('得分: 0')
        player1_layout.addWidget(self.player1_label)
        player1_layout.addWidget(self.player1_score)
        
        self.player1_cards = QHBoxLayout()
        self.player1_cards.setAlignment(Qt.AlignCenter)
        player1_layout.addLayout(self.player1_cards)
        
        player_layout.addWidget(player1_frame)
        
        # 玩家2区域
        player2_frame = QFrame()
        player2_frame.setObjectName("cardArea")
        player2_layout = QVBoxLayout(player2_frame)
        
        self.player2_label = QLabel('玩家 2')
        self.player2_score = QLabel('得分: 0')
        player2_layout.addWidget(self.player2_label)
        player2_layout.addWidget(self.player2_score)
        
        self.player2_cards = QHBoxLayout()
        self.player2_cards.setAlignment(Qt.AlignCenter)
        player2_layout.addLayout(self.player2_cards)
        
        player_layout.addWidget(player2_frame)
        
        main_layout.addWidget(player_container)
        
    def setup_control_area(self, main_layout):
        """设置控制区域"""
        # 控制按钮区域
        control_frame = QFrame()
        control_frame.setObjectName("cardArea")
        control_layout = QHBoxLayout(control_frame)
        
        # 开始新游戏按钮
        self.new_game_button = QPushButton('开始新游戏')
        self.new_game_button.clicked.connect(self.start_new_game)
        control_layout.addWidget(self.new_game_button)
        
        main_layout.addWidget(control_frame)
        
        # 创建结果显示区域
        result_frame = QFrame()
        result_frame.setObjectName("cardArea")
        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(20, 20, 20, 20)
        
        # 使用QTextEdit替代QLabel来显示结果
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setMinimumHeight(400)
        result_layout.addWidget(self.result_display)
        
        # 状态标签
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(self.status_label)
        
        main_layout.addWidget(result_frame)
        
    def initGame(self):
        """初始化游戏状态"""
        self.deck = []
        self.player1_hand = []
        self.player2_hand = []
        self.current_comparison = 0
        self.player1_wins = 0
        self.player2_wins = 0
        
        # 创建一副扑克牌
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.deck.append(Card(suit, rank))
                
    def start_new_game(self):
        """开始新游戏"""
        # 清空之前的卡牌
        self.clear_cards()
        
        # 重置状态
        self.current_comparison = 0
        self.result_display.setText('')
        self.status_label.setText('点击卡牌背面开始比较')
        
        # 洗牌并发牌
        random.shuffle(self.deck)
        self.player1_hand = self.deck[:5]
        self.player2_hand = self.deck[5:10]
        
        # 显示卡牌
        self.display_cards()
        
    def clear_cards(self):
        """清除所有卡牌显示"""
        # 清除玩家1的卡牌
        while self.player1_cards.count():
            item = self.player1_cards.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # 清除玩家2的卡牌
        while self.player2_cards.count():
            item = self.player2_cards.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def display_cards(self):
        """显示卡牌"""
        # 显示玩家1的卡牌
        for i, card in enumerate(self.player1_hand):
            card_button = QPushButton()
            card_button.setFixedSize(150, 220)
            card_button.setIcon(QIcon(card.get_card_back()))
            card_button.setIconSize(QSize(150, 220))
            card_button.clicked.connect(lambda checked, x=i: self.compare_cards(x))
            self.player1_cards.addWidget(card_button)
            
        # 显示玩家2的卡牌
        for i, card in enumerate(self.player2_hand):
            card_button = QPushButton()
            card_button.setFixedSize(150, 220)
            card_button.setIcon(QIcon(card.get_card_back()))
            card_button.setIconSize(QSize(150, 220))
            self.player2_cards.addWidget(card_button)
    
    def compare_cards(self, index):
        """比较两张卡牌"""
        if self.current_comparison != index:
            return
            
        # 获取当前比较的卡牌
        card1 = self.player1_hand[index]
        card2 = self.player2_hand[index]
        
        # 显示卡牌内容
        self.update_card_display(index, card1, card2)
        
        # 比较大小
        if card1.get_value() > card2.get_value():
            self.player1_wins += 1
            result = f"{card1} > {card2}，玩家1赢得此回合"
        elif card1.get_value() < card2.get_value():
            self.player2_wins += 1
            result = f"{card1} < {card2}，玩家2赢得此回合"
        else:
            result = f"{card1} = {card2}，平局"
            
        # 更新显示
        self.status_label.setText(result)
        self.player1_score.setText(f'得分: {self.player1_wins}')
        self.player2_score.setText(f'得分: {self.player2_wins}')
        
        # 检查是否完成所有比较
        self.current_comparison += 1
        if self.current_comparison >= 5:
            self.game_over()
        else:
            self.status_label.setText(f'{result}\n点击下一张卡牌继续比较')
    
    def update_card_display(self, index, card1, card2):
        """更新卡牌显示"""
        # 更新玩家1的卡牌
        card1_button = self.player1_cards.itemAt(index).widget()
        card1_button.setIcon(QIcon(card1.get_card_image()))
        
        # 更新玩家2的卡牌
        card2_button = self.player2_cards.itemAt(index).widget()
        card2_button.setIcon(QIcon(card2.get_card_image()))
    
    def game_over(self):
        """游戏结束"""
        # 生成详细结果信息
        result_info = (
            "游戏结束！\n\n"
            f"玩家1得分: {self.player1_wins}\n"
            f"玩家2得分: {self.player2_wins}\n\n"
        )
        
        if self.player1_wins > self.player2_wins:
            result_info += "玩家1获胜！"
        elif self.player1_wins < self.player2_wins:
            result_info += "玩家2获胜！"
        else:
            result_info += "平局！"
            
        self.result_display.setText(result_info)
        self.status_label.setText("点击'开始新游戏'重新开始")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = PokerGame()
    game.show()
    sys.exit(app.exec_()) 
