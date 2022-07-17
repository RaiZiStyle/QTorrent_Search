#!/usr/bin/env python3
"""
Example d'ouverture d'une nouvelle fenettre (class Widget)
après l'appuie d'un QAction ajouté a la toolbar & au menu
"""

import sys
from platform import python_version

from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication,
                             QWidget, QLabel, QVBoxLayout, QInputDialog,
                             QTableWidget, QTableWidgetItem)
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

        self.layout = QVBoxLayout()
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
        self.tableWidget.setRowCount(5)
        # set column count
        self.tableWidget.setColumnCount(100)
        header = ['Name', 'Size', 'Added', 'Status',
                  'Leechers', 'Seeders', 'Ratio']
        self.tableWidget.setHorizontalHeaderLabels(header)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Cell (1,1)"))
        self.layout.addWidget(self.tableWidget)
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

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')

        self.setLayout(self.layout)
        self.show()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter the torrent you want to search:')
        # print(text)
        if ok:
            results, rc = self.torrentApi.makeRequest(text)
            self.populateTable(results)
        self.results = results
        print(f"result code : {rc}")

    def populateTable(self, results: list):
        # Create table
        # for result in results:
        #     print(result)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Cell (1,1)"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Cell (1,2)"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Cell (2,1)"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("Cell (2,2)"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Cell (3,2)"))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Cell (4,1)"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Cell (4,2)"))
        self.tableWidget.move(0, 0)


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
