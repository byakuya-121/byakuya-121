#rage関数　For文
print("===============================================")

for x in range(1,10):
 for y in range(1,10):
    print(f'{x*y:2}',end='  ')
print()

print("===============================================")

#enumeratre 関数 
drink=['coffe','tea','juice']
for x in drink:
    print(x)
    #定義のdrinkのカッコ内にある文字列を順番に出す。
    
#Continue文 ・ループ内部にある残りを処理せずに次の処理を繰り返す　P229参照

catalog=[]
while len(catalog) < 3:
    item= input('item:' )
    if item in catalog:
        print(item,'is on the catalog.')
        continue
    catalog.append(item)
print ('catalog:',catalog)