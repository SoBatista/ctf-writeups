def convert_to_text(numbers):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Alphabet string
    result = ""

    for item in numbers:
        # Check if the item is a number; convert to letter if so
        if isinstance(item, int):
            result += letters[item - 1]  # Convert number to corresponding letter
        else:
            result += str(item)  # Add non-integer items directly

    return result

# Given list - challenge image
list_to_convert = [
    16, 9, 3, 15, 3, 20, 6, "{", 
    20, 8, 5, 14, 21, 13, 2, 5, 
    18, 19, 13, 1, 19, 15, 14, "}"
]

converted_text = convert_to_text(list_to_convert)
print(converted_text)