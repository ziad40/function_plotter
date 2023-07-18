import pytest
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMessageBox
from function_plotter import MainWindow
from unittest.mock import patch
import matplotlib
matplotlib.use('agg')


class MessageBoxEventFilter:
    def __init__(self):
        self.message_box_shown = False
        self.warning_message = None

    def eventFilter(self, obj, event):
        if isinstance(obj, QMessageBox) and event.type() == event.Show:
            self.message_box_shown = True
            self.warning_message = obj
        return False

@pytest.fixture
def app(qtbot):
    app = MainWindow()
    qtbot.addWidget(app)
    return app

# check plot button is working 
def test_plot_button(qtbot, app):
    app.function_input.setText("x**2")
    app.min_input.setText("0")
    app.max_input.setText("10")
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)
    assert qtbot.waitSignal(app.plot_button.clicked)

# check if there is another variable in function
def test_warning_message_4(app, qtbot):
    app.function_input.setText('2*x + 4+u')
    app.min_input.setText('0')
    app.max_input.setText('2')

    with patch.object(QMessageBox, 'warning') as mock_warning:
        qtbot.mouseClick(app.plot_button, Qt.LeftButton)
        # Assert that QMessageBox.warning was called
        assert mock_warning.called
        # Assert the contents of the warning message
        args, _ = mock_warning.call_args
        assert args[1] == 'Input Error-4'
        # Close the warning message box (mock object, no actual GUI)
        button = mock_warning.return_value.clickedButton.return_value
        button.text.return_value = QMessageBox.Ok
        button.clicked.emit()
    
    # check if there is syntax error in function
def test_warning_message_3(app, qtbot):
    app.function_input.setText('2*x + ')
    app.min_input.setText('0')
    app.max_input.setText('2')

    with patch.object(QMessageBox, 'warning') as mock_warning:
        qtbot.mouseClick(app.plot_button, Qt.LeftButton)
        # Assert that QMessageBox.warning was called
        assert mock_warning.called
        # Assert the contents of the warning message
        args, _ = mock_warning.call_args
        assert args[1] == 'Input Error-3'
        # Close the warning message box (mock object, no actual GUI)
        button = mock_warning.return_value.clickedButton.return_value
        button.text.return_value = QMessageBox.Ok
        button.clicked.emit()

# check if max value is less than min value
def test_warning_message_2(app, qtbot):
    app.function_input.setText('2*x ')
    app.min_input.setText('5')
    app.max_input.setText('2')

    with patch.object(QMessageBox, 'warning') as mock_warning:
        qtbot.mouseClick(app.plot_button, Qt.LeftButton)
        # Assert that QMessageBox.warning was called
        assert mock_warning.called
        # Assert the contents of the warning message
        args, _ = mock_warning.call_args
        assert args[1] == 'Input Error-2'
        # Close the warning message box (mock object, no actual GUI)
        button = mock_warning.return_value.clickedButton.return_value
        button.text.return_value = QMessageBox.Ok
        button.clicked.emit()

# check if max and min of x is number
def test_warning_message_1(app, qtbot):
    app.function_input.setText('2*x ')
    app.min_input.setText('5c')
    app.max_input.setText('10')

    with patch.object(QMessageBox, 'warning') as mock_warning:
        qtbot.mouseClick(app.plot_button, Qt.LeftButton)
        # Assert that QMessageBox.warning was called
        assert mock_warning.called
        # Assert the contents of the warning message
        args, _ = mock_warning.call_args
        assert args[1] == 'Input Error-1'
        # Close the warning message box (mock object, no actual GUI)
        button = mock_warning.return_value.clickedButton.return_value
        button.text.return_value = QMessageBox.Ok
        button.clicked.emit()

# check if all fields are filled with values
def test_warning_message_0(app, qtbot):
    app.function_input.setText('')
    app.min_input.setText('0')
    app.max_input.setText('10')

    with patch.object(QMessageBox, 'warning') as mock_warning:
        qtbot.mouseClick(app.plot_button, Qt.LeftButton)
        # Assert that QMessageBox.warning was called
        assert mock_warning.called
        # Assert the contents of the warning message
        args, _ = mock_warning.call_args
        assert args[1] == 'Input Error-0'
        # Close the warning message box (mock object, no actual GUI)
        button = mock_warning.return_value.clickedButton.return_value
        button.text.return_value = QMessageBox.Ok
        button.clicked.emit()

# check if there is more than one error, we handle it sequentially
def test_warning_message_5(app, qtbot):
    # for this example we predict to get error because of syntax error not because of using another variable than x
    app.function_input.setText('2*x + k + ')
    app.min_input.setText('0')
    app.max_input.setText('2')

    with patch.object(QMessageBox, 'warning') as mock_warning:
        qtbot.mouseClick(app.plot_button, Qt.LeftButton)
        # Assert that QMessageBox.warning was called
        assert mock_warning.called
        # Assert the contents of the warning message
        args, _ = mock_warning.call_args
        assert args[1] == 'Input Error-3'
        # Close the warning message box (mock object, no actual GUI)
        button = mock_warning.return_value.clickedButton.return_value
        button.text.return_value = QMessageBox.Ok
        button.clicked.emit()

# check of using special character
def test_warning_message_6(app, qtbot):
    app.function_input.setText('2*x! ')
    app.min_input.setText('0')
    app.max_input.setText('2')

    with patch.object(QMessageBox, 'warning') as mock_warning:
        qtbot.mouseClick(app.plot_button, Qt.LeftButton)
        # Assert that QMessageBox.warning was called
        assert mock_warning.called
        # Assert the contents of the warning message
        args, _ = mock_warning.call_args
        assert args[1] == 'Input Error-4'
        # Close the warning message box (mock object, no actual GUI)
        button = mock_warning.return_value.clickedButton.return_value
        button.text.return_value = QMessageBox.Ok
        button.clicked.emit()
    

if __name__ == "__main__":
    # pytest.main()
    pytest.main()