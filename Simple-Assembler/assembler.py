#!/bin/bash
from sys import stdin

a=[]
x=0
y=0
linenum=0
temp_var=[]
dict_var={} 
address=0
allowed_chars=set(("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"))
halt=False
endvar=False
kw = ['add','sub','mul','xor','or','and','rs','ls','mov','div','not','cmp','ld','st','jmp','jlt','jgt','je','hlt']

lable_dict ={}

    



for line in stdin:
    linenum+=1
        
    stripped_line=line.strip()
    line_list=stripped_line.split()
    a.append(line_list)
    if len(line_list)==0:
        continue
    def label(o):
        
            
        for i in range(0,len(o)):
    
            if o[i][0]=='var':
                o.remove(o[0])
            else:
                break
        for i in range(0,len(o)):
            if o[i][0][-1]==':':
                label=o[i][0][:-1]
                addr='{0:08b}'.format(i)
                lable_dict.update({label:addr})
        return lable_dict
    
    if halt==True:
        print(str(linenum)+ ": Syntax Error: hlt instuction must be given in the end.")
        quit()

    if line_list[0]=='var' and endvar==True:
        print(str(linenum)+ ": Syntax Error: All variables must be declared at the beginning")
        quit()

    if line_list[0]=='var':
        if len(line_list)==1:
            print(str(linenum)+ ": Wrong instruction: variable name not defined")
            quit()
        
        characters=set((line_list[1]))
        if characters.issubset(allowed_chars):
            x=1

        if x!=1:
            print(str(linenum) + ": Invalid Variable Name")    
            quit()
            

        if line_list[1]=='var':
            print(str(linenum) + ": Variable name cannot be 'var'")
            quit()

        elif line_list[1] in temp_var:
            print(str(linenum) + ": Syntax Error: 2 or more variables cannot have the same name.")
            quit()
        
        elif line_list[1] in lable_dict.keys():
            print(str(linenum) + ": Syntax Error: variables and labels can't have same name")
            quit()

        elif line_list[1] in kw:
            print(str(linenum) + ":Syntax Error: Instruction Keywords can't be used as variables")
            quit()

        
        

        else:
            temp_var.append(line_list[1])


    elif line_list[0][-1]==':':
        endvar=True

        if len(line_list)==1:
            print(str(linenum)+ ": Wrong instruction: label name not defined")
            quit()

        labelchar=set((line_list[0][:-1]))
        if labelchar.issubset(allowed_chars):
            y=1

        if y!=1:
            print(str(linenum) + ": Invalid Label Name")    
            quit()
        if line_list[0][:-1] in temp_var:
            print(str(linenum)+ ":Syntax Error: Labels and variables can't have same name")
            quit()

        elif line_list[0][:-1] in kw:
            print(str(linenum)+ ":Syntax Error: Instruction keywords can't be used as labels")
            quit()
        
   

        else:
            label(a)
        if line_list[1]=='hlt':
           endvar=True
           halt=True
        address+=1
    
    else:
        if line_list[0]=='hlt':

            endvar=True
            halt=True
        endvar=True
        address+=1

if halt ==False:
    print(str(linenum)+ ":Syntax Error: Last instruction must be halt")
    quit()

for x in temp_var:
    dict_var[x]=[address,0]
    address+=1

if(address>257):
    print("Error: Number of instructions exceeds 256")
    quit()


    




