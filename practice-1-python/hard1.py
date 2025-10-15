morze = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..',
    'e': '.', 'f': '..-.', 'g': '--.', 'h': '....',
    'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.',
    'q': '--.-', 'r': '.-.', 's': '...', 't': '-',
    'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..'
}


def encode_to_morse():
    input_text = input("Введите текст для кодирования: ")
    words = input_text.split()

    for word in words:
        encoded_word_parts = []
        for char in word:
            lower_char = char.lower()
            morse_code = morze.get(lower_char)
            if morse_code:
                encoded_word_parts.append(morse_code)

        encoded_word = " ".join(encoded_word_parts)
        print(encoded_word)


if __name__ == "__main__":
    encode_to_morse()
