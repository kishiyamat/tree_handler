# tree_handler


## How to Use

### oneliner

```
$ # Prerequisites
$ # 1. psd, inf2 を `./psd/` `./inf2/` に配置
$ cp yomi/*.inf2 inf/
```
1. mph出力
1. 実行
1. 一つのファイルにまとめる

```

```

### make morph

```sh
$ . oneliner.sh results_new.txt 0  # baseline
$ . oneliner.sh results_new.txt 1  # thiers
$ . oneliner.sh results_new.txt 2  # ours
```

### apply

```sh
$ python -m venv venv 
$ . venv/bin/activate  # 仮想環境作成
$ pip install -r requirements.txt  # ライブラリインストール
$ サンプル分析
$ python3 src/combine_morph_tree.py data/sample00.mph data/sample00.psd
```

## リファクタリング手順

```sh
$ # /yomi の真上で /yomi に格納されているファイルを
$ # 拡張子なしで変数に渡さないといけない
$ . oneliner.sh results.txt
$ cd data
$ python inf2model1.py Arabian01_00050
> Arabian01_00010 a / r a b i a N n a \ i t o
```


```sh
$ # 変更前のデータを出力
$ . oneliner.sh results_original.txt
$ # inf2model1.py を main 関数に入れる
$ # 変更後に results_new.txt を生成
$ . oneliner.sh results_new.txt
$ # Assert: 変更による変化なし
$ diff results_original.txt results_new.txt 
```
