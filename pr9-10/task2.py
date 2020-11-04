import dis


def foo(n):
    r = 1

    while n > 1:
        r *= n
        n -= 1
        
    return r 

print(foo(4))
code = dis.Bytecode(foo)
print(code.info())
print(dis.dis(foo))
for x in code: print(x)