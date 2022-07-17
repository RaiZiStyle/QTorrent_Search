#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets


class IconDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(IconDelegate, self).initStyleOption(option, index)
        if option.features & QtWidgets.QStyleOptionViewItem.HasDecoration:
            s = option.decorationSize
            s.setWidth(option.rect.width())
            option.decorationSize = s


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ServiceTableWidget = QtWidgets.QTableWidget(3, 3)

        delegate = IconDelegate(self.ServiceTableWidget)  # <---
        self.ServiceTableWidget.setItemDelegate(delegate)  # <---

        icon_file = "icons/download.png"
        status_item = QtWidgets.QTableWidgetItem()
        status_icon = QtGui.QIcon()
        status_icon.addPixmap(QtGui.QPixmap(icon_file),
                              QtGui.QIcon.Normal, QtGui.QIcon.Off)
        status_item.setIcon(status_icon)
        self.ServiceTableWidget.setItem(0, 0, status_item)

        self.setCentralWidget(self.ServiceTableWidget)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
