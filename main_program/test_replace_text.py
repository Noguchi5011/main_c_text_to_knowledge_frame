import json

def apply_difference_to_code(code, difference):
    lines = code.split('\n')
    line_num = difference['line'] - 1

    # 置換
    mistaken_text = difference['text_in_mistaken_code']
    correct_text = difference['text_in_correct_program']
    lines[line_num] = lines[line_num].replace(mistaken_text, correct_text, 1)

    return '\n'.join(lines)

if __name__ == "__main__":
    with open("./test_diff_output.json", "r") as f:
        data = json.load(f)

    mistaken_code = data["mistaken_code"]
    diffs = data["differences"]

    for idx, difference in enumerate(diffs):
        print(f"{idx + 1}. Line {difference['line']}: Replace \"{difference['text_in_mistaken_code']}\" with \"{difference['text_in_correct_program']}\"")

    selection = int(input("Choose a difference to process (enter the number): ")) - 1
    selected_difference = diffs[selection]

    corrected_code = apply_difference_to_code(mistaken_code, selected_difference)
    print(corrected_code)
