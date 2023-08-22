import PyQt5.QtWidgets as qtw


class DBConnectionConfigView(qtw.QWidget):

    def __init__(self):
        super(DBConnectionConfigView, self).__init__()

        self.setWindowTitle("Choose database connection")

        self.list_label = qtw.QLabel("Choose database connection: ")
        self.db_conn_list = qtw.QComboBox()

        self.password_label = qtw.QLabel("Enter database password: ")
        self.db_password_input = qtw.QLineEdit()
        self.db_password_input.setEchoMode(qtw.QLineEdit.Password)

        self.db_connect_btn = qtw.QPushButton(text='Connect')

        conn_list_layout = qtw.QHBoxLayout()
        conn_list_layout.addWidget(self.list_label)
        conn_list_layout.addWidget(self.db_conn_list)
        password_layout = qtw.QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.db_password_input)

        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(conn_list_layout)
        main_layout.addLayout(password_layout)
        main_layout.addWidget(self.db_connect_btn)

        self.setLayout(main_layout)
        self.show()

if __name__ == '__main__':
    from lib.helpers.visual_view_test_template import visual_test_preview
    visual_test_preview(DBConnectionConfigView())