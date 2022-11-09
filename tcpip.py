# TCP/IP classes


from PySide6.QtNetwork import QTcpSocket, QTcpServer, QHostAddress, QAbstractSocket
from PySide6.QtSerialPort import QSerialPort
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QGroupBox
from PySide6.QtWidgets import QTextEdit, QGridLayout, QButtonGroup, QLineEdit, QLabel
from PySide6.QtCore import Qt, Slot

##################################

max_pending_conn = 1  # max number of server's pending connections
port_default = '5555'  # Default port number


##################################


class TCPClient(QGroupBox):
    addr1 = '127.0.0.1'
    port1 = '5555'

    addr2 = '192.168.0.10'
    port2 = '7777'

    def __init__(self, addr_def='127.0.0.1', port_def='5555'):
        super().__init__()
        self.setTitle('TCP client')
        # add layouts
        vbox = QVBoxLayout(self)
        layout = QGridLayout()
        vbox.addLayout(layout)
        #
        self.started = 0  # indicates if socket is opened (1) or not (0)
        self.rem_addr = ''  # remote address
        self.rem_port = ''  # remote port
        self.sock = QTcpSocket(self)
        # 
        self.sock.bind()
        self.sock.connected.connect(self.connected)
        self.sock.disconnected.connect(self.disconnected)
        self.sock.errorOccurred.connect(self.sock_error)
        self.sock.stateChanged.connect(self.state_changed)
        # create buttons groups
        self.addr_group = QButtonGroup(self)
        self.port_group = QButtonGroup(self)
        self.addr_group.buttonClicked.connect(self.addr_copy)
        self.port_group.buttonClicked.connect(self.port_copy)
        # Line 0
        # create info_label
        self.info_label = QLabel('Disconnected')
        self.info_label.setStyleSheet('color: red;')
        self.info_label.setMinimumWidth(100)
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label, 0, 0)
        #
        self.addr_field = QLineEdit(addr_def)
        self.addr_field.setMinimumWidth(100)
        self.addr_field.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.addr_field, 0, 1)
        #
        self.port_field = QLineEdit(port_def)
        self.port_field.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.port_field, 0, 2)
        #
        self.open_btn = QPushButton('Connect')
        self.open_btn.setStyleSheet('background-color: #00dd00;')
        layout.addWidget(self.open_btn, 0, 3)
        self.open_btn.clicked.connect(self.start)
        # Line 1
        # create info1_label
        self.info1_label = QLabel('')
        self.info1_label.setStyleSheet('color: red;')
        self.info1_label.setMinimumWidth(90)
        self.info1_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info1_label, 1, 0)
        #
        self.addr1_btn = QPushButton(self.addr1)
        self.addr1_btn.setStyleSheet('background-color: yellow;')
        layout.addWidget(self.addr1_btn, 1, 1)
        self.addr_group.addButton(self.addr1_btn)
        #
        self.port1_btn = QPushButton(self.port1)
        self.port1_btn.setStyleSheet('background-color: yellow;')
        layout.addWidget(self.port1_btn, 1, 2)
        self.port_group.addButton(self.port1_btn)
        #
        self.close_btn = QPushButton('Disconnect')
        self.close_btn.setStyleSheet('background-color: red;')
        layout.addWidget(self.close_btn, 1, 3)
        self.close_btn.clicked.connect(self.stop)
        # Line 2
        #
        self.addr2_btn = QPushButton(self.addr2)
        self.addr2_btn.setStyleSheet('background-color: yellow;')
        layout.addWidget(self.addr2_btn, 2, 1)
        self.addr_group.addButton(self.addr2_btn)
        #
        self.port2_btn = QPushButton(self.port2)
        self.port2_btn.setStyleSheet('background-color: yellow;')
        layout.addWidget(self.port2_btn, 2, 2)
        self.port_group.addButton(self.port2_btn)
        #
        self.clear_btn = QPushButton('Clear log')
        self.clear_btn.setStyleSheet('background-color: #777777; color: #ffffff;')
        layout.addWidget(self.clear_btn, 2, 3)
        self.clear_btn.clicked.connect(self.clear_log)
        #
        # create log monitor
        self.log_monitor = QTextEdit()
        self.log_monitor.setReadOnly(True)
        self.log_monitor.setStyleSheet("""
                        background-color: #101010;
                        color: #FFFFFF;
                        font-family: Ariel;
                        font-size: 11px;
                        """)
        vbox.addWidget(self.log_monitor)

    def addr_copy(self, btn):
        addr0 = btn.text()
        self.addr_field.setText(addr0)

    def port_copy(self, btn):
        port0 = btn.text()
        self.port_field.setText(port0)

    def clear_log(self):
        self.log_monitor.clear()  # clear log monitor

    def start(self):
        if self.started == 0:
            self.rem_addr = self.addr_field.text()
            self.rem_port = self.port_field.text()
            if self.rem_addr and self.rem_port:
                self.sock.connectToHost(self.rem_addr, int(self.rem_port))
            else:
                self.info_label.setText('Pls enter IP/port')
                self.info_label.setStyleSheet('color: red;')

    def stop(self):
        if self.started:
            self.sock.disconnectFromHost()

    @Slot()
    def connected(self):
        self.info_label.setText('Connected')
        self.info_label.setStyleSheet('color: #00dd00;')  # green
        self.started = 1

    @Slot()
    def disconnected(self):
        self.info_label.setText('Disconnected')
        self.info_label.setStyleSheet('color: red;')
        self.started = 0

    @Slot()
    def state_changed(self, state):
        if state == QAbstractSocket.SocketState.UnconnectedState:
            curr_state = 'Disconnected'
        elif state == QAbstractSocket.SocketState.HostLookupState:
            curr_state = 'Host Lookup...'
        elif state == QAbstractSocket.SocketState.ConnectingState:
            curr_state = 'Connecting...'
        elif state == QAbstractSocket.SocketState.ConnectedState:
            curr_state = 'Connected'
        elif state == QAbstractSocket.SocketState.BoundState:
            curr_state = 'Bound'
        elif state == QAbstractSocket.SocketState.ClosingState:
            curr_state = 'Closing...'
        else:
            curr_state = str(self.sock.state())
        self.log_monitor.insertPlainText(curr_state + '\r')
        self.log_monitor.ensureCursorVisible()

    def sock_error(self):
        err = self.sock.error()
        if err == QAbstractSocket.ConnectionRefusedError:
            err_msg = 'Connection Refused Error'
        elif err == QAbstractSocket.RemoteHostClosedError:
            err_msg = 'Remote Host Closed Error'
        elif err == QAbstractSocket.HostNotFoundError:
            err_msg = 'Host Not Found Error'
        elif err == QAbstractSocket.SocketAccessError:
            err_msg = 'Socket Access Error'
        elif err == QAbstractSocket.SocketResourceError:
            err_msg = 'Socket Resource Error'
        elif err == QAbstractSocket.SocketTimeoutError:
            err_msg = 'Socket Timeout Error'
        elif err == QAbstractSocket.DatagramTooLargeError:
            err_msg = 'Datagram Too Large Error'
        elif err == QAbstractSocket.NetworkError:
            err_msg = 'Network Error'
        elif err == QAbstractSocket.AddressInUseError:
            err_msg = 'Address In Use Error'
        elif err == QAbstractSocket.SocketAddressNotAvailableError:
            err_msg = 'Socket Address Not Available Error'
        elif err == QAbstractSocket.UnsupportedSocketOperationError:
            err_msg = 'Unsupported Socket Operation Error'
        elif err == QAbstractSocket.ProxyAuthenticationRequiredError:
            err_msg = 'Proxy Authentication Required Error'
        elif err == QAbstractSocket.SslHandshakeFailedError:
            err_msg = 'Ssl Handshake Failed Error'
        elif err == QAbstractSocket.UnfinishedSocketOperationError:
            err_msg = 'Unfinished Socket Operation Error'
        elif err == QAbstractSocket.ProxyConnectionRefusedError:
            err_msg = 'Proxy Connection Refused Error'
        elif err == QAbstractSocket.ProxyConnectionClosedError:
            err_msg = 'Proxy Connection Closed Error'
        elif err == QAbstractSocket.ProxyConnectionTimeoutError:
            err_msg = 'Proxy Connection Timeout Error'
        elif err == QAbstractSocket.ProxyNotFoundError:
            err_msg = 'Proxy Not Found Error'
        elif err == QAbstractSocket.ProxyProtocolError:
            err_msg = 'Proxy Protocol Error'
        elif err == QAbstractSocket.OperationError:
            err_msg = 'Operation Error'
        elif err == QAbstractSocket.SslInternalError:
            err_msg = 'SslInternalError'
        elif err == QAbstractSocket.SslInvalidUserDataError:
            err_msg = 'Ssl Invalid User Data Error'
        elif err == QAbstractSocket.TemporaryError:
            err_msg = 'Temporary Error'
        elif err == QAbstractSocket.UnknownSocketError:
            err_msg = 'Unknown Socket Error'
        else:
            err_msg = 'Unknown Error'
        self.log_monitor.insertPlainText(err_msg + '\r')
        self.log_monitor.ensureCursorVisible()


