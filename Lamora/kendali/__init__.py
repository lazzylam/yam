from .d import register as register_d
from .otw import register as register_otw
from .haduh import register as register_haduh
from .reboot import register as register_reboot 
__all__ = ["register"]

def register(client):
    register_d(client)
    register_otw(client)
    register_haduh(client)
    register_reboot(client)