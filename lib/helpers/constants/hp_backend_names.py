DATABASE_NAME = 'URLogData'
SCHEMA_NAME = 'usl'

VERSION_MSG_TABLE_NAME = 'version_message'
KEY_MSG_TABLE_NAME = 'key_message'
SAFETY_MSG_TABLE_NAME = 'safety_message'
COMM_MSG_TABLE_NAME = 'communication_message'
RUN_EXP_MSG_TABLE_NAME = 'runtime_exceptions_message'
ROBOT_INFO_TABLE_NAME = 'robot_info'

SEQUENCE_NAME = 'message_sequence'

ROBOT_PK_COLUMN_NAME = 'id'
MSG_FOREIGN_KEY_COLUMN_NAME = 'robot_id'

DEFAULT_NAME = "ur_connection"
DEFAULT_IP = '0.0.0.0'
DEFAULT_PORT = 0
DEFAULT_READ_FREQ = 0