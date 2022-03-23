import pyodbc
import xml.etree.ElementTree as ET


class SqlConnCursor:

    def __init__(self, params):
        self.conn_str = params.return_connection_string()
        self.timeout = params.connTimeout

    def __enter__(self):
        try:
            self.c = pyodbc.connect(self.conn_str, autocommit=True, timeout=self.timeout)
        except:
            raise ConnectionError

        return self.c.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.c.cursor().close()
        self.c.close()


class SqlConnectionParams:
    connectionsParams = []

    def __init__(self, name, sql_ip, pwd, uid='sa', driver='SQL Server Native Client 11.0', database='master',
                 conn_timeout=5):
        self.name = name
        self.driver = driver
        self.sql_ip = sql_ip
        self.database = database
        self.uid = uid
        self.pwd = pwd
        self.connTimeout = conn_timeout

        SqlConnectionParams.connectionsParams.append(self)

    def return_connection_string(self):
        return 'DRIVER={' + self.driver + '};SERVER=' + self.sql_ip + ';DATABASE=' + \
               self.database + ';UID=SA;PWD=' + self.uid + ';PWD=' + self.pwd + ';'


class UR_messages_logger:

    # lists for storing sql table column structures - each list for one table
    # data format - [(column name, column type, optional constraint), (...), ...]
    common_logged_data = []
    ver_msg_custom_columns = []
    key_msg_custom_columns = []
    saf_msg_custom_columns = []
    comm_msg_custom_columns = []
    rt_exc_msg_custom_columns = []

    def __init__(self, database_name, sqlConnectionParams, r_seq_name='robots_ids',
                 r_info_table_name='robots_info', log_count=0):

        self.database_name = database_name
        self.robot_id_sequence_name = r_seq_name
        self.robot_info_table_name = r_info_table_name
        self.logged_msg_count = log_count
        self.sqlConnParams = sqlConnectionParams

        # read sql tables structure from xml file
        UR_messages_logger.common_logged_data = self.read_column_structure('common_logged_data')
        UR_messages_logger.ver_msg_custom_columns = self.read_column_structure('ver_msg_custom_columns')
        UR_messages_logger.key_msg_custom_columns = self.read_column_structure('key_msg_custom_columns')
        UR_messages_logger.saf_msg_custom_columns = self.read_column_structure('saf_msg_custom_columns')
        UR_messages_logger.comm_msg_custom_columns = self.read_column_structure('comm_msg_custom_columns')
        UR_messages_logger.rt_exc_msg_custom_columns = self.read_column_structure('rt_exc_msg_custom_columns')

    @classmethod
    def read_column_structure(cls, table_node_name):

        colStrTree = ET.parse('Resources/sql_columns_structure.xml')
        tableNode = colStrTree.find(table_node_name)
        colStr = []

        for colInfo in tableNode:
            colName = colInfo.find('name').text
            colType = colInfo.find('type').text
            colOptions = colInfo.find('options').text or ''

            colStr.append((colName, colType, colOptions))

        return colStr

    def create_logging_database(self):

        query = """
            IF NOT EXISTS (select * from master.sys.databases where name = ? )
            BEGIN
            CREATE DATABASE """ + self.database_name + """
            END
            """

        with SqlConnCursor(self.sqlConnParams) as cursor:
            cursor.execute(query, [self.database_name])
            cursor.execute('use ' + self.database_name)

            create_sequence_id_query = """
                    IF NOT EXISTS (select name from sys.sequences where name = ?)
                    BEGIN
                    CREATE SEQUENCE dbo.""" + self.robot_id_sequence_name + """
                        AS int
                        START WITH 0
                        INCREMENT BY 1
                    END
                    """
            cursor.execute(create_sequence_id_query, [self.robot_id_sequence_name])

            create_info_table_query = """
                    IF NOT EXISTS (SELECT table_name from information_schema.tables where table_name = ?)
                    BEGIN
                    CREATE TABLE dbo.""" + self.robot_info_table_name + """
                    (
                        id int not null DEFAULT(NEXT VALUE FOR dbo.""" + self.robot_id_sequence_name + """),
                        sn varchar(11) not null, 
                        name varchar(20),
                        primary key(id)
                    )
                    END
                    """
            cursor.execute(create_info_table_query, [self.robot_info_table_name])

    def create_robot_description_record(self, robot_name, robot_sn=000000):

        insert_data_query = """
        IF NOT EXISTS (SELECT sn from dbo.""" + self.robot_info_table_name + """ where name = ?)
        BEGIN 
        INSERT INTO dbo.""" + self.robot_info_table_name + """ (sn, name) VALUES (?,?)
        END"""

        with SqlConnCursor(self.sqlConnParams) as cursor:
            cursor.execute(insert_data_query, [robot_name, robot_sn,
                                               robot_name])

    def retrieve_robot_id_from_sql(self, robot_name):

        query = 'SELECT id from dbo.' + self.robot_info_table_name + ' where name = ?'

        with SqlConnCursor(self.sqlConnParams) as cursor:
            cursor.execute(query, robot_name)
            result = list(cursor)

        return result[0][0]

    def create_data_table_query(self, table_name, custom_column_list):

        basic_query = """
        IF NOT EXISTS (SELECT table_name from information_schema.tables where table_name = \'""" + table_name + """\')
        BEGIN
            CREATE TABLE dbo.""" + table_name + """
            (
                robot_id int not null,
                message_type varchar(2) not null,
                timestamp varchar(40) not null,
                date_time datetime2(0) not null,
                source varchar(4) not null,
                robot_message_type varchar(2) not null,
        """
        i = 0
        while i < len(custom_column_list):
            basic_query += '\t\t'
            for j in custom_column_list[i]:
                basic_query += j + ' '
            basic_query += ',\n\t\t'
            i += 1

        basic_query = basic_query[:-4]
        # basic_query += """CONSTRAINT """ + table_name + """_robot_id_exists FOREIGN KEY (robot_id)
        #                   REFERENCES dbo.robots_info (id)"""
        basic_query += '\n\t\t)\n\t\tEND'

        return basic_query

    def create_data_tables(self):

        with SqlConnCursor(self.sqlConnParams) as cursor:
            ver_msg_create_table_query = self.create_data_table_query('version_messages', self.ver_msg_custom_columns)
            cursor.execute(ver_msg_create_table_query)

            key_msg_create_table_query = self.create_data_table_query('key_messages', self.key_msg_custom_columns)
            cursor.execute(key_msg_create_table_query)

            saf_msg_create_table_query = self.create_data_table_query('safety_messages', self.saf_msg_custom_columns)
            cursor.execute(saf_msg_create_table_query)

            comm_msg_create_table_query = self.create_data_table_query('comm_messages', self.comm_msg_custom_columns)
            cursor.execute(comm_msg_create_table_query)

            rt_msg_create_table_query = self.create_data_table_query('runtime_exceptions_messages',
                                                                     self.rt_exc_msg_custom_columns)
            cursor.execute(rt_msg_create_table_query)

    def initialize_logging(self, robot_name):

        with SqlConnCursor(self.sqlConnParams) as cursor:
            self.create_logging_database(cursor)
            self.create_data_tables(cursor)
            self.create_robot_description_record(cursor, robot_name)

    def create_insert_data_query(self, table_name, robot_id, data, values_to_insert_no):

        query = """INSERT INTO dbo.""" + table_name + """ 
        VALUES ( """ + str(robot_id) + ""","""

        for i in values_to_insert_no:
            query += '\'' + str(data[i]) + '\','

        query = query[:-1]
        query += ')'

        return query

    def log_messages_data(self, decoded_data, robot_name):

        with SqlConnCursor(self.sqlConnParams) as cursor:
            robot_id = self.retrieve_robot_id_from_sql(cursor, robot_name)
            print(f'\n  Given name: {robot_name}, RETRIEVED ID: {robot_id}')

            for msg in decoded_data:

                if len(msg) > 0:
                    if msg[5] == 3:
                        query = self.create_insert_data_query('version_messages', robot_id, msg, [1, 2, 3, 4, 5, 8, 9,
                                                                                                  10, 11, 12, 13])
                    elif msg[5] == 7:
                        query = self.create_insert_data_query('key_messages', robot_id, msg,
                                                              [1, 2, 3, 4, 5, 7, 8, 10, 11])
                    elif msg[5] == 5:
                        query = self.create_insert_data_query('safety_messages', robot_id, msg, [1, 2, 3, 4, 5, 7,
                                                                                                 8, 9, 10, 11, 12])
                    elif msg[5] == 6:
                        query = self.create_insert_data_query('comm_messages', robot_id, msg, [1, 2, 3, 4, 5, 7, 8,
                                                                                               9, 10, 11, 12, 13])
                    elif msg[5] == 10:
                        query = self.create_insert_data_query('runtime_exceptions_messages', robot_id, msg,
                                                              [1, 2, 3, 4, 5,
                                                               7, 8, 9])
                    if msg[5] in (3, 7, 5, 6, 10):
                        cursor.execute(query)
                        self.logged_msg_count += 1
                    else:
                        print('Cannot create insert query for given decoded message.')
