from sentence_transformers import SentenceTransformer, util
import pandas as pd
import json

# sentence-bertモデルのロード
model_path = "../sentence_bert/strf_JSNLI_20_cl-tohoku_bert-base-japanese-whole-word-masking"
model = SentenceTransformer(model_path)

# JSONファイルを読み込む
with open("./generate/parsed_test_all_error_output.json", "r") as file:
    json_data = json.load(file)

error_text = json_data[0]["mistake_info"]["error_text"]
error_text_embedding = model.encode(error_text, convert_to_tensor=True)


# tsvファイルの読み込み
df = pd.read_csv("./check_teach_concept/test_explanation_check_not_filtering.tsv", sep="\t")

max_similarity = -1
most_similar_sentence = ""
most_similar_label = ""

for entry in json_data:
    error_text = entry["mistake_info"]["error_text"]
    error_text_embedding = model.encode(error_text, convert_to_tensor=True)

    max_similarity = -1
    most_similar_sentence = ""
    most_similar_label = ""

    # 各sentence1とerror_textとの類似度を計算
    for index, row in df.iterrows():
        sentence = row["sentence1"]
        sentence_embedding = model.encode(sentence, convert_to_tensor=True)
    
        similarity = util.pytorch_cos_sim(error_text_embedding, sentence_embedding)
    
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_sentence = sentence
            most_similar_label = row["label1"]

    print(f"For '{error_text}':")
    print(f"Most similar sentence: {most_similar_sentence}")
    print(f"Label: {most_similar_label}\n")
    print(f"cos: {max_similarity}\n")