import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from lib.views.main_toolbar_view import MainToolbarView
from lib.views.main_content_view import MainContentView

from lib.view_models.main_view_model import URMainViewModel

from lib.views.components.base_view import URLoggerBaseView
from lib.views.components.scroll_bar import CustomScrollBar

from lib.helpers.gui_tem_names import *


class URLoggerMainView(URLoggerBaseView):

    def __init__(self):
        super(URLoggerMainView, self).__init__()
        self._model = URMainViewModel()

        self._main_layout = qtw.QGridLayout()
        self._main_layout.setObjectName(MAIN_GRID_LAYOUT_NAME)
        self.setLayout(self._main_layout)

        self._toolbar_scroll_area = self._produce_scroll_area(name = TOOLBAR_SCROLL_AREA_NAME
                                                              ,v_sbar_policy=qtc.Qt.ScrollBarAlwaysOff)
        self._toolbar_scroll_area.setWidget(MainToolbarView(self._model))

        self._content_scroll_area = self._produce_scroll_area(name = CONTENT_SCROLL_AREA_NAME)
        self._content_scroll_area.setWidget(MainContentView(self._model))

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

    def _produce_scroll_area(self, name:str = None, v_sbar_policy = None, h_sbar_policy = None) -> qtw.QScrollArea:
        scroll_area = qtw.QScrollArea() 
        scroll_area.setVerticalScrollBar(CustomScrollBar())
        scroll_area.setHorizontalScrollBar(CustomScrollBar())
        
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
    visual_test_preview(URLoggerMainView())