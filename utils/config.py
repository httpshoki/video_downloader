import os
import json

class ConfigManager:
    CONFIG_PATH = 'config.json'

    def save_config(self, destination):
        config = {'destination': destination}
        with open(self.CONFIG_PATH, 'w') as config_file:
            json.dump(config, config_file)

    def load_config(self):
        if os.path.exists(self.CONFIG_PATH):
            with open(self.CONFIG_PATH, 'r') as config_file:
                config = json.load(config_file)
                return config.get('destination', '')
        return ''
