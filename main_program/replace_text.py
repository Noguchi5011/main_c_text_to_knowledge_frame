import json

# 外部のJSONファイルを読み込む
with open('./generate/multi_diff_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 利用可能な 'differences' を表示
for idx, difference in enumerate(data['differences']):
    print(f"{idx + 1}. Line {difference['line']}: Replace \"{difference['text_in_mistaken_code']}\" with \"{difference['text_in_correct_program']}\"")

# ユーザーに選択を促す
selection = int(input("Choose a difference to process (enter the number): ")) - 1
selected_difference = data['differences'][selection]

# エラーコードを行ごとに分割
lines = data['mistaken_code'].split('\n')

# 選択された差異に基づいて置換
line = selected_difference['line'] - 1
start = selected_difference['start_char_mistaken_code'] - 1
end = selected_difference['end_char_mistaken_code']
lines[line] = lines[line][:start] + selected_difference['text_in_correct_program'] + lines[line][end:]

# 置換後のコードを結合
corrected_code = '\n'.join(lines)
print(corrected_code)
