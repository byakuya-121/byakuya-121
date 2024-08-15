# Pythonの数値 整数と浮動小数点演算 参照P.74~75

print("==以下はこの様になりました。==")
print(2**6)
print(2**10) #<= これは多倍長整数の演算で()の中の2の10乗している形.

print("=============================")
RED=3
if RED>=45:
    print(RED)
else:
    print('数が合いません')

#文字列コード 変数埋め込み型
pro = 150
text = f"私のおこずかいは{pro}です"
print(text)

#クラス定義 参照P.280
 #Clss クラス名：
 #文章...

#空のクラス定義　参照P.281
 #Clss クラス名：
  #pass
class Food:
    pass

X=Food
print(X)

#　クラス属性の操作　__init__メゾット 参照P.293

class Food:
    count=0
    def __init__(self,name,price):
        self.name=name
        self.price=price
        Food.count +=1
    def show(self):
        print(Food.count,self.name,self.price)
print('===============')
x=Food('milk',170)
x.show()

y=Food('egg',300)
y.show()
print('===============')

