from sqlalchemy import Column, String, Integer

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_backend_names import *


class MDVersionMessage(MDBaseMessage):

    __tablename__ = VERSION_MSG_TABLE_NAME

    project_name = Column(String)
    major_version = Column(String)
    minor_version = Column(String)
    bugfix_version = Column(String)
    build_number = Column(String)
    build_date = Column(String)

    def __init__(self):
        pass