import os
import util
import numpy as np

def read_cfg_string(cfg,section,key,default):
    if cfg.has_option(section, key):
        return cfg.get(section,key)
    else:
        return default

def read_cfg_int(cfg,section,key,default):
    if cfg.has_option(section,key):
        return cfg.getint(section,key)
    else:
        return default

def read_cfg_float(cfg,section,key,default):
    if cfg.has_option(section,key):
        return cfg.getfloat(section,key)
    else:
        return default

def read_cfg_bool(cfg,section,key,default):
    if cfg.has_option(section,key):
        return cfg.get(section,key) in ['True','true']
    else:
        return default
