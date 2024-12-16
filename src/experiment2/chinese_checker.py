from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import re

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        Dialog.setWindowTitle("文本分析工具")
        Dialog.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: white;
                border-radius: 4px;
            }
            QTabWidget::tab-bar {
                left: 5px;
            }
            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #cccccc;
                padding: 10px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-size: 16px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background: white;
                selection-background-color: #2196F3;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QLabel {
                color: #424242;
                font-size: 16px;
            }
        """)
        
        # 创建主布局
        self.mainLayout = QtWidgets.QVBoxLayout(Dialog)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)
        
        # 创建标题
        self.titleLabel = QtWidgets.QLabel("文本分析工具")
        self.titleLabel.setStyleSheet("""
            font-size: 32px;
            color: #1976D2;
            font-weight: bold;
            margin-bottom: 15px;
        """)
        self.mainLayout.addWidget(self.titleLabel)
        
        # 创建选项卡控件
        self.tabWidget = QtWidgets.QTabWidget()
        self.mainLayout.addWidget(self.tabWidget)
        
        # 创建汉字检测标签页
        self.chineseTab = QtWidgets.QWidget()
        self.tabWidget.addTab(self.chineseTab, "汉字检测")
        
        # 汉字检测标签页布局
        self.chineseLayout = QtWidgets.QVBoxLayout(self.chineseTab)
        self.chineseLayout.setContentsMargins(20, 20, 20, 20)
        self.chineseLayout.setSpacing(15)
        
        # 输入框和标签
        self.inputLabel = QtWidgets.QLabel("请输入要分析的文本：")
        self.inputLabel.setStyleSheet("font-size: 18px; margin-bottom: 8px;")
        self.chineseLayout.addWidget(self.inputLabel)
        
        self.inputEdit = QtWidgets.QLineEdit()
        self.inputEdit.setPlaceholderText("在此输入文本...")
        self.inputEdit.setMinimumHeight(50)
        self.inputEdit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 18px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
        """)
        self.chineseLayout.addWidget(self.inputEdit)
        
        # 检测按钮
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.addStretch()
        
        self.checkButton = QtWidgets.QPushButton("分析文本")
        self.checkButton.setMinimumWidth(150)
        self.checkButton.setMinimumHeight(46)
        self.checkButton.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                padding: 10px 24px;
            }
        """)
        self.buttonLayout.addWidget(self.checkButton)
        
        self.chineseLayout.addLayout(self.buttonLayout)
        
        # 创建结果框
        self.resultFrame = QtWidgets.QFrame()
        self.resultFrame.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 15px;
            }
        """)
        self.resultLayout = QtWidgets.QVBoxLayout(self.resultFrame)
        
        # 统计结果显示
        self.summaryLabel = QtWidgets.QLabel()
        self.summaryLabel.setStyleSheet("""
            font-weight: bold;
            color: #2196F3;
            font-size: 18px;
            padding: 15px;
            background: #E3F2FD;
            border-radius: 4px;
            line-height: 150%;
        """)
        self.resultLayout.addWidget(self.summaryLabel)
        
        # 详细结果显示
        self.resultLabel = QtWidgets.QLabel()
        self.resultLabel.setWordWrap(True)
        self.resultLabel.setStyleSheet("""
            padding: 15px;
            line-height: 160%;
            color: #616161;
            font-size: 16px;
        """)
        self.resultLayout.addWidget(self.resultLabel)
        
        self.chineseLayout.addWidget(self.resultFrame)
        
        # 创建正则表达式标签页
        self.regexTab = QtWidgets.QWidget()
        self.tabWidget.addTab(self.regexTab, "格式验证")
        
        # 正则表达式标签页布局
        self.regexLayout = QtWidgets.QVBoxLayout(self.regexTab)
        self.regexLayout.setContentsMargins(20, 20, 20, 20)
        self.regexLayout.setSpacing(15)
        
        # 输入框和标签
        self.regexInputLabel = QtWidgets.QLabel("请输入要验证的文本：")
        self.regexInputLabel.setStyleSheet("font-size: 18px; margin-bottom: 8px;")
        self.regexLayout.addWidget(self.regexInputLabel)
        
        self.regexInputEdit = QtWidgets.QLineEdit()
        self.regexInputEdit.setPlaceholderText("在此输入文本...")
        self.regexInputEdit.setMinimumHeight(50)
        self.regexInputEdit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 18px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
        """)
        self.regexLayout.addWidget(self.regexInputEdit)
        
        # 结果显示框
        self.regexResultFrame = QtWidgets.QFrame()
        self.regexResultFrame.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 15px;
            }
        """)
        self.regexResultLayout = QtWidgets.QVBoxLayout(self.regexResultFrame)
        
        # 添加各种格式的验证结果标签
        self.regexResults = {}
        for format_type in ["手机号码", "身份证号码", "邮箱地址", "网址"]:
            label = QtWidgets.QLabel()
            label.setWordWrap(True)
            label.setStyleSheet("""
                padding: 15px;
                margin-bottom: 8px;
                font-size: 16px;
                border-radius: 4px;
                line-height: 150%;
            """)
            self.regexResults[format_type] = label
            self.regexResultLayout.addWidget(label)
        
        self.regexLayout.addWidget(self.regexResultFrame)
        
        # 添加弹性空间
        self.chineseLayout.addStretch()
        self.regexLayout.addStretch()
        
        # 连接信号
        self.checkButton.clicked.connect(self.check_chinese)
        self.inputEdit.textChanged.connect(self.on_text_changed)
        self.regexInputEdit.textChanged.connect(self.on_regex_text_changed)

    def is_chinese(self, char):
        """判断单个字符是否为汉字"""
        return '\u4e00' <= char <= '\u9fff'

    def analyze_text(self, text):
        """分析文本组成"""
        total_chars = len(text)
        if total_chars == 0:
            return None
        
        chinese_chars = sum(1 for c in text if self.is_chinese(c))
        digit_chars = sum(1 for c in text if c.isdigit())
        letter_chars = sum(1 for c in text if c.isalpha() and not self.is_chinese(c))
        other_chars = total_chars - chinese_chars - digit_chars - letter_chars
        
        return {
            'total': total_chars,
            'chinese': (chinese_chars, chinese_chars / total_chars * 100),
            'digit': (digit_chars, digit_chars / total_chars * 100),
            'letter': (letter_chars, letter_chars / total_chars * 100),
            'other': (other_chars, other_chars / total_chars * 100)
        }

    def get_text_summary(self, stats):
        """生成文本统计摘要"""
        if not stats:
            return "请输入文本"
        
        # 生成主要组成部分的描述
        components = []
        if stats['chinese'][0] > 0:
            components.append(f"汉字{stats['chinese'][0]}个({stats['chinese'][1]:.1f}%)")
        if stats['digit'][0] > 0:
            components.append(f"数字{stats['digit'][0]}个({stats['digit'][1]:.1f}%)")
        if stats['letter'][0] > 0:
            components.append(f"字母{stats['letter'][0]}个({stats['letter'][1]:.1f}%)")
        if stats['other'][0] > 0:
            components.append(f"其他字符{stats['other'][0]}个({stats['other'][1]:.1f}%)")
        
        # 生成文本类型描述
        if stats['chinese'][0] == stats['total']:
            type_desc = "【全是汉字】"
        elif stats['chinese'][0] == 0:
            type_desc = "【无汉字】"
        elif stats['chinese'][1] >= 50:
            type_desc = "【以汉字为主】"
        else:
            type_desc = "【混合文本】"
        
        return f"文本长度：{stats['total']}个字符 {type_desc}\n" + "，".join(components)

    def check_chinese(self):
        """检查输入文本中的汉字"""
        text = self.inputEdit.text()
        if not text:
            self.summaryLabel.setText("请输入文本")
            self.resultLabel.setText("")
            return
        
        # 分析文本统计信息
        stats = self.analyze_text(text)
        self.summaryLabel.setText(self.get_text_summary(stats))
        
        # 显示详细信息
        result = []
        for i, char in enumerate(text):
            char_type = "汉字" if self.is_chinese(char) else (
                "数字" if char.isdigit() else (
                "字母" if char.isalpha() else "其他字符"
            ))
            result.append(f"字符 '{char}' (位置 {i+1}) 是{char_type}")
        
        self.resultLabel.setText("\n".join(result))

    def on_text_changed(self):
        """输入文本改变时实时检测"""
        self.check_chinese()

    def check_regex(self):
        """使用正则表达式进行检测"""
        text = self.regexInputEdit.text()
        if not text:
            for label in self.regexResults.values():
                label.setText("请输入文本")
                label.setStyleSheet("""
                    padding: 15px;
                    margin-bottom: 8px;
                    font-size: 16px;
                    color: #757575;
                    border-radius: 4px;
                    line-height: 150%;
                """)
            return
        
        patterns = {
            "手机号码": r"^1[3-9]\d{9}$",
            "身份证号码": r"^[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$",
            "邮箱地址": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "网址": r"^(http|https)://[a-zA-Z0-9\-._~:/?#\[\]@!$&'()*+,;=]+$"
        }
        
        for format_type, pattern in patterns.items():
            label = self.regexResults[format_type]
            if re.match(pattern, text):
                label.setText(f"√ 符合{format_type}格式")
                label.setStyleSheet("""
                    padding: 15px;
                    margin-bottom: 8px;
                    font-size: 16px;
                    color: #4CAF50;
                    background: #E8F5E9;
                    border-radius: 4px;
                    font-weight: bold;
                    line-height: 150%;
                """)
            else:
                label.setText(f"× 不符合{format_type}格式")
                label.setStyleSheet("""
                    padding: 15px;
                    margin-bottom: 8px;
                    font-size: 16px;
                    color: #F44336;
                    background: #FFEBEE;
                    border-radius: 4px;
                    font-weight: bold;
                    line-height: 150%;
                """)

    def on_regex_text_changed(self):
        """输入文本改变时实时检测"""
        self.check_regex()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')  
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_()) 
