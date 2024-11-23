import importlib


def import_model(model_name, file_name):
    base_dir = 'mongodb_module.beanie_data_model'
    module_name = f'{base_dir}.{file_name}'
    module = importlib.import_module(module_name)
    return getattr(module, model_name)
