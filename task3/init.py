import numpy as np
from numpy import ndarray
import constants
from typing import List, Tuple

def solarS_mass_init() -> ndarray:
    return np.array([constants.M_SUN, constants.M_MERCURY, constants.M_VENUS, constants.M_EARTH,
                constants.M_MARS, constants.M_JUPITER, constants.M_SATURN, constants.M_URANUS,
                constants.M_NEPTUNE])



def solarS_rv_init() -> ndarray:
    #[rrr vvv     rrr vvv    ... rrr vvv]
    rv_start = []
    #Sun
    rv_start.append(np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    #Mercury
    rv_start.append(np.array([constants.R_MERCURY, 0.0, 0.0, 0.0, constants.V_MERCURY, 0.0]))
    #Venus
    rv_start.append(np.array([constants.R_VENUS, 0.0, 0.0, 0.0, constants.V_VENUS, 0.0]))
    #Earth
    rv_start.append(np.array([constants.R_EARTH, 0.0, 0.0, 0.0, constants.V_EARTH, 0.0]))
    #Mars
    rv_start.append(np.array([constants.R_MARS, 0.0, 0.0, 0.0, constants.V_MARS, 0.0]))
    #Jupiter
    rv_start.append(np.array([constants.R_JUPITER, 0.0, 0.0, 0.0, constants.V_JUPITER, 0.0]))
    #Saturn
    rv_start.append(np.array([constants.R_SATURN, 0.0, 0.0, 0.0, constants.V_SATURN, 0.0]))
    #Uranus
    rv_start.append(np.array([constants.R_URANUS, 0.0, 0.0, 0.0, constants.V_URANUS, 0.0]))
    #Neptune
    rv_start.append(np.array([constants.R_NEPTUNE, 0.0, 0.0, 0.0, constants.V_NEPTUNE, 0.0]))

    return np.array(rv_start).flatten()



def solarS_rv_init_asArray() -> ndarray:
    #[[rrr vvv]     [rrr vvv]    ... [rrr vvv]]
    rv_start = []
    #Sun
    rv_start.append((0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    #Mercury
    rv_start.append((constants.R_MERCURY, 0.0, 0.0, 0.0, constants.V_MERCURY, 0.0))
    #Venus
    rv_start.append((constants.R_VENUS, 0.0, 0.0, 0.0, constants.V_VENUS, 0.0))
    #Earth
    rv_start.append((constants.R_EARTH, 0.0, 0.0, 0.0, constants.V_EARTH, 0.0))
    #Mars
    rv_start.append((constants.R_MARS, 0.0, 0.0, 0.0, constants.V_MARS, 0.0))
    #Jupiter
    rv_start.append((constants.R_JUPITER, 0.0, 0.0, 0.0, constants.V_JUPITER, 0.0))
    #Saturn
    rv_start.append((constants.R_SATURN, 0.0, 0.0, 0.0, constants.V_SATURN, 0.0))
    #Uranus
    rv_start.append((constants.R_URANUS, 0.0, 0.0, 0.0, constants.V_URANUS, 0.0))
    #Neptune
    rv_start.append((constants.R_NEPTUNE, 0.0, 0.0, 0.0, constants.V_NEPTUNE, 0.0))

    return np.array(rv_start)