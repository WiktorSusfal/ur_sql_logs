from sqlalchemy import Column, String

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_backend_names import *

SAFETY_MODE_TYPES_DICT = {
                            1: 'NORMAL'
                          , 2: 'REDUCED'
                          , 3: 'PROTECTIVE_STOP'
                          , 4: 'RECOVERY'
                          , 5: 'SAFEGUARD_STOP'
                          , 6: 'SYSTEM_EMERGENCY_STOP'
                          , 7: 'ROBOT_EMERGENCY_STOP'
                          , 8: 'VIOLATION'
                          , 9: 'FAULT'
                          , 10: 'VALIDATE_JOINT_ID'
                          , 11: 'UNDEFINED'
                        }


class MDSafetyMessage(MDBaseMessage):

    __tablename__ = SAFETY_MSG_TABLE_NAME

    code = Column(String)
    argument = Column(String)
    safety_mode_type = Column(String)
    safety_mode_name = Column(String)
    report_data_type = Column(String)
    report_data = Column(String)

    def __init__(self):
        pass