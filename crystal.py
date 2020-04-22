import re
from itertools import permutations, product
import numpy as np

def zone_axes(*families):
    """ list all members in a zone axis family
        Usage:
            # all low index zone axis
            zone_axes('<100>','<110>','<111>',
                      '<210>','<211>','<221>')
    
    Args:
        families (str): family of zone axes, e.g., <110>, <111>

    Returns:
        Row-listed array of zone axes, sorted by magnitue and sign
    """
    axes = set()
    for family in families: 
        array = [int(d) for d in re.findall(r'-?\d',family)]
        array = (np.array(array)/np.gcd.reduce(array)).astype(int)
        for a in set(permutations(array)):
            for s in product([1,-1],repeat=len(a)):
                axes.add(tuple(sign*axis for sign,axis in zip(s,a)))
    axes = list(np.array(list(axes),dtype=int))
    axes.sort(key=lambda s:(np.sum(s*s),len(s[np.sign(s)<0])))
    return np.array(axes)
