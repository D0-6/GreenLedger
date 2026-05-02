import sys
import traceback

try:
    import api.index
    print('SUCCESS')
except Exception as e:
    print('FAIL')
    traceback.print_exc()
