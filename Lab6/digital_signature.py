from codecs import getdecoder
from codecs import getencoder
from hashlib import md5
from os import urandom


class GostCurve(object):
    def __init__(self, p, q, a, b, x, y, e=None, d=None):
        self.p = p
        self.q = q
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.e = e
        self.d = d
        r1 = self.y * self.y % self.p
        r2 = ((self.x * self.x + self.a) * self.x + self.b) % self.p
        if r1 != self.pos(r2):
            raise ValueError("Invalid parameters")
        self._st = None

    def pos(self, v):
        if v < 0:
            return v + self.p
        return v

    def _add(self, p1x, p1y, p2x, p2y):
        if p1x == p2x and p1y == p2y:
            t = ((3 * p1x * p1x + self.a) * _modinvert(2 * p1y, self.p)) % self.p
        else:
            tx = self.pos(p2x - p1x) % self.p
            ty = self.pos(p2y - p1y) % self.p
            t = (ty * _modinvert(tx, self.p)) % self.p
        tx = self.pos(t * t - p1x - p2x) % self.p
        ty = self.pos(t * (p1x - tx) - p1y) % self.p
        return tx, ty

    def exp(self, degree, x=None, y=None):
        x = x or self.x
        y = y or self.y
        tx = x
        ty = y
        if degree == 0:
            raise ValueError("Bad degree value")
        degree -= 1
        while degree != 0:
            if degree & 1 == 1:
                tx, ty = self._add(tx, ty, x, y)
            degree = degree >> 1
            x, y = self._add(x, y, x, y)
        return tx, ty

    def st(self):
        if self.e is None or self.d is None:
            raise ValueError("non twisted Edwards curve")
        if self._st is not None:
            return self._st
        self._st = (
            self.pos(self.e - self.d) * _modinvert(4, self.p) % self.p,
            (self.e + self.d) * _modinvert(6, self.p) % self.p,
        )
        return self._st

def get_curve():
    return GostCurve(
        p=_bytes2long(_hexdec("C0000000000000000000000000000000000000000000000000000000000003C7")),
        q=_bytes2long(_hexdec("5fffffffffffffffffffffffffffffff606117a2f4bde428b7458a54b6e87b85")),
        a=_bytes2long(_hexdec("C0000000000000000000000000000000000000000000000000000000000003c4")),
        b=_bytes2long(_hexdec("2d06B4265ebc749ff7d0f1f1f88232e81632e9088fd44b7787d5e407e955080c")),
        x=_bytes2long(_hexdec("0000000000000000000000000000000000000000000000000000000000000002")),
        y=_bytes2long(_hexdec("a20e034bf8813ef5c18d01105e726a17eb248b264ae9706f440bedc8ccb6b22c")),
    )


def get_private_key():
    return _bytes2long(urandom(32)[::-1])


def sign(curve, private_key, text, block_size=64):
    h = md5(text.encode()).digest()
    q = curve.q
    e = _bytes2long(h) % q

    if e == 0:
        e = 1

    while True:
        k = _bytes2long(urandom(block_size)) % q
        if k == 0:
            continue
        
        c_x, _ = curve.exp(k)
        r = c_x % q
        if r == 0:
            continue

        d = private_key * r
        k *= e
        
        s = (d + k) % q
        if s == 0:
            continue
        break

    return _long2bytes(s, block_size) + _long2bytes(r, block_size)


def verify(curve, public_key_tuple, digest, signature, block_size=64):
    if len(signature) != block_size * 2:
        raise ValueError("Invalid signature length")

    q = curve.q
    p = curve.p

    s = _bytes2long(signature[:block_size])
    r = _bytes2long(signature[block_size:])

    if r <= 0 or r >= q or s <= 0 or s >= q:
        return False

    e = _bytes2long(digest) % curve.q
    if e == 0:
        e = 1

    v = _modinvert(e, q)
    z1 = s * v % q
    z2 = q - r * v % q

    p1x, p1y = curve.exp(z1)
    q1x, q1y = curve.exp(z2, public_key_tuple[0], public_key_tuple[1])
    c_x = q1x - p1x
    if c_x < 0:
        c_x += p
    c_x = _modinvert(c_x, p)
    z1 = q1y - p1y
    c_x = c_x * z1 % p
    c_x = c_x * c_x % p
    c_x = c_x - p1x - q1x
    c_x = c_x % p
    if c_x < 0:
        c_x += p
    c_x %= q

    return c_x == r


def _bytes2long(raw):
    return int(_hexenc(raw), 16)


def _long2bytes(n, size=32):
    res = hex(int(n))[2:].rstrip("L")
    if len(res) % 2 != 0:
        res = "0" + res
    s = _hexdec(res)
    if len(s) != size:
        s = (size - len(s)) * b"\x00" + s
    return s


def _hexdec(data):
    _hexdecoder = getdecoder("hex")
    return _hexdecoder(data)[0]


def _hexenc(data):
    _hexencoder = getencoder("hex")
    return _hexencoder(data)[0].decode("ascii")


def _modinvert(a, n):
    if a < 0:
        return n - _modinvert(-a, n)
    t, newt = 0, 1
    r, newr = n, a
    while newr != 0:
        quotinent = r // newr
        t, newt = newt, t - quotinent * newt
        r, newr = newr, r - quotinent * newr
    if r > 1:
        return -1
    if t < 0:
        t = t + n
    return t