import sys
from lark import Transformer, Tree, Token
from lyra.ast.nodes import *

transformer_module = sys.modules[__name__]


class LyraTransformer(Transformer):

    def module(self, node):
        return node

    def struct_def(self, node):
        target, *members = node
        return self.init_node(
            StructDef,
            target,
            target=target,
            members=members
        )

    def struct_member(self, node):
        return node

    def function_sig(self, node):
        fname, fparams, fret = node
        return (fname, fparams, fret)
    
    def function_def(self, node):
        sig, body = node
        target, arglist, _type = sig
        
        return self.init_node(
            FunctionDef,
            target,
            type=_type,
            arglist=arglist,
            target=target,
            body=body
        )

    def parameters(self, nodes):
        return nodes
    
    def parameter(self, node):
        return node
        
    def type(self, node):
        return node[0]
    
    def if_stmt(self, node):
        else_block = None
        node.reverse()

        for block in node:
            if len(block if block else []) == 2:
                # means it has a condition i.e if or elif block
                cond, body = block
                else_block = self.init_node(
                    IfBlock, cond, expr=cond, body=body, orelse=else_block
                )
            elif block:
                else_block = block[0]

        return else_block

    def while_stmt(self, node):
        cond, body = node
        return self.init_node(WhileBlock, cond, expr=cond, body=body)

    def until_stmt(self, node):
        cond, body = node
        return self.init_node(UntilBlock, cond, expr=cond, body=body)
    
    def continue_stmt(self, node):
        return self.init_node(ContinueStatement, node[0])

    def break_stmt(self, node):
        return self.init_node(BreakStatement, node[0])

    def return_stmt(self, node):
        return self.init_node(ReturnStatement, node[0], expr=node[1])
    
    def pass_stmt(self, node):
        return self.init_node(PassStatement, node[0])

    def default_exec(self, node):
        return node

    def cond_exec(self, node):
        return node

    def variable(self, node):
        return node

    def declaration(self, node):
        (target, _type), value = node
        return self.init_node(
            Declaration,
            target,
            target=target,
            type=_type,
            value=value
        )

    def body(self, node):
        return list(filter(None, node))

    def stmt(self, node):
        return node[0]

    def call(self, node):
        target, arglist = node
        return self.init_node(
            Call,
            target,
            target=target,
            arglist=arglist
        )
    
    def arguments(self, node):
        return node
    
    def kwarg(self, node):
        return node

    def get_item(self, node):
        target, index = node
        return self.init_node(
            GetItem,
            node=target,
            target=target,
            index=index
        )
    
    def get_attr(self, node):
        target, attr = node
        return self.init_node(
            GetAttribute,
            target,
            target=target,
            attr=attr
        )
    def assign(self, node):
        target, val = node
        return self.init_node(
                Assign,
                target,
                target=target,
                value=val
        )

    def expr(self, node):
        return node[0]
    
    def get_var(self, node):
        return node[0]

    def setup_list(self, node):
        return node[0]

    def list(self, node):
        node = node or []

        if len(node) < 1:
            return

        return self.init_node(List, node[0], arglist=node)

    def number(self, node):
        n = node[0]
        return self.init_node(Number, n, value=n.value, type=n.type)
    
    def string(self, node):
        n = node[0]
        return self.init_node(String, n, value=n.value, type=n.type)

    def NAME(self, node):
        return self.init_node(Name, node, value=node.value)

    # ------------------------------------------
    #    Boolean operators
    # ------------------------------------------

    def _or(self, node):
        op = "||"
        lhs, rhs = node
        return self.init_node(BooleanOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def _and(self, node):
        op = "&&"
        lhs, rhs = node
        return self.init_node(BooleanOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def _not(self, node):
        op = "!"
        lhs = node
        return self.init_node(BooleanOp, lhs, op=op, lhs=lhs, rhs=None)

    def lt(self, node):
        op = "<"
        lhs, rhs = node
        return self.init_node(CompareOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def gt(self, node):
        op = ">"
        lhs, rhs = node
        return self.init_node(CompareOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def eq(self, node):
        op = "=="
        lhs, rhs = node
        return self.init_node(CompareOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def ne(self, node):
        op = "!="
        lhs, rhs = node
        return self.init_node(CompareOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def _in(self, node):
        op = "in"
        lhs, rhs = node
        return self.init_node(CompareOp, lhs, op=op, lhs=lhs, rhs=rhs)

    # ------------------------------------------
    #    Binary operators
    # ------------------------------------------

    def add(self, node):
        op = "+"
        if not node:
            return op
        lhs, rhs = node
        return self.init_node(BinaryOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def sub(self, node):
        op = "-"
        if not node:
            return op
        lhs, rhs = node
        return self.init_node(BinaryOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def mul(self, node):
        op = "*"
        if not node:
            return op
        lhs, rhs = node
        return self.init_node(BinaryOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def div(self, node):
        op = "/"
        if not node:
            return op
        lhs, rhs = node
        return self.init_node(BinaryOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def mod(self, node):
        op = "%"
        if not node:
            return op
        lhs, rhs = node
        return self.init_node(BinaryOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def pow(self, node):
        op = "**"
        if not node:
            return op
        lhs, rhs = node
        return self.init_node(BinaryOp, lhs, op=op, lhs=lhs, rhs=rhs)

    # ------------------------------------------
    #    Bitwise operators
    # ------------------------------------------

    def bitor(self, node):
        op = "|"
        if not node:
            return op
        lhs, rhs = node
        return self.init_node(BinaryOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def bitxor(self, node):
        op = "^"
        if not node:
            return op
        lhs, rhs = node
        return self.init_node(BinaryOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def bitand(self, node):
        op = "&"
        if not node:
            return op
        lhs, rhs = node
        return self.init_node(BinaryOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def shr(self, node):
        op = ">>"
        if not node:
            return op
        lhs, rhs = node
        return self.init_node(BinaryOp, lhs, op=op, lhs=lhs, rhs=rhs)

    def shl(self, node):
        op = "<<"
        if not node:
            return op
        lhs, rhs = node
        return self.init_node(BinaryOp, lhs, op=op, lhs=lhs, rhs=rhs)

    # ------------------------------------------
    #    Unary operators
    # ------------------------------------------

    def uadd(self, node):
        op = "+"
        lhs = node[0]
        return self.init_node(UnaryOp, lhs, op=op, lhs=lhs, rhs=None)

    def usub(self, node):
        op = "-"
        lhs = node[0]
        return self.init_node(UnaryOp, lhs, op=op, lhs=lhs, rhs=None)

    def invert(self, node):
        op = "~"
        lhs = node[0]
        return self.init_node(UnaryOp, lhs, op=op, lhs=lhs, rhs=None)

    def ptr(self, node):
        op = "*"
        lhs = node[0]
        return self.init_node(UnaryOp, lhs, op=op, lhs=lhs, rhs=None)

    def deref(self, node):
        op = "&"
        lhs = node[0]
        return self.init_node(UnaryOp, lhs, op=op, lhs=lhs, rhs=None)

    def init_node(self, node_type, node, **kwargs):
        kwargs.update(dict(
                line=node.line,
                column=node.column,
                end_column=node.end_column,
        ))
        return node_type(**kwargs)
