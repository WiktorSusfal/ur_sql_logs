from lib.view_models.vm_1_main import VmMain
from lib.view_models.vm_4_robot_connection import VmRobotConnection

class HpViewModelsManager: 

    main_view_model: VmMain     = VmMain()
    db_config_view_model        = main_view_model.db_connection_vmodel
    app_home_view_model         = main_view_model.app_home_vmodel
    robot_details_view_model    = main_view_model.app_home_vmodel.robot_details
