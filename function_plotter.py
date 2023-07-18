import sys
import matplotlib.pyplot as plt
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from sympy import sympify, SympifyError
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Function Plotter")
        self.resize(200, 200)
        # Create widgets
        self.function_label = QLabel("Enter a function of x:  ex: x^2 + 2x + 5")
        self.function_input = QLineEdit()
        self.min_label = QLabel("Minimum x value:  (number)")
        self.min_input = QLineEdit()
        self.max_label = QLabel("Maximum x value:  (number)")
        self.max_input = QLineEdit()
        self.plot_button = QPushButton("Plot")

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.function_label)
        layout.addWidget(self.function_input)
        layout.addWidget(self.min_label)
        layout.addWidget(self.min_input)
        layout.addWidget(self.max_label)
        layout.addWidget(self.max_input)
        layout.addWidget(self.plot_button)

        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connect the plot button to the plot function
        self.plot_button.clicked.connect(self.plot)

    def validate_inputs(self):
        # extract inputs
        function = self.function_input.text()
        min_value = self.min_input.text()
        max_value = self.max_input.text()
        # Check if any input field is empty
        if not (function and min_value and max_value):
            QMessageBox.warning(self, "Input Error-0", "All fields must be filled.")
            return False
        
        try:
            min_value = float(min_value)
            max_value = float(max_value)
        except ValueError:
            QMessageBox.warning(self, "Input Error-1", "Min and Max values must be numbers")
            return False
        
        # check if max value is less than min value
        if min_value >= max_value:
            QMessageBox.warning(self, "Input Error-2", "Min value must be less than Max value.")
            return False
        
        # check syntax error
        try:
            sympify(function)
        except SympifyError:
            QMessageBox.warning(self, "Input Error-3", "Invalid function syntax.\ncheck your function is correct")
            return False
        
        not_valid_variables = ['!', '@', '#', '$', '%', '&', '_', '=', '[', ']', '{', '}',
                      ';', ':', "'", '"', ',', '.', '<', '>', '?', '\\', '|', 'i', 'p', 'u', 'g', 'w', 'y', 'f', 'o', 'n', 'd', 'e',
                        'r', 't', 'z', 'b', 'a', 'k', 'h', 'm', 'j', 'l', 'c', 'v', 's', 'q', 'K', 'C', 'Y', 'F', 'B', 'P', 'A', 'S',
                          'N', 'L', 'M', 'W', 'U', 'X', 'G', 'R', 'E', 'V', 'J', 'I', 'D', 'H', 'Z', 'T', 'O', 'Q']
        
        for i in not_valid_variables:
            if i in function:
                QMessageBox.warning(self, "Input Error-4", "your function contain "+str(i)+"\nfunction must contain only variable x.\n with numbers and operations : +, -, *, /, ^, (, )")
                return False

        return True

    def plot(self):
        if(not self.validate_inputs()):
            return 

        function = self.function_input.text()
        function = function.replace('^','**')
        function = function.replace('x','(x)')
        min_value = int(self.min_input.text())
        max_value = int(self.max_input.text())
        x = np.linspace(min_value, max_value, num = 100*(max_value - min_value))
        y = [eval(function.replace('x', str(i))) for i in x]
        # Plot the Data
        plt.figure()
        plt.plot(x, y)
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title("Function Plot")
        plt.grid(True)
        plt.show()
    

if __name__ == "__main__":
    # Application and main window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Execute the application
    sys.exit(app.exec_())
