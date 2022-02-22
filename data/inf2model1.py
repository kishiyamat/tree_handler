# -*- coding: utf-8 -*-
# ファイル syn.py
#
import sys
import re

if len( sys.argv ) < 2:
    print( "処理ファイル名を指定してください。\n" )
    sys.exit()

obj = open( "yomi/" + sys.argv[1] + ".inf2", "r" )
rlist = obj.read()
rlist = rlist.split( "\n" )
obj.close()
if ( rlist[-1] == "" ): rlist.pop()

lin = [[ "sil", 0, 100, 100, 100, 0 ]]
for w in rlist:
    c = w.split(" ")
    m = c[2].split("/")

    if c[2].split("-")[1].split("+")[0] == "pau":
        lin += [[ "pau", 0, 100, 100, 100, 0 ]]
        continue

    p  = re.findall(r"\-(.*?)\+.*?\/A:([0-9\-]+).*?\/F:.*?_([0-9])", c[2])
    a2 = re.findall(r"\/A:.*?\+([0-9]+)\+", c[2])
    p2 = re.findall(r"\/L:.*?_([0-9\-]+)*", c[2])
    p3 = re.findall(r"\/M:.*?_([0-9\-]+)*", c[2])
#    p2 = c[2][-14:]
    if len(p) == 1:
        lin += [[ p[0][0], int( p[0][2] ), int( p[0][1] ), int( p2[0] ), int( a2[0] ),
            int( p3[0] ) ]]

lin += [[ "sil", 0, -100, 200, 100, 0 ]]
#print( lin )

txt = ""
for i, l in enumerate( lin, 0 ):
    if   ( l[0] == "sil" ):
        if   ( i           == 0 ): continue
        elif ( lin[i-1][5] == 2 ): txt += ". "
        elif ( lin[i-1][5] == 3 ): txt += "? "
        elif ( lin[i-1][5] == 4 ): txt += "! "
        continue

    elif ( l[0] == "pau" ):
        if   ( lin[i-1][5] == 1 ): txt += ", "
        elif ( lin[i-1][5] == 2 ): txt += ". "
        elif ( lin[i-1][5] == 3 ): txt += "? "
        elif ( lin[i-1][5] == 4 ): txt += "! "
        else :                     txt += "_ "
        continue

    txt += l[0] + " "

    if   ( l[2] == 0 and lin[i+1][2] == 1 ):  txt += "\ "
    elif ( l[4] == 1 and lin[i+1][4] == 2 ):  txt += "/ "


    if ( lin[i][2] > lin[i+1][2] or lin[i][1] != lin[i+1][1] ): 
        if   ( (l[3] > 1 ) and ( lin[i][3] == lin[i+1][3] ) ): dd = "#1 "
        elif (  l[3] < 1 ): dd = "#1 "
        elif (  l[3] > 6 ): dd = "#6 "
        else:               dd = "#" + str( l[3] ) + " "

        if ( lin[i+1][3] != 200 ): txt += dd 

print( sys.argv[1], txt )
