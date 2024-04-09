# -*- coding: utf-8 -*-
import sys

################################################################################
## Form generated from reading UI file 'main_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide2.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QMainWindow, QMenuBar, QPushButton,
                               QSizePolicy, QTextEdit, QVBoxLayout, QWidget, QDesktopWidget)
# from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
#                             QMetaObject, QObject, QPoint, QRect,
#                             QSize, QTime, QUrl, Qt)
# from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
#                            QFont, QFontDatabase, QGradient, QIcon,
#                            QImage, QKeySequence, QLinearGradient, QPainter,
#                            QPalette, QPixmap, QRadialGradient, QTransform)
# from PyQt5.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
#                                QLineEdit, QMainWindow, QMenuBar, QPushButton,
#                                QSizePolicy, QTextEdit, QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

            # Calculate window size based on screen ratio
        desktop = QDesktopWidget()
        screen_geometry = desktop.screenGeometry()
        screen_ratio = screen_geometry.width() / screen_geometry.height()

        width = int(0.8 * screen_geometry.width())  # Adjust the factor as needed
        height = int(width / screen_ratio)

        x = (screen_geometry.width() - width) // 2
        y = (screen_geometry.height() - height) // 2

        MainWindow.setGeometry(x, y, width, height)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        font = QFont()
        font.setBold(True)
        self.groupBox.setFont(font)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.pic_show = QLabel(self.groupBox)
        self.pic_show.setObjectName(u"pic_show")

        self.horizontalLayout_3.addWidget(self.pic_show)

        self.horizontalLayout_4.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.groupBox_2.setFont(font1)
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.res_show = QTextEdit(self.groupBox_2)
        self.res_show.setObjectName(u"res_show")

        self.verticalLayout.addWidget(self.res_show)

        self.horizontalLayout_4.addWidget(self.groupBox_2)

        self.horizontalLayout_4.setStretch(0, 4)
        self.horizontalLayout_4.setStretch(1, 2)

        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(50, -1, 50, -1)
        self.screenshot = QPushButton(self.groupBox_3)
        self.screenshot.setObjectName(u"screenshot")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.screenshot.sizePolicy().hasHeightForWidth())
        self.screenshot.setSizePolicy(sizePolicy)
        self.screenshot.setStyleSheet(u"font: 700 15pt \"Microsoft YaHei UI\";")

        self.horizontalLayout.addWidget(self.screenshot)

        self.recognize = QPushButton(self.groupBox_3)
        self.recognize.setObjectName(u"recognize")
        sizePolicy.setHeightForWidth(self.recognize.sizePolicy().hasHeightForWidth())
        self.recognize.setSizePolicy(sizePolicy)
        self.recognize.setStyleSheet(u"font: 700 15pt \"Microsoft YaHei UI\";")

        self.horizontalLayout.addWidget(self.recognize)

        self.save_result = QPushButton(self.groupBox_3)
        self.save_result.setObjectName(u"save_result")
        sizePolicy.setHeightForWidth(self.save_result.sizePolicy().hasHeightForWidth())
        self.save_result.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setFamilies([u"Microsoft YaHei UI"])
        font2.setPointSize(15)
        font2.setBold(True)
        font2.setItalic(False)
        self.save_result.setFont(font2)
        self.save_result.setStyleSheet(u"font: 700 15pt \"Microsoft YaHei UI\";\n"
                                       "")
        self.save_result.setFlat(False)

        self.horizontalLayout.addWidget(self.save_result)

        self.print_result = QPushButton(self.groupBox_3)
        self.print_result.setObjectName(u"print_result")
        sizePolicy.setHeightForWidth(self.print_result.sizePolicy().hasHeightForWidth())
        self.print_result.setSizePolicy(sizePolicy)
        self.print_result.setStyleSheet(u"font: 700 15pt \"Microsoft YaHei UI\";\n"
                                        "")

        self.horizontalLayout.addWidget(self.print_result)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, -1, 10, -1)
        self.path = QLineEdit(self.groupBox_3)
        self.path.setObjectName(u"path")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.path.sizePolicy().hasHeightForWidth())
        self.path.setSizePolicy(sizePolicy1)
        self.path.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")
        self.path.setCursorMoveStyle(Qt.LogicalMoveStyle)
        self.path.setClearButtonEnabled(False)

        self.horizontalLayout_2.addWidget(self.path)

        self.path_slc = QPushButton(self.groupBox_3)
        self.path_slc.setObjectName(u"path_slc")
        sizePolicy.setHeightForWidth(self.path_slc.sizePolicy().hasHeightForWidth())
        self.path_slc.setSizePolicy(sizePolicy)
        self.path_slc.setStyleSheet(u"font: 700 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_2.addWidget(self.path_slc)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalLayout_3.addWidget(self.groupBox_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1034, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u663e\u793a", None))
        self.pic_show.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u7ed3\u679c\u8f93\u51fa", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u529f\u80fd\u5b9e\u73b0", None))
        self.screenshot.setText(QCoreApplication.translate("MainWindow", u"\u622a\u56fe", None))
        self.recognize.setText(QCoreApplication.translate("MainWindow", u"\u590d\u5236", None))
        self.save_result.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
        self.print_result.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5370", None))
        self.path.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u9ed8\u8ba4\u4fdd\u5b58\u8def\u5f84", None))
        self.path_slc.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8", None))
    # retranslateUi


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    mainwindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec())
