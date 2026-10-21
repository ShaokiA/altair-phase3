import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/hp/altair-phase3/altair_phase3_ws/install/altair_phase3'
