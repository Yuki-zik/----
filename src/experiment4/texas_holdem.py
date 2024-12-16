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

class HandEvaluator:
    """手牌评估器"""
    @staticmethod
    def evaluate_hand(cards):
        """评估一手牌的大小"""
        if len(cards) < 5:
            return 0, "高牌", []
            
        # 获取所有花色和点数
        suits = [card.suit for card in cards]
        ranks = [card.get_value() for card in cards]
        
        # 检查同花顺
        if len(set(suits)) == 1:  # 同花
            sorted_ranks = sorted(ranks)
            if sorted_ranks[-1] - sorted_ranks[0] == 4:  # 顺子
                return 8, "同花顺", sorted(cards, key=lambda x: x.get_value())[-5:]
                
        # 检查四条
        for rank in set(ranks):
            if ranks.count(rank) == 4:
                four_cards = [card for card in cards if card.get_value() == rank]
                kicker = max([card for card in cards if card.get_value() != rank], key=lambda x: x.get_value())
                return 7, "四条", four_cards + [kicker]
                
        # 检查葫芦
        if len(set(ranks)) == 2:
            for rank in set(ranks):
                if ranks.count(rank) == 3:
                    three_cards = [card for card in cards if card.get_value() == rank]
                    pair_cards = [card for card in cards if card.get_value() != rank][:2]
                    return 6, "葫芦", three_cards + pair_cards
                    
        # 检查同花
        if len(set(suits)) == 1:
            return 5, "同花", sorted(cards, key=lambda x: x.get_value())[-5:]
            
        # 检查顺子
        sorted_ranks = sorted(ranks)
        if sorted_ranks[-1] - sorted_ranks[0] == 4:
            straight_cards = sorted(cards, key=lambda x: x.get_value())[-5:]
            return 4, "顺子", straight_cards
            
        # 检查三条
        for rank in set(ranks):
            if ranks.count(rank) == 3:
                three_cards = [card for card in cards if card.get_value() == rank]
                kickers = sorted([card for card in cards if card.get_value() != rank], 
                               key=lambda x: x.get_value())[-2:]
                return 3, "三条", three_cards + kickers
                
        # 检查两对
        pairs = [(rank, [card for card in cards if card.get_value() == rank]) 
                for rank in set(ranks) if ranks.count(rank) == 2]
        if len(pairs) == 2:
            pair_cards = sorted(pairs, key=lambda x: x[0])[-2:]
            two_pairs = pair_cards[0][1] + pair_cards[1][1]
            kicker = max([card for card in cards if card.get_value() not in [p[0] for p in pairs]], 
                        key=lambda x: x.get_value())
            return 2, "两对", two_pairs + [kicker]
        elif len(pairs) == 1:
            pair_cards = pairs[0][1]
            kickers = sorted([card for card in cards if card.get_value() != pairs[0][0]], 
                           key=lambda x: x.get_value())[-3:]
            return 1, "一对", pair_cards + kickers
            
        high_cards = sorted(cards, key=lambda x: x.get_value())[-5:]
        return 0, "高牌", high_cards

