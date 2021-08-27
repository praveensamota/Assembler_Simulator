#!/bin/bash
from sys import stdin
import matplotlib.pyplot as plt


a=[]


dict_var={}    # for store purposes key = mem address value = register
address=0

opc ={
        "00000": "add",
        "00001": "sub",
        "00010": "mov",
        "00011": "mov",
        "00100": "ld",
        "00101": "st",
        "00110": "mul",
        "00111": "div",
        "01000": "rs",
        "01001": "ls",
        "01010": "xor",
        "01011": "or",
        "01100": "and",
        "01101": "not",
        "01110": "cmp",
        "01111": "jmp",
        "10000": "jlt",
        "10001": "jgt",
        "10010": "je",
        "10011": "hlt",
    }

opctype = {
    "00000": "A",
    "00001": "A",
    "00110": "A",
    "01010": "A",
    "01011": "A",
    "01100": "A",
    "00010": "B",
    "01000": "B",
    "01001": "B",
    "00011": "C",
    "00111": "C",
    "01101": "C",
    "01110": "C",
    "00100": "D",
    "00101": "D",
    "01111": "E",
    "10000": "E",
    "10001": "E",
    "10010": "E",
    "10011": "F"}
 
Store_reg = {
    "000": "0",    # Store_reg[a]=Store_var[mem_addr]
    "001": "0", 
    "010": "0", 
    "011": "0",
    "100": "0",
    "101": "0",
    "110": "0",
    "111": "0000000000000000"}

def input():
    for line in stdin:
        line_strip=line.strip()

        a.append(line_strip)
      
            

def counterline(number): #returns optype and line 
    optype=None
    line=a[number]
    temp=line[0:5]  
    for i in opctype.keys():
        if temp==i:
            optype=opctype[i]

    
    return(optype,line)





