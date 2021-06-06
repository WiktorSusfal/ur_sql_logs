import pyodbc

class UR_SQL_connection:

    def __init__(self, sql_ip, pwd, uid='SA', driver='SQL Server Native Client 11.0', database='master'):

        self.driver = driver
        self.sql_ip = sql_ip
        self.database = database
        self.uid = uid
        self.pwd = pwd

    def sql_connect(self):

<<<<<<< HEAD
        conncetion_string = 'DRIVER={' + self.driver + '};SERVER=' + self.sql_ip + ';DATABASE=' + \
                            self.database + ';UID=SA;PWD=' + self.uid + ';PWD=' + self.pwd + ';'
=======
        conncetion_string = 'DRIVER={' + self.driver + '};SERVER=' + self.sql_ip + ';DATABASE=' + self.database + ';UID=SA;PWD=' + self.uid + ';PWD=' + self.pwd + ';'
>>>>>>> e455e9b6e43f8e6ae84d563feb398e344a89cb48
        c = pyodbc.connect(conncetion_string, autocommit=True)

        return c.cursor()

<<<<<<< HEAD

class UR_messages_logger:

    common_logged_data = [['robot_id', 'int', 'primary_key'], ['message_type', 'varchar(2)'], ['timestamp', 'varchar(30)'],
=======
class UR_messages_logger:


    common_logged_data = [['robot_id', 'int', 'primary_key'], ['message_type', 'varchar(2)'], ['timestamp', 'varchar(15)'],
>>>>>>> e455e9b6e43f8e6ae84d563feb398e344a89cb48
                          ['date_time', 'datetime2(0)'], ['source', 'varchar(4)'], ['robot_message_type', 'varchar(2)']]

    ver_msg_custom_columns = [['project_name', 'varchar(15)'], ['major_version', 'varchar(2)'], ['minor_version', 'varchar(2)'],
                              ['bugfix_version', 'varchar(5)'], ['build_number', 'varchar(5)'], ['build_date', 'varchar(25)']]

    key_msg_custom_columns = [['robot_message_code', 'varchar(3)'], ['robot_message_argument', 'varchar(3)'],
                              ['robot_message_title', 'varchar(50)'], ['key_text_message', 'varchar(100)']]

    saf_msg_custom_columns = [['robot_message_code', 'varchar(3)'], ['robot_message_argument', 'varchar(3)'],
                              ['safety_mode_type', 'varchar(3)'], ['safety_mode_type_txt', 'varchar(20)'],
                              ['report_data_type', 'varchar(5)'], ['report_data', 'varchar(20)']]

    comm_msg_custom_columns = [['robot_message_code', 'varchar(3)'], ['robot_message_argument', 'varchar(3)'],
                               ['report_level', 'varchar(5)'], ['report_level_txt', 'varchar(15)'],
                               ['robot_message_data_type', 'varchar(5)'], ['robot_message_data', 'varchar(10)'],
                               ['robot_comm_text_message', 'varchar(100)']]

    rt_exc_msg_custom_columns = [['script_line_no', 'int'], ['script_column_no', 'int'],
                                 ['runtime_exception_text_message', 'varchar(100)']]


<<<<<<< HEAD
    def __init__(self, database_name, r_seq_name='robots_ids',
                 r_info_table_name='robots_info', log_count=0):

        self.database_name = database_name
        self.robot_id_sequence_name = r_seq_name
        self.robot_info_table_name = r_info_table_name
=======
    def __init__(self, database_name, robot_sn, robot_friendly_name, r_seq_name='robots_ids',
                 r_info_table_name='robots_info', a_r_id=-1, log_count=0):

        self.database_name = database_name
        self.assigned_robot_friendly_name = robot_friendly_name
        self.assigned_robot_sn_no = robot_sn
        self.robot_id_sequence_name = r_seq_name
        self.robot_info_table_name = r_info_table_name
        self.assigned_robot_id = a_r_id
>>>>>>> e455e9b6e43f8e6ae84d563feb398e344a89cb48
        self.logged_msg_count = log_count

    def create_logging_database(self, cursor):

        query = """
            IF NOT EXISTS (select * from master.sys.databases where name = ? )
            BEGIN
            CREATE DATABASE """ + self.database_name + """
            END
            """

        cursor.execute(query, [self.database_name])
        cursor.execute('use ' + self.database_name)

<<<<<<< HEAD
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

    def create_robot_description_record(self, cursor, robot_name, robot_sn=000000):

        insert_data_query = """
        IF NOT EXISTS (SELECT sn from dbo.""" + self.robot_info_table_name + """ where name = ?)
=======
    def create_robot_description_record(self, cursor):

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

        insert_data_query = """
        IF NOT EXISTS (SELECT sn from dbo.""" + self.robot_info_table_name + """ where sn = ?)
>>>>>>> e455e9b6e43f8e6ae84d563feb398e344a89cb48
        BEGIN 
        INSERT INTO dbo.""" + self.robot_info_table_name + """ (sn, name) VALUES (?,?)
        END"""

<<<<<<< HEAD
        cursor.execute(insert_data_query, [robot_name, robot_sn,
                                           robot_name])


    def retrieve_robot_id_from_sql(self, cursor, robot_name):

        query = 'SELECT id from dbo.' + self.robot_info_table_name + ' where name = ?'
        cursor.execute(query, robot_name)
        result = list(cursor)

        return result[0][0]
=======
        cursor.execute(insert_data_query, [self.assigned_robot_sn_no, self.assigned_robot_sn_no,
                                           self.assigned_robot_friendly_name])


    def retrieve_robot_id_from_sql(self, cursor):

        query = 'SELECT id from dbo.' + self.robot_info_table_name + ' where sn = ?'
        cursor.execute(query, self.assigned_robot_sn_no)
        self.assigned_robot_id = list(cursor)[0][0]
>>>>>>> e455e9b6e43f8e6ae84d563feb398e344a89cb48

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

<<<<<<< HEAD
        basic_query = basic_query[:-4]
        #basic_query += """CONSTRAINT """ + table_name + """_robot_id_exists FOREIGN KEY (robot_id)
        #                   REFERENCES dbo.robots_info (id)"""
=======
        basic_query += """CONSTRAINT """ + table_name + """_robot_id_exists FOREIGN KEY (robot_id)
                            REFERENCES dbo.robots_info (id)"""
>>>>>>> e455e9b6e43f8e6ae84d563feb398e344a89cb48
        basic_query += '\n\t\t)\n\t\tEND'

        return basic_query

    def create_data_tables(self, cursor):

        ver_msg_create_table_query = self.create_data_table_query('version_messages', self.ver_msg_custom_columns)
        cursor.execute(ver_msg_create_table_query)

        key_msg_create_table_query = self.create_data_table_query('key_messages', self.key_msg_custom_columns)
        cursor.execute(key_msg_create_table_query)

        saf_msg_create_table_query = self.create_data_table_query('safety_messages', self.saf_msg_custom_columns)
        cursor.execute(saf_msg_create_table_query)

        comm_msg_create_table_query = self.create_data_table_query('comm_messages', self.comm_msg_custom_columns)
        cursor.execute(comm_msg_create_table_query)

        rt_msg_create_table_query = self.create_data_table_query('runtime_exceptions_messages', self.rt_exc_msg_custom_columns)
        cursor.execute(rt_msg_create_table_query)

<<<<<<< HEAD
    def initialize_logging(self, cursor, robot_name):

        self.create_logging_database(cursor)
        self.create_data_tables(cursor)
        self.create_robot_description_record(cursor, robot_name)


    def create_insert_data_query(self, table_name, robot_id, data, values_to_insert_no):

        query = """INSERT INTO dbo.""" + table_name + """ 
        VALUES ( """ + str(robot_id) + ""","""
=======
    def initialize_logging(self, cursor):

        self.create_logging_database(cursor)
        self.create_robot_description_record(cursor)
        self.retrieve_robot_id_from_sql(cursor)
        self.create_data_tables(cursor)

    def create_insert_data_query(self, table_name, data, values_to_insert_no):

        query = """INSERT INTO dbo.""" + table_name + """ 
        VALUES ( """ + str(self.assigned_robot_id) + """, """
>>>>>>> e455e9b6e43f8e6ae84d563feb398e344a89cb48

        for i in values_to_insert_no:
            query += '\'' + str(data[i]) + '\','

        query = query[:-1]
        query += ')'

        return query

<<<<<<< HEAD
    def log_messages_data(self, cursor, decoded_data, robot_name):

        robot_id = self.retrieve_robot_id_from_sql(cursor, robot_name)
        print(f'\n  Given name: {robot_name}, RETRIEVED ID: {robot_id}')
=======
    def log_messages_data(self, cursor, decoded_data):
>>>>>>> e455e9b6e43f8e6ae84d563feb398e344a89cb48

        for msg in decoded_data:

            if len(msg) > 0:
                if msg[5] == 3:
<<<<<<< HEAD
                    query = self.create_insert_data_query('version_messages', robot_id, msg, [1, 2, 3, 4, 5, 8, 9,
                                                                                    10, 11, 12, 13])
                elif msg[5] == 7:
                    query = self.create_insert_data_query('key_messages', robot_id, msg, [1, 2, 3, 4, 5, 7, 8, 10, 11])
                elif msg[5] == 5:
                    query = self.create_insert_data_query('safety_messages', robot_id, msg, [1, 2, 3, 4, 5, 7,
                                                                                   8, 9, 10, 11, 12])
                elif msg[5] == 6:
                    query = self.create_insert_data_query('comm_messages', robot_id, msg, [1, 2, 3, 4, 5, 7, 8,
                                                                                 9, 10, 11, 12, 13])
                elif msg[5] == 10:
                    query = self.create_insert_data_query('runtime_exceptions_messages', robot_id, msg, [1, 2, 3, 4, 5,
                                                                                               7, 8, 9])
=======
                    query = self.create_insert_data_query('version_messages', msg, [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13])
                elif msg[5] == 7:
                    query = self.create_insert_data_query('key_messages', msg, [1, 2, 3, 4, 5, 7, 8, 10, 11])
                elif msg[5] == 5:
                    query = self.create_insert_data_query('safety_messages', msg, [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12])
                elif msg[5] == 6:
                    query = self.create_insert_data_query('comm_messages', msg, [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13])
                elif msg[5] == 10:
                    query = self.create_insert_data_query('runtime_exceptions_messages', msg, [1, 2, 3, 4, 5, 7, 8, 9])
>>>>>>> e455e9b6e43f8e6ae84d563feb398e344a89cb48

                if msg[5] in (3, 7, 5, 6, 10):
                    cursor.execute(query)
                    self.logged_msg_count += 1
                else:
                    print('Cannot create insert query for given decoded message.')
