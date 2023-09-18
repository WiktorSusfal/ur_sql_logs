from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, Session

from threading import Thread, Lock
from time import time, sleep

from lib.helpers.hp_vm_utils import HpVmUtils
from lib.helpers.constants.hp_indicators import *

DATA_SAVE_INTERVAL = 6.0
HEALTH_CHECK_INTERVAL = 2.0
HEALTH_ERROR_THRESHOLD = 3


class HpDBConnectionManager:

    _connection_string: str = str()
    
    _engine: Engine = None
    _session_maker: sessionmaker = None
    _session_ok: bool = False
    
    _disconnect_flag = False

    _data_lock = Lock()
    _health_check_thread = Thread()
    _save_data_thread = Thread()
    _health_check_finished: bool = True
    _data_save_finished: bool = True 

    _session_health_callbacks = list()
    _worker_threads_status_callbacks = list()

    @classmethod
    @HpVmUtils.run_in_thread
    def subscribe_to_health_status(cls, func):
        with cls._data_lock:
            if func not in cls._session_health_callbacks:
                cls._session_health_callbacks.append(func)

    @classmethod
    @HpVmUtils.run_in_thread
    def subscribe_to_threads_status(cls, func):
        with cls._data_lock:
            if func not in cls._worker_threads_status_callbacks:
                cls._worker_threads_status_callbacks.append(func)

    @classmethod
    def _trigger_health_callbacks(cls, status: int):
        for func in cls._session_health_callbacks:
            func(status)

    @classmethod
    def _trigger_threads_status_callbacks(cls, status: int):
        for func in cls._worker_threads_status_callbacks:
            func(status)

    @classmethod
    def set_connection_string(cls, connection_string: str):
        cls._connection_string = connection_string
        cls._set_connection()

    @classmethod
    @HpVmUtils.run_in_thread
    def _set_connection(cls):
        with cls._data_lock:
            cls._engine = create_engine(cls._connection_string)
            cls._session_maker = sessionmaker(bind=cls._engine)

    @classmethod
    @HpVmUtils.run_in_thread
    def connect(cls):
        with cls._data_lock:
            if cls._data_save_finished and cls._health_check_finished:
                cls._start_worker_threads()

    @classmethod
    @HpVmUtils.run_in_thread
    def disconnect(cls):
        with cls._data_lock:
            if not cls._data_save_finished and not cls._health_check_finished:
                cls._disconnect_flag = True

    @classmethod
    def _get_session_maker(cls) -> sessionmaker:
        with cls._data_lock: 
            return cls._session_maker
    
    @classmethod
    def _get_session_status(cls) -> bool:
        with cls._data_lock:
            return cls._session_ok
    
    @classmethod
    def _get_disconnect_flag(cls) -> bool:
        with cls._data_lock:
            return cls._disconnect_flag
        
    @classmethod
    @HpVmUtils.run_in_thread
    def _start_worker_threads(cls):
        session_maker = cls._get_session_maker()

        cls._health_check_thread = Thread(target=cls._handle_health_check, args=(session_maker, ))
        cls._health_check_thread.start()

        cls._save_data_thread = Thread(target=cls._handle_data_save, args=(session_maker, ))
        cls._save_data_thread.start()

        cls._trigger_threads_status_callbacks(DB_THREADS_RUNNING)

    @classmethod
    def _handle_health_check(cls, session_maker: sessionmaker):
        with cls._data_lock:
            cls._health_check_finished = False

        conn_err_cnt = 0
        while True:
            conn_err_cnt = cls._check_connection_health(session_maker, conn_err_cnt)

            start_time = time()
            while time() - start_time < HEALTH_CHECK_INTERVAL:
                if conn_err_cnt > HEALTH_ERROR_THRESHOLD or cls._get_disconnect_flag():
                    with cls._data_lock:
                        cls._health_check_finished = True
                        cls._disconnect_flag = True
                        cls._session_ok = False
                    return cls._clear_disconnect_flag()
                
                sleep(0.2)

    @classmethod
    def _check_connection_health(cls, session_maker: sessionmaker, err_cnt: int) -> int: 
        try:
            with session_maker() as session:
                session.execute(text("SELECT 1"))     
            with cls._data_lock:
                cls._session_ok = True

            cls._trigger_health_callbacks(DB_CONNECTED)
        except Exception as e:
            with cls._data_lock:
                cls._session_ok = False

            cls._trigger_health_callbacks(DB_HAS_ERRORS)
            err_cnt += 1
        finally:
            return err_cnt

    @classmethod
    def _handle_data_save(cls, session: Session):
        with cls._data_lock:
            cls._data_save_finished = False

        while True: 
            if cls._get_session_status():
                cls._save_data()

            start_time = time()
            while time() - start_time < DATA_SAVE_INTERVAL:
                if cls._get_disconnect_flag():
                    with cls._data_lock:
                        cls._data_save_finished = True
                    return cls._clear_disconnect_flag()
            
                sleep(0.2)

    @classmethod
    def _save_data(cls):
        print('SAVING DO DATABASE')

    @classmethod
    @HpVmUtils.run_in_thread
    def _clear_disconnect_flag(cls):
        with cls._data_lock:
            if cls._data_save_finished and cls._health_check_finished:
                cls._disconnect_flag = False
        
        cls._trigger_health_callbacks(DB_DISCONNECTED)
        cls._trigger_threads_status_callbacks(DB_THREADS_FINISHED)

            
if __name__ == '__main__':
    hdcm = HpDBConnectionManager
    hdcm.set_connection_string('postgresql://{user}:{password}@{host}:345/{database}')
    import time
    time.sleep(1)