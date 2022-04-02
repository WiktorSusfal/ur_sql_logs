import pyodbc
from collections import namedtuple
import xml.etree.ElementTree as ET


class SqlConnCursor:

    def __init__(self, params):
        self.conn_str = params.return_connection_string()
        self.timeout = params.connTimeout

    def __enter__(self):
        try:
            self.c = pyodbc.connect(self.conn_str, autocommit=True, timeout=self.timeout)
        except:
            print('Connection Error')
            raise ConnectionError

        return self.c.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.c.cursor().close()
        self.c.close()


class SqlConnectionParams:
    connectionsParams = []

    def __init__(self, name, sql_ip, pwd, uid='SA', driver='SQL Server Native Client 11.0', database='master',
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
               self.database + ';UID=' + self.uid + ';PWD=' + self.pwd + ';'


# function for reading column names for tables used to store messages from robots
def read_column_structure(table_node_name):

    colStrTree = ET.parse('Resources/ur_data_structure.xml')
    tableNode = colStrTree.find(table_node_name)
    colStr = []

    ColumnData = namedtuple('ColumnData', 'columnName columnType columnOptions')

    # colInfo = 'data_item' node from xml file
    for colInfo in tableNode:

        if int(colInfo.find('logged_to_sql').text) == 1:
            colName = colInfo.find('sql_column_name').text
            colType = colInfo.find('sql_column_type').text
            colOptions = colInfo.find('sql_column_options').text or ''

            cd = ColumnData(colName, colType, colOptions)
            colStr.append(cd)

    return colStr

class UR_messages_logger:

    # lists for storing sql table column structures - each list for one table
    # data format - [(column name, column type, optional constraint), (...), ...]
    # the objective is to store data from all versions of robots in one set of tables, so these are class variables
    common_logged_data = read_column_structure('common_logged_data')
    ver_msg_custom_columns = common_logged_data + read_column_structure('version_message')
    key_msg_custom_columns = common_logged_data + read_column_structure('key_message')
    saf_msg_custom_columns = common_logged_data + read_column_structure('safety_message')
    comm_msg_custom_columns = common_logged_data + read_column_structure('communication_message')
    rt_exc_msg_custom_columns = common_logged_data + read_column_structure('runtime_exception_message')

    def __init__(self, database_name, sqlConnectionParams, r_seq_name='robots_ids',
                 r_info_table_name='robots_info', log_count=0):

        self.database_name = database_name
        self.robot_id_sequence_name = r_seq_name
        self.robot_info_table_name = r_info_table_name
        self.logged_msg_count = log_count
        self.sqlConnParams = sqlConnectionParams

    def create_logging_database(self):
        query = """
            IF NOT EXISTS (select * from master.sys.databases where name = ? )
            BEGIN
            CREATE DATABASE """ + self.database_name + """
            END
            """

        with SqlConnCursor(self.sqlConnParams) as cursor:
            cursor.execute(query, [self.database_name])
            cursor.execute('USE ' + self.database_name)

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
        print('insert data query ' , insert_data_query)
        with SqlConnCursor(self.sqlConnParams) as cursor:
            cursor.execute('USE ' + self.database_name)
            cursor.execute(insert_data_query, [robot_name, robot_sn, robot_name])

    def retrieve_robot_id_from_sql(self, robot_name):

        query = 'SELECT id from dbo.' + self.robot_info_table_name + ' where name = ?'

        with SqlConnCursor(self.sqlConnParams) as cursor:
            cursor.execute('USE ' + self.database_name)
            cursor.execute(query, robot_name)
            result = list(cursor)

        return result[0][0]

    def create_data_table_query(self, table_name, custom_column_list):

        basic_query = """
        IF NOT EXISTS (SELECT table_name from information_schema.tables where table_name = \'""" + table_name + """\')
        BEGIN
            CREATE TABLE dbo.""" + table_name + """
            (
        """

        for col_data in custom_column_list:
            basic_query += '\t\t'
            basic_query += col_data.columnName + " " + col_data.columnType + " " + col_data.columnOptions
            basic_query += ',\n\t\t'

        basic_query = basic_query[:-4]
        basic_query += '\n\t\t)\n\t\tEND'

        return basic_query

    def create_data_tables(self):
        with SqlConnCursor(self.sqlConnParams) as cursor:

            cursor.execute('USE ' + self.database_name)

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
            cursor.execute('USE ' + self.database_name)
            self.create_logging_database(cursor)
            self.create_data_tables(cursor)
            self.create_robot_description_record(cursor, robot_name)

    def create_insert_data_query(self, table_name, robot_id, data_dictionary, sql_columns_struct):
        query = """INSERT INTO dbo.""" + table_name + """ 
        VALUES ( """

        for col_data in sql_columns_struct:
            query += '\'' + str(data_dictionary[col_data.columnName]) + '\','

        query = query[:-1]
        query += ')'

        return query

    def log_messages_data(self, decoded_data, robot_name):

        with SqlConnCursor(self.sqlConnParams) as cursor:
            cursor.execute('USE ' + self.database_name)
            robot_id = self.retrieve_robot_id_from_sql(robot_name)
            print(f'\n  Given name: {robot_name}, RETRIEVED ID: {robot_id}')

            for msg in decoded_data:

                msg['robot_id'] = robot_id
                if len(msg) > 0:
                    if int(msg['robot_message_type']) == 3:
                        query = self.create_insert_data_query('version_messages', robot_id, msg,
                                                              self.ver_msg_custom_columns)
                    elif int(msg['robot_message_type']) == 7:
                        query = self.create_insert_data_query('key_messages', robot_id, msg,
                                                              self.key_msg_custom_columns)
                    elif int(msg['robot_message_type']) == 5:
                        query = self.create_insert_data_query('safety_messages', robot_id, msg,
                                                              self.saf_msg_custom_columns)
                    elif int(msg['robot_message_type']) == 6:
                        query = self.create_insert_data_query('comm_messages', robot_id, msg,
                                                              self.comm_msg_custom_columns)
                    elif int(msg['robot_message_type']) == 10:
                        query = self.create_insert_data_query('runtime_exceptions_messages', robot_id, msg,
                                                              self.rt_exc_msg_custom_columns)

                    if int(msg['robot_message_type']) in (3, 7, 5, 6, 10):
                        cursor.execute(query)
                        self.logged_msg_count += 1
                    else:
                        print('Cannot create insert query for given decoded message.')
