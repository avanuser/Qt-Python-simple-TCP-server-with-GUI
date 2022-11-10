# Qt-Python-simple-TCP-server-with-GUI
Qt Python simple TCP server with GUI (PySide6)

This is a simple TCP server supporting one connection (socket) only.
It can be used to facilitate testing of simple TCP clients, etc.

Use "Port number" field to specify the desired TCP port.
Received messages can be seen in the main black field.
Transmitted messages can be assigned to individual buttons or entered into editable text fields during testing.
Additional black field in "TCP server" area is intended for displaying server status messages.

If you need to migrate from PySide6 to PySide2 just rename "PySide6" to "PySide2" in imports and change the following lines at the end of main.py:

\# sys.exit(app.exec())  \# PySide6

sys.exit(app.exec_())   \# PySide2


![Qt Python simple TCP server with GUI](/avanuser/Qt-Python-simple-TCP-server-with-GUI/blob/main/qt-python-tcp-server-with-gui.png)
