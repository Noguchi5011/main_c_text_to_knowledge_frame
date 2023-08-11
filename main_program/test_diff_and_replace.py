import json
import difflib

def find_differences(str1, str2):
    d = difflib.Differ()
    diff = list(d.compare(str1.splitlines(keepends=True), str2.splitlines(keepends=True)))

    differences = []

    line_num = 1
    offset_str1 = 0
    offset_str2 = 0

    for d in diff:
        if d.startswith("  "):  # 両方の文字列で一致する行
            offset_str1 += len(d[2:])
            offset_str2 += len(d[2:])
            line_num += 1
        elif d.startswith("- "):  # str1にのみ存在する行
            start_position_str1 = offset_str1
            end_position_str1 = start_position_str1 + len(d[2:])

            differences.append({
                'line': line_num,
                'text_in_mistaken_code': d[2:].strip(),
                'start_char_mistaken_code': start_position_str1,
                'end_char_mistaken_code': end_position_str1,
                'text_in_correct_program': "",
                'start_char_correct_program': offset_str2,
                'end_char_correct_program': offset_str2
            })

            offset_str1 += len(d[2:])
            line_num += 1
        elif d.startswith("+ "):  # str2にのみ存在する行
            start_position_str2 = offset_str2
            end_position_str2 = start_position_str2 + len(d[2:])

            differences.append({
                'line': line_num,
                'text_in_mistaken_code': "",
                'start_char_mistaken_code': offset_str1,
                'end_char_mistaken_code': offset_str1,
                'text_in_correct_program': d[2:].strip(),
                'start_char_correct_program': start_position_str2,
                'end_char_correct_program': end_position_str2
            })

            offset_str2 += len(d[2:])
            line_num += 1

    return differences

def apply_difference_to_code(code, difference):
    lines = code.split('\n')
    line_num = difference['line'] - 1

    # 置換
    if difference['text_in_mistaken_code'] and not difference['text_in_correct_program']:
        # 間違ったコードの部分を削除
        lines.pop(line_num)
    elif not difference['text_in_mistaken_code'] and difference['text_in_correct_program']:
        # 正しいコードの部分を追加
        lines.insert(line_num, difference['text_in_correct_program'])

    return '\n'.join(lines)

if __name__ == "__main__":
    with open("./test_generate_test1/parsed_correct_output.json", "r") as f:
        data = json.load(f)

    mistaken_code = data["mistaken_code"]
    correct_program = data["mistake_info"]["correct_program"]

    diffs = find_differences(mistaken_code, correct_program)
    
    if not diffs:
        print("差分はありません")
    else:
        for idx, difference in enumerate(diffs):
            print(f"{idx + 1}. Line {difference['line']}: Replace \"{difference['text_in_mistaken_code']}\" with \"{difference['text_in_correct_program']}\"")

        selection = int(input("Choose a difference to process (enter the number): ")) - 1
        selected_difference = diffs[selection]

        corrected_code = apply_difference_to_code(mistaken_code, selected_difference)
        print(corrected_code)
