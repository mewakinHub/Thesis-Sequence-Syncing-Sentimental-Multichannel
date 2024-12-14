import os
import yaml

class AppSettings:
    @staticmethod
    def get_settings():
        with open('configs/client_config.yaml', 'r') as file:
            client_config = yaml.safe_load(file)
        
        with open('configs/dev_config.yaml', 'r') as file:
            dev_config = yaml.safe_load(file)
        
        # Merge the configurations
        config = {**client_config, **dev_config}
        return config
