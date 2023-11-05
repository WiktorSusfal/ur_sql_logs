"""Contains class which stores all view models referenced by views objects present in app.
For simplifying view model referencing."""

from lib.view_models.vm_1_main import VmMain
from lib.view_models.vm_4a_robot_connection import VmRobotConnection

class HpViewModelsManager:
    """Class which stores all view models referenced by views objects present in app.
    For simplifying view model referencing.""" 

    main_view_model: VmMain     = VmMain()
    db_config_view_model        = main_view_model.db_connection_vmodel
    app_home_view_model         = main_view_model.app_home_vmodel
    robot_details_view_model    = main_view_model.app_home_vmodel.robot_details