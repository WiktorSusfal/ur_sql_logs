import struct
import datetime
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

    last_primary_client_messages = []

    def __init__(self, pr_cl_msg_cd=20):
        self.primary_client_messages_code = pr_cl_msg_cd

    def return_primary_client_messages(self, data_buffer):

        offset = 0
        self.last_primary_client_messages = []

        while offset < len(data_buffer):

            main_package_length = struct.unpack('!I', data_buffer[offset:offset+4])[0]
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

    last_message_decoded = []

    def __init__(self, msg_sz=0, msg_tp=20, tsp=0, dt_txt='', sr=0, r_msg_tp=-1, r_msg_tp_txt=''):
        self.message_size = msg_sz
        self.message_type = msg_tp
        self.timestamp = tsp  # This is not world time. It is time elapsed from robot controller power-up.
        self.date_time_text = dt_txt
        self.source = sr
        self.robot_message_type = r_msg_tp
        self.robot_message_type_txt = r_msg_tp_txt

    @abstractmethod
    def decode_message(self, data_buffer):
        pass

    @abstractmethod
    def fill_last_message_decoded(self):
        pass

    def fill_last_message_decoded(self):

        self.date_time_text = str(datetime.datetime.now())

        # get list of object attributes names
        attr_list = list(self.__dict__.keys())

        # fill the 'last_message_decoded' variable list
        for i in attr_list:
            self.last_message_decoded.append(self.__getattribute__(i))


class version_message_decoder(primary_client_message_decoder):

    last_message_decoded = []

    def __init__(self, pr_ns=0, pr_n='', ma_ver='', mi_ver='', bg_ver=0, bl_no=0, bl_dt=''):
        super().__init__(0, 20, 0, '', 0, 3, 'Version Message')
        self.project_name_size = pr_ns
        self.project_name = pr_n
        self.major_version = ma_ver
        self.minor_version = mi_ver
        self.bugfix_version = bg_ver
        self.build_number = bl_no
        self.build_date = bl_dt

    def decode_message(self, data_buffer):
        offset = 0
        self.last_message_decoded.clear()

        [self.message_size, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)

        # The next value is 'message type' which is static for this message.
        offset += 1

        [self.timestamp, offset] = get_8_bytes_int_or_uint('!Q', data_buffer, offset)
        [self.source, offset] = get_1_byte_int_or_uint('!b', data_buffer, offset)

        # The next value is 'robot message type' which is static for this message.
        offset += 1

        [self.project_name_size, offset] = get_1_byte_int_or_uint('!b', data_buffer, offset)
        [self.project_name, offset] = get_char_array_as_string(data_buffer, offset, self.project_name_size)
        [self.major_version, offset] = get_1_byte_int_or_uint('!B', data_buffer, offset)
        [self.minor_version, offset] = get_1_byte_int_or_uint('!B', data_buffer, offset)
        [self.bugfix_version, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)
        [self.build_number, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)
        [self.build_date, offset] = get_char_array_as_string(data_buffer, offset, (self.message_size - offset))

        self.fill_last_message_decoded()

        return self.last_message_decoded


class key_message_decoder(primary_client_message_decoder):

    last_message_decoded = []

    def __init__(self, msc_c=-1, msg_arg=-1, msg_ttl_s=-1, msg_ttl='', txt_msg=''):
        super().__init__(0, 20, 0, '', 0, 7, 'Key Message')

        self.robot_message_code = msc_c
        self.robot_message_argument = msg_arg
        self.robot_message_title_size = msg_ttl_s
        self.robot_message_title = msg_ttl
        self.key_text_message = txt_msg

    def decode_message(self, data_buffer):
        offset = 0
        self.last_message_decoded.clear()

        [self.message_size, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)

        # The next value is 'message type' which is static for this message.
        offset += 1

        [self.timestamp, offset] = get_8_bytes_int_or_uint('!Q', data_buffer, offset)
        [self.source, offset] = get_1_byte_int_or_uint('b', data_buffer, offset)

        # The next value is 'robot message type' which is static for this message.
        offset += 1

        [self.robot_message_code, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)
        [self.robot_message_argument, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)
        [self.robot_message_title_size, offset] = get_1_byte_int_or_uint('!B', data_buffer, offset)
        [self.robot_message_title, offset] = get_char_array_as_string(data_buffer, offset,
                                                                      self.robot_message_title_size)
        [self.key_text_message, offset] = get_char_array_as_string(data_buffer, offset, (self.message_size - offset))

        self.fill_last_message_decoded()

        return self.last_message_decoded


