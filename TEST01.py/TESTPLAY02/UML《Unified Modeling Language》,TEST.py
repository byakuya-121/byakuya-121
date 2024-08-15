# Class構文を使用して2つのクラスに別れた処理をする。
 # また派生クラス定義と言う。

class Food:
    def __init__(self,name,price,use_by_date):
        self.name=name
        self.price=price
        self.use_by_date=use_by_date
        
def show(self):
    print('name:',self.name)
    print('price:',self.price)
    print('use-by date:',self.use_by_date)
    
class Toy:
    def __init__(self,name,price,target_age):
        self.name=name
        self.price=price
        self.target_age=target_age
    
    def show(self):
        print('name:',self.name)
        print('price:',self.price)
        print('target age:',self.target_age)

x=Food('chocolate',100,180)
x.show:() # type: ignore

print()

y=Toy('figure',350,3)
y.show()