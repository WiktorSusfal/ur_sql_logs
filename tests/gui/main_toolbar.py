from lib.views.vw_3b_main_toolbar import VwMainToolbar
from lib.helpers.utils.hp_visual_view_test_template import visual_test_preview

if __name__ == '__main__':
    view = VwMainToolbar()
    # temporary add background color
    # in the entire app it must be transparent - it is controlled by the parent widget
    view.setStyleSheet("background-color: #2f3b52;")
    visual_test_preview(view)