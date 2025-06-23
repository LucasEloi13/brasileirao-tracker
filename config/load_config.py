import os
import yaml 
from dotenv import dotenv_values

def load_config():
    config = {}

    env_vars = dotenv_values(".env")
    config.update(env_vars)

    with open("config/config.yaml", "r") as file:
        config_yml= yaml.safe_load(file)
        
    config = {**env_vars, **config_yml}
    return config
