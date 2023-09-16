from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from threading import Thread, Lock

from lib.helpers.hp_vm_utils import HpVmUtils


DB_POOL_INTERVAL = 6.0
CONNECTION_ERROR_THRESHOLD = 3


class HpDBConnectionManager:

    _connection_string: str = str()
    
    _engine: Engine = None
    _session: Session = None
    _conn_err_cnt: int = 0

    _connection_status = False
    _disconnect_flag = False

    _data_lock = Lock()
    _worker_thread = Thread()

    @classmethod
    def set_connection_string(cls, connection_string):
        cls._connection_string = connection_string
        cls._set_connection()

    @classmethod
    def connect(cls):
        if not cls._worker_thread.is_alive():
            cls._start_worker_thread()

    @classmethod
    def disconnect(cls):
        if cls._worker_thread.is_alive():
            cls._disconnect_flag = True

    @classmethod
    @HpVmUtils.run_in_thread
    def _set_connection(cls):
        with cls._data_lock:
            cls._engine = create_engine(cls._connection_string)
            cls._session = sessionmaker(bind=cls._engine)
            cls._conn_err_cnt = 0

    @classmethod
    def _get_session(cls) -> Session:
        with cls._data_lock: 
            session = cls._session
        return session
        
    @classmethod
    @HpVmUtils.run_in_thread
    def _start_worker_thread(cls):
        session = cls._get_session()
        cls._worker_thread = Thread(target=cls._handle_db_connection, args=(session, ))
        cls._worker_thread.start()

    @classmethod
    def _handle_db_connection(cls, session: Session):
        pass

    @classmethod
    def _connection_check(cls):
        pass


if __name__ == '__main__':
    hdcm = HpDBConnectionManager
    hdcm.set_connection_string('postgresql://{user}:{password}@{host}:345/{database}')
    import time
    time.sleep(1)