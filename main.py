import os
import sys
import json

root_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.join(root_path, 'libs', 'applibs'))
sys.path.insert(0, os.path.join(root_path, 'libs', 'uix'))

from kivy.factory import Factory  # NOQA: E402
 
from netpulse import NetPulse  # NOQA: E402

__version__ = '1.0.0'


with open('factory_register.json', 'r') as fr:
    custom_widget = json.load(fr)
    for module, _classes in custom_widget.items():
        for _class in _classes:
            Factory.register(_class, module=module)

NetPulse().run()