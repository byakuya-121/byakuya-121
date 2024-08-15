# グローバル変数  参照P.268
print("===================")
def f():
    print('f():',text)

def g():
    print('g():',text)
text= 'Hello wold'
f()
g()
print(text)
print("===================")
   # f()とG()を呼び出して関数の外側にあるtextをターミナルに出力させる。