#coding:utf-8

f = open('lg-203466147999847691/main.txt')
data1 = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()
#print data1 # 文字列データ
lines1 = data1.split(' ') # 改行で区切る(改行文字そのものは戻り値のデータには含まれない)
print lines1
