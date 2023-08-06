import os
import sys

root_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.join(root_path, 'libs', 'applibs'))
sys.path.insert(0, os.path.join(root_path, 'libs', 'uix'))
 
from netpulse import NetPulse  # NOQA: E402

__version__ = '1.0.0'

NetPulse().run()