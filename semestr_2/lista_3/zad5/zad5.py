def is_brackets_balanced(expression):
    stack = []
    bracket_pairs = {')': '(', '}': '{', ']': '['}

    for char in expression:
        if char in bracket_pairs.values():
            stack.append(char)
        elif char in bracket_pairs.keys():
            if not stack or stack.pop() != bracket_pairs[char]:
                return False

    return not stack 

if __name__ == "__main__":
    expression = input("Podaj wyrażenie do sprawdzenia: ")
    if is_brackets_balanced(expression):
        print("Nawiasy są poprawnie użyte.")
    else:
        print("Błąd: Nawiasy są źle sparowane lub zagnieżdżone!")
