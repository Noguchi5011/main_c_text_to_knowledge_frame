import json

def normalize_code(code):
    # コードを正規化: 連続する空白行を1つにまとめる
    lines = code.splitlines()
    normalized_lines = []
    was_previous_line_empty = False

    for line in lines:
        is_empty = not line.strip()
        if is_empty and was_previous_line_empty:
            continue
        normalized_lines.append(line)
        was_previous_line_empty = is_empty

    return "\n".join(normalized_lines)

def find_differences(str1, str2):
    differences = []

    # 正規化
    str1 = normalize_code(str1)
    str2 = normalize_code(str2)

    mistaken_code_content = str1.splitlines()
    correct_program_content = str2.splitlines()

    for line_num, (line_a, line_b) in enumerate(zip(mistaken_code_content, correct_program_content), 1):
        i, j = 0, 0

        while i < len(line_a) or j < len(line_b):
            if i < len(line_a) and line_a[i].isspace():
                i += 1
            if j < len(line_b) and line_b[j].isspace():
                j += 1

            if (i < len(line_a) and j < len(line_b) and line_a[i] != line_b[j]) or (i == len(line_a) and j < len(line_b)) or (j == len(line_b) and i < len(line_a)):
                start_i, start_j = i, j

                # Differences in mistaken_code
                while i < len(line_a) and (j >= len(line_b) or line_a[i] != line_b[j]):
                    i += 1
                # Differences in correct_program
                while j < len(line_b) and (i >= len(line_a) or line_b[j] != line_a[i]):
                    j += 1

                differences.append({
                    'line': line_num,
                    'start_char_mistaken_code': start_i + 1,  # 1-indexed
                    'end_char_mistaken_code': i,
                    'text_in_mistaken_code': line_a[start_i:i],
                    'start_char_correct_program': start_j + 1,  # 1-indexed
                    'end_char_correct_program': j,
                    'text_in_correct_program': line_b[start_j:j]
                })
            else:
                i += 1
                j += 1

    return differences

if __name__ == "__main__":
    # input.jsonからデータを読み込む
    with open("./test_generate_test1/parsed_correct_output.json", "r") as f:
        data = json.load(f)

    mistaken_code = data["mistaken_code"]
    correct_program = data["mistake_info"]["correct_program"]

    diffs = find_differences(mistaken_code, correct_program)
    
    if not diffs:
        print("差分はありません")
    else:
        # 結果をoutput.jsonに保存
        with open("./test_generate/diff_output.json", "w") as out_file:
            output_data = {
                "differences": diffs,
                "mistaken_code": mistaken_code,
                "correct_program": correct_program
            }
            json.dump(output_data, out_file, ensure_ascii=False, indent=4)
        print("差分が検出され、output.jsonに保存されました。")


# import json
# import difflib

# def find_differences(str1, str2):
#     d = difflib.ndiff(str1, str2)

#     differences = []
#     line_num = 1
#     char_num = 1

#     for diff in d:
#         tag = diff[0]
#         text = diff[2:]

#         if tag == ' ':
#             char_num += len(text)
#         elif tag == '-':
#             differences.append({
#                 "line": line_num,
#                 "start_char_mistaken_code": char_num,
#                 "end_char_mistaken_code": char_num + len(text) - 1,
#                 "text_in_mistaken_code": text,
#                 "start_char_correct_program": 0,
#                 "end_char_correct_program": 0,
#                 "text_in_correct_program": ""
#             })
#             char_num += len(text)
#         elif tag == '+':
#             differences.append({
#                 "line": line_num,
#                 "start_char_mistaken_code": 0,
#                 "end_char_mistaken_code": 0,
#                 "text_in_mistaken_code": "",
#                 "start_char_correct_program": char_num,
#                 "end_char_correct_program": char_num + len(text) - 1,
#                 "text_in_correct_program": text
#             })
#             char_num += len(text)
#         if '\n' in text:
#             line_num += 1
#             char_num = 1

#     return differences

# if __name__ == "__main__":
#     with open("./test_generate_test1/parsed_correct_output.json", "r") as f:
#         data = json.load(f)

#     mistaken_code = data["mistaken_code"]
#     correct_program = data["mistake_info"]["correct_program"]

#     diffs = find_differences(mistaken_code, correct_program)

#     # 結果をoutput.jsonに保存
#     with open("./test_diff_output.json", "w") as out_file:
#         output_data = {
#             "differences": diffs,
#             "mistaken_code": mistaken_code,
#             "correct_program": correct_program
#         }
#         json.dump(output_data, out_file, ensure_ascii=False, indent=4)
