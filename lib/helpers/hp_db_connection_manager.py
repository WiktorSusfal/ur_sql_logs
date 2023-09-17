from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from threading import Thread, Lock
from time import time, sleep

from lib.helpers.hp_vm_utils import HpVmUtils


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
    def disconnect(cls):
        if cls._save_data_thread.is_alive():
            cls._disconnect_flag = True

    @classmethod
    def _get_session_maker(cls) -> sessionmaker:
        with cls._data_lock: 
            session_maker = cls._session_maker
        return session_maker
    
    @classmethod
    def _get_session_status(cls) -> bool:
        with cls._data_lock:
            session_ok = cls._session_ok
        return session_ok
    
    @classmethod
    def _get_disconnect_flag(cls) -> bool:
        with cls._data_lock:
            flag = cls._disconnect_flag
        return flag
        
    @classmethod
    @HpVmUtils.run_in_thread
    def _start_worker_threads(cls):
        session_maker = cls._get_session_maker()

        cls._health_check_thread = Thread(target=cls._handle_health_check, args=(session_maker, ))
        cls._health_check_thread.start()

        cls._save_data_thread = Thread(target=cls._handle_data_save, args=(session_maker, ))
        cls._save_data_thread.start()

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
                session.execute("SELECT 1")     
            with cls._data_lock:
                cls._session_ok = True
        except Exception as e:
            with cls._data_lock:
                cls._session_ok = False
                return err_cnt + 1
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
    def _clear_disconnect_flag(cls):
        with cls._data_lock:
            if cls._data_save_finished and cls._health_check_finished:
                cls._disconnect_flag = False

            
if __name__ == '__main__':
    hdcm = HpDBConnectionManager
    hdcm.set_connection_string('postgresql://{user}:{password}@{host}:345/{database}')
    import time
    time.sleep(1)