class TCPServer(QGroupBox):

    def __init__(self, handler, port_def='5555'):
        super().__init__()
        self.setTitle('TCP server')
        #
        self.server_started = 0  # indicates if server is listening (1) or not (0)
        self.sock_started = 0  # indicates if socket is opened (1) or not (0)
        self.port = ''  # port
        self.server = None
        self.sock = None
        self.handler = handler
        # add layouts
        vbox = QVBoxLayout(self)
        layout = QGridLayout()
        vbox.addLayout(layout)
        # Line 0
        # create info_label
        self.info_label = QLabel('Stopped')
        self.info_label.setStyleSheet('color: red;')
        self.info_label.setMinimumWidth(120)
        # self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label, 0, 0)
        #
        self.port_field = QLineEdit(port_def)
        self.port_field.setMinimumWidth(120)
        self.port_field.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.port_field, 0, 1)
        #
        self.open_btn = QPushButton('Start server')
        self.open_btn.setStyleSheet('background-color: green;')
        layout.addWidget(self.open_btn, 0, 2)
        # Line 1
        # create rem_addr_label
        self.rem_addr_label = QLabel('Remote addr: ')
        # self.rem_addr_label.setStyleSheet('color: red;')
        self.rem_addr_label.setMinimumWidth(100)
        # self.rem_addr_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.rem_addr_label, 1, 0)
        #
        self.rem_addr = QLabel('----')
        self.rem_addr_label.setMinimumWidth(120)
        self.rem_addr.setStyleSheet('color: green;')
        layout.addWidget(self.rem_addr, 1, 1)
        #
        self.close_btn = QPushButton('Stop server')
        self.close_btn.setStyleSheet('background-color: red;')
        layout.addWidget(self.close_btn, 1, 2)
        # Line 2
        #
        self.rem_port_label = QLabel('Remote port: ')
        # self.rem_port_label.setStyleSheet('color: red;')
        self.rem_port_label.setMinimumWidth(100)
        # self.rem_port_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.rem_port_label, 2, 0)
        #
        self.rem_port = QLabel('----')
        self.rem_port.setMinimumWidth(120)
        self.rem_port.setStyleSheet('color: green;')
        layout.addWidget(self.rem_port, 2, 1)
        #
        self.clear_btn = QPushButton('Clear log')
        self.clear_btn.setStyleSheet('background-color: #101010; color: #eeeeee;')
        layout.addWidget(self.clear_btn, 2, 2)
        # create log monitor
        self.log_monitor = QTextEdit()
        self.log_monitor.setReadOnly(True)
        self.log_monitor.setStyleSheet("""
                        background-color: #101010;
                        color: #FFFFFF;
                        font-family: Ariel;
                        font-size: 11px;
                        """)
        vbox.addWidget(self.log_monitor)
        #
        self.open_btn.clicked.connect(self.start_serv)
        self.close_btn.clicked.connect(self.stop_serv)
        self.clear_btn.clicked.connect(self.clear_log_monitor)

    def start_serv(self):
        if self.server_started == 0:
            self.port = self.port_field.text()
            if self.port:
                self.server = QTcpServer(self)
                self.server.setMaxPendingConnections(max_pending_conn)
                self.server.acceptError.connect(self.accept_error)
                self.server.newConnection.connect(self.new_connection)
                if self.server.listen(QHostAddress.Any, int(self.port)):
                    self.info_label.setText('Listening...')
                    self.info_label.setStyleSheet('color: #00dd00;')  # green
                    self.server_started = 1
                    self.log_monitor.insertPlainText('Server is listening...\r')
                    self.log_monitor.insertPlainText('Port: ' + port_default + '\r')
                    self.log_monitor.ensureCursorVisible()
                else:
                    self.info_label.setText(self.server.errorString())
                    self.info_label.setStyleSheet('color: red;')  # red
                    self.log_monitor.insertPlainText(self.server.errorString() + '\r')
                    self.log_monitor.ensureCursorVisible()
            else:
                self.info_label.setText('Pls enter port')
                self.info_label.setStyleSheet('color: red;')

    def stop_serv(self):
        if self.server_started:
            self.server.close()
            if self.sock:
                self.sock.close()
                self.sock_started = 0  # indicates that the socket is closed
            self.info_label.setText('Stopped')
            self.info_label.setStyleSheet('color: red;')
            self.log_monitor.insertPlainText('Server is stopped...\r')
            self.log_monitor.ensureCursorVisible()
            self.server_started = 0

    @Slot()
    def new_connection(self):
        if not self.sock_started:  # if socket is closed
            self.sock = self.server.nextPendingConnection()  # accept connection
            # self.server.pauseAccepting()        # pause accepting new connections
            if self.sock:
                self.sock_started = 1
                self.sock.readyRead.connect(self.on_rx)
                self.sock.readyRead.connect(self.handler)
                self.sock.aboutToClose.connect(self.about_to_close)
                self.sock.errorOccurred.connect(self.sock_error)
                self.sock.bytesWritten.connect(self.bytes_written)
                self.sock.disconnected.connect(self.disconnected)
                self.sock.stateChanged.connect(self.state_changed)
                #
                rem_addr = self.sock.peerAddress()
                rem_port = self.sock.peerPort()
                self.rem_addr.setText(rem_addr.toString())
                self.rem_port.setText(str(rem_port))
                #
                self.info_label.setText('Connected')
                self.info_label.setStyleSheet('color: #00dd00;')  # green
                self.log_monitor.insertPlainText('Connected: ' + rem_addr.toString() + ' : ' + str(rem_port) + '\r')
                self.log_monitor.ensureCursorVisible()

    @Slot()
    def about_to_close(self):
        self.log_monitor.insertPlainText('Socket is about to close\r')
        self.log_monitor.ensureCursorVisible()

    def clear_log_monitor(self):
        self.log_monitor.clear()  # clear log monitor

    @Slot()
    def on_rx(self):  # display number of bytes received on log_monitor
        num_rx_bytes = self.sock.bytesAvailable()
        self.log_monitor.insertPlainText('Bytes received: ' + str(num_rx_bytes) + '\r')
        self.log_monitor.ensureCursorVisible()

    @Slot()
    def disconnected(self):
        self.rem_addr.setText('----')
        self.rem_port.setText('----')
        if self.sock:
            self.sock.close()
        self.sock_started = 0  # indicates that the socket is closed
        # self.server.resumeAccepting()        # resume accepting new connections
        if self.server.isListening():
            self.info_label.setText('Listening...')
            self.info_label.setStyleSheet('color: #00dd00;')  # green
            self.log_monitor.insertPlainText('Server is listening...\r')
            self.log_monitor.ensureCursorVisible()

    def bytes_written(self, num_bytes):
        self.log_monitor.insertPlainText('Bytes sent: ' + str(num_bytes) + '\r')
        self.log_monitor.ensureCursorVisible()

    @Slot()
    def state_changed(self, state):
        if state == QAbstractSocket.SocketState.UnconnectedState:
            curr_state = 'Socket disconnected'
        elif state == QAbstractSocket.SocketState.HostLookupState:
            curr_state = 'Host Lookup...'
        elif state == QAbstractSocket.SocketState.ConnectingState:
            curr_state = 'Socket connecting...'
        elif state == QAbstractSocket.SocketState.ConnectedState:
            curr_state = 'Socket connected'
        elif state == QAbstractSocket.SocketState.BoundState:
            curr_state = 'Bound'
        elif state == QAbstractSocket.SocketState.ClosingState:
            curr_state = 'Socket closing...'
        else:
            curr_state = str(self.server.state())
        self.info_label.setText(curr_state)
        self.log_monitor.insertPlainText(curr_state + '\r')
        self.log_monitor.ensureCursorVisible()

    def sock_error(self):
        self.info_label.setText(self.sock.errorString())
        self.info_label.setStyleSheet('color: red;')
        err = self.sock.error()
        if err == QSerialPort.SerialPortError.ResourceError:
            self.stop_serv()  # close if port is not available, etc.

    def accept_error(self):
        self.info_label.setText(self.server.errorString())
        self.info_label.setStyleSheet('color: red;')
        self.log_monitor.insertPlainText(self.server.errorString() + '\r')
        self.log_monitor.ensureCursorVisible()
        err = self.server.error()
        if err == QSerialPort.SerialPortError.ResourceError:
            self.stop_serv()  # close if port is not available, etc.
