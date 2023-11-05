"""Contains class which produces robot connection model objects. 
Model production can be invoked by user action or by new database connection established.
Also provides methods for updating existing model's data (in database) and deleting the models."""

from PyQt5.QtCore import QObject, pyqtSignal
from threading import Lock
from dataclasses import dataclass

from lib.models.md_robot_connection import MdRobotConnection

from lib.helpers.database.hp_db_connection_manager import HpDBConnectionManager
from lib.helpers.constants.hp_indicators import HEALTH_OK
from lib.helpers.utils.hp_vm_utils import HpVmUtils


@dataclass
class MdRobotModelStatus:
    model: MdRobotConnection = None
    is_saved: bool = False


class FmdRobotConnection(QObject):
    """Class which produces robot connection model objects. 
    Model production can be invoked by user action or by new database connection established.
    Also provides methods for updating existing model's data (in database) and deleting the models."""

    robot_models_get = pyqtSignal(list)

    def __init__(self):
        super(FmdRobotConnection, self).__init__()
        self._data_lock = Lock()

        self._robot_connection_models: list[MdRobotModelStatus] = list()

        HpDBConnectionManager.subscribe_to_init_queries_status(self._get_robot_connection_models)

    def create_robot_model(self, model_id: str) -> MdRobotConnection:
        rm = self._get_robot_model_from_cache(model_id)
        if rm:
            return rm
        
        rm = MdRobotConnection(model_id)
        self._robot_connection_models.append(MdRobotModelStatus(model=rm, is_saved=False))
        return rm
    
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
            model_data = self._get_robot_model_data_from_cache(model.id)
            model_data.is_saved = True

            self._check_if_deletion(model)

    def _is_model_present(self, model: MdRobotConnection) -> bool:
        rd = self._get_robot_model_data_from_cache(model_id=model.id)
        
        if rd is None:
            return False
        return rd.is_saved

    def _get_robot_model_from_cache(self, model_id: str) -> MdRobotConnection:
        return next((data.model for data in  self._robot_connection_models if data.model.id == model_id), None)
    
    def _get_robot_model_data_from_cache(self, model_id: str) -> MdRobotModelStatus:
        return next((data for data in  self._robot_connection_models if data.model.id == model_id), None)
    
    def _check_if_deletion(self, model: MdRobotConnection):
        with self._data_lock:
            if model.is_deleted == True:
                model_data = self._get_robot_model_data_from_cache(model.id)
                self._robot_connection_models.remove(model_data)

    @HpVmUtils.run_in_thread
    def _get_robot_connection_models(self, db_status: int): 
        if db_status != HEALTH_OK:
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
                    self._robot_connection_models.append(MdRobotModelStatus(model=model, is_saved=False))
                    continue

                model_data = model.produce_data_struct()
                cached_model.update_data(model_data)