# 二叉排序树
# 要求:输入一组关键值,建立相应的二叉排序树
# 实现查找和删除功能
import os

import cv2
from PySide2.QtWidgets import QApplication, QMessageBox, QGraphicsPixmapItem, QGraphicsScene
from PySide2.QtCore import Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon, QPixmap, QImage
from BSTree import BSTNode, BinarySortTree
from draw_tree import draw


class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()


class BST_Front:
    def __init__(self, bstree):
        self.bstree = bstree
        # 从文件中加载UI定义
        qfile_BST = QFile("ui/BST.ui")
        qfile_BST.open(QFile.ReadOnly)
        qfile_BST.close()
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('ui/BST.ui')
        self.ui.pushButton_1.clicked.connect(self.create_front)
        self.ui.pushButton_2.clicked.connect(self.insert_front)
        self.ui.pushButton_3.clicked.connect(self.delete_front)
        self.ui.pushButton_4.clicked.connect(self.search_front)
        self.ui.pushButton_5.clicked.connect(self.clear_history)
        self.ui.pushButton.clicked.connect(self.show)

    def clear_history(self):
        self.ui.listWidget.clear()

    def create_front(self):
        if not self.bstree.is_empty():  # 非空树,已经建立
            choice = QMessageBox.question(self.ui, '询问', '已经建立了二叉树,此操作将重新建树,确认?')
            if choice == QMessageBox.No:
                self.ui.plainTextEdit_1.clear()
                return
            if choice == QMessageBox.Yes:
                pass
        # 初次建树
        self.bstree = BinarySortTree()
        info = self.ui.plainTextEdit_1.toPlainText()
        if not info:
            QMessageBox.critical(self.ui, "错误", "您还没有输入数据!")
            return
        info = info.strip().split(' ')
        prompt = "【建立二叉树】,插入了"
        for i in info:
            if i.strip():
                try:
                    data = int(i)
                except ValueError:
                    QMessageBox.critical(self.ui, "错误", "含有非整型数据!")
                    self.ui.plainTextEdit_1.clear()
                    return
                self.bstree.insert(data)
                prompt += i + ' '
        self.ui.listWidget.addItem(prompt)
        self.ui.plainTextEdit_1.clear()
        QMessageBox.about(self.ui, "完毕", "成功创建!")
        draw(self.bstree._root)
        return

    def insert_front(self):
        if self.bstree.is_empty():  # 非空树,已经建立
            QMessageBox.information(self.ui, "提示", "还未创建二叉树,此次操作将自动建树!")

        info = self.ui.plainTextEdit_2.toPlainText()
        if not info:
            QMessageBox.critical(self.ui, "错误", "您还没有输入数据!")
            return
        info = info.strip().split(' ')
        prompt = "【插入结点】,插入了"
        for i in info:
            if i.strip():
                try:
                    data = int(i)
                except ValueError:
                    QMessageBox.critical(self.ui, "错误", "含有非整型数据!")
                    self.ui.plainTextEdit_2.clear()
                    return
                self.bstree.insert(data)
                prompt += i + ' '
        self.ui.listWidget.addItem(prompt)
        self.ui.plainTextEdit_2.clear()
        QMessageBox.about(self.ui, "完毕", "成功插入!")
        draw(self.bstree._root)
        return

    def delete_front(self):
        if self.bstree.is_empty():
            QMessageBox.critical(self.ui, "错误", "尚未建树,无法删除!")
            self.ui.plainTextEdit_3.clear()
            return
        info = self.ui.plainTextEdit_3.toPlainText()
        if not info:
            QMessageBox.critical(self.ui, "错误", "您还没有输入数据!")
            self.ui.plainTextEdit_3.clear()
            return
        times = 0
        info = info.strip().split(' ')
        prompt = "【删除结点】,删除了"
        for i in info:
            if i.strip():
                try:
                    data = int(i)
                except ValueError:
                    QMessageBox.critical(self.ui, "错误", "含有非整型数据!")
                    self.ui.plainTextEdit_3.clear()
                    return
                if self.bstree.delete(data):
                    prompt += i + ' '
                    times += 1
        self.ui.listWidget.addItem(prompt)
        self.ui.plainTextEdit_3.clear()
        QMessageBox.about(self.ui, "完毕", f"成功删除{times}个结点!")
        draw(self.bstree._root)
        return

    def search_front(self):
        if self.bstree.is_empty():
            QMessageBox.critical(self.ui, "错误", "尚未建树,无法查询!")
            self.ui.plainTextEdit_4.clear()
        info = self.ui.plainTextEdit_4.toPlainText()
        if not info:
            QMessageBox.critical(self.ui, "错误", "您还没有输入数据!")
            self.ui.plainTextEdit_4.clear()
            return
        info = info.strip().split(' ')
        prompt = "【查询结点】,"
        suc_times = fail_times = 0
        result = "【查询结果】:\n"
        for i in info:
            if i.strip():
                try:
                    data = int(i)
                except ValueError:
                    QMessageBox.critical(self.ui, "错误", "含有非整型数据!")
                    self.ui.plainTextEdit_4.clear()
                    return
                if self.bstree.search(data) is None:
                    fail_times += 1
                    result += i + "--查询失败\n"
                else:
                    suc_times += 1
                    result += i + "--查询成功\n"
        prompt += f"成功{suc_times}次,失败{fail_times}次"
        self.ui.listWidget.addItem(prompt)
        self.ui.plainTextEdit_4.clear()
        QMessageBox.about(self.ui, "完毕", result)
        draw(self.bstree._root)
        return

    def show(self):
        img = cv2.imread('1.png')  # 读取图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.ui.graphicsView.setScene(self.scene)


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication([])
app.setWindowIcon(QIcon('image/logo.png'))  # 主窗口图标
mybst = BinarySortTree()
bst_front = BST_Front(mybst)
styleFile = './style/Aqua.qss'
qssStyle = CommonHelper.readQss(styleFile)
bst_front.ui.setStyleSheet(qssStyle)
bst_front.ui.show()
app.exec_()
