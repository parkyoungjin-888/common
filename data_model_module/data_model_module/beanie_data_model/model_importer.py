import importlib


def import_model(module_name: str, model_name: str):
    base_dir = 'data_model_module.beanie_data_model'
    module_name = f'{base_dir}.{module_name}'
    module = importlib.import_module(module_name)
    return getattr(module, model_name)
