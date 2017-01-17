# -*- coding: utf-8 -*-
import importlib


class SettingsSingleton(object):
    """
    Let's load a settings in the memory one time when the app starts
    Than override some settings with command arguments
    After this we not should change the object
    """
    instance = None

    def __init__(self):
        if not SettingsSingleton.instance:
            SettingsSingleton.instance = Settings()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)


class Settings(object):

    def __init__(self):
        mod = importlib.import_module('settings')

        for setting in dir(mod):
            setting_value = getattr(mod, setting)
            setattr(self, setting, setting_value)

settings = SettingsSingleton()
