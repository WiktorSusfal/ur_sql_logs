from lib.models.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_indicators import *


class MDVersionMessage(MDBaseMessage):

    __tablename__ = VERSION_MSG_TABLE_NAME

    def __init__(self):
        pass