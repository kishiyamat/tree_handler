#lsで表示されたtxtをリストとして扱う。
touch $1
rm $1
# inf2を fname として ベースに処理を回していく
if [ $2 == -1 ]; then
    for fname in `ls yomi/*.inf2 | sed s@yomi/@@ | sed s/.inf2//`
        do
            python3 prog/inf2model1.py $fname >> $1
        done
else
    for fname in `ls inf/*.inf2 | sed s@inf/@@ | sed s/.inf2//`
        do
            if [ $2 == 0 ]; then
                python3 prog/inf2model1.py $fname $2 >> $1
            elif [ $2 == 1 ]; then
                python3 prog/inf2model1.py $fname $2 >> $1
            elif [ $2 == 2 ]; then
                # ここで失敗しているケースがある
                # cat mph/Arabian01_00220.mph
                # cat: mph/Arabian01_00220.mph: No such file or directory
                # cat mph/Arabian01_00330.mph
                # cat: mph/Arabian01_00330.mph: No such file or directory
                # cat mph/Arabian01_00350.mph
                # cat: mph/Arabian01_00350.mph: No such file or directory
                # cat mph/Arabian01_00390.mph
                # cat: mph/Arabian01_00390.mph: No such file or directory
                # cat mph/Arabian01_00020.mph
                # cat: mph/Arabian01_00020.mph: No such file or directory
                # cat mph/Arabian01_00110.mph
                # cat: mph/Arabian01_00110.mph: No such file or directory
                # cat mph/Arabian01_00130.mph
                # cat: mph/Arabian01_00130.mph: No such file or directory
                # cat mph/Arabian01_00490.mph
                # cat: mph/Arabian01_00490.mph: No such file or directory
                # cat mph/Arabian01_01150.mph
                python3 prog/inf2model1.py $fname $2 > mph/$fname.mph
                python3 src/combine_morph_tree.py $fname >> $1
            else
                echo "illegal input!"
            fi
        done
fi
