#!/usr/bin/env python3
"""
Example d'ouverture d'une nouvelle fenettre (class Widget)
après l'appuie d'un QAction ajouté a la toolbar & au menu
"""

import sys
from platform import python_version

from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication,
                             QWidget, QLabel, QVBoxLayout, QInputDialog,
                             QTableWidget, QTableWidgetItem, QStyledItemDelegate, QStyleOptionViewItem)
# from PyQt5
from PyQt5.QtGui import QIcon
from PyQt5.Qt import PYQT_VERSION_STR

from review import ReviewForm
from torrent import TorrentApi


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        exitAct = QAction(
            QIcon('icons/exit24.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Quit')
        exitAct.triggered.connect(self.close)

        searchAct = QAction(QIcon("icons/search.png"), "Search", self)
        searchAct.setShortcut("Ctrl+o")
        searchAct.setStatusTip("Search Torrent")
        searchAct.triggered.connect(self.showDialog)

        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)

        layout = QVBoxLayout()
        self.helpWindow = HelpWindow()
        self.reviewForm = ReviewForm()
        self.torrentApi = TorrentApi()
        # searchLE = QInputDialog.getText(self, 'Input Dialog',
        #                                      'Enter your name:')
        # self.helpWindow.showHelp()
        # helpWindow.setStatusTip('Show the help for using the application')

        helpAct = QAction(QIcon("icons/info.png"), 'Info', self)
        helpAct.setShortcut("F1")
        helpAct.setStatusTip("Show the help for using the application")
        helpAct.triggered.connect(self.helpWindow.showHelp)

        reviewAct = QAction(QIcon("icons/form.png"), 'Review', self)
        reviewAct.setStatusTip(
            "Show a form to send to the autor of the application")
        reviewAct.triggered.connect(self.reviewForm.showReview)

        self.statusBar()

        self.tableWidget = QTableWidget()
        # set row count
        self.tableWidget.setRowCount(100)
        # set column count
        self.tableWidget.setColumnCount(8)
        header = ['Name', 'Size', 'Added', 'Status',
                  'Leechers', 'Seeders', 'Ratio', 'Download']
        self.tableWidget.setHorizontalHeaderLabels(header)
        # self.tableWidget.setItem(0, 0, QTableWidgetItem("Cell (1,1)"))

        layout.addWidget(self.tableWidget)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(searchAct)
        fileMenu.addAction(exitAct)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(reviewAct)
        helpMenu.addAction(helpAct)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(searchAct)
        toolbar.addAction(helpAct)
        toolbar.addAction(exitAct)

        # self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')

        # self.setLayout(self.layout)
        mainWidget.setLayout(layout)
        self.show()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter the torrent you want to search:')
        # print(text)
        if ok:
            if not text:
                results, rc = self.torrentApi.makeRequest()
            else:
                results, rc = self.torrentApi.makeRequest(text)
            # results, rc = self.torrentApi.makeRequest(text if text == '' else False)
            self.populateTable(results)
        self.results = results
        print(f"result code : {rc}")

    # TODO : Need to be able to "update"
    def populateTable(self, results: list):
        # TODO: Handle better float
        def getRation(result: list):
            try:
                ratio = int(result["seeders"]) / int(result["leechers"])
            except ZeroDivisionError:
                ratio = int(result["seeders"])
            return str(ratio)
        # Create table
        for x, result in enumerate(results):
            # print(f"Result : {result} , x : {x}")
            # icon = QIcon("icons/download.png")

            # Used for icon in cell
            delegate = IconDelegate(self.tableWidget)
            self.tableWidget.setItemDelegate(delegate)
            icon_file = "icons/download.png"
            status_item = QTableWidgetItem()
            status_icon = QIcon(icon_file)
            status_item.setIcon(status_icon)

            self.tableWidget.setItem(x, 0, QTableWidgetItem(result["name"]))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(result["size"]))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(result["added"]))
            self.tableWidget.setItem(x, 3, QTableWidgetItem(result["status"]))
            self.tableWidget.setItem(
                x, 4, QTableWidgetItem(result["leechers"]))
            self.tableWidget.setItem(x, 5, QTableWidgetItem(result["seeders"]))
            self.tableWidget.setItem(x, 6, QTableWidgetItem(getRation(result)))
            self.tableWidget.setItem(x, 7, status_item)

        self.tableWidget.move(0, 0)


class IconDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index) -> None:
        super(IconDelegate, self).initStyleOption(option, index)
        if option.features & QStyleOptionViewItem.HasDecoration:
            s = option.decorationSize
            s.setWidth(option.rect.width())
            option.decorationSize = s


class HelpWindow(QWidget):
    def __init__(self):
        super(HelpWindow, self).__init__()
        self.resize(400, 300)

        # Labelxc
        layout = QVBoxLayout()
        msg = f"<h1> Welcome to QTorrent_Search </h1>\
                <p>The version of PyQt5 is {PYQT_VERSION_STR}.</p>\
                <p>Python version is {python_version()}.</p>\
                <p>Feel free to give any review/issue in the review contact</p>"
        self.label = QLabel(msg)
        # self.
        layout.addWidget(self.label)
        self.setLayout(layout)

    def showHelp(self):
        print("[DEBUG] - In showHelp()")
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    # helpWindow = HelpWindow()
    # helpWindow.showHelp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
