from abc import ABCMeta
from Helper.Singleton import Singleton


class MetaSingleton(ABCMeta, Singleton):
    pass