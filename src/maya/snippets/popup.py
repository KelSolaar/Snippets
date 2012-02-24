from PyQt4.QtCore import QStringList
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QStringListModel
from PyQt4.QtGui import QWidget


class Window(QWidget):
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        
        gridLayout = QGridLayout()
        self.setLayout(gridLayout)
        
        comboBox = QComboBox(self)
        comboBox.setEditable(True)
        comboBox.addItems(["Aeiou", "Bcdef", "ghij", "kldm"])
        gridLayout.addWidget(comboBox)
        
        completer = QCompleter()
        completer.setModel(QStringListModel(["Stuff", "Ken", "Barbie", "Allo"]))
        comboBox.setCompleter(completer)
		
ui = Window()
ui.setWindowFlags(Qt.Popup)
ui.show()
ui.raise_()