# ローカル変数　参照P.267
def f():
 text='Good Morning'
 print('f():',text)

def g():
 text='Good Morning'
 print('g():',text)

text='Hello'
f()
g()
print(text)
