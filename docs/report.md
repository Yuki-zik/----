## 任务四：扑克牌游戏实现

### 4.1 基本功能实现

#### 4.1.1 游戏规则
- 为2个玩家随机分配5张扑克牌
- 玩家轮流点击卡牌背面，显示并比较对应位置的牌的大小
- 每轮比较后计算得分
- 5张牌全部比较完后，显示最终胜负结果

#### 4.1.2 核心类设计

1. Card类（扑克牌类）
```python
class Card:
    SUITS = ['♠', '♥', '♦', '♣']  # 花色
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  # 点数
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def get_value(self):
        return Card.RANKS.index(self.rank)  # 获取牌的大小值
```

2. PokerGame类（游戏主类）
- 继承自QMainWindow
- 实现游戏界面和逻辑控制
- 主要功能：
  - 发牌和洗牌
  - 卡牌显示和更新
  - 比较规则实现
  - 得分统计
  - 游戏状态管理

#### 4.1.3 界面设计
1. 布局结构
- 顶部：玩家标签和得分显示
- 中间：卡牌显示区域
  - 左侧：玩家1的卡牌
  - 中间：游戏状态和控制按钮
  - 右侧：玩家2的��牌
- 底部：游戏状态提示

2. 视觉设计
- 使用现代化的扁平设计
- 深色主题背景（#2C3E50）
- 突出显示的按钮和交互元素
- 红黑双色的扑克牌显示
- 圆角边框和阴影效果

#### 4.1.4 关键功能实现

1. 发牌机制
```python
def start_new_game(self):
    random.shuffle(self.deck)  # 洗牌
    self.player1_hand = self.deck[:5]  # 玩家1发5张牌
    self.player2_hand = self.deck[5:10]  # 玩家2发5张牌
```

2. 卡牌比较
```python
def compare_cards(self, index):
    card1 = self.player1_hand[index]
    card2 = self.player2_hand[index]
    
    if card1.get_value() > card2.get_value():
        self.player1_wins += 1
        result = f"{card1} > {card2}，玩家1赢得此回合"
    elif card1.get_value() < card2.get_value():
        self.player2_wins += 1
        result = f"{card1} < {card2}，玩家2赢得此回合"
    else:
        result = f"{card1} = {card2}，平局"
```

3. 游戏状态管理
```python
def game_over(self):
    if self.player1_wins > self.player2_wins:
        result = "游戏结束！玩家1获胜！"
    elif self.player1_wins < self.player2_wins:
        result = "游戏结束！玩家2获胜！"
    else:
        result = "游戏结束！平局！"
```

### 4.2 扩展功能：德州扑克基本实现

#### 4.2.1 计划实现的功能
1. 发牌规则
   - 每位玩家2张手牌
   - 5张公共牌（翻牌、转牌、河牌）

2. 牌型判断
   - 同花顺
   - 四条
   - 葫芦
   - 同花
   - 顺子
   - 三条
   - 两对
   - 一对
   - 高牌

3. 游戏流程
   - 发手牌
   - 下注阶段
   - 发公共牌
   - 最终比牌

#### 4.2.2 技术要点
1. 牌型判断算法
2. 下注系统实现
3. 多人游戏支持
4. 动画效果
5. 游戏进度保存

### 4.3 实现难点及解决方案

1. 界面布局优化
   - 问题：需要合理安排卡牌显示和操作区域
   - 解决：使用QGridLayout实现灵活的网格布局

2. 卡牌点击顺序控制
   - 问题：确保玩家按顺序点击卡牌
   - 解决：使用current_comparison变量追踪当前比较进度

3. 游戏状态管理
   - 问题：需要准确追踪游戏进程和得分
   - 解决：实现完整的状态管理系统

4. 视觉反馈
   - 问题：提供清晰的游戏状态反馈
   - 解决：使用样式表和动态更新实现即时反馈

### 4.4 改进方向

1. 界面美化
   - 添加卡牌翻转动画
   - 优化视觉效果
   - 添加音效

2. 功能扩展
   - 实现完整的德州扑克规则
   - 添加AI对手
   - 支持联网对战

3. 性能优化
   - 优化卡牌渲染
   - 改进内存管理
   - 提高响应速度 

