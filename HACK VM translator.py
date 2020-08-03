s = input()
with open(s + ".vm", "r") as fileread:
    filer = fileread.readlines()
    num = -2
    k = -1
    index = ""
with open(s + ".asm", "w") as hfile:
    for lin in filer:
        line = lin.split("//")
        line = line[0].split()
        if len(line) != 0:
            hfile.write("//" + str(line)+"\n")
            cmd = line[0]
            i = 0
            if len(line) == 1:
                if (cmd == "add") or (cmd == "sub") or (cmd == "and") or (cmd == "or"):
                    hfile.write("@SP\nA=M\nA=A-1\nD=M\nA=A-1\n")
                    if cmd == "add":
                        hfile.write("M=M+D\n")
                    elif cmd == "sub":
                        hfile.write("M=M-D\n")
                    elif cmd == "and":
                        hfile.write("M=M&D\n")
                    elif cmd == "or":
                        hfile.write("M=M|D\n")
                    hfile.write("@SP\nM=M-1\n")
                elif (cmd == "neg") or (cmd == "not"):
                    hfile.write("@SP\nA=M\nA=A-1\n")
                    if cmd == "neg":
                        hfile.write("M=-M\n")
                    elif cmd == "not":
                        hfile.write("M=!M\n")
                elif (cmd == "eq") or (cmd == "lt") or (cmd == "gt"):
                    num += 2
                    hfile.write("@SP\nA=M\nA=A-1\nD=M\nA=A-1\nD=M-D\n@ALabel_" + str(num) + "\nD;J")
                    if cmd == "eq":
                        hfile.write("EQ\n")
                    elif cmd == "lt":
                        hfile.write("LT\n")
                    elif cmd == "gt":
                        hfile.write("GT\n")
                    hfile.write(
                        "D=0\n@ALabel_" + str(num + 1) + "\n0;JMP\n(ALabel_" + str(num) + ")\nD=-1\n(ALabel_" + str(
                            num + 1) + ")\n@SP\nM=M-1\nA=M\nA=A-1\nM=D\n")
                elif cmd == "return":
                    hfile.write("@LCL\nD=M\n@R14\nM=D\n@5\nD=D-A\nA=D\nD=M\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@ARG\nM=D\nD=A+1\n@SP\nM=D\n@R14\nD=M\nA=D-1\nD=M\n@THAT\nM=D\n@R14\nD=M\nA=D-1\nA=A-1\nD=M\n@THIS\nM=D\n@R14\nD=M\nA=D-1\nA=A-1\nA=A-1\nD=M\n@ARG\nM=D\n@R14\nD=M\nA=D-1\nA=A-1\nA=A-1\nA=A-1\nD=M\n@LCL\nM=D\n@R13\nA=M\n0;JMP\n")

            elif len(line) == 2:
                if line[0] == "label":
                    hfile.write("(" + str(line[1]) + ")\n")
                elif line[0] == "goto":
                    hfile.write("@" + str(line[1]) + "\n0;JMP\n")
                elif line[0] == "if-goto":
                    hfile.write("@SP\nM=M-1\nA=M\nD=M\n@" + str(line[1]) + "\nD;JNE")

            elif len(line) == 3:
                seg = line[1]
                index = str(line[2])
                if (cmd == "pop") or (cmd == "push"):

                    if cmd == "push":
                        if seg == "static":
                            hfile.write("@xxx." + index + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
                        else:
                            if seg == "constant":
                                hfile.write("@" + index + "\nD=A\n")
                            else:
                                if seg == "argument":
                                    hfile.write("@ARG\nD=M\n")
                                elif seg == "temp":
                                    hfile.write("@5\nD=A\n")
                                elif seg == "pointer":
                                    hfile.write("@3\nD=A\n")
                                elif seg == "local":
                                    hfile.write("@LCL\nD=M\n")
                                elif seg == "this":
                                    hfile.write("@THIS\nD=M\n")
                                elif seg == "that":
                                    hfile.write("@THAT\nD=M\n")
                                hfile.write("@" + index + "\nA=A+D\nD=M\n")
                            hfile.write("@SP\nA=M\nM=D\n@SP\nM=M+1\n")
                    elif cmd == "pop":
                        if seg == "static":
                            hfile.write("@SP\nA=M\nA=A-1\nD=M\n@xxx." + index + "\nM=D\n@SP\nM=M-1\n")
                        else:
                            if seg == "constant":
                                print("error in pop statement")
                            else:
                                if seg == "argument":
                                    hfile.write("@ARG\nD=M\n")
                                elif seg == "temp":
                                    hfile.write("@5\nD=A\n")
                                elif seg == "pointer":
                                    hfile.write("@3\nD=A\n")
                                elif seg == "local":
                                    hfile.write("@LCL\nD=M\n")
                                elif seg == "this":
                                    hfile.write("@THIS\nD=M\n")
                                elif seg == "that":
                                    hfile.write("@THAT\nD=M\n")
                                hfile.write("@" + index + "\nD=A+D\n@R13\nM=D\n")
                            hfile.write("@SP\nA=M\nA=A-1\nD=M\n@R13\nA=M\nM=D\n@SP\nM=M-1\n")
                elif cmd == "call":
                    hfile.write("@"+seg + "_return_index\nD=A\n@SP\nAM=M+1\nA=A-1\nM=D\n@LCL\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n@ARG\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n@THIS\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n@THAT\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n@SP\nD=M\n@5\nD=D-A\n@"+index+"\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@"+seg+"\n0;JMP\n"+"("+seg+"_return_index)")

                elif cmd == "function":
                    hfile.write("("+seg+")\n@SP\nD=M\n@LCL\nM=D\n@"+index+"\nD=A\n("+seg+"-loop)\n@"+seg+"-end\nD;JEQ\n@SP\nAM=M+1\nA=A-1\nM=0\nD=D-1\n@"+seg+"-loop\n0;JMP\n("+seg+"-end)\n")