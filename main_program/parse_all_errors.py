import json
import os
import dirtyjson

file_path = "generate/test_all_error_text.json"
output_path = "generate/parsed_test_all_error_output.json"

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# すべての`arguments`を抽出し、それに基づいて新しいフォーマットのデータを作成
output_data_list = []

for item in data:
    arguments = item["choices"][0]["message"]["function_call"]["arguments"]
    parsed_arguments = dirtyjson.loads(arguments)
    
    formatted_data = {
        "line": parsed_arguments["line"],
        "explain_text": parsed_arguments["explain_text"],
        "error_text": parsed_arguments["error_text"],
        "question": parsed_arguments["question"]
    }

    # 各`arguments`に対する新しい形式のデータをリストに追加
    output_data_list.append({"mistake_info": formatted_data})

# 新しい形式のデータを新しいJSONファイルに保存
with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(output_data_list, file, ensure_ascii=False, indent=4)
