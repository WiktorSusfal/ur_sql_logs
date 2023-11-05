import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.components.base_view import USLBaseView
from lib.views.vw_3b_main_toolbar import VwMainToolbar
from lib.views.vw_3a_main_content import VwMainContent

from lib.helpers.constants.hp_gui_tem_names import *


class VwMain(USLBaseView):

    def __init__(self, parent=None):
        super(VwMain, self).__init__(parent=parent)
        self.setObjectName(CUSTOM_VIEW_WIDGET_NAME)

        self._main_layout = qtw.QGridLayout()
        self._main_layout.setObjectName(MAIN_GRID_LAYOUT_NAME)
        self.setLayout(self._main_layout)

        self._toolbar_scroll_area = self._produce_scroll_area(name = TOOLBAR_SCROLL_AREA_NAME
                                                              ,v_sbar_policy=qtc.Qt.ScrollBarAlwaysOff)
        self._toolbar_scroll_area.setWidget(VwMainToolbar(parent=self))

        self._content_scroll_area = self._produce_scroll_area(name = CONTENT_SCROLL_AREA_NAME)
        self._content_scroll_area.setWidget(VwMainContent(parent=self))

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