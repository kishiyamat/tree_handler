# README

See https://github.com/kishiyamat/tree_handler/pull/58

`_reduce_2` と `align_np` のsubtree挿入時にエラーが起きていた。`_reduce_2` の問題点は POS と leaf を reduce するケースが発生していたことで、こちらは POSとleafの処理はブロックして対処した。`align_np` の問題点は NPの後ろに"P-"が来ることを期待していたが、NPの後ろがNPのような、前終端記号が来る場合があった。こちらも、NPの後ろが "P-" で始まらないケースをブロックして対処した。その結果、 `Arabian01_00070` と `Arabian01_00280` は処理が完了した。

対して、以下のファイルは結局 `IndexError` となった。

```
tgt_id = "Arabian01_00220"  # IndexError(LESS) # _reduce_2起因
tgt_id = "Arabian01_00330"  # IndexError(LESS) # _reduce_2起因
tgt_id = "Arabian01_00350"  # IndexError(LESS) # _reduce_2起因
tgt_id = "Arabian01_00390"  # IndexError(LESS) # _reduce_2起因
tgt_id = "Arabian01_00020"  # IndexError(LESS) # align_np起因
tgt_id = "Arabian01_00110"  # IndexError(LESS) # align_np起因
tgt_id = "Arabian01_00130"  # IndexError(OOR) # align_np起因
tgt_id = "Arabian01_00490"  # IndexError(OOR) # align_np起因
```

