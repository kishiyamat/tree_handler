# tree_handler


## How to Use

### make venv


```sh
$ python3 -m venv venv 
$ . venv/bin/activate  # 仮想環境作成
$ pip install -r requirements.txt  # ライブラリインストール
```

### oneliner

以下は `results.txt` にファイルの結果を作りたい場合

```sh
$ # Prerequisites
$ # 1. psd, inf2 を `./psd/` `./inf/` に配置
$ cp yomi/*.inf2 inf/
$ cp kaki/*.psd psd/  # comainuの結果
$ . oneliner.sh results.txt 2  # ours
$ # 2の時はmph/に出力&別のpyが走る
$ # . oneliner.sh results.txt 0  # baseline
$ # . oneliner.sh results.txt 1  # thiers
```
