
import sys
import os

# Add this directory (animations/) to sys.path if not already there
this_dir = os.path.dirname(__file__)
if this_dir not in sys.path:
    sys.path.insert(0, this_dir)

# Optional: expose key files for "from animations import *"
from . import Combination
from . import Published
from . import FinalThoughts
from . import MainEquation
from . import ForwardDifference
from . import Misc
from . import RecursiveFormula
from . import SpecificSolutions
from . import __init__
from . import NestedSums
from . import ToTheRight
from . import Intro
from . import ProblemIntroduction
