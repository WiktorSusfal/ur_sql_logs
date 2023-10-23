from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, Session
from collections.abc import Callable

from lib.models.md_robot_connection import MdRobotConnection

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

    _ltm: HpLoopedTaskManager = None

    _check_health_task_name = 'check_health'
    _init_execute_task_name = 'init_execute'
    _get_models_task_name = 'get_robot_models'
    _save_msg_task_name = 'save_msgs'

    _robot_models_get_callbacks: list[ Callable[[list[MdRobotConnection]], None] ] = list()

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
    def subscribe_to_robot_models_get(cls, func: Callable[[list[MdRobotConnection]], None]):
        if func not in cls._robot_models_get_callbacks:
            cls._robot_models_get_callbacks.append(func)

    @classmethod
    def _trigger_robot_models_get(cls, models_list: list[MdRobotConnection]):
        for func in cls._robot_models_get_callbacks:
            func(models_list)

    @classmethod
    def set_connection_string(cls, connection_string: str):
        cls._connection_string = connection_string
        cls._set_connection()

    @classmethod
    def _set_connection(cls):
        cls._engine = create_engine(cls._connection_string)
        cls._session_maker = sessionmaker(bind=cls._engine)

    @classmethod
    def _set_task_manager(cls):
        health_task = HpLoopedTask(cls._check_health_task_name
                                   , cls._check_connection_health
                                   , interval=HEALTH_CHECK_INTERVAL
                                   , max_errors=HEALTH_ERROR_THRESHOLD)
        init_task = HpLoopedTask(cls._init_execute_task_name,cls._execute_init_queries, interval=None)
        get_models_task = HpLoopedTask(cls._get_models_task_name,cls._get_robot_models, interval=None)
        save_task = HpLoopedTask(cls._save_msg_task_name, cls._save_robot_msgs, interval=DATA_SAVE_INTERVAL)

        cls._ltm = HpLoopedTaskManager()
        cls._ltm.register_task(health_task)
        cls._ltm.register_task(init_task)
        cls._ltm.register_task(get_models_task)
        cls._ltm.register_task(save_task)

        cls._ltm.set_task_execution_dependency(cls._check_health_task_name, cls._init_execute_task_name)
        cls._ltm.set_task_execution_dependency(cls._init_execute_task_name, cls._get_models_task_name)
        cls._ltm.set_task_execution_dependency(cls._get_models_task_name, cls._save_msg_task_name)
        
        cls._ltm.set_task_status_dependency(cls._check_health_task_name, cls._init_execute_task_name)
        cls._ltm.set_task_status_dependency(cls._init_execute_task_name, cls._get_models_task_name)
        cls._ltm.set_task_status_dependency(cls._check_health_task_name, cls._save_msg_task_name)

    @classmethod
    def connect(cls):
        if not cls._ltm:
            cls._set_task_manager()
        
        cls._ltm.start_process()

    @classmethod
    def disconnect(cls):
        cls._ltm.abort_process()

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
    def _get_robot_models(cls) -> bool:
        try:
            with cls._session_maker() as session:
                s: Session = session
                robot_models = s.query(MdRobotConnection).filter_by(is_deleted = False).all()
                s.expunge_all()
                cls._trigger_robot_models_get(robot_models)    
            return True
        except Exception as e:
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
    
    @classmethod
    def save_robot_model(cls, model) -> bool:
        err_flag = False 
        try:
            with cls._session_maker() as session:
                s: Session = session
                s.expire_on_commit = False
                s.add(model)
                s.commit()
        except:
            err_flag = True

        return not err_flag
    
    @classmethod
    def get_robot_model_by_id(cls, robot_id: str) -> MdRobotConnection:
        try:
            with cls._session_maker() as session:
                s: Session = session
                robot_model = s.query(MdRobotConnection).filter_by(id = robot_id).first()
                s.expunge(robot_model)
                return robot_model
        except Exception as e:
            return None

            
if __name__ == '__main__':
    from time import time, sleep
    
    hdcm = HpDBConnectionManager
    hdcm.set_connection_string(f'postgresql://ur_logger:ur_logger_password@127.0.0.1:5432/UR_LOG_DATA')

    from lib.models.log_messages.md_comm_message import MDCommMessage
    cm = MDCommMessage(bytes, str(), None)
    from lib.models.md_robot_connection import MdRobotConnection
    rc = MdRobotConnection('abc')
    from lib.models.log_messages.md_key_message import MDKeyMessage
    from lib.models.log_messages.md_base_message import Base
    km = MDKeyMessage(bytes(), str(), None)
    #Base.metadata.create_all(hdcm._engine)

    hdcm.connect()
    sleep(1)
    hdcm.disconnect()