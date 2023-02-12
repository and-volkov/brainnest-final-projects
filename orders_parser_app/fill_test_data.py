import random
import string


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_letters
    result_str = "".join(
        [
            random.choice(letters) + " "
            if i % random.randint(5, 8) == 0
            else random.choice(letters)
            for i in range(length)
        ]
    )
    return result_str


def generate_items_string():
    return ", ".join(
        [
            get_random_string(random.randint(1, 5))
            for _ in range(random.randint(1, 7))
        ]
    )


def fill_test_data():
    with open("example.txt", "w") as f:
        for i in range(100):
            if i % random.randint(3, 7) == 0:
                f.write(
                    f"Order #{i}"
                    f" Customer: {get_random_string(random.randint(1, 5))}"
                    f" Items: {generate_items_string()}"
                    f"\n"
                )
            f.write((get_random_string(random.randint(1, 100))) + "\n")


if __name__ == "__main__":
    fill_test_data()
