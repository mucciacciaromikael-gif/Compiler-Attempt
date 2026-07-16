import ctypes
import errno
import sys

#from get_variable.checkDataTypes import checkType
#from get_variable.setValue import setValue

var :list = []
done :bool = False
errorCode :int = 0

class checkType:

    @staticmethod
    def is_int(x :str) -> int:
        match x:
            # signed integer
            case "int8": return -8
            case "int16": return -16
            case "int32": return -32
            case "int64": return -64
    
            # unsigned integer
            case "uint8": return 8
            case "uint16": return 16
            case "uint32": return 32
            case "uint64": return 64
        
    def is_float(x :str) -> int:
        match x:
            case "float8": return 8
            case "float16": return 16
            case "float32": return 32
            case "float64": return 64

class setValue:

    @staticmethod
    def set_int(code :list[str],i :int, signed :bool, array: int) -> None | int:
        global var
        global errorCode

        sign :str = "" if signed == False else "u"
        value :int = code[i + 4]

        if sign == "u" and int(value) < 0:
            print(f"this variable is unsigned, you cannot give it a negative value.\nname: {code[i+2]} value: {value}")
            errorCode = 22
            return 0

        new_var :dict = {"name": code[i + 2], "value": value, "signed": signed, "type": f"{sign}int{array}"}
        var.append(new_var)

with open('../input/test.mik', 'r') as file:
    line :list[str] = file.readlines()

    a :int = 0
    total_lines :int = len(line)

    while a < total_lines:
        # ignore blank lines
        if not line[a].strip():
            a += 1
            continue
        
        if errorCode != 0:
            match errorCode:
                case 22: sys.exit(errno.EINVAL)
                case 0: done = True

        code :list[str] = line[a].strip().split()

        #print(f"analysing line {a}: {code}")
        # ====== variables declaration and assignation ======

        # === integer declaration ===
        if code[0] == 'var' and done == True:
            done = False
            i :int = code.index('var')
            match checkType.is_int(code[1]):
                # if is signed
                case -8: setValue.set_int(code,i,False,8); done :bool = True
                case -16: setValue.set_int(code,i,False,16); done :bool = True
                case -32: setValue.set_int(code,i,False,32); done :bool = True
                case -64: setValue.set_int(code,i,False,64); done :bool = True

                # if is unsigned
                case 8: setValue.set_int(code,i,True,8); done :bool = True
                case 16: setValue.set_int(code,i,True,16); done :bool = True
                case 32: setValue.set_int(code,i,True,32); done :bool = True
                case 64: setValue.set_int(code,i,True,64); done :bool = True
            
        if code[-1] == ";" and done == True:
            print(f"{var[a]["name"]} = {var[a]["value"]}")
            a += 1
            continue

        elif code[-1] == "kill" and done == True:
            break
        
        a += 1