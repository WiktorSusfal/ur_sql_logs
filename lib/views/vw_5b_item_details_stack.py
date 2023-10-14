import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.components.base_view import USLBaseView
from lib.views.vw_6b_item_details import VwItemDetails
from lib.views.vw_6c_item_details_placeholder import VwItemDetailsPlaceholder

from lib.helpers.resources.hp_view_models_manager import HpViewModelsManager
from lib.helpers.constants.hp_gui_tem_names import *
from lib.helpers.constants.hp_indicators import *


class VwItemDetailsStack(USLBaseView):
    
    def __init__(self, parent=None):
        super(VwItemDetailsStack, self).__init__(parent=parent)
        self.setObjectName(UR_ITEM_DETAILS_STACK_VIEW_NAME)
        self._model = HpViewModelsManager.robot_details_view_model

        self._details_widget = VwItemDetails(parent=self)
        self._placeholder_widget = VwItemDetailsPlaceholder(parent=self)

        self._widget_manager = qtw.QStackedWidget()
        self._widget_manager.addWidget(self._placeholder_widget)
        self._widget_manager.addWidget(self._details_widget)
        
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self._widget_manager)
        self.setLayout(main_layout)

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        pass
    
    def _init_actions(self):
        pass
    
    def _set_value_subscriptions(self):
        self._model.model_empty.connect(self.set_current_widget)
    
    def set_current_widget(self, model_empty: bool):
        self._widget_manager.setCurrentIndex(int(not model_empty))