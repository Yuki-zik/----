# Python课程设计项目

基于PyQt5的四个实验项目实现，包括进程管理器、汉字检测、验证码系统和扑克牌游戏。

## 项目结构

```
python-course-design/
├── docs/                      # 文档目录
│   ├── 实验报告.md            # 详细实验报告
│   └── 验证码设计说明.md      # 验证码实现说明
├── src/                       # 源代码目录
│   ├── experiment1/          # 实验一：进程管理
│   ├── experiment2/          # 实验二：汉字检测
│   ├── experiment3/          # 实验三：验证码系统
│   │   ├── login_with_captcha.py        # 基础验证码实现
│   │   └── login_with_enhanced_captcha.py# 增强版验证码实现
│   └── experiment4/          # 实验四：扑克牌游戏
├── requirements.txt          # 项目依赖
├── LICENSE                   # 开源协议
└── README.md                # 项目说明
```

## 功能特性

### 1. 进程管理器
- 进程查看与管理
- 实时性能监控
- 进程关闭功能
- 异常处理机制

### 2. 汉字检测程序
- 汉字判断功能
- 正则表达式验证
- 实时检测响应
- 多种格式验证

### 3. 验证码系统
- 基础滑块验证
- 增强版障碍验证
- 现代化界面设计
- 完整的验证机制

### 4. 扑克牌游戏
- 基础扑克对战
- 德州扑克玩法
- 动画效果系统
- 声音反馈机制

## 环境要求

- Python 3.8+
- PyQt5
- psutil (用于进程管理)
- 其他依赖见requirements.txt

## 安装说明

1. 克隆仓库
```bash
git clone https://github.com/yourusername/python-course-design.git
cd python-course-design
```

2. 创建虚拟环境（可选）
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

## 使用说明

### 进程管理器
```bash
cd src/experiment1
python process_manager.py
```

### 汉字检测程序
```bash
cd src/experiment2
python chinese_detector.py
```

### 验证码系统
```bash
cd src/experiment3
python login_with_captcha.py        # 基础版本
python login_with_enhanced_captcha.py# 增强版本
```

### 扑克牌游戏
```bash
cd src/experiment4
python poker_game.py
```

## 项目特点

1. 模块化设计
   - 清晰的代码结构
   - 高度的可维护性
   - 便于功能扩展

2. 现代化界面
   - PyQt5实现
   - 响应式设计
   - 美观的视觉效果

3. 完善的文档
   - 详细的设计说明
   - 完整的实验报告
   - 清晰的注��说明

## 贡献指南

1. Fork 本仓库
2. 创建新的分支 `git checkout -b feature/your-feature`
3. 提交更改 `git commit -am 'Add some feature'`
4. 推送到分支 `git push origin feature/your-feature`
5. 创建 Pull Request

## 开源协议

本项目采用 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。

## 作者

- 作者：[Your Name]
- 邮箱：[Your Email]
- GitHub：[Your GitHub Profile]

## 致谢

感谢以下开源项目的支持：
- PyQt5
- psutil
- Python标准库
``` 
