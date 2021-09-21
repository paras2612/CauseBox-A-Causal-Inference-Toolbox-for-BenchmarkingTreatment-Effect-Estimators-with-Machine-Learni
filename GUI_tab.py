from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import os
import json

table1 ={
    "CFRNET":"1.67",
    "SITE":"1.48",
    "BART":"3.3",
    "CForest":"3.6",
    "DRNET":"1.2",
    "CEVAE":"2.9",
    "PM":"1.3"
}
table2 = {
    "CFRNET":"0.19",
    "SITE":"0.15",
    "BART":"0.22",
    "CForest":"0.20",
    "DRNET":"0.18",
    "CEVAE":"0.17",
    "PM":"0.16"

}
table3 ={
    "CFRNET1":"1.75",
    "CFRNET2":"1.67"
}
table4 ={
    "CFRNET1":"0.14",
    "CFRNET2":"0.08"
}

class Tab1(QTabBar):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        plotLayout = QHBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.plot()
        plotLayout.addWidget(self.canvas)

        tableLayout = QHBoxLayout()
        self.table()
        tableLayout.addWidget(self.tableWidget1)
        tableLayout.addWidget(self.tableWidget2)

        layout.addLayout(plotLayout)
        layout.addLayout(tableLayout)
        self.setLayout(layout)


    def plot(self):
        self.figure.clf()
        self.figure.subplots_adjust(hspace=0.5)
        self.figure.subplots_adjust(wspace=0.5)

        ax1 = self.figure.add_subplot(121)
        x1 = table1.keys()
        y1 = [float(value) for value in table1.values()]
        ax1.bar(x1, y1, color='rgbc')
        ax1.set_title("IHDP Dataset")
        ax1.set_ylabel('PEHE')
        ax1.set_xlabel('Model')
        plt.xticks(rotation=45)

        ax2 = self.figure.add_subplot(122)
        x2 = table2.keys()
        y2 = [float(value) for value in table2.values()]
        ax2.bar(x2, y2, color='rgbc')
        ax2.set_title("Jobs Dataset")
        ax2.set_ylabel('Policy Risk')
        ax2.set_xlabel('Model')
        plt.xticks(rotation=45)

        self.canvas.draw_idle()

    def table(self):
        self.numrow = 7
        self.numcol = 2
        self.tableWidget1 = QTableWidget(self.numrow, self.numcol)
        self.tableWidget1.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget1.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget1.setHorizontalHeaderLabels(
            ['Model', 'PEHE']
        )
        self.tableWidget1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        i = j = 0
        for key, value in table1.items():
            self.tableWidget1.setItem(i, j, QTableWidgetItem(str(key)))
            self.tableWidget1.setItem(i, j+1, QTableWidgetItem(str(value)))
            i+=1
            j=0
        self.tableWidget2 = QTableWidget(self.numrow, self.numcol)
        self.tableWidget2.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget2.setHorizontalHeaderLabels(
            ['Model', 'Policy Risk']
        )
        self.tableWidget2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        i = j = 0
        for key, value in table2.items():
            self.tableWidget2.setItem(i, j, QTableWidgetItem(str(key)))
            self.tableWidget2.setItem(i, j+1, QTableWidgetItem(str(value)))
            i+=1
            j=0

class Tab2(QTabBar):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.combobox()
        layout.addWidget(self.modelComboBox)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.plot()
        layout.addWidget(self.canvas)

        self.table()
        layout.addWidget(self.tableWidget)

        self.setLayout(layout)
    def combobox(self):
        self.modelComboBox = QComboBox()
        self.modelComboBox.addItem("Counterfactual Regression Network (CRFNet)")
        self.modelComboBox.addItem("Causal Effect Inference with Deep Latent-Variable Models (CEVAE)")
        self.modelComboBox.addItem("Bayesian Additive Regression Trees (BART)")
        self.modelComboBox.addItem("Causal Forests")
        self.modelComboBox.addItem("Perfect Match")
        self.modelComboBox.addItem("Learning Disentangled Representations for counterfactual regression (DRNet)")
        self.modelComboBox.addItem("Local similarity preserved individual treatment effect (SITE)")
        # self.modelComboBox.activated[str].connect(self.modelChoice)

    def table(self):
        self.numrow = 50
        self.numcol = 50
        self.tableWidget = QTableWidget(self.numrow, self.numcol)
        #Need to change dynamicall refelec attrivtues
        with open("ParamsInputCFR", "r") as file:
            text  = file.read()
        headers = [param.split()[0] for param in text.split("\n")]
        headers.insert(0, "Model")
        self.tableWidget.setHorizontalHeaderLabels(
            headers
        )
        self.modelbuttons = list()
        dirpath = os.getcwd() + "\\PlotData\\"
        files = os.listdir(dirpath)
        temp = ["CFRNET1", "CFRNET2", "CFRNET3"]
        for row, file in enumerate(files):
            with open(dirpath+file) as result:
                data = json.load(result)
            if row == 0:
                selectplotbtn = QPushButton("Select"+" "+temp[0])
            elif row == 1:
                selectplotbtn = QPushButton("Select"+" "+temp[1])

            self.tableWidget.setCellWidget(row, 0, selectplotbtn)
            # self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
            col = 0
            for key, val in data["params"].items():
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(val)))
                col+=1
            self.modelbuttons.append(selectplotbtn)

    def plot(self):
        self.figure.clf()
        self.figure.subplots_adjust(hspace=0.5)
        self.figure.subplots_adjust(wspace=0.5)

        ax1 = self.figure.add_subplot(121)
        x1 = table3.keys()
        y1 = [float(value) for value in table3.values()]
        ax1.bar(x1, y1, color='rgbc')
        ax1.set_title("IHDP Dataset")
        ax1.set_ylabel('PEHE')
        ax1.set_xlabel('Model')
        # plt.xticks(rotation=45)

        ax2 = self.figure.add_subplot(122)
        x2 = table4.keys()
        y2 = [float(value) for value in table4.values()]
        ax2.bar(x2, y2, color='rgbc')
        ax2.set_title("IHDP Dataset")
        ax2.set_ylabel('Error on ATE')
        ax2.set_xlabel('Model')
        # plt.xticks(rotation=45)

        self.canvas.draw_idle()