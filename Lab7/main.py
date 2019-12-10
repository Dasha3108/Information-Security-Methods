import diffie_hellman


def main():
    # shared elliptic curve system of examples
    ec = diffie_hellman.EC(1, 18, 19)
    g, _ = ec.at(7)
    assert ec.order(g) <= ec.q

    # ECDH usage
    dh = diffie_hellman.DiffieHellman(ec, g)

    apriv = 11
    apub = dh.gen(apriv)

    bpriv = 3
    bpub = dh.gen(bpriv)

    cpriv = 7
    cpub = dh.gen(cpriv)
    # same secret on each pair
    assert dh.secret(apriv, bpub) == dh.secret(bpriv, apub)
    assert dh.secret(apriv, cpub) == dh.secret(cpriv, apub)
    assert dh.secret(bpriv, cpub) == dh.secret(cpriv, bpub)

    # not same secret on other pair
    assert dh.secret(apriv, cpub) != dh.secret(apriv, bpub)
    assert dh.secret(bpriv, apub) != dh.secret(bpriv, cpub)
    assert dh.secret(cpriv, bpub) != dh.secret(cpriv, apub)

    print("Success!")


if __name__ == "__main__":
    main()