class TexasHoldem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initGame()
        
    def initUI(self):
        """初始化UI"""
        self.setWindowTitle('德州扑克')
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
        
        # 公共牌区域
        self.setup_community_cards(main_layout)
        
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
        self.player1_chips = QLabel('筹码: 1000')
        player1_layout.addWidget(self.player1_label)
        player1_layout.addWidget(self.player1_chips)
        
        self.player1_cards = QHBoxLayout()
        self.player1_cards.setAlignment(Qt.AlignCenter)
        player1_layout.addLayout(self.player1_cards)
        
        player_layout.addWidget(player1_frame)
        
        # 玩家2区域
        player2_frame = QFrame()
        player2_frame.setObjectName("cardArea")
        player2_layout = QVBoxLayout(player2_frame)
        
        self.player2_label = QLabel('玩家 2')
        self.player2_chips = QLabel('筹码: 1000')
        player2_layout.addWidget(self.player2_label)
        player2_layout.addWidget(self.player2_chips)
        
        self.player2_cards = QHBoxLayout()
        self.player2_cards.setAlignment(Qt.AlignCenter)
        player2_layout.addLayout(self.player2_cards)
        
        player_layout.addWidget(player2_frame)
        
        main_layout.addWidget(player_container)
        
    def setup_community_cards(self, main_layout):
        """设置公共牌区域"""
        community_frame = QFrame()
        community_frame.setObjectName("cardArea")
        community_layout = QVBoxLayout(community_frame)
        
        # 奖池显示
        self.pot_label = QLabel('奖池: 0')
        community_layout.addWidget(self.pot_label, alignment=Qt.AlignCenter)
        
        # 公共牌区域
        self.community_cards = QHBoxLayout()
        self.community_cards.setAlignment(Qt.AlignCenter)
        community_layout.addLayout(self.community_cards)
        
        main_layout.addWidget(community_frame)
        
    def setup_control_area(self, main_layout):
        """设置控制区域"""
        # 控制按钮区域
        control_frame = QFrame()
        control_frame.setObjectName("cardArea")
        control_layout = QHBoxLayout(control_frame)
        
        # 下注按钮
        self.bet_button = QPushButton('下注')
        self.bet_button.clicked.connect(self.bet)
        
        # 跟注按钮
        self.call_button = QPushButton('跟注')
        self.call_button.clicked.connect(self.call)
        
        # 加注按钮
        self.raise_button = QPushButton('加注')
        self.raise_button.clicked.connect(self.raise_bet)
        
        # 弃牌按钮
        self.fold_button = QPushButton('弃牌')
        self.fold_button.clicked.connect(self.fold)
        
        # 开始新游戏按钮
        self.new_game_button = QPushButton('开始新游戏')
        self.new_game_button.clicked.connect(self.start_new_game)
        
        # 添加按钮到布局
        control_layout.addWidget(self.bet_button)
        control_layout.addWidget(self.call_button)
        control_layout.addWidget(self.raise_button)
        control_layout.addWidget(self.fold_button)
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
        self.community_cards_list = []
        self.pot = 0
        self.current_bet = 0
        self.player1_chip_count = 1000
        self.player2_chip_count = 1000
        self.current_player = 1
        
        # 创建一副扑克牌
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.deck.append(Card(suit, rank))
                
        # 禁用游戏按钮
        self.disable_game_buttons()
        
    def start_new_game(self):
        """开始新游戏"""
        # 清空所有卡牌
        self.clear_all_cards()
        
        # 重置状态
        self.pot = 0
        self.current_bet = 0
        self.current_player = 1
        self.pot_label.setText('奖池: 0')
        
        # 洗牌
        random.shuffle(self.deck)
        
        # 发手牌
        self.player1_hand = self.deck[:2]
        self.player2_hand = self.deck[2:4]
        self.community_cards_list = []
        
        # 显示卡牌
        self.display_cards()
        
        # 启用游戏按钮
        self.enable_game_buttons()
        
        self.status_label.setText('游戏开始！玩家1回合')
        
    def clear_all_cards(self):
        """清除所有卡牌"""
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
                
        # 清除公共牌
        while self.community_cards.count():
            item = self.community_cards.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
    def display_cards(self):
        """显示卡牌"""
        # 显示玩家1的手牌
        for card in self.player1_hand:
            card_button = QPushButton()
            card_button.setFixedSize(150, 220)
            card_button.setIcon(QIcon(card.get_card_image()))
            card_button.setIconSize(QSize(150, 220))
            self.player1_cards.addWidget(card_button)
            
        # 显示玩家2的手牌（背面）
        for card in self.player2_hand:
            card_button = QPushButton()
            card_button.setFixedSize(150, 220)
            card_button.setIcon(QIcon(card.get_card_back()))
            card_button.setIconSize(QSize(150, 220))
            self.player2_cards.addWidget(card_button)
            
        # 显示公共牌
        for card in self.community_cards_list:
            card_button = QPushButton()
            card_button.setFixedSize(150, 220)
            card_button.setIcon(QIcon(card.get_card_image()))
            card_button.setIconSize(QSize(150, 220))
            self.community_cards.addWidget(card_button)
            
    def bet(self):
        """下注"""
        bet_amount = 20  # 固定下注额
        if self.current_player == 1:
            self.player1_chip_count -= bet_amount
            self.player1_chips.setText(f'筹码: {self.player1_chip_count}')
        else:
            self.player2_chip_count -= bet_amount
            self.player2_chips.setText(f'筹码: {self.player2_chip_count}')
            
        self.pot += bet_amount
        self.current_bet = bet_amount
        self.pot_label.setText(f'奖池: {self.pot}')
        
        self.next_turn()
        
    def call(self):
        """跟注"""
        if self.current_player == 1:
            self.player1_chip_count -= self.current_bet
            self.player1_chips.setText(f'筹码: {self.player1_chip_count}')
        else:
            self.player2_chip_count -= self.current_bet
            self.player2_chips.setText(f'筹码: {self.player2_chip_count}')
            
        self.pot += self.current_bet
        self.pot_label.setText(f'奖池: {self.pot}')
        
        self.next_turn()
        
    def raise_bet(self):
        """加注"""
        raise_amount = self.current_bet * 2
        if self.current_player == 1:
            self.player1_chip_count -= raise_amount
            self.player1_chips.setText(f'筹码: {self.player1_chip_count}')
        else:
            self.player2_chip_count -= raise_amount
            self.player2_chips.setText(f'筹码: {self.player2_chip_count}')
            
        self.pot += raise_amount
        self.current_bet = raise_amount
        self.pot_label.setText(f'奖池: {self.pot}')
        
        self.next_turn()
        
    def fold(self):
        """弃牌"""
        winner = 2 if self.current_player == 1 else 1
        self.game_over(winner)
        
    def next_turn(self):
        """进入下一轮"""
        # 切换玩家
        self.current_player = 2 if self.current_player == 1 else 1
        
        # 如果没有公共牌，发放翻牌
        if not self.community_cards_list:
            self.deal_flop()
        # 如果有3张公共牌，发放转牌
        elif len(self.community_cards_list) == 3:
            self.deal_turn()
        # 如果有4张公共牌，发放河牌
        elif len(self.community_cards_list) == 4:
            self.deal_river()
        # 如果有5张公共牌，进行最终比较
        elif len(self.community_cards_list) == 5:
            self.compare_hands()
            
        self.status_label.setText(f'玩家{self.current_player}回合')
        
    def deal_flop(self):
        """发放翻牌"""
        self.community_cards_list = self.deck[4:7]  # 发3张公共牌
        self.clear_all_cards()
        self.display_cards()
        
    def deal_turn(self):
        """发放转牌"""
        self.community_cards_list.append(self.deck[7])  # 发第4张公共牌
        self.clear_all_cards()
        self.display_cards()
        
    def deal_river(self):
        """发放河牌"""
        self.community_cards_list.append(self.deck[8])  # 发第5张公共牌
        self.clear_all_cards()
        self.display_cards()
        
    def compare_hands(self):
        """比较双方手牌"""
        # 评估玩家1的牌
        player1_cards = self.player1_hand + self.community_cards_list
        player1_score, player1_hand_type, player1_best_hand = HandEvaluator.evaluate_hand(player1_cards)
        
        # 评估玩家2的牌
        player2_cards = self.player2_hand + self.community_cards_list
        player2_score, player2_hand_type, player2_best_hand = HandEvaluator.evaluate_hand(player2_cards)
        
        # 生成详细结果信息，使用空格而不是制表符来缩进
        result_info = (
            "游戏结束！\n\n"
            f"奖池: {self.pot}\n\n"
            f"公共牌：{', '.join(str(card) for card in self.community_cards_list)}\n\n"
            "玩家1：\n"
            f"    筹码: {self.player1_chip_count}\n"
            f"    手牌：{', '.join(str(card) for card in self.player1_hand)}\n"
            f"    牌型：{player1_hand_type}\n"
            f"    最佳组合：{', '.join(str(card) for card in player1_best_hand)}\n\n"
            "玩家2：\n"
            f"    筹码: {self.player2_chip_count}\n"
            f"    手牌：{', '.join(str(card) for card in self.player2_hand)}\n"
            f"    牌型：{player2_hand_type}\n"
            f"    最佳组合：{', '.join(str(card) for card in player2_best_hand)}"
        )
        
        # 确定赢家
        if player1_score > player2_score:
            result_info += "\n\n玩家1获胜"
            self.game_over(1, result_info)
        elif player2_score > player1_score:
            result_info += "\n\n玩家2获胜！"
            self.game_over(2, result_info)
        else:
            result_info += "\n\n平局！"
            self.game_over(0, result_info)
            
    def game_over(self, winner, result_info=""):
        """游戏结束"""
        if winner == 0:
            self.result_display.setText(result_info)  # 使用QTextEdit显示结果
            # 平分奖池
            split_pot = self.pot // 2
            self.player1_chip_count += split_pot
            self.player2_chip_count += split_pot
        else:
            self.result_display.setText(result_info)  # 使用QTextEdit显示结果
            if winner == 1:
                self.player1_chip_count += self.pot
            else:
                self.player2_chip_count += self.pot
                
        # 更新筹码显示
        self.player1_chips.setText(f'筹码: {self.player1_chip_count}')
        self.player2_chips.setText(f'筹码: {self.player2_chip_count}')
        
        # 显示所有卡牌
        self.clear_all_cards()
        self.display_all_cards()
        
        # 禁用游戏按钮
        self.disable_game_buttons()
        
    def display_all_cards(self):
        """显示所有卡牌（包括玩家2的手牌）"""
        # 显示玩家1的手牌
        for card in self.player1_hand:
            card_button = QPushButton()
            card_button.setFixedSize(150, 220)
            card_button.setIcon(QIcon(card.get_card_image()))
            card_button.setIconSize(QSize(150, 220))
            self.player1_cards.addWidget(card_button)
            
        # 显示玩家2的手牌（正面）
        for card in self.player2_hand:
            card_button = QPushButton()
            card_button.setFixedSize(150, 220)
            card_button.setIcon(QIcon(card.get_card_image()))
            card_button.setIconSize(QSize(150, 220))
            self.player2_cards.addWidget(card_button)
            
        # 显示公共牌
        for card in self.community_cards_list:
            card_button = QPushButton()
            card_button.setFixedSize(150, 220)
            card_button.setIcon(QIcon(card.get_card_image()))
            card_button.setIconSize(QSize(150, 220))
            self.community_cards.addWidget(card_button)
            
    def enable_game_buttons(self):
        """启用游戏按钮"""
        self.bet_button.setEnabled(True)
        self.call_button.setEnabled(True)
        self.raise_button.setEnabled(True)
        self.fold_button.setEnabled(True)
        
    def disable_game_buttons(self):
        """禁用游戏按钮"""
        self.bet_button.setEnabled(False)
        self.call_button.setEnabled(False)
        self.raise_button.setEnabled(False)
        self.fold_button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = TexasHoldem()
    game.show()
    sys.exit(app.exec_()) 
