from .brent import Brent
from .cbr_fx import USDRUR
from .ust import UST
from .kep import KEP_Annual, KEP_Qtr, KEP_Monthly

PARSERS = (KEP_Annual, KEP_Qtr, KEP_Monthly,
           Brent, USDRUR, UST) 
