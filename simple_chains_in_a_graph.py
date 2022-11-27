dict = {}
print('''введите все соединения;
обозначения соединения через: запятую
разделитель: пробел
если соединение являеться грайнью написать через запятую любой символ''')
print("пример:")
print("1,2 2,3,r 1,3,d 1,6 3,4,r")
#обработка
for i in (input().split(" ")):
    i = i.split(",")
    try:
        if dict[i[0]] == "":
            pass
    except:
        dict[i[0]] = i[1] 
    else:
        dict[i[0]] = dict[i[0]] + "," + i[1]
    try:
        if i[2] != "":
            try:
                if dict[i[1]] == "":
                    pass
            except:
                dict[i[1]] = i[0] 
            else:
                dict[i[1]] = dict[i[1]] + "," + i[0]
    except:
        pass
#поиск всех возможных решений
start_end = input("введите точку начала и точку конца через запятую:").split(",")
print(dict)
y = []
x = dict[start_end[0]].split(",")
for i in x:
    if i != start_end[0]:
	    if i == start_end[1]:
	        print(start_end[0] + '-' + i +"∆")
	    else:
	        try:
	        	y.append([start_end[0] + '-' + i]+dict[i].split(","))
	        	print(start_end[0] + '-' + i + "✓")
	        except:
	        	print(start_end[0] + '-' + i + "X")
    else:
    	print("точка начала совпадает с точкой конца")

while True :
    if y == []:
    	break
    x = y
    y = []
    for i in x:
        test = 0
        loop = 0
        for j in i:
            if loop == 0:
                sequence = j
                loop += 1
            else:
                if j == start_end[1]:
                    test = 1              
                    print(sequence + '-' + j+'∆')
                else:
                    coincidence = 0
                    for i2 in sequence.split("-"):
                        if j == i2:
                            coincidence = 1
                            break
                    if coincidence == 0:
                       	 try:
                       	 	y.append([sequence + '-' + j]+dict[j].split(","))
                       	 	test = 1
                       	 	print(sequence + '-' + j + '✓')
                       	 except:
                       	 	test = 1
                       	 	print(sequence + '-' + j + 'X')
        if test == 0:
        	print(sequence + "-X")                     	 