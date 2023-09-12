import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit

class IPInputWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("Enter IP Address:")
        self.ip_input = QLineEdit(self)
        
        # Set the input mask to format the IP address with dots
        self.ip_input.setInputMask("000.000.000.000;_")
        #self.ip_input.setPlaceholderText("000.000.000.000")

        layout.addWidget(label)
        layout.addWidget(self.ip_input)

        self.setLayout(layout)
        self.setWindowTitle("IP Address Input")

def main():
    app = QApplication(sys.argv)
    window = IPInputWidget()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()