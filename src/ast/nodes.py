NODE_DEFAULT_FIELDS = {
    "source",
    "line",
    "column",
    "end_column"
}

class LyraNode:
    """
    Base class for Lyra AST nodes
    """

    __fields__ = NODE_DEFAULT_FIELDS

    def __init__(self, **kwargs):
        self._fields = set(self.__fields__).union(NODE_DEFAULT_FIELDS)

        for field in self._fields:
            if field in kwargs:
                setattr(self, field, kwargs[field])
            else:
                setattr(self, field, None)

    def to_dict(self):
        d = {k: self._to_dict(getattr(self, k, None)) for k in self.__fields__}
        d["nodeType"] = self.__class__.__name__
        return d

    def _to_dict(self, item):
        if isinstance(item, list):
            for i, it in enumerate(item):
                v = self._to_dict(it)
                item[i] = v
            return item
        elif isinstance(item, LyraNode):
            return item.to_dict()

        return item

    def __repr__(self):
        props = ", ".join([f"{k}={getattr(self, k, None)}" for k in self.__fields__ ])
        return f"{self.__class__.__name__}({props})"



class Module(LyraNode):
    __fields__ = ("body",)

class StructDef(LyraNode):
    __fields__ = ("target", "members")

class FunctionDef(LyraNode):
    __fields__ = ("type", "arglist", "target", "body")

class Statement(LyraNode):
    pass

class BreakStatement(Statement):
    __fields__ = ()

class PassStatement(Statement):
    __fields__ = ()

class ContinueStatement(Statement):
    __fields__ = ()

class ContinueStatement(Statement):
    __fields__ = ()

class ReturnStatement(Statement):
    __fields__ = ("expr",)

class BreakStatement(Statement):
    __fields__ = ()

class Declaration(Statement):
    __fields__ = ("target", "type", "value")

class Assign(Statement):
    __fields__ = ("target", "value")

class Block(LyraNode):
    __fields__ = ("expr", "body")

class IfBlock(Block):
    __fields__ = ("expr", "body", "orelse")

class WhileBlock(Block):
    pass

class UntilBlock(Block):
    pass

class Expression(LyraNode):
    pass

class GetAttribute(Expression):
    __fields__ = ("target", "attr")

class GetItem(Expression):
    __fields__ = ("target", "index")

class Call(Expression):
    __fields__ = ("target", "arglist")

class Name(Expression):
    __fields__ = ("value",)

class Constant(Expression):
    __fields__ = ("value",)

class Operation(Expression):
    __fields__ = ("op", "lhs", "rhs")

class List(LyraNode):
    __fields__ = ("arglist",)

class UnaryOp(Operation):
    pass

class BinaryOp(Operation):
    pass

class BooleanOp(Operation):
    pass

class CompareOp(BooleanOp):
    pass

class Number(Constant):
    __fields__ = ("value", "type")

class String(Constant):
    __fields__ = ("value", "type")

class Boolean(Constant):
    __fields__ = ("value",)

