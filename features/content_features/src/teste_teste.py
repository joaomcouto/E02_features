
a = "123#Olá minha nega"
a = "123#238"

for i in range(len(a)):
    if a[0].isalpha():
        print("funcionou")
        break
    else:
        a = a[1:]
        print(a)
        print("NOOO")
if not a:
    print("DEU RUIM")
else:
    print("DEU BOM")
print("a: =",a)
