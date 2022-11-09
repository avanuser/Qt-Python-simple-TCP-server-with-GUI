# This is a simple Qt Python TCP server program

from PySide6.QtWidgets import QTextEdit, QApplication, QMainWindow
from PySide6.QtCore import Slot
import sys
from tcpip import TCPServer
from controls import *

###############################################################

term_title = 'Qt TCP server [PySide6]'

win_min_height = 650
win_min_width = 500

term_min_width = 300

# Names of notebook's tables
tab1Name = 'Basic'
tab2Name = 'Edit'

def_btn_fg_color = 'black'
def_btn_bg_color = '#eeeeee'
btn_font_family = 'Titillium'
btn_font_size = '12px'

cmd_end = b'\r'

###############################################################

# Tab button [0,1,2,3]:
# 0 - label of the button
# 1 - command to send
# 2 - foreground color
# 3 - background color

# --------------- TAB1 BUTTONS ---------------
T1_0 = [['00000', '00000', '', 'blue'],
        ['11111', '11111', '', ''],
        ['22222', '22222', '', ''],
        ['33333', '33333', '', ''],
        ['44444', '44444', '', ''],
        ['55555', '55555', '', ''],
        ['6' * 5, '6' * 5, '', ''],
        ['7' * 5, '7' * 5, '', ''],
        ['8' * 5, '8' * 5, '', ''],
        ['9' * 5, '9' * 5, '', ''],
        ['', '', '', ''],
        ['', '', '', '']]

T1_1 = [['abcdef', 'abcdef', '', ''],
        ['-------', '-------', '', 'green'],
        ['hello!', 'hello!', '', ''],
        ['privet', 'privet', '', ''],
        ['!!!!!!!!!!', '!!!!!!!!!!', '', ''],
        ['', '', '', ''],
        ['', '', '', '']]

T1_2 = [['a' * 10, 'a' * 10, '', ''],
        ['b' * 10, 'b' * 10, '', ''],
        ['c' * 10, 'c' * 10, '', ''],
        ['d' * 10, 'd' * 10, '', ''],
        ['e' * 10, 'e' * 10, '', ''],
        ['', '', '', ''],
        ['', '', '', '']]

T1 = [T1_0, T1_1, T1_2]

# --------------- TAB2 BUTTONS ---------------
T2 = ['1' * 10, '2' * 10, '3' * 10, '4' * 10, '5' * 10, '6' * 10, '7' * 10, '8' * 10, '9' * 10, '0' * 10]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(term_title)
        self.statusBar().showMessage('Welcome!')
        # central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        hbox = QHBoxLayout(central_widget)
        vbox1 = QVBoxLayout()
        # create term
        self.term = QTextEdit()
        self.term.setReadOnly(True)
        self.term.setMinimumWidth(term_min_width)
        self.term.setStyleSheet("""
                background-color: #101010;
                color: #FFFFFF;
                font-family: Titillium;
                font-size: 12px;
                """)
        vbox1.addWidget(self.term)
        # clear term button
        self.clear_term_btn = QPushButton('Clear terminal')
        self.clear_term_btn.setStyleSheet('background-color: #101010; color: #eeeeee;')
        vbox1.addWidget(self.clear_term_btn)
        hbox.addLayout(vbox1)
        # create side panel
        self.side_panel = QWidget()
        vbox2 = QVBoxLayout(self.side_panel)
        # add side panel to main window
        hbox.addWidget(self.side_panel)
        # create controls and bind handlers
        self.tcp_server = TCPServer(self.on_port_rx)
        # create send_any_cmd
        self.send_any_msg = SendAny()
        self.send_any_msg.any_btn.clicked.connect(self.send_any)
        # create notebook
        self.notebook = Notebook()
        # add tables to the notebook
        self.notebook.add_tab_btn(tab1Name, T1, self.send)
        self.notebook.add_tab_edit(tab2Name, len(T2), T2, self.send_any)
        # add controls and notebook to side panel
        vbox2.addWidget(self.tcp_server)
        vbox2.addWidget(self.send_any_msg)
        vbox2.addWidget(self.notebook)
        #
        self.clear_term_btn.clicked.connect(self.clear_term)

    def send(self, btn):
        if self.tcp_server.sock_started:
            cmd_to_send = btn.get_cmd()
            if cmd_to_send:
                if isinstance(cmd_to_send, str):  # if type of cmd_to_send is a <string>
                    self.tcp_server.sock.write(cmd_to_send.encode('ascii'))
                    self.tcp_server.sock.write(cmd_end)

    def send_any(self):
        if self.tcp_server.sock_started:
            ref = self.sender()  # get object created received signal
            data = ref.parent().any_field.text()  # get text from any_field using parent
            if data:
                self.tcp_server.sock.write(data.encode('ascii'))
                self.tcp_server.sock.write(cmd_end)

    def clear_term(self):
        self.term.clear()  # clear terminal

    def closeEvent(self, event):
        self.tcp_server.stop_serv()
        event.accept()

    @Slot()
    def on_port_rx(self):
        num_rx_bytes = self.tcp_server.sock.bytesAvailable()
        rx_bytes = self.tcp_server.sock.read(num_rx_bytes)
        try:
            data = bytes(rx_bytes).decode('ascii')
        except Exception:
            data = '?' * num_rx_bytes
        try:
            self.term.insertPlainText(data)
            self.term.ensureCursorVisible()
        except Exception:
            pass


def main():
    app = QApplication([])
    main_win = MainWindow()
    main_win.resize(win_min_width, win_min_height)
    main_win.show()
    sys.exit(app.exec())  # PySide6
    # sys.exit(app.exec_())  # PySide2


if __name__ == '__main__':
    main()
