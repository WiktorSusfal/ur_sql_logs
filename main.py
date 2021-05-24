import UR_Connections
import UR_Messages
import UR_SQL_Logging
import time

recv_count = 0

UR_connection = UR_Connections.UR_connection('192.168.1.3', 30011)
UR_connection.connect_to_UR()

message_parser = UR_Messages.messageParser(20)
decoding_manager = UR_Messages.message_decoding_manager

c = UR_SQL_Logging.UR_SQL_connection('192.168.1.1', 'sample_password')
cursor = c.sql_connect()

log = UR_SQL_Logging.UR_messages_logger('UR_LOG_DATA', '20200504678', 'Robot - linia nr 1')
log.initialize_logging(cursor)

time.sleep(1.0)

while True:

    data = UR_connection.return_data()

    messages_list = message_parser.return_primary_client_messages(data)
    decoded_data = decoding_manager.get_decoded_data(decoding_manager, messages_list)

    if len(decoded_data) > 0:
        i=0
        while i < len(decoded_data):
            print(decoded_data[i])
            i += 1
            recv_count += 1

        log.log_messages_data(cursor, decoded_data)

        print("Recieved Messages: " + str(recv_count) + "   Logged Messages: " + str(log.logged_msg_count))

    time.sleep(UR_connection.refresh_interval)


UR_connection.disconnect_from_UR()


