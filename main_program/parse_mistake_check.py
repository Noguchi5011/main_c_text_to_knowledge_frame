import json
import os
import dirtyjson

file_path = "generate/correct_combined_results.json" 
output_path = "generate/parsed_correct_output.json"

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 2. `choices`の中の`arguments`を抽出し、Pythonの辞書に変換
arguments = data[0]["choices"][0]["message"]["function_call"]["arguments"]
parsed_arguments = dirtyjson.loads(arguments)

formatted_data = {
    "mistake_bool": parsed_arguments["mistake_bool"],
    "explain_text": parsed_arguments["explain_text"],
	"error_text": parsed_arguments["error_text"],
    "correct_program": parsed_arguments["correct_program"].replace("\\\"", "\"").replace("\\\\", "\\")
}

# 4. JSONデータの後に続く間違ったコードを取得
mistaken_code = data[1]

# 5. 新しい形式のデータと間違ったコードを新しいJSONファイルに保存
output_data = {
    "mistake_info": formatted_data,
    "mistaken_code": mistaken_code
}

with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(output_data, file, ensure_ascii=False, indent=4)