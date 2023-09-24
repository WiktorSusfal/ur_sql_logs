from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, Session
from collections.abc import Callable

from lib.helpers.hp_looped_task_manager import HpLoopedTaskManager
from lib.helpers.constants.hp_indicators import *

DATA_SAVE_INTERVAL = 6.0
HEALTH_CHECK_INTERVAL = 2.0
HEALTH_ERROR_THRESHOLD = 3


class HpDBConnectionManager:

    _connection_string: str = str()
    
    _engine: Engine = None
    _session_maker: sessionmaker = None

    _ltm = None

    @classmethod
    def subscribe_to_health_status(cls, func: Callable[[int], None]):
        if not cls._ltm:
            cls._set_task_manager()
        cls._ltm.subscribe_to_health_status(func)

    @classmethod
    def subscribe_to_threads_status(cls, func: Callable[[int], None]):
        if not cls._ltm:
            cls._set_task_manager()
        cls._ltm.subscribe_to_process_status(func)

    @classmethod
    def set_connection_string(cls, connection_string: str):
        cls._connection_string = connection_string
        cls._set_connection()

    @classmethod
    def _set_connection(cls):
        cls._engine = create_engine(cls._connection_string)
        cls._session_maker = sessionmaker(bind=cls._engine)
        cls._set_task_manager_arguments()

    @classmethod
    def _set_task_manager(cls):
        cls._ltm = HpLoopedTaskManager(
            main_task=cls._save_data
            ,main_interval=DATA_SAVE_INTERVAL
            ,health_check=cls._check_connection_health
            ,health_interval=HEALTH_CHECK_INTERVAL
            ,max_health_errors=HEALTH_ERROR_THRESHOLD
        )
        cls._set_task_manager_arguments()

    @classmethod
    def _set_task_manager_arguments(cls):
        current_session_maker = cls._session_maker
        args = (current_session_maker, )
        cls._ltm.set_arguments(main_args=args, health_args=args)

    @classmethod
    def connect(cls):
        cls._ltm.start_process()

    @classmethod
    def disconnect(cls):
        cls._ltm.abort_process()

    @classmethod
    def _check_connection_health(cls, session_maker: sessionmaker) -> bool: 
        try:
            with session_maker() as session:
                session.execute(text("SELECT 1"))     
            return True
        except Exception as e:
            return False

    @classmethod
    def _save_data(cls, session_maker: sessionmaker) -> bool:
        print('SAVING DO DATABASE')
        return True

            
if __name__ == '__main__':
    from time import time
    hdcm = HpDBConnectionManager
    hdcm.set_connection_string('postgresql://{user}:{password}@{host}:345/{database}')
    import time
    time.sleep(1)