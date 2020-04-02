"""
Mesa Agent-Based Modeling Framework Extension
Core Objects: Model, and Agent.
"""
import datetime

from .mesa_SIR import calculations_and_plots
from .mesa_SIR import SIR

__all__ = ["Infection"]


__title__ = 'Mesa_SIR'
__version__ = '0.0.1'
__license__ = 'MIT'
__copyright__ = 'Copyright %s Mark Bailey' % datetime.date.today().year