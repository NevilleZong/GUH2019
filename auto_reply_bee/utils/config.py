"""
Configuration data for managing caches.
Must call init() before using it.
"""
import os
import copy as mycopy
import yaml

__all__ = ['set', 'get', 'copy', 'update', '_print']


def get_yaml():

    #Analyse yaml
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '_config.yaml')
    try:

        with open(path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            # config = yaml.load(file, Loader=yaml.Loader)
        return config
    except Exception as exception:
        print(str(exception))
        print('There is something wrong with your _config.yaml...')
    return None

opts = get_yaml()

def set(key, value):
    """ Set value through key """
    opts[key] = value


def get(key, default=None):
    """ Get value through key """
    return opts.get(key, default)


def copy():
    """ Copy configuration """
    return mycopy.deepcopy(opts)


def update(new_opts):   
    """ Replace all configuration """
    opts.update(new_opts)


def _print():
    print(opts)


if __name__ == '__main__':
    you = get('is_forced_switch')
    print(you)
