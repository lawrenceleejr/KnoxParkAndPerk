"""Print the derived serial-check key for register QRs.

Usage:  python3 tools/ckkey.py 'YOUR-PROGRAM-KEY'
Each shop's register QR should point at:
  https://.../redeem.html?shop=<slug>&k=<this value>
The derived key lets the scanner verify serial checksums locally (even
offline); it cannot be used to access the backup action.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from serials import DEMO_KEY, derive_ck_key

if __name__ == '__main__':
    key = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('KPMU_PROGRAM_KEY', '')
    if not key:
        print('WARNING: no key given — deriving from the public demo key.')
        key = DEMO_KEY
    print(derive_ck_key(key))
