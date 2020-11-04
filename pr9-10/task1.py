import dis


def foo(x):
    while x:
        x -= 1
    return x + 1


code = dis.Bytecode(foo)
print(code.info())
print(dis.dis(foo))
for x in code: print(x)