from sly import Lexer, Parser
from pprint import pprint
import json
class CalcLexer(Lexer):
    tokens = {NUMBER, NAME, STRING}

    literals = {"(", ")"}

    ignore = " \t"
    ignore_comment = r"\#.*"
    ignore_newline = r"\n+"

    NUMBER = r"\d+"
    NAME = r"[a-z]+\d*"
    STRING = r"(\"|\').*?(\"|\')"

    def NUMBER(self, c):
        c.value = int(c.value)
        return c

    def NAME(self, c):
        c.value = str(c.value)
        return c

    def STRING(self, c):
        c.value = str(c.value)[1:-1]
        return c

    def ignore_newline(self, c):
        self.lineno += c.value.count("\n")

    def error(self, c):
        print("Line %d: Bad character %r" % (self.lineno, c.value[0]))
        self.index += 1

class CalcParser(Parser):
    debugfile = 'parexp.out'
    tokens = CalcLexer.tokens
    literals = CalcLexer.literals
    @_("'(' s_list ')'")
    def program(self, p):
        return p.s_list

    @_("s_exp s_exp")
    def s_list(self, p):
        return p.s_exp0 | p.s_exp1 
    
    @_("name '(' list ')'")
    def s_exp(self, p):
        res = dict()
        res[p.name] = p.list
        return res

    @_("s_exp object")
    def s_exp(self, p):
        return  p.s_exp | p.object

    @_("list data")
    def list(self, p):
        p.list.append(p.data)
        return p.list
    
    @_("list '(' objects ')'")
    def list(self, p):
        p.list.append(p.objects)
        return p.list
    
    @_("empty")
    def list(self, p):
        return []

    @_("objects '(' object ')'")
    def objects(self, p):
        return p.objects | p.object
    
    @_("empty")
    def objects(self, p):
        return {}

    @_("name data")
    def object(self, p):
        res = dict()
        res[p.name] = p.data
        return res



    @_("STRING")
    def data(self, p):
        return p.STRING

    @_("NUMBER")
    def data(self, p):
        return p.NUMBER

    @_("NAME")
    def name(self, p):
        return p.NAME

    @_("")
    def empty(self, p):
        pass

    @staticmethod
    def pars(data):
        lexer = CalcLexer()
        parexp = CalcParser()
        try:
            s = parexp.parse(lexer.tokenize(data))
            pprint(s)
        except EOFError:
            print("Error in creating result")

if __name__ == "__main__":
    with open("/Users/valyazaikin/testpy/task2/exampe.txt") as f:
        text = f.read()
    CalcParser.pars(text)

"""
program     | s_list

s_list           | s_exp s_exp

s_exp          | name (list)
s_exp          | s_exp object

list              | list data
list              | list (objects)
list              | empty 

objects       | objects (object)
objects       | empty 

object         | name data

data           | STRING
data           | NUMBER

name         | NAME
"""