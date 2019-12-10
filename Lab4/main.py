import elgamal


def write_to_file(file_name, data):
    with open(file_name, "w") as file:
        file.write(str(data))


def main():
    with open("files/initial.txt", "r") as file:
        data = file.read()

        public_key, private_key = elgamal.generate_keys()
        print("\nPublic Key: {}\nPrivate Key: {}\n".format(public_key, private_key))

        encrypted_data = elgamal.encrypt(data, public_key)
        write_to_file("files/encrypted.txt", encrypted_data)
        print("\nencrypted data:\n{}".format(encrypted_data))

        decrypted_data = elgamal.decrypt(encrypted_data, private_key)
        write_to_file("files/decrypted.txt", decrypted_data)
        print("\ndecrypted data:\n{}".format(decrypted_data))


if __name__ == "__main__":
    main()
