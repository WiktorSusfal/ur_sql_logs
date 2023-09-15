import yaml
import os

CONN_CONFIG_FILENAME = 'db_connections.yml'

SCRIPT_PATH = os.path.realpath(os.path.dirname(__file__))
CONFIG_REL_PATH = r'../../config'
CONFIG_PATH = os.path.normpath(os.path.join(SCRIPT_PATH, CONFIG_REL_PATH, CONN_CONFIG_FILENAME))


class HpConnectionConfigData:

    _configs_cached: list[dict] = list()

    @classmethod
    def _get_connections_config(cls) -> list[dict]:
        config_content = str()
        with open(CONFIG_PATH, 'r') as cf:
            config_content = cf.read()

        configs_raw: dict = yaml.load(config_content, Loader=yaml.Loader)
        cls._configs_cached = configs_raw.get('db_connections', list())

        return cls._configs_cached
    
    @classmethod
    def _is_configs_cached(cls) -> bool:
        return len(cls._configs_cached) > 0
    
    @classmethod
    def get_db_connection_names(cls) -> list[str]:
        cnfgs = cls._configs_cached if cls._is_configs_cached() else cls._get_connections_config()
        
        return [f_name for f_name in 
                    [conn_data.get('friendly_name', None) for conn_data in cnfgs]
                if f_name ]
    
    @classmethod
    def get_db_connection_string(cls, connection_name: str, password: str) -> str:
        configs = cls._configs_cached if cls._is_configs_cached() else cls._get_connections_config()
        
        if not cls._is_configs_cached():
            raise Exception(f'Connection config file corrupted - no connections data')
        
        host, port, user, database = cls._get_db_connection_data(connection_name, configs)
        
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
    
    @classmethod
    def _get_db_connection_data(cls, connection_name:str, connections_data: list[dict]) -> tuple[str]:
        for conn_data in connections_data:
            if conn_data.get('friendly_name', str()) == connection_name:
                return  conn_data.get('host', str()), \
                        conn_data.get('port', str()), \
                        conn_data.get('user', str()), \
                        conn_data.get('database', str())
            
        raise Exception(f'Connection {connection_name} not present in connections config file')
        

if __name__ == '__main__':
    print(HpConnectionConfigData.get_db_connection_names())
    print(HpConnectionConfigData.get_db_connection_string('postgres_dev', 'abc'))