import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import threading
import time
import queue
import sys

import UR_Connections
import UR_Messages
import UR_SQL_Logging


# raw_robot_messages_storage = list of [robot name, raw message (with all sub-messages)]
raw_robot_messages_storage = queue.Queue()
# raw_parsed_messages_storage = list of [robot name, (robot message types, parsed raw messages (all targeted messages))]
raw_parsed_messages_storage = queue.Queue()
# decoded_robot_messages_storage = list of [robot name, decoded messages (all of targeted messages)]
decoded_robot_messages_storage = queue.Queue()

thread_lock = threading.Lock()

class ur_app_gui(qtw.QWidget):

    # Main layout for GUI window
    main_layout = qtw.QVBoxLayout()
    # Connection properties forms = [connection_properties_set (list), connection_buttons (list)]
    # Multiple forms, each one for each new connection with UR robot
    ur_connection_properties_forms = []
    # There is one add_robot_connection form for whole application. Responsible for collecting robot name property and
    # passing it to the new 'ur_connection_form' class instance
    add_robot_connection_form = []
    # List of objects that represent single connections with UR robots
    # Handy with terminating connection threads. Find object with 'robot_name' property corresponding with
    # the connection to terminate and set its 'terminate' property to True
    ur_connections = []
    # Single message parser. Argument '20' ensures that only messages with code '20' will be extracted from stream
    msg_parser = UR_Messages.messageParser(20)
    # Single decoding manager
    msg_decoding_manager = UR_Messages.message_decoding_manager()
    #Connection with single SQL server
    sql_conn = UR_SQL_Logging.UR_SQL_connection('192.168.1.1', 'sample_password')
    sql_cursor = sql_conn.sql_connect()
    # Single logger object for logging to the sql database
    sql_logger = UR_SQL_Logging.UR_messages_logger('UR_LOG_DATA')

    def __init__(self):
        super().__init__()
        # Set AppGUI title
        self.setWindowTitle("UR log messages logger")
        # Add single robot connection form
        self.add_robot_connection_form = self.return_add_robot_connection_form()
        self.add_robot_connection_form[2].clicked.connect(self.add_new_robot_connection)

        # Set initial main layout
        self.main_layout = qtw.QVBoxLayout()
        new_horizontal_layout = self.build_horizontal_layout(self.add_robot_connection_form)
        self.main_layout.addLayout(new_horizontal_layout)
        self.setLayout(self.main_layout)

        self.show()

        # Thread for parsing raw messages from ur robots
        parserThread = threading.Thread(target=self.parse_messages)
        parserThread.daemon = True
        parserThread.start()

        # Thread for decoding raw messages from ur robots
        decoderThread = threading.Thread(target=self.decode_messages)
        decoderThread.daemon = True
        decoderThread.start()

        # Create necessary databases on the sql server once, at start
        self.sql_logger.create_logging_database(self.sql_cursor)
        self.sql_logger.create_data_tables(self.sql_cursor)
        #Thread for logging data to a SQL database
        logger_Thread = threading.Thread(target=self.log_messages_to_sql, args=(self.sql_cursor, self.sql_logger,))
        logger_Thread.daemon = True
        logger_Thread.start()



    def return_add_robot_connection_form(self):

        elements = []

        elements.append(qtw.QLabel())
        elements[0].setText('Type unique robot name: ')
        elements[0].setObjectName("new_robot_name_label")

        elements.append(qtw.QLineEdit())
        elements[1].setObjectName("new_robot_name_entry")

        elements.append(qtw.QPushButton('Add New Connection', self))
        elements[2].setToolTip('Type the robot name first, then use this button to see the rest of properties')

        return elements

    # Properties_set = [robot_name (label), ip_request (label), ip_entry (field), port_request (label),
    # port_entry (field), frequency_request (label), frequency (field)]
    def return_robot_connection_properties_set(self, robot_name):

        connection_properties = []

        connection_properties.append(qtw.QLabel())
        connection_properties[0].setText(robot_name)
        connection_properties[0].setObjectName(robot_name + "_NameLabel")

        connection_properties.append(qtw.QLabel())
        connection_properties[1].setText("IP Address")
        connection_properties[1].setObjectName(robot_name + "_IPLabel")
        connection_properties.append(qtw.QLineEdit())
        connection_properties[2].setObjectName(robot_name + "_IPEntry")

        connection_properties.append(qtw.QLabel())
        connection_properties[3].setText("Port Number")
        connection_properties[3].setObjectName(robot_name + "_PortLabel")
        connection_properties.append(qtw.QLineEdit())
        connection_properties[4].setObjectName(robot_name + "_PortEntry")

        connection_properties.append(qtw.QLabel())
        connection_properties[5].setText("Refresh Frequency")
        connection_properties[5].setObjectName(robot_name + "_RefreshFreqLabel")
        connection_properties.append(qtw.QLineEdit())
        connection_properties[6].setObjectName(robot_name + "_RefreshFreqEntry")

        return connection_properties

    # Action_buttons_set = [connect_push_button, disconnect_push_button]
    def return_robot_connection_action_buttons_set(self):

        action_buttons = []
        action_buttons.append(qtw.QPushButton('Connect', self))
        action_buttons.append(qtw.QPushButton('Disconnect', self))

        return action_buttons

    def build_horizontal_layout(self, elements):

        horizontal_layout = qtw.QHBoxLayout()

        for element in elements:
            horizontal_layout.addWidget(element)

        return horizontal_layout

    def build_vertical_layout(self, elements):

        vertical_layout = qtw.QVBoxLayout()

        for element in elements:
            vertical_layout.addWidget(element)

        return vertical_layout

    # Based on data from 'add_robot_connection_form' add a new widget for new connection properties and buttons
    # bind buttons with proprietary functions
    def add_new_robot_connection(self):

        robot_name = self.add_robot_connection_form[1].text()
        ur_connection_properties = self.return_robot_connection_properties_set(robot_name)
        ur_connection_action_buttons = self.return_robot_connection_action_buttons_set()

        new_properties_horizontal_layout = self.build_horizontal_layout(ur_connection_properties)
        new_buttons_horizontal_layout = self.build_horizontal_layout(ur_connection_action_buttons)

        self.main_layout.addLayout(new_properties_horizontal_layout)
        self.main_layout.addLayout(new_buttons_horizontal_layout)
        self.setLayout(self.main_layout)
        self.update()

        self.ur_connection_properties_forms.append([ur_connection_properties, ur_connection_action_buttons])

        # Bind 'connect action button' with proprietary function and data from corresponding connection parameters
        curr_idx = len(self.ur_connection_properties_forms) - 1
        self.ur_connection_properties_forms[curr_idx][1][0].clicked.connect(
            lambda: self.start_thread_for_retrieving_data(self.ur_connection_properties_forms[curr_idx][0]))

        # Bind 'disconnect action button' with proprietary function and data from corresponding connection parameters
        self.ur_connection_properties_forms[curr_idx][1][1].clicked.connect(
            lambda: self.disconnect_with_choosen_robot(self.ur_connection_properties_forms[curr_idx][0]))


    def start_thread_for_retrieving_data(self, connection_properties):

        communication_thread = threading.Thread(target=self.connect_to_ur_and_retrieve_data,
                                                args=(connection_properties,))

        communication_thread.daemon = True
        communication_thread.start()

    # Have to add mechanism to check, if needed connection exists, and if yes, do not create new one but
    # use existed
    def connect_to_ur_and_retrieve_data(self, connection_properties):

        ip = connection_properties[2].text()
        port = int(connection_properties[4].text())
        freq = int(connection_properties[6].text())
        robot_name = connection_properties[0].text()

        connection_exists = False

        for conn_object in self.ur_connections:
            if conn_object.robot_name == robot_name:
                current_index = self.ur_connections.index(conn_object)
                connection_exists = True
                break

        if connection_exists == False:
            self.ur_connections.append(UR_Connections.UR_connection(ip, port, freq, robot_name))
            current_index = len(self.ur_connections) - 1

        self.ur_connections[current_index].connect_to_UR()

        while True:
            data = self.ur_connections[current_index].return_data()

            if len(data) > 0:
                thread_lock.acquire()
                raw_robot_messages_storage.put([robot_name, data])
                thread_lock.release()

            if self.ur_connections[current_index].terminate:
                self.ur_connections[current_index].terminate = False
                break

            time.sleep(self.ur_connections[current_index].refresh_interval)

        self.ur_connections[current_index].disconnect_from_UR()


    def disconnect_with_choosen_robot(self, connection_properties):

        robot_name = connection_properties[0].text()
        for conn_object in self.ur_connections:
            if conn_object.robot_name == robot_name:
                conn_object.terminate = True
                break

    def parse_messages(self):

        while True:

            if raw_robot_messages_storage.empty() == False:

                thread_lock.acquire()
                robot_name, raw_msg = raw_robot_messages_storage.get()
                thread_lock.release()

                parsed_messages_list = self.msg_parser.return_primary_client_messages(raw_msg)

                if len(parsed_messages_list) > 0:
                    thread_lock.acquire()
                    raw_parsed_messages_storage.put([robot_name, parsed_messages_list])
                    thread_lock.release()

            time.sleep(0.05)

    def decode_messages(self):

        while True:

            if raw_parsed_messages_storage.empty() == False:

                thread_lock.acquire()
                robot_name, raw_msg_list = raw_parsed_messages_storage.get()
                thread_lock.release()

                decoded_messages_list = self.msg_decoding_manager.get_decoded_data(raw_msg_list)

                thread_lock.acquire()
                decoded_robot_messages_storage.put([robot_name, decoded_messages_list])
                thread_lock.release()

                #print('\nPUTTING in DECODED storage:')
                for msg in decoded_messages_list:
                    print(f'Robot Name: {robot_name}, {msg}')

            time.sleep(0.05)

    def log_messages_to_sql(self, cursor, logger):

        while True:

            if decoded_robot_messages_storage.empty() == False:

                thread_lock.acquire()
                robot_name, decoded_messages = decoded_robot_messages_storage.get()
                thread_lock.release()

                """
                print('\nRETRIEVING from DECODED storage: ')
                for msg in decoded_messages:
                    print(f'Robot Name: {robot_name}, {msg}')
                """

                # decoded_messages is a list of all messages from this robot
                logger.create_robot_description_record(cursor, robot_name)
                logger.log_messages_data(cursor, decoded_messages, robot_name)

            time.sleep(0.05)


  
app = qtw.QApplication(sys.argv)
win = QMainindow()
win.setGeometry(300, 300, 300, 300)
win.setWindowTitle("Demo App")
win.show()

app_main_gui = ur_app_gui()
app.exec_()