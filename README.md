# Compiler

This is an unfinished compiler that I'm building without any resources. Pure imagination. It translates a programming
language I made up (with a syntax in between C++ and Python) into x86 assembly to later be compiled into bytecode.

The current implementation can parse the following constructs into an abstract syntax tree:

- variable declaration (with local variables always taking precedence just like in Python)
- variable value assignment
- mathematical expressions (all available operators can be found in ```utils.Op```)
- if / else statements
- while loops
- the ```print``` keyword to output to the terminal.
 
Example:

```
int a = 10 + 2 * 4;
int b = 5;

if (a > b + 6){
  print a;
} else {
  print b + 2 ^ (a + 1);
}

while (b < 8){
  b = b + 1;
  print b;
}
```

will get converted into:

```
DeclareIntInstr(name='a', expr=[10, Op(ADD), 2, Op(MUL), 4])
DeclareIntInstr(name='b', expr=[5])
CondInstr(cond=['a', Op(GT), 'b', Op(ADD), 6], instrs=[PrintInstr(expr=['a'])], instrs_else=[PrintInstr(expr=['b', Op(ADD), 2, Op(POW), ['a', Op(ADD), 1]])])
LoopInstr(cond=['b', Op(LT), 8], instrs=[SetVarInstr(name='b', expr=['b', Op(ADD), 1]), PrintInstr(expr=['b'])])
```

and if we run this code, this gets printed (currently all resolution logic is implemented in Python. It remains to have
this step write the corresponding x86 code to be later compiled and run):

```
18
6
7
8
```

### Tests

Due to frequent refactoring from on-the-fly learning, I’ve decided to write tests after implementing all core
functionalities. I'll be using pytest.
