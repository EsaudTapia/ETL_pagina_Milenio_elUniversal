import yaml

__config = None

#Verificamos si existe la configuración y si no la cargamos.
def config():
    global __config
    if not __config:
        with open('config.yaml', mode='r') as f:
            __config = yaml.full_load(f)
        
    return __config