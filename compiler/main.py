import ctypes # for the usage of data types like C
import errno  # error codes lib
import sys    # system lib

#from get_variable.checkDataTypes import checkType #other file 
#from get_variable.setValue import setValue #other file

var :list = []     # the list of variables in the given code
done :bool = False # help to know if an action is done or not (default = False)
errorCode :int = 0 # current error code

# class to check the type of a given variable
# I am trying to be as precise as possible
class checkType:

    @staticmethod
    def is_int(x :str) -> int:
        """
        This function detect if the given parameter (string) is an int
        It returns an integer corresponding to the size of the given param (negative if signed, positive if unsigned)
        """
        match x:
            # signed integer
            case "int8": return -8
            case "int16": return -16
            case "int32": return -32
            case "int64": return -64 # or long
    
            # unsigned integer
            case "uint8": return 8
            case "uint16": return 16
            case "uint32": return 32
            case "uint64": return 64 # or ulong
        
    def is_float(x :str) -> int:
        """
        Same thing then the previous one but with floats.
        But there is only signed value with this one
        """
        match x:
            case "float8": return 8
            case "float16": return 16
            case "float32": return 32
            case "float64": return 64 # or double

class setValue:

    @staticmethod
    def set_int(code :list[str],i :int, signed :bool, array: int) -> int | None:
        global var
        global errorCode

        """
        this function add an object (usually a dict) corresponding to the new var that was declared
        Given the index of the 'var' key-word and get the name, the value, if it signed, and the size.
        This function is just for ints and it throws and error code 22 if an signed integer is negative
        """

        sign :str = "" if signed == False else "u" # if it signed or not
        value :int = code[i + 4]                   # the value of the int

        # negative usigned integer error
        # if it is signed and the value is less than 0
        if sign == "u" and int(value) < 0: 
            print(f"this variable is unsigned, you cannot give it a negative value.\nname: {code[i+2]} value: {value}") # print an error
            errorCode = 22 # set the global errorCode to 22
            return 1       # stop the function

        new_var :dict = {"name": code[i + 2], "value": value, "signed": signed, "type": f"{sign}int{array}"} # create a new dict for the new int
        var.append(new_var) # adds it to the global list of variables

with open('../input/test.mik', 'r') as file: # test file
    line :list[str] = file.readlines()       # gives a list of the lines of the entire file

    a :int = 0                   # index of the current line that is being analyse
    total_lines :int = len(line) # total lines

    while a < total_lines: # continue while there is other lines to analyse
        # ignore blank lines
        if not line[a].strip():
            a += 1 
            continue # pass

        # check if there is an error
        # if there is, stop evrything !
        if errorCode != 0:
            match errorCode:
                case 22: sys.exit(errno.EINVAL) # error code 22
                case 0: done = True

        code :list[str] = line[a].strip().split() # transform the content of a line to a list

        #print(f"analysing line {a}: {code}") #debug
        # ====== variables declaration and assignation ======

        # === integer declaration ===
        if code[0] == 'var' and done == True: # if the first index is the variable declarater and the past action is done
            done = False                      # set the global done var as False to indicate that this action is not done
            i :int = code.index('var')        # index of the key-word 'var'
            match checkType.is_int(code[1]):
            
                # set the value and assigne the global done as True to indicate that this function is done
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

        # if the last index is a ';' and that the last action is done
        # go to the next line
        if code[-1] == ";" and done == True:
            print(f"{var[a]["name"]} = {var[a]["value"]}") # (debug) see the new variable added in the global list
            a += 1; done = False                           # go to the next line and reset the done variable
            continue 

        # if the last index is 'kill' and that the last action is done
        # stop the program
        elif code[-1] == "kill" and done == True:
            sys.exit(0) # evrything went fine :)
            break
        
        a += 1 # security
