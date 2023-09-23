import os 

CURRENT_SCRIPT_PATH = os.path.realpath(os.path.dirname(__file__))

STYLES_REL_PATH = r'../../../resources/styles'
STYLES_CONFIG_PATH = os.path.normpath(os.path.join(CURRENT_SCRIPT_PATH, STYLES_REL_PATH))
STYLE_FILE_EXTENSION = '.qss'

ICONS_REL_PATH = r'../../../resources/icons'
ICONS_CONFIG_PATH = os.path.normpath(os.path.join(CURRENT_SCRIPT_PATH, ICONS_REL_PATH))

class HpResourcesManager:

    @classmethod
    def get_styles_code(cls) -> str:
        style_code = str()
        
        for file_name in os.listdir(STYLES_CONFIG_PATH):
            if file_name.endswith(STYLE_FILE_EXTENSION):
                file_full_path = os.path.join(STYLES_CONFIG_PATH, file_name)
                with open(file_full_path, 'r') as style_file:
                    style_code = '\n'.join([style_code, style_file.read()])

        return style_code
    
    @classmethod
    def get_icon_abs_path(cls, icon_rel_path: str) -> str:
        return os.path.join(ICONS_CONFIG_PATH, icon_rel_path)