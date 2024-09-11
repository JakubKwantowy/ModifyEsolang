#!/bin/python3

import sys, math, signal

print('The Modify Esolang Interpreter')
print('    written by JakubKwantowy')
print()

def print_help(arg0: str):
    print(
        f'Usage: {arg0} <script> [-v]',
         '<script>: The .modify Script to Run',
         '-v: Verbose Flag, Prints extra Debug Info',

        sep='\n'
    )

class InterpreterError(Exception):
    def __init__(self, type: str, line: int, desc: str) -> None:
        super().__init__('{} on Line {}: {}'.format(type, line, desc))
class InvalidCmdInterpreterError(InterpreterError):
    def __init__(self, line: int, cmd: str) -> None:
        super().__init__('Invalid Command', line, f'Invalid Command {cmd}')
class BadArgInterpreterError(InterpreterError):
    def __init__(self, line: int, desc: str) -> None:
        super().__init__('Bad Argument(s)', line, desc)
class SigIntInterpreterError(InterpreterError):
    def __init__(self, line: int) -> None:
        super().__init__('Signal Interrupt', line, 'SIGINT Keyboard Interrupt')

class Interpreter:
    def loadFile(self, path: str) -> None:
        with open(path, 'r') as f:
            self.lines = f.read().split('\n')
        self.current = 0

    validflags = [
        '-v'
    ]

    def processFlags(self, rawflags: 'list[str]') -> None:
        self.flags = ''.join([
            rawflag.strip('-')
            for rawflag in rawflags
            if rawflag.startswith('-')
            if rawflag in self.validflags
        ])

    def processLabels(self) -> None:
        for id, line in enumerate(self.lines):
            if not line.startswith(':'): continue
            name = line[1:]
            if not name: continue
            self.labels[name] = id

    def onSigInt(self, *_) -> None: 
        raise SigIntInterpreterError(self.current + 1)

    def __init__(self, path: str, rawflags: 'list[str]') -> None:
        self.lines: 'list[str]' = []
        self.current: int = 0
        self.flags: str = ''
        self.labels: 'dict[str, int]' = {}
        self.stack: 'list[int]' = []

        self.loadFile(path)
        self.processFlags(rawflags)
        self.processLabels()

        signal.signal(signal.SIGINT, self.onSigInt)

    regs: 'dict[str, int]' = {
        'a': 0, 'b': 0,
        'c': 0, 'd': 0,
    }

    def evaluate(self, input: str) -> 'str | int':
        if input.isnumeric(): return int(input)
        if input.lower() in self.regs: return self.regs[input.lower()]
        if input.startswith('#'):
            line = input.strip('#')
            if not line.isnumeric(): 
                if not line in self.regs: return ''
                line = self.regs[line]
            line = int(line)
            if line < 0 or line >= len(self.lines): return ''
            line = self.lines[line]
            if line.isnumeric(): return int(line)
            return line
        if input in self.labels: return self.labels[input] 
        return ''

    def process(self, line: str, location: int, verbose: bool) -> None:
        def cmd_print(args: 'list[str]', location: int, verbose: bool) -> None: print(self.evaluate(args[0]), end='')
        def cmd_println(args: 'list[str]', location: int, verbose: bool) -> None: print(self.evaluate(args[0]))
        def cmd_exit(args: 'list[str]', location: int, verbose: bool) -> None:
            code = 0
            if len(args): code = self.evaluate(args[0])
            sys.exit(code)
        def cmd_setreg(args: 'list[str]', location: int, verbose: bool) -> None: 
            if len(args) < 2: raise BadArgInterpreterError(location, 'Not Enough Args (2 Required)')
            reg = args[0].lower()
            src = self.evaluate(args[1])
            if not reg in self.regs: raise BadArgInterpreterError(location, f'Arg1 not a Valid Register! ({reg})')
            if isinstance(src, str): src = len(src)
            self.regs[reg] = src
            if verbose: print(f'[ {reg} = {src} ]')
        def cmd_pushreg(args: 'list[str]', location: int, verbose: bool) -> None: 
            if len(args) < 1: raise BadArgInterpreterError(location, 'Not Enough Args (1 Required)')
            reg = args[0].lower()
            if not reg in self.regs: raise BadArgInterpreterError(location, f'Arg1 not a Valid Register! ({reg})')
            self.stack.append(self.regs[reg])
            if verbose: print(f'[ PUSH {reg} ]')
        def cmd_popreg(args: 'list[str]', location: int, verbose: bool) -> None: 
            if len(args) < 1: raise BadArgInterpreterError(location, 'Not Enough Args (1 Required)')
            reg = args[0].lower()
            if not reg in self.regs: raise BadArgInterpreterError(location, f'Arg1 not a Valid Register! ({reg})')
            self.regs[reg] = self.stack.pop()
            if verbose: print(f'[ POP {reg} ]')
        def cmd_peekreg(args: 'list[str]', location: int, verbose: bool) -> None: 
            if len(args) < 1: raise BadArgInterpreterError(location, 'Not Enough Args (1 Required)')
            reg = args[0].lower()
            if not reg in self.regs: raise BadArgInterpreterError(location, f'Arg1 not a Valid Register! ({reg})')
            self.regs[reg] = self.stack[-1]
            if verbose: print(f'[ PEEK {reg} ]')
        def cmd_math(operation: 'function', id: str) -> 'function':
            def command(args: 'list[str]', location: int, verbose: bool): 
                if len(args) < 3: raise BadArgInterpreterError(location, 'Not Enough Args (3 Required)')
                reg = args[0].lower()
                num1 = self.evaluate(args[1])
                num2 = self.evaluate(args[2])
                if not reg in self.regs: raise BadArgInterpreterError(location, f'Arg1 not a Valid Register! ({reg})')
                if isinstance(num1, str): num1 = len(num1)
                if isinstance(num2, str): num2 = len(num2)
                self.regs[reg] = operation(num1, num2)
                if verbose: print(f'[ {reg} = {args[1]} {id} {args[2]} ]')
            return command
        def cmd_sqrtreg(args: 'list[str]', location: int, verbose: bool) -> None: 
            if len(args) < 2: raise BadArgInterpreterError(location, 'Not Enough Args (2 Required)')
            reg = args[0].lower()
            src = self.evaluate(args[1])
            if not reg in self.regs: raise BadArgInterpreterError(location, f'Arg1 not a Valid Register! ({reg})')
            if isinstance(src, str): src = len(src)
            self.regs[reg] = int(math.sqrt(src))
            if verbose: print(f'[ {reg} = sqrt({src}) ]')
        def cmd_setline(args: 'list[str]', location: int, verbose: bool) -> None:
            if len(args) < 2: raise BadArgInterpreterError(location, 'Not Enough Args (2 Required)')
            line = self.evaluate(args[0])
            src = str(self.evaluate(args[1]))
            if not isinstance(line, int): raise BadArgInterpreterError(location, f'Arg1 not a Valid Line Number! ({line})')
            self.lines[line] = src
            if verbose: print(f'[ #{line} = {src} ]')
        def cmd_jumpline(args: 'list[str]', location: int, verbose: bool) -> None:
            if len(args) < 1: raise BadArgInterpreterError(location, 'Not Enough Args (1 Required)')
            line = self.evaluate(args[0])
            if not isinstance(line, int): raise BadArgInterpreterError(location, f'Arg1 not a Valid Line Number! ({line})')
            self.current = line - 1
            if verbose: print(f'[ -> #{line} ]')
        def cmd_inputline(args: 'list[str]', location: int, verbose: bool) -> None:
            if len(args) < 1: raise BadArgInterpreterError(location, 'Not Enough Args (1 Required)')
            line = self.evaluate(args[0])
            if not isinstance(line, int): raise BadArgInterpreterError(location, f'Arg1 not a Valid Line Number! ({line})')
            data = input()
            self.lines[line] = data
            if verbose: print(f'[ #{line} <- {data} ]')
        def cmd_conditional(args: 'list[str]', location: int, verbose: bool) -> None:
            if len(args) < 5: raise BadArgInterpreterError(location, 'Not Enough Args (5 Required)')
            str_conditions: 'dict[str, function[str, str]]' = {
                'eq': lambda v1, v2: v1 == v2,
            }
            num_conditions: 'dict[str, function[int, int]]' = {
                'numeq': lambda v1, v2: v1 == v2,
                'less': lambda v1, v2: v1 < v2,
                'gtr': lambda v1, v2: v1 > v2,
                'lesseq': lambda v1, v2: v1 <= v2,
                'gtreq': lambda v1, v2: v1 >= v2,
            }
            v1 = self.evaluate(args[0])
            v2 = self.evaluate(args[1])
            condition = args[2]
            line = self.evaluate(args[3])
            src = str(self.evaluate(args[4]))
            if not isinstance(line, int): raise BadArgInterpreterError(location, f'Arg4 not a Valid Line Number! ({line})')
            result = False
            if condition in str_conditions:
                result = str_conditions[condition](str(v1), str(v2))
            elif condition in num_conditions:
                if isinstance(v1, str): v1 = len(v1)
                if isinstance(v2, str): v2 = len(v2)
                result = num_conditions[condition](v1, v2)
            else: raise BadArgInterpreterError(location, f'Not Enough Arg3 not a valid Condition! ({condition})')
            if result: self.lines[line] = src
            if verbose: print(f'[ {v1} {condition} {v2}', f'| #{line} = {src} ]' if result else '| false ]')

        cmdlist: 'dict[str, function["list[str]", int, bool]]' = {
            'print': cmd_print,
            'println': cmd_println,
            'exit': cmd_exit,
            'setreg': cmd_setreg,
            'pushreg': cmd_pushreg,
            'popreg': cmd_popreg,
            'peekreg': cmd_peekreg,
            'addreg': cmd_math(lambda num1, num2: num1 + num2, '+'),
            'subreg': cmd_math(lambda num1, num2: num1 - num2, '-'),
            'mulreg': cmd_math(lambda num1, num2: num1 * num2, '*'),
            'divreg': cmd_math(lambda num1, num2: int(num1 / num2), '/'),
            'sqrtreg': cmd_sqrtreg,
            'setline': cmd_setline,
            'jumpline': cmd_jumpline,
            'inputline': cmd_inputline,
            'conditional': cmd_conditional,
        }

        if not line: return
        if line.startswith(':'): return
        tokens = line.split(' ')
        tok0 = tokens[0].lower()
        if not tok0 in cmdlist: 
            raise InvalidCmdInterpreterError(location, tok0)
        cmdlist[tok0](tokens[1:], location, verbose)

    def processById(self, line: int, verbose: bool) -> None: self.process(self.lines[line], line + 1, verbose)
    def processCurrent(self, verbose: bool) -> None: self.processById(self.current, verbose)
    def run(self) -> None:
        running = True
        verbose = 'v' in self.flags
        while running:
            self.processCurrent(verbose)
            self.current += 1
            if self.current == len(self.lines): running = False

def main(argc: int, argv: 'list[str]') -> int:
    if argc == 1:
        print_help(argv[0])
        return 0
    
    interpreter = Interpreter(argv[1], argv[2:])
    try: interpreter.run()
    except SigIntInterpreterError as e:
        print('\n' + str(e))
    except InterpreterError as e:
        print(e)
        return 1

    return 0

if __name__ == '__main__': sys.exit(main(len(sys.argv), sys.argv))
