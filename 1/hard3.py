def process_file_requests():
    operation_map = {
        "write": "w",
        "read": "r",
        "execute": "x"
    }

    file_permissions = {}

    num_files = int(input())

    for _ in range(num_files):
        parts = input().split()
        file_name = parts[0]
        allowed_operations = set(parts[1:])
        file_permissions[file_name] = allowed_operations

    num_requests = int(input())

    for _ in range(num_requests):
        request_parts = input().split()
        operation_word = request_parts[0]
        file_name = request_parts[1]

        operation_code = operation_map.get(operation_word)

        if file_name in file_permissions and operation_code in file_permissions[file_name]:
            print("OK")
        else:
            print("Access denied")


if __name__ == "__main__":
    process_file_requests()
