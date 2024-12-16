from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import psutil
import time
from datetime import datetime

class ProcessTableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([
            "进程名称", "PID", "状态", "CPU使用率", "内存使用", "启动时间"
        ])
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSortingEnabled(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.verticalHeader().setVisible(False)
        
        # 启用自动滚动条
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        
        # 优化表格性能
        self.setUpdatesEnabled(False)
        self.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.setStyleSheet("QTableWidget { gridline-color: #d8d8d8; }")
        
        # 存储进程信息的字典，用于优化更新
        self.process_items = {}

class SystemInfoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        
        # CPU使用率
        self.cpuLabel = QtWidgets.QLabel("CPU: 0%")
        self.cpuLabel.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.cpuLabel)
        
        # 内存使用率
        self.memLabel = QtWidgets.QLabel("内存: 0/0 GB (0%)")
        self.memLabel.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.memLabel)
        
        # 进程数量
        self.processLabel = QtWidgets.QLabel("进程数: 0")
        self.processLabel.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.processLabel)
        
        # 搜索框
        self.searchBox = QtWidgets.QLineEdit()
        self.searchBox.setPlaceholderText("搜索进程...")
        self.searchBox.setMaximumWidth(200)
        layout.addWidget(self.searchBox)
        
        layout.addStretch()

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        # 设置窗口基本属性
        Dialog.setObjectName("Task Manager")
        Dialog.resize(800, 600)
        Dialog.setWindowTitle("任务管理器")
        Dialog.setWindowFlags(Dialog.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint)
        
        # 创建主布局
        self.mainLayout = QtWidgets.QVBoxLayout(Dialog)
        
        # 创建系统信息面板
        self.sysInfoWidget = SystemInfoWidget()
        self.mainLayout.addWidget(self.sysInfoWidget)
        
        # 创建进程表格
        self.processTable = ProcessTableWidget()
        self.mainLayout.addWidget(self.processTable)
        
        # 创建按钮布局
        self.buttonLayout = QtWidgets.QHBoxLayout()
        
        # 创建刷新按钮
        self.refreshButton = QtWidgets.QPushButton("刷新")
        self.refreshButton.setMinimumWidth(100)
        self.buttonLayout.addWidget(self.refreshButton)
        
        # 创建结束进程按钮
        self.endTaskButton = QtWidgets.QPushButton("结束进程")
        self.endTaskButton.setMinimumWidth(100)
        self.buttonLayout.addWidget(self.endTaskButton)
        
        # 创建查看详情按钮
        self.detailsButton = QtWidgets.QPushButton("查看详情")
        self.detailsButton.setMinimumWidth(100)
        self.buttonLayout.addWidget(self.detailsButton)
        
        self.buttonLayout.addStretch()
        self.mainLayout.addLayout(self.buttonLayout)
        
        # 连接信号
        self.refreshButton.clicked.connect(self.refresh_data)
        self.endTaskButton.clicked.connect(self.end_task)
        self.detailsButton.clicked.connect(self.show_details)
        self.sysInfoWidget.searchBox.textChanged.connect(self.filter_processes)
        
        # 创建定时器，定期更新数据
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(1000)  # 每秒更新系统信息
        
        # 创建进程更新定时器
        self.process_timer = QtCore.QTimer()
        self.process_timer.timeout.connect(self.refresh_data)
        self.process_timer.start(5000)  # 每5秒更新进程列表
        
        # 初始化数据
        self.refresh_data()
        
        # 设置最小窗口大小
        Dialog.setMinimumSize(600, 400)

    def update_system_info(self):
        """只更新系统信息，不更新进程列表"""
        try:
            cpu_percent = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            mem_total = mem.total / (1024 * 1024 * 1024)  # GB
            mem_used = mem.used / (1024 * 1024 * 1024)    # GB
            process_count = len(psutil.pids())
            
            self.sysInfoWidget.cpuLabel.setText(f"CPU: {cpu_percent}%")
            self.sysInfoWidget.memLabel.setText(
                f"内存: {mem_used:.1f}/{mem_total:.1f} GB ({mem.percent}%)")
            self.sysInfoWidget.processLabel.setText(f"进程数: {process_count}")
        except:
            pass

    def refresh_data(self):
        """更新进程列表，使用增量更新方式"""
        try:
            self.processTable.setUpdatesEnabled(False)  # 暂停界面更新
            current_filter = self.sysInfoWidget.searchBox.text().lower()
            
            # 获取当前所有进程
            current_processes = {}
            for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 
                                           'memory_info', 'create_time']):
                try:
                    pinfo = proc.info
                    pid = str(pinfo['pid'])
                    current_processes[pid] = pinfo
                except:
                    continue
            
            # 删除已经不存在的进程
            rows_to_remove = []
            for row in range(self.processTable.rowCount()):
                pid = self.processTable.item(row, 1).text()
                if pid not in current_processes:
                    rows_to_remove.append(row)
            
            for row in reversed(rows_to_remove):
                self.processTable.removeRow(row)
            
            # 更新或添加进程
            for pid, pinfo in current_processes.items():
                if not self.match_filter(pinfo['name'], current_filter):
                    continue
                    
                row = self.find_process_row(pid)
                if row == -1:
                    # 添加新进程
                    row = self.processTable.rowCount()
                    self.processTable.insertRow(row)
                
                try:
                    # 更新进程信息
                    self.processTable.setItem(row, 0, 
                        QtWidgets.QTableWidgetItem(str(pinfo['name'])))
                    self.processTable.setItem(row, 1, 
                        QtWidgets.QTableWidgetItem(str(pid)))
                    self.processTable.setItem(row, 2, 
                        QtWidgets.QTableWidgetItem(str(pinfo['status'])))
                    self.processTable.setItem(row, 3, 
                        QtWidgets.QTableWidgetItem(f"{pinfo['cpu_percent']:.1f}%"))
                    memory_mb = pinfo['memory_info'].rss / (1024 * 1024)
                    self.processTable.setItem(row, 4, 
                        QtWidgets.QTableWidgetItem(f"{memory_mb:.1f} MB"))
                    create_time = datetime.fromtimestamp(pinfo['create_time'])
                    self.processTable.setItem(row, 5, 
                        QtWidgets.QTableWidgetItem(create_time.strftime("%Y-%m-%d %H:%M:%S")))
                except:
                    continue
            
            self.processTable.setUpdatesEnabled(True)  # 恢复界面更新
        except Exception as e:
            print(f"Error refreshing data: {e}")

    def find_process_row(self, pid):
        """查找进程在表格中的行号"""
        for row in range(self.processTable.rowCount()):
            if self.processTable.item(row, 1).text() == str(pid):
                return row
        return -1

    def match_filter(self, process_name, filter_text):
        """检查进程是否匹配过滤条件"""
        if not filter_text:
            return True
        return filter_text in process_name.lower()

    def filter_processes(self):
        """根据搜索框过滤进程"""
        self.refresh_data()

    def end_task(self):
        selected_rows = self.processTable.selectedItems()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(None, "警告", "请选择要结束的进程")
            return
        
        # 获取选中行的PID
        row = selected_rows[0].row()
        pid = int(self.processTable.item(row, 1).text())
        
        try:
            process = psutil.Process(pid)
            process_name = process.name()
            
            reply = QtWidgets.QMessageBox.question(None, "确认", 
                f"确定要结束进程 {process_name} (PID: {pid})?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            
            if reply == QtWidgets.QMessageBox.Yes:
                process.terminate()
                QtWidgets.QMessageBox.information(None, "成功", 
                    f"已结束进程：{process_name} (PID: {pid})")
                self.refresh_data()
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            QtWidgets.QMessageBox.warning(None, "错误", "无法结束该进程")

    def show_details(self):
        selected_rows = self.processTable.selectedItems()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(None, "警告", "请选择要查看的进程")
            return
        
        # 获取选中行的PID
        row = selected_rows[0].row()
        pid = int(self.processTable.item(row, 1).text())
        
        try:
            process = psutil.Process(pid)
            info = (
                f"进程名称: {process.name()}\n"
                f"PID: {process.pid}\n"
                f"状态: {process.status()}\n"
                f"CPU使用率: {process.cpu_percent()}%\n"
                f"内存使用: {process.memory_info().rss / (1024*1024):.1f} MB\n"
                f"创建时间: {datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"命令行: {' '.join(process.cmdline())}\n"
                f"工作目录: {process.cwd()}\n"
                f"用户: {process.username()}"
            )
            QtWidgets.QMessageBox.information(None, "进程详情", info)
            
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            QtWidgets.QMessageBox.warning(None, "错误", "无法获取进程信息")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_()) 
