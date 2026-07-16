import ctypes

class setValue:
    
    def set_int(array :int, signed :bool, name :str, value :int) -> dict:
        sign :str = "" if signed == False else "u"
        return {"name": name, "type": f"{str(sign)}+int+{str(array)}", "value": value}