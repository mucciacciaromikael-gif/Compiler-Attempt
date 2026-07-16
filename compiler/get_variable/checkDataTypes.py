import ctypes

class checkType:

    def is_int(inp: str | int) -> int:
        match inp:
            # signed integer
            case "int8": return 8
            case "int16": return 16
            case "int32": return 32
            case "int64": return 64

            # unsigned integer
            case "uint8": return -8
            case "uint16": return -16
            case "uint32": return -32
            case "uint64": return -64
    
    def is_float(inp :str | float) -> int:
        match inp:
            case "float8": return 8
            case "float16": return 16
            case "float32": return 32
            case "float64": return 64