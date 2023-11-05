from lib.views.vw_6a_list_item import VwListItem
from lib.view_models.vm_4a_robot_connection import VmRobotConnection
from lib.models.factories.fmd_robot_connection import FmdRobotConnection
from lib.helpers.utils.hp_visual_view_test_template import visual_test_preview

if __name__ == '__main__':
    model_factory = FmdRobotConnection()
    model = VmRobotConnection(model_factory)
    view = VwListItem(model)
    # temporary add background color
    # in the entire app it must be transparent - it is controlled by the parent list widget
    view.setStyleSheet("background-color: #2f3b52;")
    visual_test_preview(view)