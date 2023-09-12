import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.v_3b_main_toolbar import VMainToolbar
from lib.views.v_3a_main_content import VMainContent
from lib.views.components.base_view import BaseView

from lib.view_models.vm_1_main import VMMain

from lib.helpers.gui_tem_names import *


class VMain(BaseView):

    def __init__(self, parent=None):
        super(VMain, self).__init__(parent=parent)
        self.setObjectName(CUSTOM_VIEW_WIDGET_NAME)
        self._model = VMMain()

        self._main_layout = qtw.QGridLayout()
        self._main_layout.setObjectName(MAIN_GRID_LAYOUT_NAME)
        self.setLayout(self._main_layout)

        self._toolbar_scroll_area = self._produce_scroll_area(name = TOOLBAR_SCROLL_AREA_NAME
                                                              ,v_sbar_policy=qtc.Qt.ScrollBarAlwaysOff)
        self._toolbar_scroll_area.setWidget(VMainToolbar(self._model, parent=self))

        self._content_scroll_area = self._produce_scroll_area(name = CONTENT_SCROLL_AREA_NAME)
        self._content_scroll_area.setWidget(VMainContent(self._model, parent=self))

        self._main_layout.addWidget(self._toolbar_scroll_area, 0, 0)
        self._main_layout.addWidget(self._content_scroll_area, 1, 0)
        self._style_grid_layout()

        self._setup()
        self.show()

    def _bind_buttons_to_commands(self):
        pass

    def _init_actions(self):
        pass

    def _set_value_subscriptions(self):
        pass

    def _style_grid_layout(self):
        self._main_layout.setRowStretch(0, 0)
        self._main_layout.setRowStretch(1, 1)
        self._main_layout.setContentsMargins(0, 0, 0, 5)

    def _produce_scroll_area(self, name:str = None, v_sbar_policy = None, h_sbar_policy = None) -> qtw.QScrollArea:
        scroll_area = qtw.QScrollArea() 
        
        if name:
            scroll_area.setObjectName(name)
        if v_sbar_policy:   
            scroll_area.setVerticalScrollBarPolicy(v_sbar_policy)
        if h_sbar_policy:
            scroll_area.setHorizontalScrollBarPolicy(h_sbar_policy)

        scroll_area.setWidgetResizable(True)
        return scroll_area 


if __name__ == '__main__':
    from lib.helpers.visual_view_test_template import visual_test_preview
    visual_test_preview(VMain())