def register_users():
    n = int(input())

    registered_users = set()

    for _ in range(n):
        try:
            name = input()
        except EOFError:
            break

        if name not in registered_users:
            print("OK")
            registered_users.add(name)
        else:
            counter = 1
            while True:
                new_name = f"{name}{counter}"

                if new_name not in registered_users:
                    print(new_name)
                    registered_users.add(new_name)
                    break
                counter += 1


if __name__ == "__main__":
    register_users()
