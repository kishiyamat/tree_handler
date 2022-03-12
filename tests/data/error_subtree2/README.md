- reduce_1起因のものも、POSとleaveの操作になっていたので修正
- align_vp のものは VB->PUのケースを除外(かき混ぜによる誤パース?)
    - VB-> NP_SBJ(ネスト)のものは検討中
```
tgt_id = "Arabian03_03100"  #reduce_1起因
tgt_id = "Arabian03_04540"  #reduce_1起因
tgt_id = "Arabian03_02230"  #reduce_1起因
tgt_id = "Arabian03_02100"  #reduce_1起因
tgt_id = "Arabian02_06640"  #reduce_1起因
tgt_id = "Arabian02_01350"  #reduce_1起因
tgt_id = "Arabian01_02930"  #reduce_1起因
tgt_id = "Arabian01_02920"  #reduce_1起因
tgt_id = "Arabian01_02460"  #reduce_1起因
tgt_id = "Arabian01_01420"  #reduce_1起因
tgt_id = "Arabian01_01420"  #reduce_1起因
tgt_id = "Arabian01_01150"  #fix align_vp -> IndexError
tgt_id = "Arabian01_03980"  #fix align_vp -> IndexError
tgt_id = "Arabian02_00890"  #fix align_vp -> IndexError
tgt_id = "Arabian02_05860"  #fix align_vp -> IndexError
```
