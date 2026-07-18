"""Serial checksum primitives — shared by the card generators and helpers.

One program secret (PROGRAM_KEY) exists in the whole system. The serial
checksum uses a key DERIVED from it — HMAC(PROGRAM_KEY, 'serial-v1') as hex —
so the derived key can travel in printed register QRs (letting the scanner
verify serials locally, even offline) without ever exposing the program key
itself, which also gates the full-data backup action.

Must stay byte-identical with the Apps Script and redeem.html implementations
(see design/LOGGING.md) — printed cards freeze this algorithm.
"""
import hashlib
import hmac

CK_ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ'   # 24 letters, no I/O (read as 1/0)
DEMO_KEY = 'demo-key'                       # samples & demo artwork ONLY


def derive_ck_key(program_key):
    """The scanner-safe checksum key, as lowercase hex."""
    return hmac.new(program_key.encode(), b'serial-v1', hashlib.sha256).hexdigest()


def serial_letter(base, ck_key_hex):
    """Checksum letter for a serial's base (e.g. 'KPMU-2026-00004217')."""
    d = hmac.new(ck_key_hex.encode(), base.encode(), hashlib.sha256).digest()
    return CK_ALPHABET[d[0] % 24]
