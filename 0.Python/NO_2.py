# -*- coding: utf-8 -*-
import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MyWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.prd = 0.5

    def setupUI(self):
        self.setGeometry(500,200,700,500)
        
        self.plus = QPushButton('+')
        self.plus.clicked.connect(self.putSignal)
        self.minus = QPushButton('-')
        self.minus.clicked.connect(self.putSignal)
        #버튼 사이즈 조절
        self.plus.setSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.Expanding)
        self.minus.setSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.Preferred)
        
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        
        
        LayButton = QVBoxLayout()
        LayButton.addWidget(self.plus,3)
        LayButton.addWidget(self.minus,3)
        LayButton.addStretch(1)
        
        LayFig = QVBoxLayout()
        LayFig.addWidget(self.canvas)
        
        layout = QHBoxLayout()
        layout.addLayout(LayFig)
        layout.addLayout(LayButton)
        layout.setStretchFactor(LayFig, 1)
        layout.setStretchFactor(LayButton, 0)

        
        self.setLayout(layout)
    
    def putSignal(self):
        
        Pdraw = self.fig.add_subplot(111)
        sender = self.sender()
        
        if sender.text() == '+':
            self.prd += 1
        if sender.text() == '-' and self.prd > 0:
            self.prd -= 1
        
        X = np.linspace(-np.pi, np.pi, 256,endpoint=True)
        Cy,Sy = np.cos(X), np.sin(X)
        Pdraw.plot(X, Cy, color="red", linewidth = self.prd, linestyle="-", 
                                           label = sender.text() + str(self.prd))
        Pdraw.plot(X, Sy, color="blue", linewidth = self.prd, linestyle="-", 
                                           label = sender.text()+ str(self.prd))
        
        self.canvas.draw()
        Pdraw.clear()


if __name__ == "__main__":    
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

