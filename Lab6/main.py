import digital_signature

from hashlib import md5


if __name__ == "__main__":
    text = 'Hello World'
    
    curve = digital_signature.get_curve()
    user_private_key = digital_signature.get_private_key()
    public_key_tuple = curve.exp(user_private_key)
    
    signatured_text = digital_signature.sign(curve, user_private_key, text)
    print("\nSignatured message: {}".format(signatured_text))

    is_true = digital_signature.verify(curve, public_key_tuple, md5((text).encode()).digest(), signatured_text)
    print("\nThe digital signature is verified\n" if is_true else "\nThe digital signature isn't verified\n")
