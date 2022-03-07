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
                python3 prog/inf2model1.py $fname $2 > mph/$fname.mph
                python3 src/combine_morph_tree.py $fname >> $1
            else
                echo "illegal input!"
            fi
        done
fi
