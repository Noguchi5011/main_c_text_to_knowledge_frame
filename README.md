# 未完成プログラムからのテキスト化

以下に動作方法の記述を行う。

## 仮想環境構築
仮想環境の構築には、`python3-venv`を用いる。以下のコードで`python3-venv`をインストールする
```
apt install python3-venv
```

続いて仮想環境の作成を行う。以下のコードで仮想環境の作成並びに必要モジュールのインストールを行う。

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## C言語からのテキスト化

仮想環境の構築が終わった後は、`chatgpt_api_key`を登録する`.env`ファイルを作成する。
`.env`ファイルの記載例を以下に示す。[your_api_key]の箇所を発行した`api_key`の中身に置き換える
```
api_key=[your_api_key]
```

これが完了すれば準備はOK。
以下のコマンドを実行することで、c言語のエラー箇所の特定並びにテキスト化したものをjsonファイルとして`main_program/generate/`以下に出力する。
```
cd main_program
bash run.sh
```
`main_program/`フォルダ以下のプログラムの内容は以下のとおりである。

```
main_program/
├── c_lang_mistake_check.py ##C言語プログラムから`プログラムの動作内容について`、`正解プログラム`、`入力されたプログラム`を出力するコード
├── diff_program_mistake_correct.py ##`入力プログラム`と`正解プログラム`を比較し、差分を取るコード
├── generate/ 
├── get_clang_error_text_all.py ##`入力プログラム`と`差分を取り出したコードの行`を入力として入れて、`その行の動作内容テキスト`、`エラー内容`、`エラー内容について聞く質問文`を出力する。
├── parse_all_errors.py
├── parse_mistake_check.py
└── run.sh
```
