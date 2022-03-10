## Appendix

### add test

### apply

基本は oneliner の中身で呼ばれるから、こちらをいじることはない

```sh
$ サンプル分析
$ python3 src/combine_morph_tree.py data/sample00.mph data/sample00.psd
```

## リファクタリング手順

```sh
$ # /yomi の真上で /yomi に格納されているファイルを
$ # 拡張子なしで変数に渡さないといけない
$ . oneliner.sh results.txt
$ cd data
$ python3 inf2model1.py Arabian01_00050
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

## Bugfix

```sh
$ # 以下を実施していき、問題を潰していく
$ . oneliner.sh results.txt 2  # mph を生成
$ python3 src/combine_morph_tree.py Aa1_001  # 生成したmphを使って動作チェック
$ # もし修正が必要なら、mphを手で書き換えてみる
```

