import socket


class UR_connection:
    URConnections = []

    def __init__(self, ip, port, ref_freq=-1, robot_name='emptyName', refresh_interval=0.0, terminate=False):

        self.ip = ip
        self.port = port
        self.robot_name = robot_name
        self.refresh_interval = refresh_interval

        self.data_buffer = []
        self.UR_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.UR_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Used for terminate threads in application GUI. Based on this property, the data retrieval is broken and the
        # connection is terminated

        self.terminate = terminate

        self.available_interfaces = [30001, 30011, 30002, 30012, 30003, 30013, 30004]

        if ref_freq != -1:
            self.refresh_interval = 1.0 / ref_freq

        if self.port in [30001, 30011]:
            self.interface_name = 'Primary Client'
        elif self.port in [30002, 30012]:
            self.interface_name = 'Secondary Client'
        elif self.port in [30003, 30013]:
            self.interface_name = 'Real Time Client'
        elif self.port in [30004]:
            self.interface_name = 'Real Time Data Exchange'
        else:
            self.interface_name = 'Not known interface, probably mistake'

        if self.port in [30001, 30011, 30002, 30012] and ref_freq == -1:
            self.refresh_interval = 1.0 / 10.0
        elif self.port in [30003, 30013, 30004] and ref_freq == -1:
            self.refresh_interval = 1.0 / 500.0
        elif ref_freq == -1:
            self.refresh_interval = 1.0

        UR_connection.URConnections.append(self)

    def connect_to_UR(self) -> None:

        if self.port in self.available_interfaces:
            print(f'{self.robot_name} - creating connection with server')
            self.UR_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.UR_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.UR_server.connect((self.ip, self.port))
        else:
            print('\nCannot connect to not known interface\n')

    def disconnect_from_UR(self) -> None:
        print(f'{self.robot_name} - closing connection with server')
        self.UR_server.close()

    def return_data(self):
        self.data_buffer = self.UR_server.recv(4096)
        return self.data_buffer
