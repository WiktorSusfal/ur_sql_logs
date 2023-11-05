"""Contains class which produces robot connection model objects. 
Model production can be invoked by user action or by new database connection established.
Also provides methods for updating existing model's data (in database) and deleting the models."""

from PyQt5.QtCore import QObject, pyqtSignal
from threading import Lock

from lib.models.md_robot_connection import MdRobotConnection

from lib.helpers.database.hp_db_connection_manager import HpDBConnectionManager
from lib.helpers.constants.hp_indicators import HEALTH_OK, HEALTH_LOST
from lib.helpers.utils.hp_vm_utils import HpVmUtils


class FmdRobotConnection(QObject):
    """Class which produces robot connection model objects. 
    Model production can be invoked by user action or by new database connection established.
    Also provides methods for updating existing model's data (in database) and deleting the models."""

    robot_models_get = pyqtSignal(list)

    def __init__(self):
        super(FmdRobotConnection, self).__init__()
        self._last_db_health = HEALTH_LOST
        self._data_lock = Lock()

        self._robot_connection_models: list[MdRobotConnection] = list()

        HpDBConnectionManager.subscribe_to_health_status(self._get_robot_connection_models)

    def get_robot_model_by_id(self, robot_id: str) -> MdRobotConnection:
        s = HpDBConnectionManager.get_session()
        if s is not None:
            robot_model = s.query(MdRobotConnection).filter_by(id = robot_id).first()
            return robot_model
        
    def save_robot_model(self, model: MdRobotConnection):
        s = HpDBConnectionManager.get_session()
        if s is not None:

            if self._is_model_present(model):
                s.merge(model)
            else:
                s.add(model)
            s.commit()

            self._check_if_deletion(model)

    def _is_model_present(self, model: MdRobotConnection) -> bool:
        rm = self._get_robot_model_from_cache(model_id=model.id)
        return not rm is None

    def _get_robot_model_from_cache(self, model_id: str) -> MdRobotConnection:
        return next((model for model in  self._robot_connection_models if model.id == model_id), None)
    
    def _check_if_deletion(self, model: MdRobotConnection):
        with self._data_lock:
            if model.is_deleted == True:
                self._robot_connection_models.remove(model)

    @HpVmUtils.run_in_thread
    def _get_robot_connection_models(self, db_conn_status: int): 
        if not self._is_initial_connection(db_conn_status):
            return
        
        s = HpDBConnectionManager.get_session()
        if s is not None:
            robot_models = s.query(MdRobotConnection).filter_by(is_deleted = False).all()
            self._merge_models_data(robot_models)
            self.robot_models_get.emit(robot_models) 

    def _merge_models_data(self, models: list[MdRobotConnection]):
        with self._data_lock:
            for model in models:
                cached_model = self._get_robot_model_from_cache(model.id)
                
                if cached_model is None: 
                    self._robot_connection_models.append(model)
                    continue

                model_data = model.produce_data_struct()
                cached_model.update_data(model_data)

    def _is_initial_connection(self, current_status: int) -> bool:
        with self._data_lock:
            ldh = self._last_db_health
            self._last_db_health = current_status

            if ldh == HEALTH_LOST and current_status == HEALTH_OK:
                return True
            return False