class safety_mode_message_decoder(primary_client_message_decoder):

    last_message_decoded = []
    safety_mode_types_dict = {1: 'NORMAL', 2: 'REDUCED', 3: 'PROTECTIVE_STOP', 4: 'RECOVERY',
                              5: 'SAFEGUARD_STOP', 6: 'SYSTEM_EMERGENCY_STOP', 7: 'ROBOT_EMERGENCY_STOP',
                              8: 'VIOLATION', 9: 'FAULT', 10: 'VALIDATE_JOINT_ID', 11: 'UNDEFINED'}


    def __init__(self, msg_c=-1, msg_arg=-1, sf_md_tp=-1, sf_md_tp_txt='', r_data_tp=0, r_data=0):
        super().__init__(0, 20, 0, '', 0, 5, 'Safety Mode Message')

        self.robot_message_code = msg_c
        self.robot_message_argument = msg_arg
        self.safety_mode_type = sf_md_tp
        self.safety_mode_type_txt = sf_md_tp_txt
        self.report_data_type = r_data_tp
        self.report_data = r_data

    def decode_message(self, data_buffer):
        offset = 0
        self.last_message_decoded.clear()

        [self.message_size, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)

        # Next Value - message type - static for this message
        offset += 1

        [self.timestamp, offset] = get_8_bytes_int_or_uint('!Q', data_buffer, offset)
        [self.source, offset] = get_1_byte_int_or_uint('!b', data_buffer, offset)

        # Next Value - robot message type - static for this message
        offset += 1

        [self.robot_message_code, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)
        [self.robot_message_argument, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)
        [self.safety_mode_type, offset] = get_1_byte_int_or_uint('!B', data_buffer, offset)
        [self.report_data_type, offset] = get_4_bytes_int_or_uint('!I', data_buffer, offset)
        [self.report_data, offset] = get_4_bytes_int_or_uint('!I', data_buffer, offset)

        self.safety_mode_type_txt = self.safety_mode_types_dict[self.safety_mode_type]
        self.fill_last_message_decoded()

        return self.last_message_decoded


class robot_comm_message_decoder(primary_client_message_decoder):

    last_message_decoded = []
    report_levels_dict = {0: 'DEBUG', 1: 'INFO', 2: 'WARNING', 3: 'VIOLATION', 4: 'FAULT',
                          128: 'DEVL_DEBUG', 129: 'DEVL_INFO', 130: 'DEVL_WARNING',
                          131: 'DEVL_VIOLATION', 132: 'DEVL_FAULT'}

    def __init__(self, msg_c=-1, msg_arg=-1, rep_lvl=-1, rep_lvl_txt='', msg_data_tp=0, msg_data=0, c_txt_msg=''):
        super().__init__(0, 20, 0, '', 0, 6, 'Robot Comm Message')

        self.robot_message_code = msg_c
        self.robot_message_argument = msg_arg
        self.report_level = rep_lvl
        self.report_level_txt = rep_lvl_txt
        self.robot_message_data_type = msg_data_tp
        self.robot_message_data = msg_data
        self.robot_comm_text_message = c_txt_msg


    def decode_message(self, data_buffer):
        offset = 0
        self.last_message_decoded.clear()

        [self.message_size, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)

        # Next value - message type - is static for this message
        offset += 1

        [self.timestamp, offset] = get_8_bytes_int_or_uint('!Q', data_buffer, offset)
        [self.source, offset] = get_1_byte_int_or_uint('!b', data_buffer, offset)

        # Next Value - robot message type - is static for this message
        offset += 1

        [self.robot_message_code, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)
        [self.robot_message_argument, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)
        [self.report_level, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)
        [self.robot_message_data_type, offset] = get_4_bytes_int_or_uint('!I', data_buffer, offset)
        [self.robot_message_data, offset] = get_4_bytes_int_or_uint('!I', data_buffer, offset)
        [self.robot_comm_text_message, offset] = get_char_array_as_string(data_buffer, offset,
                                                                          (self.message_size - offset))

        self.report_level_txt = self.report_levels_dict[self.report_level]
        self.fill_last_message_decoded()

        return self.last_message_decoded


class runtime_exception_message_decoder(primary_client_message_decoder):

    last_message_decoded = []

    def __init__(self, sc_ln_no=-1, sc_col_no=-1, rt_ec_txt_msg=''):
        super().__init__(0, 20, 0, '', 0, 10, 'Runtime Exception Message')

        self.script_line_no = sc_ln_no
        self.script_column_no = sc_col_no
        self.runtime_exception_text_message = rt_ec_txt_msg

    def decode_message(self, data_buffer):
        offset = 0
        self.last_message_decoded.clear()

        [self.message_size, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)

        # Next value - message type - is static for that message
        offset += 1

        [self.timestamp, offset] = get_8_bytes_int_or_uint('!Q', data_buffer, offset)
        [self.source, offset] = get_1_byte_int_or_uint('!b', data_buffer, offset)

        # Next value - robot message type is static for this message
        offset += 1

        [self.script_line_no, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)
        [self.script_column_no, offset] = get_4_bytes_int_or_uint('!i', data_buffer, offset)
        [self.runtime_exception_text_message, offset] = get_char_array_as_string(data_buffer, offset,
                                                                                 (self.message_size - offset))

        self.fill_last_message_decoded()

        return self.last_message_decoded


"""
class popup_message (primary_client_message_decoder):

    last_message_decoded = []

    robot_message_type = 2
    robot_message_type_txt = 'Popup Message'

    def __init__(self):
        super().__init__()

        self.requestId = 0
        self.request_type = 0
        self.warning = False
        self.error = False
        self.blocking = False
        self.message_title_size = 0
        self.message_title = ''
        self.popup_text_message = ''
"""


class message_decoding_manager:
    last_decoded_messages_set = []

    ver_msg_decoder = version_message_decoder(0, '', '', '', 0, 0, '')
    key_msg_decoder = key_message_decoder(-1, -1, -1, '', '')
    saf_msg_decoder = safety_mode_message_decoder(-1, -1, -1, '', 0, 0)
    comm_msg_decoder = robot_comm_message_decoder(-1, -1, -1, '', 0, 0, '')
    run_msg_except_decoder = runtime_exception_message_decoder(-1, -1, '')

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
