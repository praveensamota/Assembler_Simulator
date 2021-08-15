#!/bin/bash
from sys import stdin
a=[]
linenum=0
temp_var=[]
dict_var={} #dict_var is a dictionary which takes key as variable names and value as addresses of variable.
address=0
halt=False
endvar=False
kw = ['add','sub','mul','xor','or','and','rs','ls','mov','div','not','cmp','ld','st','jmp','jlt','jgt','je','hlt'] #list of keywords we've to use in the program accordingly

lable_dict ={} #label_dic is a dictionary which takes key as lable names and value as addresses of lable.

    



for line in stdin:
    linenum+=1
        
    stripped_line=line.strip()
    line_list=stripped_line.split()
    a.append(line_list)
    def label(o): # This function is a global function and is used to fetch the label and their addresses.
        
        for i in range(0,len(o)):
            if o[0][0]=='var':
                o.remove(o[0])
            else:
                break
        for i in range(0,len(o)):
            if o[i][0][-1]==':':
                label=o[i][0][:-1]
                addr='{0:08b}'.format(i)
                lable_dict.update({label:addr})
        return lable_dict
    label(a)
    if halt==True:
        print(str(linenum)+ ": Syntax Error: hlt instuction must be given in the end.")
        quit()

    if line_list[0]=='var' and endvar==True:
        print(str(linenum)+ ": Syntax Error: All variables must be declared at the beginning")
        quit()

    if line_list[0]=='var':
        if line_list[1] in temp_var:
            print(str(linenum) + ": Syntax Error: 2 or more variables cannot have the same name.")
            quit()
        
        if line_list[1] in lable_dict.keys():
            print(str(linenum) + ": Syntax Error: variables and labels can't have same name")
            quit()

        elif line_list[1] in kw:
            print(str(linenum) + ":Syntax Error: Instruction Keywords can't be used as variables")
            quit()

        else:
            temp_var.append(line_list[1])


    elif line_list[0][-1]==':':
        endvar=True

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

    def registers(k): # This function returns a list of binary numbers accordance to the registers used.Takes one parameter.
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

    def opcode(word):  # This is a kind of helper function which has a opcode dictionary embedded in it with key as the parameter word and value as opcode.Takes only one parameter.
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
        
    def typeA(g): # This function is made exclusively for creating a type A machine code.

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
 
    
    
    def typeB(t):  # This function is made exclusively for creating a type B machine code.
        if((t[1][0]=='R' and t[1][1].isdecimal() and t[2][0]=='$' and t[2][1:].isdecimal())==0):
            print("Invalid Syntax: Type B can't be interpreted in this way")
            quit()

        if(t[2][0]=='$'):
            x=int(t[2][1:])
            if x<0 or x>255:
                print("Syntax: Immediate Value out of limits(0-255)")
                quit()
        z=opcode(t[0])
        y=registers(t)
        x=int(t[-1][1:])
        imm='{0:08b}'.format(x)
        code=z+y[0]+str(imm)
        print(code)
   
    def typeC(m):  # This function is made exclusively for creating a type C machine code.
        if(m[1][0]=='R' and m[1][1].isdecimal() and ((m[2][0]=='R' and m[2][1].isdecimal())  or m[2]=='FLAGS')==0):
           print("Invalid Syntax: Type C can't be interpreted in this way")
           quit()
        z=opcode(m[0])
        y=registers(m)
        code=z+'00000'+y[0]+y[1]
        print(code)
    
    def typeD(p):  # This function is made exclusively for creating a type D machine code.
        if((p[1][0]=='R' and p[1][1].isdecimal())==0):
            print("Invalid Syntax: Type D can't be interpreted in this way")
            quit()

        if(p[2] not in dict_var.keys()):
            print("Variable" +" "+ p[2]+ " "  + "not found")
            quit()
        z=opcode(p[0])
        y=registers(p)
        addtemp=dict_var[p[2]]
        li=addtemp[0]
        add1 ='{0:08b}'.format(li)
        
        code = z+y[0]+ str(add1)
        print(code)
        
        

    def typeE(q):  # This function is made exclusively for creating a type E machine code.
        if q[0]=='jmp' or q[0]=='jlt' or q[0]=='jgt' or q[0]=='je':
            z=opcode(q[0])

        x=label(a)
        code=z+"000"+x.get(q[1])
        print(code)
    
    def typeF(n): # This function is made exclusively for creating a type F machine code.
        if a[i][0][-1]==':':
            z=opcode(n[1])
        else:
            z=opcode(n[0])
        code=z+'00000000000'
        print(code)
    

#below if-else statements are used to call the respective fuctions accordingly 

    if a[i][0]=='add' or a[i][0]=='sub' or a[i][0]=='mul' or a[i][0]=='xor' or a[i][0]=='or' or a[i][0]=='and':
        typeA(a[i])
    

    if a[i][0]=='mov' and a[i][1][0]=='R' and (a[i][2][0]=='R' or a[i][2][0]=='F'):
        typeC(a[i])
    if a[i][0]=='mov' and a[i][1][0]=='R' and a[i][2][0]=='$':
        typeB(a[i])
    if a[i][0]=='rs' or a[i][0]=='ls':
        typeB(a[i])
    if a[i][0]=='div' or a[i][0]=='not' or a[i][0]=='cmp':
        typeC(a[i])
    if a[i][0]=='ld' or a[i][0]=='st':
        typeD(a[i])
    if a[i][0]=='jmp' or a[i][0]=='jlt' or a[i][0]=='jgt' or a[i][0]=='je':
        typeE(a[i])
    if a[i][0]=='hlt':
        typeF(a[i])
        
#below if-else statement is used to call function in which label is read first.

    if a[i][0][-1]==':':
        if a[i][1]=='add' or a[i][1]=='sub' or a[i][1]=='mul':
            typeA(a[i]) 
        if a[i][1]=='div' or a[i][1]=='not' or a[i][1]=='cmp':
            typeC(a[i])
        if a[i][1]=='hlt':
            typeF(a[i])
