import struct
import datetime
import xml.etree.ElementTree as ET
from collections import namedtuple
from abc import ABC, abstractmethod


def get_4_bytes_int_or_uint(int_type, data_buffer, offset):
    integer_value = struct.unpack(int_type, data_buffer[offset:offset + 4])[0]
    offset += 4

    return [integer_value, offset]


def get_1_byte_int_or_uint(int_type, data_buffer, offset):
    integer_value = struct.unpack(int_type, data_buffer[offset:offset + 1])[0]
    offset += 1

    return [integer_value, offset]


def get_8_bytes_int_or_uint(int_type, data_buffer, offset):
    integer_value = struct.unpack(int_type, data_buffer[offset:offset + 8])[0]
    offset += 8

    return [integer_value, offset]


def get_char_array_as_string(data_buffer, offset, length):
    i = 0
    char_array = ''
    while i < length:
        char_array += str(struct.unpack('!c', data_buffer[offset + i:offset + 1 + i]))[3]
        i = i + 1

    return [char_array, (offset + length)]


class messageParser:

    def __init__(self, pr_cl_msg_cd=20):
        self.primary_client_messages_code = pr_cl_msg_cd
        self.last_primary_client_messages = []

    '''
    function splits sequence of binary data to single messages and filter messages from 'Primary Client Interface'
    of robot - with 'message_type' field = 20 by default
    :param data_buffer : sequence of binary data read from robot via TCP/IP which consists of raw messages 
    :return : list of tuples: [(robot message type, parsed single raw message)...]
    '''
    def return_primary_client_messages(self, data_buffer):

        offset = 0
        self.last_primary_client_messages = []
        while offset < len(data_buffer):

            main_package_length = struct.unpack('!I', data_buffer[offset:offset + 4])[0]
            main_message_type = struct.unpack('!B', data_buffer[offset + 4:offset + 5])[0]

            if main_package_length == 0 or main_package_length > 4096:
                break
            else:
                if main_message_type == self.primary_client_messages_code:
                    robot_message_type = struct.unpack('!B', data_buffer[offset + 14:offset + 15])[0]
                    self.last_primary_client_messages.append(
                        (robot_message_type, data_buffer[offset:(offset + main_package_length)]))

                offset += main_package_length

        return self.last_primary_client_messages


class primary_client_message_decoder(ABC):

    def __init__(self, msg_struct_xml_node_name):

        # name of xml node in 'Resources/ur_data_structure.xml' file which contains info about structure of
        # relevant robot message type
        self.msg_struct_xml_node_name = msg_struct_xml_node_name

        self.message_struct_dict = self.return_whole_message_struct()
        self.last_message_dict = self.return_decoded_message_dict()

    '''
    :param self (self.msg_struct_xml_node_name): Name of XML node with message data structure 
    :return: Empty dictionary corresponding to message structure read from XML. Keys are 'sql_column_names', 
    values are named tuples (read_from_robot, read_bytes, read_datatype, data_ordinal) 
    '''
    def return_whole_message_struct(self):

        common_data_dict = self.return_message_struct('common_logged_data')
        special_data_dict = self.return_message_struct(self.msg_struct_xml_node_name)
        result_data_dict = common_data_dict | special_data_dict

        i = 0
        for k, v in result_data_dict.items():
            result_data_dict[k] = v._replace(dataOrdinal=i)
            i += 1

        return result_data_dict

    @classmethod
    def return_message_struct(cls, node_name):
        tree = ET.parse('Resources/ur_data_structure.xml')
        result_dict = {}

        node = tree.find(node_name)
        for dataInfo in node:
            data_name = dataInfo.find('sql_column_name').text
            read_from_robot = int(dataInfo.find('read_from_robot').text)
            data_ordinal = int(dataInfo.find('data_ordinal').text)
            read_bytes = ''
            read_datatype = ''
            if read_from_robot == 1:
                read_bytes = dataInfo.find('read_bytes').text
                read_datatype = dataInfo.find('read_datatype').text

            DataStruct = namedtuple('DataStruct', 'readFromRobot readBytes readDatatype dataOrdinal')
            ds = DataStruct(read_from_robot, read_bytes, read_datatype, data_ordinal)
            result_dict[data_name] = ds
            result_dict = {k: v for k, v in sorted(result_dict.items(), key=lambda item: item[1].dataOrdinal)}

        return result_dict

    '''
    :return: Empty dictionary with data field names as keys and empty values.
    '''
    def return_decoded_message_dict(self):
        return {k: None for k in self.message_struct_dict.keys()}

    '''
    decode main part of the data in message - common fields and another which are read from robot
    :param data_buffer : binary data read from robot via TCP/IP connection
    :return : message dictionary with decoded common fields and those which are read from robot
    '''
    def decode_message(self, data_buffer):
        offset = 0
        tmp_msg_dict = {k: None for k in self.last_message_dict.keys()}

        # update common values which are not decoded from the robot
        tmp_msg_dict['date_time'] = str(datetime.datetime.now())

        # decode all values which are read from the robot
        for k, v in self.message_struct_dict.items():
            if v.readFromRobot == 1:
                # if the length of data is a variable
                if v.readBytes.startswith('var:'):
                    # field describing variable which store the length of data
                    var_length_name = v.readBytes[4:]
                    # if variable is a keyword ...
                    if var_length_name.startswith("#"):
                        match var_length_name:
                            case '#to_the_end':
                                data_length = int(tmp_msg_dict['message_size']) - offset
                            case _:
                                data_length = 0
                    # if variable is not a keyword it must be another (previous) value in the message
                    else:
                        data_length = int(tmp_msg_dict[var_length_name])

                    # decode next part of message
                    [tmp_msg_dict[k], offset] = get_char_array_as_string(data_buffer, offset, data_length)

                # if the length of data is constant
                else:
                    match v.readBytes:
                        case '1':
                            [tmp_msg_dict[k], offset] = get_1_byte_int_or_uint(v.readDatatype, data_buffer, offset)
                        case '4':
                            [tmp_msg_dict[k], offset] = get_4_bytes_int_or_uint(v.readDatatype, data_buffer, offset)
                        case '8':
                            [tmp_msg_dict[k], offset] = get_8_bytes_int_or_uint(v.readDatatype, data_buffer, offset)

        return tmp_msg_dict


