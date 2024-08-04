"""Set context for bots.

This enables imports of other modules from the project.
"""

import os # https://docs.python-guide.org/writing/structure/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