## 4. 扑克游戏实现

### 4.1 基本功能实现

#### 4.1.1 实现思路

1. 游戏界面设计
   - 采用PyQt5实现现代化的游戏界面
   - 使用深绿色主题，营造扑克游戏氛围
   - 界面分为三个主要区域：玩家区域、控制区域和结果显示区域

2. 扑克牌的实现
   - 创建Card类表示扑克牌
   - 使用PyQt5的绘图功能实现扑克牌的可视化
   - 实现正面和背面的绘制
   ```python
   class Card:
       SUITS = ['S', 'H', 'D', 'C']  # 黑桃、红心、方块、梅花
       RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
   ```

3. 游戏逻辑实现
   - 初始化：创建52张牌的完整牌组
   - 发牌：随机分配每人5张牌
   - 比较逻辑：按顺序比较对应位置的牌
   - 计分系统：记录每位玩家的胜利次数

#### 4.1.2 关键代码实现

1. 扑克牌绘制
   ```python
   def get_card_image(self):
       """获取卡牌图片"""
       pixmap = QPixmap(150, 220)
       # 绘制卡牌边框和阴影
       painter.setPen(Qt.NoPen)
       painter.setBrush(QColor(0, 0, 0, 20))
       painter.drawRoundedRect(5, 5, 146, 216, 8, 8)
       # 绘制点数和花色
       painter.drawText(QRect(15, 15, 45, 45), Qt.AlignCenter, self.rank)
       # ... 其他绘制代码
   ```

2. 发牌和洗牌
   ```python
   def start_new_game(self):
       random.shuffle(self.deck)  # 洗牌
       self.player1_hand = self.deck[:5]  # 玩家1发5张牌
       self.player2_hand = self.deck[5:10]  # 玩家2发5张牌
   ```

3. 比较逻辑
   ```python
   def compare_cards(self, index):
       card1 = self.player1_hand[index]
       card2 = self.player2_hand[index]
       if card1.get_value() > card2.get_value():
           self.player1_wins += 1
           result = f"{card1} > {card2}，玩家1赢得此回合"
       # ... 其他比较逻辑
   ```

#### 4.1.3 功能特点

1. 游戏流程
   - 点击"开始新游戏"按钮开始新一局
   - 玩家通过点击卡牌背面进行比较
   - 每次比较后显示当前回合结果
   - 完成5轮比较后显示最终结果

2. 界面交互
   - 卡牌采用可点击的按钮形式
   - 动态显示比较结果和得分
   - 使用QTextEdit显示详细的游戏结果
   - 状态标签提供游戏进度提示

3. 视觉效果
   - 扑克牌采用现代化设计
   - 使用圆角和阴影增强视觉效果
   - 红色和黑色区分不同花色
   - 背面采用网格纹理设计

#### 4.1.4 实现难点及解决方案

1. 卡牌点击事件处理
   - 难点：需要确保按正确顺序点击卡牌
   - 解决：使用current_comparison变量追踪当前比较进度
   ```python
   if self.current_comparison != index:
       return  # 确保按顺序点击
   ```

2. 界面布局管理
   - 难点：需要合理组织多个区域的布局
   - 解决：使用嵌套的布局管理器和QFrame
   ```python
   def setup_player_area(self, main_layout):
       player_container = QWidget()
       player_layout = QHBoxLayout(player_container)
       # ... 布局代码
   ```

3. 结果显示
   - 难点：需要清晰展示比较过程和最终结果
   - 解决：使用QTextEdit显示详细信息，状态标签显示即时反馈
   ```python
   def game_over(self):
       result_info = (
           "游戏结束！\n\n"
           f"玩家1得分: {self.player1_wins}\n"
           f"玩家2得分: {self.player2_wins}\n\n"
       )
   ```

### 4.2 改进与优化

1. 界面美化
   - 采用现代化的深绿色主题
   - 统一的按钮和卡牌样式
   - 合理的间距和边距设置

2. 交互优化
   - 清晰的游戏状态提示
   - 即时的比较结果反馈
   - 详细的最终得分展示

3. 代码结构优化
   - 类的合理划分
   - 功能模块化
   - 代码复用性提高
