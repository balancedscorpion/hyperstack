from .client import Hyperstack

hyperstack = Hyperstack()

# You can also import and expose other modules if needed
from . import api

__all__ = ['hyperstack', 'api']