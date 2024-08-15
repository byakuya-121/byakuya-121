# 可変長引数　参照P.254
print('=========================')
print()
print('hotcake')
print('hotcake','pizza')
print('hotcake','pizza','steak')
print('=========================')
# Print関数の引数　参照以下同じ

def f(*x):
    print(x)
f()
f('hotcake')
f('hotcake','pizza')
print('hotcake','pizza','steak')
print('===========END==============')