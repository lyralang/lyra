# Typed Lyra: static typechecker

from lyra.types import *
from lyra.ast.nodes import *

# This is very close to WebAssembly (WASM). 
# Take a look at AssemblyScript
# There might be a WASM to LLVM shortcut.
PRIMITIVES = {
    "i32": LyraIntType(32),
    "i64": LyraIntType(64),
    "bool": LyraBoolType(),
    "char": LyraIntType(8),
    "void": LyraVoidType(),
    "f32": LyraFloatType(),
    "f64": LyraDoubleType()
}


class LyraTypeChecker:

    def __init__(self, module, source):
        self.module = module
        self.source = source.split("\n")
        self.types_def = PRIMITIVES
        self.func_def = {}
        
        for node in module:
            self.visit(node, {})

    def visit(self, node, s_locals):
        """
        Calls the right visit function for `node`

        Args:
            node (ast.LyraNode): target lyra node
            s_locals (dict): local variables

        Returns:
            lyra_type (types.LyraBaseType)
        """

        lyra_type = None

        if isinstance(node, FunctionDef):
            lyra_type = self.visit_function(node)
            
        elif isinstance(node, Call):
            lyra_type = self.visit_call(node, s_locals)
        
        elif isinstance(node, Name):
            lyra_type = self.visit_name(node, s_locals)

        elif isinstance(node, Number):
            lyra_type = self.visit_number(node)

        elif isinstance(node, Declaration):
            lyra_type = self.visit_declaration(node, s_locals)

        elif isinstance(node, IfBlock) or isinstance(node, WhileBlock) or isinstance(node, UntilBlock):
            self.visit_cond_block(node, s_locals)

        elif isinstance(node, CompareOp):
            lyra_type = self.visit_boolop(node, s_locals)

        elif isinstance(node, BinaryOp):
            lyra_type = self.visit_binop(node, s_locals)

        elif isinstance(node, UnaryOp):
            lyra_type = self.visit_uop(node, s_locals)

        elif isinstance(node, Assign):
            lyra_type = self.visit_assign(node, s_locals)

        elif isinstance(node, List):
            lyra_type = self.visit_list(node, s_locals)

        elif isinstance(node, GetItem):
            lyra_type = self.visit_getitem(node, s_locals)

        elif isinstance(node, StructDef):
            lyra_type = self.visit_struct(node)

        elif isinstance(node, GetAttribute):
            lyra_type = self.visit_attr(node, s_locals);

        elif isinstance(node, ReturnStatement):
            lyra_type = self.visit_return(node, s_locals)

        setattr(node, "lyra_type", lyra_type)
        return lyra_type

    def visit_return(self, node, s_locals):
        """
        Check for `ast.nodes.ReturnStatement`

        Args:
            node (lyra.ast.nodes.ReturnStatement): target lyra node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraBaseType): type of `node.expr`
        """

        lyra_type = None

        if node.expr is None:
            return self.types_def["void"]

        lyra_type = self.visit(node.expr, s_locals)
        return lyra_type

    def visit_struct(self, node):
        """
        Check for `lyra.ast.nodes.StructDef`

        Args:
            node (ast.nodes.StructDef): target lyra struct node

        Returns:
            lyra_type (lyra.types.LyraStructType)
        """
        target = node.target
        members = node.members

        if target.value in self.types_def:
            self.error(f"Type `{target.value}`already exists", target)

        arglist = []
        for name, typ in members:
            typ = self._type_exists(typ)
            arglist.append((name.value, typ))

        s_type = LyraStructType(target.value, *arglist)
        self.types_def[target.value] = s_type
        return s_type

    def visit_getitem(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.GetItem`

        Args:
            node (ast.nodes.GetItem): target lyra node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraBaseType): expression type
        """

        target = node.target
        t_type = self.visit(target, s_locals)

        if not isinstance(t_type, LyraArrayType):
            self.error(f"Expected an array but got `{t_type.str_rep()}`")
        return t_type.elem

    def visit_attr(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.GetAttribute`

        Args:
            node (ast.nodes.GetAttribute): target lyra node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraBaseType): expression type
        """

        t_type = self.visit(node.target, s_locals)
        attr = node.attr

        if not hasattr(t_type, "members"):
            self.error(f"`{t_type.str_rep()}` does not have the attribute `{attr.value}`")

        if attr.value not in t_type.members:
            self.error(f"`{t_type.str_rep()}` does not have the attribute `{attr.value}`")

        return t_type.members[attr.value]

    def visit_list(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.List`

        Args:
            node (ast.nodes.List): target lyra `List` node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraArrayType): lyra array type
        """

        items = node.arglist

        i_type = None
        for i in items:
            if i_type is None:
                i_type = self.visit(i, s_locals)
            else:
                _i_type = self.visit(i, s_locals)

                if i_type != _i_type:
                    self.error(f"Expected element of type `{i_type.str_rep()}` but got `{_i_type.str_rep()}`", i)

        return LyraArrayType(i_type, len(items))

    def visit_assign(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.Assign`

        Args:
            node (ast.nodes.Assign): target lyra `Assign` node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraBaseType): variable value type
        """

        target = node.target
        val = node.value
        t_type = None

        if isinstance(target, Name) or isinstance(target, GetItem) or isinstance(target, GetAttribute):
            t_type = self.visit(target, s_locals)
        else:
            self.error("Invalid assignment", target)

        v_type = self.visit(val, s_locals)

        if not(t_type == v_type):
            self.error(f"Expected type `{t_type.str_rep()}` but got `{v_type.str_rep()}`", val)

        return t_type

    def visit_comp(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.CompareOp`

        Args:
            node (ast.nodes.CompareOp): target lyra `CompareOp` node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraBoolType): lyra boolean type
        """

        lhs = node.lhs
        rhs = node.rhs

        lhs_type = self.visit(lhs, s_locals)
        rhs_type = self.visit(rhs, s_locals)

        if not (lhs_type == rhs_type):
            self.error(f"Operation on different types (`{lhs_type.str_rep()}` {node.op} `{rhs_type.str_rep()}`)", lhs)

        typ = LyraBoolType()
        return LyraBoolType()

    def visit_boolop(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.BooleanOp`

        Args:
            node (ast.nodes.BooleanOp): target lyra `BooleanOp` node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraBoolType): lyra boolean type
        """

        return self.visit_comp(node, s_locals)

    def visit_uop(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.UnaryOp`

        Args:
            node (ast.nodes.UnaryOp): target lyra `UnaryOp` node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraBaseType): lyra type
        """

        lhs = node.lhs
        lhs_type = self.visit(lhs, s_locals)

        if node.op == "*": # For pointer
            return LyraPointerType(lhs_type)
        elif node.op == "&": # For deferencing
            if not isinstance(lhs_type, LyraPointerType):
                self.error(f"Expected a pointer but got `{lhs_type.str_rep()}`", node)
            return lhs_type.lyra_type

        if node.op not in lhs_type.bin_ops + lhs_type.bit_ops:
            self.error(f"Invalid operator `{node.op}` on type `{lhs_type.str_rep()}`", lhs)

        return lhs_type

    def visit_binop(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.BinaryOp`

        Args:
            node (ast.nodes.BinaryOp): target lyra `BinaryOp` node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraBaseType): lyra type
        """

        lhs = node.lhs
        rhs = node.rhs

        lhs_type = self.visit(lhs, s_locals)
        rhs_type = self.visit(rhs, s_locals)

        if not (lhs_type == rhs_type):
            self.error(f"Operation on different types (`{lhs_type.str_rep()}` {node.op} `{rhs_type.str_rep()}`)", lhs)

        if node.op not in lhs_type.bin_ops + lhs_type.bit_ops:
            self.error(f"Invalid operator `{node.op}` on type `{lhs_type.str_rep()}`", lhs)

        return lhs_type

    def visit_number(self, node):
        """
        Check for `lyra.ast.nodes.Number`

        Args:
            node (ast.nodes.Number): target lyra `Number` node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraBaseType): lyra type
        """

        _type = node.type

        if _type in ["DEC_NUMBER", "HEX_NUMBER", "OCT_NUMBER", "BIN_NUMBER"]:
            typ = self.types_def["i32"]
        elif _type == "FLOAT_NUMBER":
            typ = self.types_def["f32"]

        return typ

    def visit_name(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.Name`

        Args:
            node (ast.nodes.Name): target lyra `Name` node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraBaseType): lyra type
        """

        n_str = node.value
        v_type = s_locals.get(n_str)

        if v_type is None:
            self.error(f"Identifier `{n_str}` is undefined", node)
        return v_type


    def visit_declaration(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.Declaration`

        Args:
            node (ast.nodes.Declaration): target lyra `Declaration` node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraBaseType): variable type
        """

        target = node.target.value
        value = node.value

        type = self._type_exists(node.type)

        if target in s_locals:
            self.error(f"Identifier `{target}` is already defined", node.target)

        if value is None:
            s_locals[target] = type
            return type

        val_type = self.visit(value, s_locals)

        if not (type == val_type):
            self.error(f"Expected type `{type.str_rep()}` but got `{val_type.str_rep()}`", value)

        s_locals[target] = type
        return type

    def visit_call(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.Call`

        Args:
            node (ast.nodes.Call): target lyra `Call` node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraBaseType): function return type
        """

        target = node.target
        arglist = node.arglist or []

        _lyra_args = []

        for n in arglist:
            _lyra_args.append(self.visit(n, s_locals))
        
        if isinstance(target, Name):
            _args = ",".join(arg.str_rep() for arg in _lyra_args)
            func_sig = f"{target.value}({_args})"

            if func_sig not in self.func_def:
                if target.value in self.types_def:
                    return self.visit_obj(node, s_locals)

                self.error(f"Unknown function with signature `{func_sig}`", target)

        func = self.func_def[func_sig]
        return func.return_type

    def visit_obj(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.Call` for a new struct
        instance

        Args:
            node (ast.nodes.Call): target lyra `Call` node
            s_locals (dict): local variables

        Returns:
            lyra_type (lyra.types.LyraObjectType): lyra object type
        """

        target = node.target
        arglist = node.arglist or []
        struct_ = self.types_def[target.value]

        if len(arglist) < 1:
            return struct_

        s_args = struct_.args

        if len(arglist) != len(s_args):
            self.error(f"Expected `{len(s_args)}` arguements but got `{len(arglist)}`", target)

        for i, a in enumerate(arglist):
            typ = self.visit(a, s_locals)
            name, s_typ = s_args[i]
            if not (typ == s_typ):
                self.error(f"Expected type `{s_type.str_rep()}` but got `{s_type.str_rep()}` for ({name})", arglist[i])
        
        return struct_

    def visit_function(self, node):
        """
        Check for `lyra.ast.nodes.FunctionDef` new function
        declaration

        Args:
            node (ast.nodes.Call): target lyra `Call` node

        Returns:
            lyra_type (lyra.types.LyraFunctionType): lyra function type
        """

        return_type = node.type
        arglist = node.arglist or []
        func_name = node.target.value
        body = node.body

        exists = []
        _lyra_ret = self._type_exists(return_type)
        _lyra_params = []
        
        func_locals = {}

        for name, typ in arglist:
            name_str = name.value

            if name_str in exists:
                self.error(f"Arguement `{name_str}` appears more than once", name)
            else:
                exists.append(name_str)
            
            v_type = self._type_exists(typ)
            _lyra_params.append(v_type)
            func_locals[name_str] = v_type

        func_typ =  LyraFunctionType(_lyra_ret, *_lyra_params)
        _params = ",".join(p.str_rep() for p in _lyra_params)
        func_sig = f"{func_name}({_params})"

        self.func_def[func_sig] = func_typ

        for node in body:
            self.visit(node, func_locals)

        return func_typ

    def visit_cond_block(self, node, s_locals):
        """
        Check for `lyra.ast.nodes.Block` (while-loops, until-loops, if-else)

        Args:
            node (ast.nodes.Block): target lyra `Block` node

        """

        cond = node.expr

        cond_type = self.visit(cond, s_locals)

        if cond_type != LyraBoolType():
            self.error(f"Expected a boolean but got `{cond_type.str_rep()}`", cond)

        body = node.body
        _locals = dict(s_locals) # copying previous locals
        for n in body:
            self.visit(n, _locals)

        if hasattr(node, "orelse"): # if-else block
            orelse = node.orelse
            _locals = dict(s_locals)

            if isinstance(orelse, list):
                for n in orelse:
                    self.visit(n, _locals)
            else:
                self.visit(orelse, _locals)

    def _type_exists(self, node):
        """
        Checks if the type infered in `node` exists

        Args:
            node (ast.nodes.LyraNode): target lyra node

        Return:
            lyra_type (lyra.types.LyraBaseType): lyra type
        """

        if node is None:
            return self.types_def["void"]

        if isinstance(node, Name):
            n_str = node.value

            if n_str not in self.types_def:
                self.error(f"Unknown datatype `{n_str}`", node)
            return self.types_def[n_str]
        
        elif isinstance(node, GetItem):
            n_type = self._type_exists(node.target)
            index = node.index
            if not isinstance(index, Number):
                self.error("Expected an integer constant", index)

            count = int(index.value)
            arr_type = LyraArrayType(n_type, count)
            return arr_type
        
        elif isinstance(node, UnaryOp):
            if node.op != "*":
                self.error(f"Invalid unary operation `{node.op}`", node)
            lhs = node.lhs
            typ = self._type_exists(lhs)
            return LyraPointerType(typ)

    def error(self, msg, node):
        """
        Lyra custom error

        Args:
            node (ast.nodes.LyraNode): target lyra node
        """

        line = node.line
        col = node.column
        col_end = node.end_column

        line_source = self.source[line-1]
        fname = "<filename>"
        err_msg = f"{fname}:{line}:{col} "
        err_msg += msg + "\n"
        err_msg += line_source + "\n"
        err_msg += " "*(col-1) + ("^"*(col_end-col))
        print(err_msg)
        exit(1)
