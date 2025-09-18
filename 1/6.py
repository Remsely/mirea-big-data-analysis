A = [1, 2, 3, 4, 2, 1, 3, 4, 5, 6, 5, 4, 3, 2]
B = ['a', 'b', 'c', 'c', 'c', 'b', 'a', 'c', 'a', 'a', 'b', 'c', 'b', 'a']

result_dict_zip = {}
for value, key in zip(A, B):
    result_dict_zip[key] = result_dict_zip.get(key, 0) + value

print(result_dict_zip)
