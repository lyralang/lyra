from llvmlite import ir


class LyraBaseType:
    llvm_base_type = None
    llvm_type = None
    bin_ops = ["+", "-", "/", "*"]
    bit_ops = [">>", "<<", "|", "&", "~"]
    bool_ops = ["==", "!=", ">", "<", "!"]

class LyraIntType(LyraBaseType):

    llvm_base_type = ir.IntType
    llvm_type = None

    def __init__(self, bits=64, signed=True):
        self.bits = bits
        self.signed = signed
        self.llvm_type = self.llvm_base_type(bits)

    def str_rep(self):
        rep = "i" if self.signed else "u"
        return f"{rep}{self.bits}"

    def as_pointer(self):
        return self.llvm_type.as_pointer()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.bits == other.bits and self.signed == other.signed

    def __repr__(self):
        rep = "i" if self.signed else "u"
        return f"<{self.__class__.__name__} ({rep}{self.bits})>"

class LyraBoolType(LyraIntType):
    bin_ops = []
    bit_ops = []
    bool_ops = ["==", "!=", "!"]

    def __init__(self):
        super().__init__(bits=1, signed=False)

    def str_rep(self):
        return "bool"

    def as_pointer(self):
        return self.llvm_type.as_pointer()

class LyraFloatType(LyraBaseType):

    llvm_base_type = ir.FloatType
    llvm_type = llvm_base_type()
    bit_ops = []

    def as_pointer(self):
        return self.llvm_type.as_pointer()

    def str_rep(self):
        return "f32"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.llvm_type == other.llvm_type

    def __repr__(self):
        return f"<{self.__class__.__name__} (f32)>"


class LyraDoubleType(LyraBaseType):

    llvm_base_type = ir.DoubleType
    llvm_type = llvm_base_type()
    bit_ops = []
    bool_ops = []

    def as_pointer(self):
        return self.llvm_type.as_pointer()

    def str_rep(self):
        return "f64"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.llvm_type == other.llvm_type

    def __repr__(self):
        return f"<{self.__class__.__name__} (f64)>"

class LyraArrayType(LyraBaseType):

    llvm_base_type = ir.ArrayType
    llvm_type = None
    bit_ops = []
    bool_ops = []
    bin_ops = []

    def __init__(self, elem, count):
        if not isinstance(elem, LyraBaseType):
            raise ValueError(f"Expected an instance of LyraBaseType")

        self.llvm_type = self.llvm_base_type(elem.llvm_type, count)
        self.elem = elem
        self.count = count

    def as_pointer(self):
        return self.llvm_type.as_pointer()

    def str_rep(self):
        return f"{self.elem.str_rep()}[{self.count}]"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.elem == other.elem and self.count == other.count

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.str_rep()})>"


class LyraVoidType(LyraBaseType):

    llvm_base_type = ir.VoidType
    llvm_type = llvm_base_type()
    bin_ops = []
    bit_ops = []
    bool_ops = []

    def as_pointer(self):
        return self.llvm_type.as_pointer()
    
    def str_rep(self):
        return "void"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

    def __repr__(self):
        return f"<{self.__class__.__name__} (void)>"

class LyraFunctionType(LyraBaseType):

    llvm_base_type = ir.FunctionType
    llvm_type = None
    bin_ops = []
    bit_ops = []
    bool_ops = []

    def __init__(self, ret, *args):
        """
        Instantiates a New llvm function type

        Args:
            ret (LyraBaseType): function return type
            args (List[LyraBaseType]): list of the function parameters
        """


        v_error = ValueError(f"Expected an instance of LyraBaseType")

        for i, typ in enumerate(args):
            if not isinstance(typ, LyraBaseType):
                raise v_error

        if not isinstance(ret, LyraBaseType):
            raise v_error

        self.args = args
        self.return_type = ret

    def str_rep(self):
        return f"def({','.join([x.str_rep() for x in self.args])}):{self.return_type.str_rep()}"

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.str_rep()})>"



class LyraPointerType(LyraBaseType):

    llvm_base_type = ir.PointerType
    llvm_type = None

    def __init__(self, lyra_type):
        if not isinstance(lyra_type, LyraBaseType):
            raise ValueError(f"Expected an instance of LyraBaseType")
        self.llvm_type = self.llvm_base_type(lyra_type.llvm_type)
        self.lyra_type = lyra_type

    def str_rep(self):
        return f"*{self.lyra_type.str_rep()}"

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.str_rep()})>"

class LyraStructType(LyraBaseType):

    llvm_base_type = ir.LiteralStructType
    llvm_type = None
    bin_ops = []
    bit_ops = []
    bool_ops = []

    def __init__(self, name, *args):
        m_types = []
        members = {}
        for k, v in args:
            if not isinstance(v, LyraBaseType):
                raise ValueError(f"Expected an instance of LyraBaseType")

            m_types.append(v.llvm_type)
            members[k] = v

        self.name = name
        self.args = args # need to know the order of the parameters
        self.members = members
        self.llvm_type = self.llvm_base_type(m_types)

    def str_rep(self):
        return f"{self.name}{{{','.join([f'{k}:{v.str_rep()}' for k,v in self.members.items()])}}}"

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.str_rep()})>"

class LyraObjectType(LyraBaseType):

    llvm_type = None
    bin_ops = []
    bit_ops = []
    bool_ops = []

    def __init__(self, struct_type):
        self.llvm_type = struct_type

    def str_rep(self):
        return f"object({self.llvm_type.str_rep()})"

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.str_rep()})>"
