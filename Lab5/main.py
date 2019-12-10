import hmac


if __name__ == "__main__":
    key = 'some_random_key'

    first_message = 'Hello world'
    first_result = hmac.hmac(first_message, key)
    print("\nFirst result:\t{}".format(first_result))

    second_message = 'Hello world'
    second_result = hmac.hmac(second_message, key)
    print("Second result:\t{}".format(second_result))

    print("\nResults are equal\n" if first_result == second_result else "Results aren't equal\n")