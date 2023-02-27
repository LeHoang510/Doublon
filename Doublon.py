from PyQt5.QtWidgets import QApplication, QFrame
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QCheckBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json


# ============================================================================= #
# Class text
class Text(QTextEdit):

    # Constructor
    def __init__(self):
        QTextEdit.__init__(self)
        self.show()

    # Display text
    def display(self, t):
        cursor = self.textCursor()
        cursor.insertText(t)

    # Delete text
    def delete(self):
        self.setPlainText("")

# Class line
class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

# ============================================================================= #
# Class App
class Window(QMainWindow):
    def __init__(self, saving="save.json", output=""):

        # Input-output management
        if output == "":
            self.out = self
        else:
            self.out = output
        # Read json file
        self.jsonReader(saving)
        # Show widget
        QMainWindow.__init__(self)
        self.init_ui()
        self.show()
        # self.updateForm()

    def jsonReader(self, saving):
        # Read json saving file
        try:
            f = open(saving, 'r')
        except IOError:
            print("The json file is not found - " + saving)
        else:
            try:
                # Load json file
                self.infor = json.load(f)
            except:
                print("Failed to load json file - " + saving)
            f.close()
            # Save json file name
            self.savingFile = saving

    # Interface initialization
    def init_ui(self):
        # Application name
        self.setWindowTitle("Doublon")
        self.setWindowIcon(QIcon("./Icons/GMIcon.png"))
        # Main widget
        self.window = QWidget()

        # Add layout
        self.addLayout()

        # Set center zone
        self.setCentralWidget(self.window)
        self.setGeometry(0, 0, 600, 350)

        # Set infor
        self.updateForm()

    def updateForm(self):
        self.editNomcol.setText(self.infor["Noms des Colonnes"])
        self.editSoldat1.setText(self.infor["Soldat1"])
        self.editSoldat2.setText(self.infor["Soldat2"])

    # ==========================================================VISUALISATION=====================================================================#
    def addLayout(self):
        # Create layout
        self.boxVMain = QVBoxLayout()
        self.window.setLayout(self.boxVMain)
        # Add Info soldat
        self.createInfoSoldat()
        self.createLayoutCompare()
        self.boxVMain.addLayout(self.gridInfoSoldat)
        self.boxVMain.addWidget(QHLine())
        self.boxVMain.addLayout(self.gridCompare)

    def createInfoSoldat(self):
        self.gridInfoSoldat = QGridLayout()
        self.gridInfoSoldat.setAlignment(Qt.AlignTop)
        # Noms des colonnes
        self.labelNomcol = QLabel("Noms des colonnes")
        self.editNomcol = QLineEdit()
        # Info soldat
        self.labelSoldat1 = QLabel("Soldat 1")
        self.editSoldat1 = QLineEdit()
        self.buttonDelete1 = QPushButton("X")

        self.labelSoldat2 = QLabel("Soldat 2")
        self.editSoldat2 = QLineEdit()
        self.buttonDelete2 = QPushButton("X")

        self.buttonReset = QPushButton("Reset")
        # Connect function
        self.editNomcol.textChanged.connect(self.changeNomCol)
        self.editSoldat1.textChanged.connect(self.changeSoldat1)
        self.editSoldat2.textChanged.connect(self.changeSoldat2)

        self.buttonReset.clicked.connect(self.reset)
        self.buttonDelete1.clicked.connect(self.deleteSoldat1)
        self.buttonDelete2.clicked.connect(self.deleteSoldat2)
        # Add widgets
        lig = 0;col = 0
        self.gridInfoSoldat.addWidget(self.labelNomcol, lig, col)
        col += 1;self.gridInfoSoldat.addWidget(self.editNomcol, lig, col)
        col += 1;self.gridInfoSoldat.addWidget(self.buttonReset, lig, col)
        lig += 1;col = 0
        self.gridInfoSoldat.addWidget(self.labelSoldat1, lig, col)
        col += 1;self.gridInfoSoldat.addWidget(self.editSoldat1, lig, col)
        col += 1;self.gridInfoSoldat.addWidget(self.buttonDelete1, lig, col)
        lig += 1;col = 0
        self.gridInfoSoldat.addWidget(self.labelSoldat2, lig, col)
        col += 1;self.gridInfoSoldat.addWidget(self.editSoldat2, lig, col)
        col += 1;self.gridInfoSoldat.addWidget(self.buttonDelete2, lig, col)

    def createLayoutCompare(self):
        self.gridCompare = QGridLayout()
        self.gridCompare.setAlignment(Qt.AlignTop)
        self.labelS1 = QLabel("Soldat 1")
        self.labelS2 = QLabel("Soldat 2")
        # Info compare
        self.label = ["Nom", "Prénom", "Prénom père", "Nom mère", "Prénom mère", "Régiment"]
        self.formLabel = {}
        self.formEdit1 = {}
        self.formEdit2 = {}
        self.checkbox = {}

        self.resultLabel = QLabel("Résult")
        self.result = QLabel("Entrez des données")
        for i in self.label:
            self.formLabel[i] = QLabel(i)
            self.formEdit1[i] = QLineEdit()
            self.formEdit2[i] = QLineEdit()
            self.checkbox[i] = QCheckBox()
        # Add widget
        lig = 0;col = 1
        self.gridCompare.addWidget(self.labelS1, lig, col)
        col += 1;self.gridCompare.addWidget(self.labelS2, lig, col)
        lig += 1;col = 0
        for i in self.label:
            self.gridCompare.addWidget(self.formLabel[i], lig, col)
            col += 1;self.gridCompare.addWidget(self.formEdit1[i], lig, col)
            col += 1;self.gridCompare.addWidget(self.formEdit2[i], lig, col)
            col += 1;self.gridCompare.addWidget(self.checkbox[i], lig, col)
            lig += 1;col = 0
        self.gridCompare.addWidget(self.resultLabel, lig, col)
        col += 1;self.gridCompare.addWidget(self.result, lig, col, 1, 2)

    # ==========================================================VISUALISATION=====================================================================#

    # ==========================================================CHANGE-ACTION=====================================================================#
    def generateSoldat1(self):
        soldat1 = self.editSoldat1.text()
        tableSoldat1 = soldat1.split("\t")
        tabRes1 = {}
        length = min(len(tableSoldat1), len(self.tableCol))
        for i in range(length):
            tabRes1[self.tableCol[i]] = tableSoldat1[i]
        for i in self.label:
            self.formEdit1[i].setText(tabRes1[i])
        if self.checkResult():
            self.giveResult()

    def generateSoldat2(self):
        soldat2 = self.editSoldat2.text()
        tableSoldat2 = soldat2.split("\t")
        tabRes2 = {}
        length = min(len(tableSoldat2), len(self.tableCol))
        for i in range(length):
            tabRes2[self.tableCol[i]] = tableSoldat2[i]
        for i in self.label:
            self.formEdit2[i].setText(tabRes2[i])
        if self.checkResult():
            self.giveResult()

    def generateInfo(self):
        self.generateSoldat1()
        self.generateSoldat2()
        if self.checkResult():
            self.giveResult()

    def changeNomCol(self):
        self.infor["Noms des Colonnes"] = self.editNomcol.text()
        self.updateJson()
        self.nomColonne = self.editNomcol.text()
        self.tableCol = self.nomColonne.split("\t")
        if self.editNomcol.text() != '' and self.editSoldat1.text() != '' and self.editSoldat2.text() != '':
            self.generateInfo()
        elif self.editNomcol.text() != '' and self.editSoldat1.text() != '':
            self.generateSoldat1()
        elif self.editNomcol.text() != '' and self.editSoldat2.text() != '':
            self.generateSoldat2()

    def changeSoldat1(self):
        self.infor["Soldat1"] = self.editSoldat1.text()
        self.updateJson()
        if self.editNomcol.text() != '' and self.editSoldat1.text() != '':
            self.generateSoldat1()

    def changeSoldat2(self):
        self.infor["Soldat2"] = self.editSoldat2.text()
        self.updateJson()
        if self.editNomcol.text() != '' and self.editSoldat2.text() != '':
            self.generateSoldat2()

    def checkResult(self):
        for i in self.label:
            if self.formEdit1[i].text() == '' or self.formEdit2[i].text() == '':
                return False
        return True

    def giveResult(self):
        self.result.setText("True")
        for i in self.label:
            if self.formEdit1[i].text() == self.formEdit2[i].text():
                self.checkbox[i].setChecked(True)
            else:
                self.checkbox[i].setChecked(False)
                self.result.setText("Faux")

    def updateJson(self):
        # Write json saving file
        try:
            f = open(self.savingFile, 'w')
        except IOError:
            print("The json file is not found - " + self.savingFile)
        else:
            json.dump(self.infor, f, sort_keys=False, indent=2, ensure_ascii=False)
            f.close()

    # ==========================================================CHANGE-ACTION=====================================================================#

    # ==========================================================BUTTON-ACTION=====================================================================#
    def reset(self):
        self.editNomcol.setText('')
        self.deleteSoldat1()
        self.deleteSoldat2()

    def deleteSoldat1(self):
        self.editSoldat1.setText('')
        for i in self.label:
            self.formEdit1[i].setText('')

    def deleteSoldat2(self):
        self.editSoldat2.setText('')
        for i in self.label:
            self.formEdit2[i].setText('')

    # ==========================================================BUTTON-ACTION=====================================================================#



# =================================================================== #
#                         Programme principal                         #
# =================================================================== #
if __name__ == "__main__":
    # Vérification de la syntaxe d'appel
    syntaxe = "Syntaxe: " + sys.argv[0]
    if (len(sys.argv) != 1):
        print(syntaxe)
        exit()

    app = QApplication([])
    mf = Window()
    app.exec_()



