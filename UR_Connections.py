import socket

class UR_connection:
    UR_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    UR_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ip = ''
    port = 0
    refresh_interval = 0.0
    data_buffer = []

    def __init__(self, ip, port, ref_freq=-1):

        self.ip = ip
        self.port = port

        if ref_freq != -1:
            self.refresh_interval = 1.0 / ref_freq

        if port in [30001, 30011]:
            self.interface_name = 'Primary Client'
        elif port in [30002, 30012]:
            self.interface_name = 'Secondary Client'
        elif port in [30003, 30013]:
            self.interface_name = 'Real Time Client'
        elif port in [30004]:
            self.interface_name = 'Real Time Data Exchange'
        else:
            self.interface_name = 'Not known interface, probably mistake'

        if port in [30001, 30011, 30002, 30012] and ref_freq == -1:
            self.refresh_interval = 1.0 / 10.0
        elif port in [30003, 30013, 30004] and ref_freq == -1:
            self.refresh_interval = 1.0 / 500.0
        elif ref_freq == -1:
            self.refresh_interval = 1.0

    def connect_to_UR(self):

        if self.interface_name not in ['Not known interface, probably mistake']:
            self.UR_server.connect((self.ip, self.port))
        else:
            print('\nCannot connect to not known interface\n')

    def disconnect_from_UR(self):
        self.UR_server.close()

    def return_data(self):
        self.data_buffer = self.UR_server.recv(4096)
        return self.data_buffer
