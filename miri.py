with open("mbox-short.txt","r") as f:
    ls=f.readlines()
    for i in ls:
        if "@" in i:
            print(i.split("@")[-1])
            
            
