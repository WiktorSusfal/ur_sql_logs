from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, Session
from collections.abc import Callable

from lib.helpers.messages.hp_message_storage import HpMessageStorage
from lib.helpers.utils.looped_tasks.hp_looped_task_manager import HpLoopedTaskManager
from lib.helpers.utils.looped_tasks.hp_looped_task import HpLoopedTask
from lib.helpers.resources.hp_resources_manager import HpResourcesManager
from lib.helpers.constants.hp_indicators import *

DATA_SAVE_INTERVAL = 6.0
HEALTH_CHECK_INTERVAL = 2.0
HEALTH_ERROR_THRESHOLD = 3


class HpDBConnectionManager:

    _connection_string: str = str()
    
    _engine: Engine = None
    _session_maker: sessionmaker = None
    _session: Session = None

    _ltm: HpLoopedTaskManager = None

    _check_health_task_name = 'check_health'
    _init_execute_task_name = 'init_execute'
    _save_msg_task_name = 'save_msgs'

    @classmethod
    def get_session(cls) -> Session:
        return cls._session

    @classmethod
    def subscribe_to_health_status(cls, func: Callable[[int], None]):
        if not cls._ltm:
            cls._set_task_manager()
        cls._ltm.subscribe_to_health_status(cls._check_health_task_name, func)

    @classmethod
    def subscribe_to_threads_status(cls, func: Callable[[int], None]):
        if not cls._ltm:
            cls._set_task_manager()
        cls._ltm.subscribe_to_process_status(cls._save_msg_task_name, func)

    @classmethod
    def set_connection_string(cls, connection_string: str):
        cls._connection_string = connection_string
        cls._set_connection()

    @classmethod
    def _set_connection(cls):
        cls._engine = create_engine(cls._connection_string)
        cls._session_maker = sessionmaker(bind=cls._engine)
        cls._set_session()

    @classmethod
    def _set_session(cls):
        if cls._session:
            cls._session.close()
        cls._session: Session = cls._session_maker()
        cls._session.expire_on_commit = False

    @classmethod
    def _reset_session(cls):
        if cls._session:
            cls._session.close()
        cls._session = None

    @classmethod
    def _set_task_manager(cls):
        health_task = HpLoopedTask(cls._check_health_task_name
                                   , cls._check_connection_health
                                   , interval=HEALTH_CHECK_INTERVAL
                                   , max_errors=HEALTH_ERROR_THRESHOLD)
        init_task = HpLoopedTask(cls._init_execute_task_name,cls._execute_init_queries, interval=None)
        save_task = HpLoopedTask(cls._save_msg_task_name, cls._save_robot_msgs, interval=DATA_SAVE_INTERVAL)

        cls._ltm = HpLoopedTaskManager()
        cls._ltm.register_task(health_task)
        cls._ltm.register_task(init_task)
        cls._ltm.register_task(save_task)

        cls._ltm.set_task_execution_dependency(cls._check_health_task_name, cls._init_execute_task_name)
        cls._ltm.set_task_execution_dependency(cls._init_execute_task_name, cls._save_msg_task_name)
        
        cls._ltm.set_task_status_dependency(cls._check_health_task_name, cls._init_execute_task_name)
        cls._ltm.set_task_status_dependency(cls._check_health_task_name, cls._save_msg_task_name)

    @classmethod
    def connect(cls):
        if not cls._ltm:
            cls._set_task_manager()
        
        cls._ltm.start_process()

    @classmethod
    def disconnect(cls):
        cls._ltm.abort_process()
        cls._reset_session()

    @classmethod
    def _check_connection_health(cls) -> bool: 
        try:
            with cls._session_maker() as session:
                s: Session = session
                s.execute(text("SELECT 1"))     
            return True
        except Exception as e:
            return False
        
    @classmethod
    def _execute_init_queries(cls) -> bool:
        try:
            with cls._session_maker() as session:
                s: Session = session
                for query in HpResourcesManager.get_init_queries():
                        s.execute(text(query))
                        s.commit()
            
            return True
        except:
            return False

    @classmethod
    def _save_robot_msgs(cls) -> bool:
        err_flag = False

        messages = HpMessageStorage.get_save_staged()
        with cls._session_maker() as session:
            s: Session = session
            for msg in messages:
                try:
                    s.add(msg)
                    s.commit()
                except:
                    err_flag = True
                    continue
        
        return not err_flag