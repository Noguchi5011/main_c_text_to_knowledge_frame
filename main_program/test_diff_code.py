import difflib
import json
import re

def normalize_code(code):
    # { の前の改行を取り除いて正規化
    return re.sub(r'\s*{', ' {', code)

def find_differences(str1, str2):
    # コードを正規化
    str1 = normalize_code(str1)
    str2 = normalize_code(str2)

    d = difflib.Differ()
    diff = list(d.compare(str1.splitlines(), str2.splitlines()))

    differences = []
    i = 0
    while i < len(diff):
        line = diff[i]

        if line.startswith('-'):
            mistaken_line = line[2:]

            if i+1 < len(diff) and diff[i+1].startswith('+'):
                correct_line = diff[i+1][2:]
                differences.append({
                    'type': 'change',
                    'mistaken_code': mistaken_line,
                    'correct_code': correct_line
                })
                i += 2
            else:
                differences.append({
                    'type': 'deletion',
                    'mistaken_code': mistaken_line
                })
                i += 1

        elif line.startswith('+'):
            correct_line = line[2:]
            differences.append({
                'type': 'addition',
                'correct_code': correct_line
            })
            i += 1

        else:
            i += 1

    return differences

# こちらはテスト用のコードです

data = {
    "mistake_info": {
        "mistake_bool": "False",
        "explain_text": "このプログラムは、0から9までの数をカウントして表示するものです。",
        "error_text": "",
        "correct_program": "#include <stdio.h>\n\nint main() \n{\n    for (int i = 0; i < 10; i++) \n    {\n        printf(\"Count: %d\\n\", i);\n    }\n    return 0;\n}"
    },
    "mistaken_code": "#include <stdio.h>\n\nint main() {\n    for (int i = 0; i < 10; i++) \n        printf(\"Count: %d\\n\", i);\n    }\n    return 0;\n}"
}

mistaken_code = data["mistaken_code"]
correct_program = data["mistake_info"]["correct_program"]

diffs = find_differences(mistaken_code, correct_program)
for diff in diffs:
    print(diff)