class version_message_decoder(primary_client_message_decoder):

    def __init__(self):
        super().__init__('version_message')

    def decode_message(self, data_buffer):
        # get common message values and those which are read from robot
        tmp_msg_dict = super().decode_message(data_buffer)
        self.last_message_dict = tmp_msg_dict

        return self.last_message_dict


class key_message_decoder(primary_client_message_decoder):

    def __init__(self):
        super().__init__('key_message')

    def decode_message(self, data_buffer):
        # get common message values and those which are read from robot
        tmp_msg_dict = super().decode_message(data_buffer)
        self.last_message_dict = tmp_msg_dict

        return self.last_message_dict


class safety_mode_message_decoder(primary_client_message_decoder):

    safety_mode_types_dict = {1: 'NORMAL', 2: 'REDUCED', 3: 'PROTECTIVE_STOP', 4: 'RECOVERY',
                              5: 'SAFEGUARD_STOP', 6: 'SYSTEM_EMERGENCY_STOP', 7: 'ROBOT_EMERGENCY_STOP',
                              8: 'VIOLATION', 9: 'FAULT', 10: 'VALIDATE_JOINT_ID', 11: 'UNDEFINED'}

    def __init__(self):
        super().__init__('safety_message')

    def decode_message(self, data_buffer):
        # get common message values and those which are read from robot
        tmp_msg_dict = super().decode_message(data_buffer)

        # fill rest of specific values
        tmp_msg_dict['safety_mode_type_txt'] = self.safety_mode_types_dict[int(tmp_msg_dict['safety_mode_type'])]

        self.last_message_dict = tmp_msg_dict
        return self.last_message_dict


class robot_comm_message_decoder(primary_client_message_decoder):
    report_levels_dict = {0: 'DEBUG', 1: 'INFO', 2: 'WARNING', 3: 'VIOLATION', 4: 'FAULT',
                          128: 'DEVL_DEBUG', 129: 'DEVL_INFO', 130: 'DEVL_WARNING',
                          131: 'DEVL_VIOLATION', 132: 'DEVL_FAULT'}

    def __init__(self):
        super().__init__('communication_message')

    def decode_message(self, data_buffer):
        # get common message values and those which are read from robot
        tmp_msg_dict = super().decode_message(data_buffer)

        # fill specific data values
        tmp_msg_dict['report_level_txt'] = self.report_levels_dict[int(tmp_msg_dict['report_level'])]

        self.last_message_dict = tmp_msg_dict
        return self.last_message_dict


class runtime_exception_message_decoder(primary_client_message_decoder):

    def __init__(self):
        super().__init__('runtime_exception_message')

    def decode_message(self, data_buffer):
        # get common message values and those which are read from robot
        tmp_msg_dict = super().decode_message(data_buffer)
        self.last_message_dict = tmp_msg_dict

        return self.last_message_dict


class message_decoding_manager:
    last_decoded_messages_set = []

    ver_msg_decoder = version_message_decoder()
    key_msg_decoder = key_message_decoder()
    saf_msg_decoder = safety_mode_message_decoder()
    comm_msg_decoder = robot_comm_message_decoder()
    run_msg_except_decoder = runtime_exception_message_decoder()

    # Returns list of decoded messages
    def get_decoded_data(self, messages_list):

        self.last_decoded_messages_set.clear()

        i = 0
        while i < len(messages_list):

            if messages_list[i][0] == 3:
                temp_decoded_data = self.ver_msg_decoder.decode_message(messages_list[i][1])
            elif messages_list[i][0] == 7:
                temp_decoded_data = self.key_msg_decoder.decode_message(messages_list[i][1])
            elif messages_list[i][0] == 5:
                temp_decoded_data = self.saf_msg_decoder.decode_message(messages_list[i][1])
            elif messages_list[i][0] == 6:
                temp_decoded_data = self.comm_msg_decoder.decode_message(messages_list[i][1])
            elif messages_list[i][0] == 10:
                temp_decoded_data = self.run_msg_except_decoder.decode_message(messages_list[i][1])
            else:
                temp_decoded_data = []

            if messages_list[i][0] in (3, 7, 5, 6, 10):
                self.last_decoded_messages_set.append(temp_decoded_data)

            i += 1

        return self.last_decoded_messages_set
