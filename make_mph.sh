#lsで表示されたtxtをリストとして扱う。
touch $1
rm $1
for fname in `ls yomi/*.inf2 | sed s@yomi/@@ | sed s/.inf2//`
do
  python3 prog/inf2model1.py $fname $2 >> $1
done
