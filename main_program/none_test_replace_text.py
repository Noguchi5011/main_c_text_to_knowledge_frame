import json

with open('./test_diff_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for idx, difference in enumerate(data['differences']):
    print(f"{idx + 1}. Line {difference['line']}: Replace \"{difference['text_in_mistaken_code']}\" with \"{difference['text_in_correct_program']}\"")

selection = int(input("Choose a difference to process (enter the number): ")) - 1
selected_difference = data['differences'][selection]

lines = data['mistaken_code'].split('\n')
line = selected_difference['line'] - 1
start = selected_difference['start_char_mistaken_code'] - 1
end = selected_difference['end_char_mistaken_code']

# エラーコード内の該当文字列と正答コード内の該当文字列が一致している場合、置き換える必要がないのでスキップ
if lines[line][start:end] == selected_difference['text_in_correct_program']:
    pass
else:
    # 置き換え処理
    lines[line] = lines[line][:start] + selected_difference['text_in_correct_program'] + lines[line][end:]

corrected_code = '\n'.join(lines)
print(corrected_code)
