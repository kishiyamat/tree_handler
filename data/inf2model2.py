# -*- coding: utf-8 -*-
# ファイル syn.py
#
# %%
import sys
import re

if len( sys.argv ) < 2:
    print( "処理ファイル名を指定してください。\n" )
    sys.exit()

sys_argv = [0, "Arabian01_00050"]
obj = open( "yomi/" + sys_argv[1] + ".inf2", "r" )
# obj = open( "yomi/" + sys.argv[1] + ".inf2", "r" )
rlist = obj.read()
rlist = rlist.split( "\n" )
obj.close()
print(rlist)
# %%
