#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton)


class ReviewForm(QWidget):

    def __init__(self):
        super().__init__()
        title = QLabel('Email')
        author = QLabel('Subject')
        review = QLabel('Review')

        sendBtn = QPushButton('Send Email', self)
        sendBtn.setToolTip('This will send an email')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        grid.addWidget(sendBtn, 8, 1)
        # grid.addW

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')

        # self.initUI()

    def showReview(self):

        self.show()