for i in range (0,len(a)):
    if len(a[i])==0:
        continue 
    def registers(k):
        reg =[]
        var = k
        for j in range(1,len(a[i])):
            if a[i][j]=="R0":
                reg.append("000")
            if a[i][j]=="R1":
                reg.append("001")
            if a[i][j]=="R2":
                reg.append("010")
            if a[i][j]=="R3":
                reg.append("011")
            if a[i][j]=="R4":
                reg.append("100")
            if a[i][j]=="R5":
                reg.append("101")
            if a[i][j]=="R6":
                reg.append("110")
            if a[i][j]=="FLAGS":
                reg.append("111")
        return reg

    def opcode(word):
        opc={"add":"00000",
             "sub":"00001",
             "mov":tuple(["00010","00011"]),
             "ld":"00100",
             "st":"00101",
             "mul":"00110",
             "div":"00111",
             "rs":"01000",
             "ls":"01001",
             "xor":"01010",
             "or":"01011",
             "and":"01100",
             "not":"01101",
             "cmp":"01110",
             "jmp":"01111",
             "jlt":"10000",
             "jgt":"10001",
             "je":"10010",
             "hlt":"10011",}
        if word=='mov' and len(registers(a[i]))==1:
            p=opc.get("mov")
            x=p[0]
            return x
        if word=='mov' and len(registers(a[i]))!=1:
            p=opc.get("mov")
            x=p[1]
            return x
        else:
            x=opc.get(word)

        return x
    def typeA(g):

        if a[i][0][-1]==':':
            if((g[2][0]=='R' and g[3][0]=='R' and g[4][0]=='R')==0):
                print("Invalid Syntax: can't be implemented in this way")
                quit()
            elif(g[2][0]=='$'):
                print("Invalid Syntax: can't be implemented in this way")
                quit()
            else:
                z=opcode(g[1])
        else:
            if((g[1][0]=='R' and g[2][0]=='R' and g[3][0]=='R')==0):
                print("Invalid Syntax: Type A can't be interpreted in this way")
                quit()
            elif(g[2][0]=='$'):
                print("Invalid Syntax: can't be implemented in this way")
                quit()
            z=opcode(g[0])
        y=registers(g)
        code=z+"00"+y[0]+y[1]+y[2]
        print(code)
 
    
    
    def typeB(t):
        if((t[1][0]=='R' and t[1][1].isdecimal() and t[2][0]=='$' and t[2][1:].isdecimal())==0):
            print("Invalid Syntax: Type B can't be interpreted in this way")
            quit()

        if(t[2][0]=='$'):
            x=int(t[2][1:])
            if x<0 or x>255:
                print(str(i) + " : Immediate Value out of limits(0-255)")
                quit()
        z=opcode(t[0])
        y=registers(t)
        x=int(t[-1][1:])
        imm='{0:08b}'.format(x)
        code=z+y[0]+str(imm)
        print(code)
   
    def typeC(m):  
        if(m[1][0]=='R' and m[1][1].isdecimal() and ((m[2][0]=='R' and m[2][1].isdecimal())  or m[2]=='FLAGS')==0):
           print("Invalid Syntax: Type C can't be interpreted in this way")
           quit()
        z=opcode(m[0])
        y=registers(m)
        code=z+'00000'+y[0]+y[1]
        print(code)
    
    def typeD(p):
        if((p[1][0]=='R' and p[1][1].isdecimal())==0):
            print("Invalid Syntax: Type D can't be interpreted in this way")
            quit()

        if(p[2] not in dict_var.keys()):
            print(str(i+1)+" "+": Variable" +" "+ p[2]+ " "  + "not found")
            quit()
        z=opcode(p[0])
        y=registers(p)
        addtemp=dict_var[p[2]]
        li=addtemp[0]
        add1 ='{0:08b}'.format(li)
        
        code = z+y[0]+ str(add1)

        
        print(code)
        
        

    def typeE(q):
        if q[0]=='jmp' or q[0]=='jlt' or q[0]=='jgt' or q[0]=='je':
            z=opcode(q[0])
            


        x=label(a)
        if not x:
            print(str(i+1)+ ": Label not found")
            quit()
        else :    
            code=z+"000"+x.get(q[1])
        
        print(code)
    


    def typeF(n):
        if a[i][0][-1]==':':
            z=opcode(n[1])
        else:
            z=opcode(n[0])
        code=z+'00000000000'
        print(code)
    



    if a[i][0] not in kw:
        if a[i][0]!="var":
            if a[i][0][-1]!=":":
                if a[i][0]!="hlt":
                    print(str(i+1)+ ": given instruction is invalid")
                    quit()
    if a[i][0]=='add' or a[i][0]=='sub' or a[i][0]=='mul' or a[i][0]=='xor' or a[i][0]=='or' or a[i][0]=='and':
        typeA(a[i])
    

    if a[i][0]=="mov":
        if len(a[i])==1 or len(a[i])==2:
            print(str(i+1) + ": wrong instruction given (no operation provided)")
            quit()
        elif(a[i][0]=='mov' and a[i][1][0]=='R' and (a[i][2][0]=='R' or a[i][2][0]=='F')):
            typeC(a[i])
        elif a[i][0]=='mov' and a[i][1][0]=='R' and a[i][2][0]=='$':
             typeB(a[i])
        else:
            print(str(i+1)+ ": wrong instruction given")
            quit()

    if a[i][0]=='rs' or a[i][0]=='ls':
        typeB(a[i])
    if a[i][0]=='div' or a[i][0]=='not' or a[i][0]=='cmp':
        typeC(a[i])
    if a[i][0]=='ld' or a[i][0]=='st':
        typeD(a[i])
    if a[i][0]=='jmp' or a[i][0]=='jlt' or a[i][0]=='jgt' or a[i][0]=='je':
        typeE(a[i])
    if a[i][0]=='hlt':
        if len(a[i])!=1:
            print(str(i+1) + ": Wrong syntax used for instructions")
            quit()
        else:
            typeF(a[i])
    if a[i][0][-1]==':':
        if a[i][1]=='add' or a[i][1]=='sub' or a[i][1]=='mul' or a[i][1]=="and" or a[i][1]=='xor' or a[i][1]=='or':
            typeA(a[i]) 
        if a[i][1]=='div' or a[i][1]=='not' or a[i][1]=='cmp':
            typeC(a[i])
        if a[i][1]=='hlt':
            typeF(a[i])
