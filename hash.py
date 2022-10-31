import os
import os.path
import binascii
import hashlib
import pickle
 
def CRC(filename):
    buf = open(filename,'rb').read()
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return "%08X" % buf

def MD5(filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()
    
inpt = ""
while inpt != "stop" and inpt != "2":
    print("\n1.Поставить на проверку новые каталоги.\n2.Посмотреть ранее записанные.")
    inpt = input()
    if inpt=="1":
        print("stop - закончить ввод директорий.\n")
        dct = {}
        inpt=input()
        while inpt != "stop":
            files = os.listdir(inpt)
            nameDir = inpt
            dct[nameDir]={}
            for i in files:
                if not (os.path.isdir(inpt+"/"+i)):
                    dct[nameDir][i]=[CRC(inpt+"/"+i),MD5(inpt+"/"+i)]
            inpt = input()
        with open('data.pickle', 'wb') as f:
            pickle.dump(dct, f)
    
nxt = ""
while nxt != "exit":
    with open('data.pickle', 'rb') as f:
        data_new = pickle.load(f)
    print("\n\n1.Проверка наличия всех файлов, записанных ранее из нашего каталога.\n",
          "2.Проверка на новые файлы в нашем каталоге.\n",
          "3.Проверка контрольной хеш-суммы наших файлов.\n",
          "4.Показать наши файлы, их хеш-суммы и CRC коды.\n",
          "exit - завершить работу программы.\n\n")
    nxt = input()
    if nxt=="1":
        ss = 0
        for i in data_new:
            lst = os.listdir(i)
            for j in data_new[i].items():
                if j[0] not in lst:
                    print(f"Файл {j[0]} не найден в каталоге {i} !")
                    ss+=1
        if ss==0:print("Все файлы на месте.")

    if nxt=="2":
        ss=0
        for i in data_new:
            lst = os.listdir(i)
            for j in lst:
                if j not in data_new[i].keys():
                    ss+=1
                    print(f"Обнаружен новый файл: {j} в каталоге {i}")
        if ss==0:print("Новых файлов не обнаружено.")
    
    if nxt =="3":
        ss=0
        for i in data_new:
            lst = os.listdir(i)
            for j in data_new[i].items():
                if j[0] in lst:
                    hashh = MD5(i+"/"+j[0])
                    if hashh != j[1][1]:
                        print(f"Хеш-сумма файла {j[0]} в каталоге {i} не",
                              "совпадает с ранее записанным.")
                        ss+=1
        if ss==0: print("Все хеш-суммы совпадают !")
    if nxt=="4":
        print("Файлы:")
        for i in data_new:
            print(i)
            for j in data_new[i].items():
                print(f"  {j}")
