import json
import os
from datetime import date, datetime
from typing import List, Dict, Union

from scipy.optimize import minimize
import numpy as np


APPOS_JSON = os.path.join(os.path.dirname(__file__), 'APPOS.json')


