import os 
from typing import Generator

from lib.helpers.constants.hp_backend_names import *

CURRENT_SCRIPT_PATH = os.path.realpath(os.path.dirname(__file__))

STYLES_REL_PATH = r'../../../resources/styles'
STYLES_CONFIG_PATH = os.path.normpath(os.path.join(CURRENT_SCRIPT_PATH, STYLES_REL_PATH))
STYLE_FILE_EXTENSION = '.qss'

ICONS_REL_PATH = r'../../../resources/icons'
ICONS_CONFIG_PATH = os.path.normpath(os.path.join(CURRENT_SCRIPT_PATH, ICONS_REL_PATH))

QUERIES_REL_PATH = r'../../../resources/queries'
QUERIES_CONFIG_PATH = os.path.normpath(os.path.join(CURRENT_SCRIPT_PATH, QUERIES_REL_PATH))
QUERY_FILE_EXTENSION = '.sql'


class HpResourcesManager:

    @classmethod
    def get_styles_code(cls) -> str:
        style_code = str()
        
        for file_name in os.listdir(STYLES_CONFIG_PATH):
            if file_name.endswith(STYLE_FILE_EXTENSION):
                file_full_path = os.path.join(STYLES_CONFIG_PATH, file_name)
                with open(file_full_path, 'r') as style_file:
                    style_code = '\n'.join([style_code, style_file.read()])

        return style_code
    
    @classmethod
    def get_icon_abs_path(cls, icon_rel_path: str) -> str:
        return os.path.join(ICONS_CONFIG_PATH, icon_rel_path)
    
    @classmethod
    def get_init_queries(cls) -> Generator[str, None, None]:
        for file_name in os.listdir(QUERIES_CONFIG_PATH):
            if file_name.endswith(QUERY_FILE_EXTENSION):
                file_full_path = os.path.join(QUERIES_CONFIG_PATH, file_name)
                
                with open(file_full_path, 'r') as query_file:
                    query = query_file.read()

                yield query.format(database_name=DATABASE_NAME
                                   , schema_name=SCHEMA_NAME
                                   , sequence_name=SEQUENCE_NAME
                                   , version_msg_table_name=VERSION_MSG_TABLE_NAME
                                   , safety_msg_table_name=SAFETY_MSG_TABLE_NAME
                                   , run_exp_msg_table_name=RUN_EXP_MSG_TABLE_NAME
                                   , key_msg_table_name=KEY_MSG_TABLE_NAME
                                   , comm_msg_table_name=COMM_MSG_TABLE_NAME
                                   , robot_info_table_name=ROBOT_INFO_TABLE_NAME
                                   , msg_foreign_key_column_name=MSG_FOREIGN_KEY_COLUMN_NAME
                                   , robot_pk_column_name=ROBOT_PK_COLUMN_NAME)