def exeengine(type,line):
    jumps= 0
    address= ""
    change=[jumps,address]

    if type=="A":
        opcode=line[0:5]
        if opcode=="00000":     #add
            k1=line[10:13]
            k2=line[13:16]
            k3=line[7:10]
            b=int(Store_reg[k1])
            c=int(Store_reg[k2])
            a=str(b+c)
            if int(a)>65535:
                a1='{0:016b}'.format(int(a))
                k=a1[(len(a1)-16):len(a1)]
                q=int(k,2) 
                Store_reg[k3]=q
                Store_reg["111"]="0000000000001000"
            else:
                Store_reg[k3]=a
                Store_reg["111"]="0000000000000000"
            return change
        
        elif opcode=="00001":   #sub
            k1=line[10:13]  	#reg 2
            k2=line[13:16]      #reg 3
            k3=line[7:10]       #reg 1
            
            b=int(Store_reg[k1])
            c=int(Store_reg[k2])
            if b-c<0:        
                Store_reg[k3]="0"
                Store_reg["111"]="0000000000001000"

            else:

                a=str(b-c)
                Store_reg[k3]=a
                Store_reg["111"]="0000000000000000"
            return change

        elif opcode=="00110":    #mul   >>  <<  
            k1=line[10:13]
            k2=line[13:16]
            k3=line[7:10]
            b=int(Store_reg[k1])
            c=int(Store_reg[k2])
            a=str(b*c)
            if int(a)>65535:
                a1='{0:016b}'.format(int(a))
                k=a1[(len(a1)-16):len(a1)]
                q=int(k,2) 
                Store_reg[k3]=q
                Store_reg["111"]="0000000000001000"
            else:
                Store_reg[k3]=a
                Store_reg["111"]="0000000000000000"
            return change

        elif opcode=="01010": 
            k1=line[10:13]
            k2=line[13:16]
            k3=line[7:10]
            b=int(Store_reg[k1])
            c=int(Store_reg[k2])
            a=str(b^c)
            Store_reg[k3]=a
            Store_reg["111"]="0000000000000000"
            return change

        elif opcode=="01011":
            k1=line[10:13]
            k2=line[13:16]
            k3=line[7:10]
            b=int(Store_reg[k1])
            c=int(Store_reg[k2])
            a=str(b|c)
            Store_reg[k3]=a
            Store_reg["111"]="0000000000000000"
            return change

        elif opcode=="01100":
            k1=line[10:13]
            k2=line[13:16]
            k3=line[7:10]
            b=int(Store_reg[k1])
            c=int(Store_reg[k2])
            a=str(b&c)
            Store_reg[k3]=a
            Store_reg["111"]="0000000000000000"
            return change

    elif type=="B":
        opcode=line[0:5]
        if opcode=="00010":
            k1=line[5:8]
            k2=line[8:]
            a=int(k2,2)
            Store_reg[k1]=str(a)
            Store_reg["111"]="0000000000000000"
            return change
        
        if opcode=="01000":
            k1=line[5:8]
            i=int(str(line[8:]),2)
            Store_reg[k1]=int(int(Store_reg[k1])>>i)
            Store_reg["111"]="0000000000000000"
            return change

        if opcode=="01001":
            k1=line[5:8]
            i=int(str(line[8:]),2)
            Store_reg[k1]=int(int(Store_reg[k1])<<i)
            Store_reg["111"]="0000000000000000"
            return change



    elif type=="C":
        opcode=line[0:5]
        if opcode=="00011":
            k1=line[13:16]
            k2=line[10:13]
            a=int(Store_reg[k1])
            Store_reg[k2]=str(a)
            Store_reg["111"]="0000000000000000"
            return change
        
        elif opcode=="00111":
            k1=line[13:16]
            k2=line[10:13]
            a=int(Store_reg[k2])
            b=int(Store_reg[k1])
            c=str(int(a//b))
            d=str(int(a%b))
            Store_reg["000"]=c
            Store_reg["001"]=d
            Store_reg["111"]="0000000000000000"
            return change

        elif opcode=="01101":
            k1=line[13:16]
            k2=line[10:13]
            a=int(Store_reg[k1])
            Store_reg[k2]=str(~a)
            Store_reg["111"]="0000000000000000"
            return change

        elif opcode=="01110":   #compare
            k1=line[13:16]
            k2=line[10:13]
            a=int(Store_reg[k1])
            b=int(Store_reg[k2])
            if b>a:
                Store_reg["111"]="0000000000000010"
                return change
            elif b<a:
                Store_reg["111"]="0000000000000100"
                return change
            else:
                Store_reg["111"]="0000000000000001"
                return change


    elif type=="D":
        opcode=line[0:5]
        if opcode=="00101":
            k1=line[5:8]
            a=int(Store_reg[k1])
            dict_var[line[8:16]] = a
            Store_reg["111"]="0000000000000000"
            return change
        
        elif opcode=="00100":
            k1=line[5:8]
            Store_reg[k1]=dict_var[line[8:16]]
            Store_reg["111"]="0000000000000000"
            return change


    
    elif type=="E":
        opcode=line[0:5]
        if(opcode=="01111"):
            address=line[8:16]
            change[1]=int(address,2)-len(dict_var)
            change[0]=change[0]+1
            return change
        
        elif(opcode=="10000" and Store_reg["111"]=="0000000000000100"):
            address = line[8:16]
            change[1]=int(address,2)-len(dict_var)
            change[0]=change[0]+1
            Store_reg["111"]="0000000000000000"
            return change

        elif(opcode=="10001" and Store_reg["111"]=="0000000000000010"):
            address = line[8:16]
            change[1]=int(address,2)-len(dict_var)
            change[0]=change[0]+1
            Store_reg["111"]="0000000000000000"
            return change

        elif(opcode=="10010" and Store_reg["111"]=="0000000000000001"):
            address = line[8:16]
            change[1]=int(address,2)-len(dict_var)
            change[0]=change[0]+1
            Store_reg["111"]="0000000000000000"
            return change
        
        else:
            Store_reg["111"]="0000000000000000"
            return change
    
    elif type=="F":
        main.hlted=True
        Store_reg["111"]="0000000000000000"
        return change


def registers(number):
    a1='{0:08b}'.format(number)
    a2='{0:016b}'.format(int(Store_reg["000"]))
    a3='{0:016b}'.format(int(Store_reg["001"]))
    a4='{0:016b}'.format(int(Store_reg["010"]))
    a5='{0:016b}'.format(int(Store_reg["011"]))
    a6='{0:016b}'.format(int(Store_reg["100"]))
    a7='{0:016b}'.format(int(Store_reg["101"]))
    a8='{0:016b}'.format(int(Store_reg["110"]))
    a9=Store_reg["111"]
    print(a1,a2,a3,a4,a5,a6,a7,a8,a9)

    






def mem_dump(pc):      
    k=int(pc)
    pc=0
    main.hlted=False   
    while(k>pc):
        type, linenum=counterline(pc)
        
        jumps=0
        address=""
        change=[jumps,address]
        if (linenum == "1001100000000000"):
            main.hlted = True
        print(linenum)

        if change[0]==0:
            pc=pc+1
        else:
            pc=change[1]


            #variables dumping
    if len(dict_var)>0:
        for i,j in dict_var.items():
            ktemp='{0:016b}'.format(j)
            print(ktemp)

    for i in range(0, 256-k-len(dict_var)): 
        print("0000000000000000")

def main():
    input()
    
    pc=0
    cycle=0
    xcoordinates=[]
    ycoordinates=[]
    main.hlted=False 
    while(not main.hlted):
        
        type, linenum=counterline(pc)    #linenum here is line
        temp2=exeengine(type, linenum) 
        xcoordinates.append(cycle)
        ycoordinates.append(pc)
        registers(pc)
        if temp2[0]==0:                 # jump=1, address=mem_add
            pc=pc+1                 #
        else:
            pc=temp2[1]
        
        cycle+=1

    mem_dump(pc)
    plt.plot(xcoordinates,ycoordinates)
    plt.xlabel("Cycle Number")
    plt.ylabel("Memory Address")
    plt.title("Memory Address Trace")
    plt.show()
    plt.savefig("graph.png")




if __name__ == "__main__":
    main()







