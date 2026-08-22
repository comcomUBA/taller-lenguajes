from __future__ import annotations
from dataclasses import dataclass, fields, is_dataclass
from typing import Any
from visitor import Label

@dataclass
class Frame:
    instructions: list[Any]
    pc: int
    parent: Frame
    local_scope: dict[str, Any]
    stack: list[Any]

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()

    def __repr__(self):
        return f'Frame(id={id(self)}, instructions={id(self.instructions)}, pc={self.pc!r}, parent={self.parent!r}, local_scope={self.local_scope!r}, stack={self.stack!r})'

@dataclass
class VMFunc:
    instructions: list[Any]

    def __repr__(self):
        return f'VMFunc(instructions={id(self.instructions)!r})'

    def print_bytecode(self):
        visited = set()
        queue = [self]
        while queue:
            func = queue.pop()
            if id(func) in visited:
                continue
            visited.add(id(func))

            print(f'{func}:')
            for i, (instr, *args) in enumerate(func.instructions):
                instr_args = ', '.join(repr(arg) for arg in args)
                print(f'{i:3} {instr} {instr_args}')

                for arg in args:
                    if isinstance(arg, VMFunc):
                        queue.append(arg)


@dataclass
class Print:
    def invoke(self, vm, *args):
        print(*args)
        vm.frame.push(None)


@dataclass
class IsEmpty:
    def invoke(self, vm, arr):
        vm.frame.push(len(arr) == 0)


@dataclass
class Pop:
    def invoke(self, vm, arr):
        vm.frame.push(arr.pop())


@dataclass
class Contains:
    def invoke(self, vm, arr, value):
        vm.frame.push(value in arr)


@dataclass
class Push:
    def invoke(self, vm, arr, value):
        arr.append(value)
        vm.frame.push(arr)


@dataclass
class Concat:
    def invoke(self, vm, arr, another_arr):
        arr.extend(another_arr)
        vm.frame.push(arr)


@dataclass
class Get:
    def invoke(self, vm, arr, idx):
        vm.frame.push(arr[idx])


@dataclass
class Set:
    def invoke(self, vm, arr, idx, value):
        arr[idx] = value
        vm.frame.push(value)


@dataclass
class ListOf:
    def invoke(self, vm, size):
        vm.frame.push([0] * size)


@dataclass
class Size:
    def invoke(self, vm, arr):
        vm.frame.push(len(arr))


@dataclass
class CoStart:
    yield_or_resume_to: Frame | CoStart | None
    running: bool

    def __repr__(self):
        if self.running:
            return f'CoStart(id={id(self)}, yield_to={id(self.yield_or_resume_to)})'
        else:
            return f'CoStart(id={id(self)}, resume_to={id(self.yield_or_resume_to)})'


@dataclass
class Start:
    def invoke(self, vm, func, args):
        assert isinstance(func, VMFunc), "start() only works for VM functions"
        co_start = CoStart(func, False)

        co_program = [
            ('DROP',),
            ('CALL', len(args)),
            ('CALL', 1)
        ]
        co_start.yield_or_resume_to = Frame(co_program, 0, co_start, {}, [Yield(), func, *args])
        vm.frame.push(co_start)


@dataclass
class Yield:
    def invoke(self, vm, value):
        co_frame = vm.frame
        while not isinstance(co_frame, CoStart) and co_frame is not None:
            co_frame = co_frame.parent

        assert co_frame is not None, "yield() could not find a running coroutine"
        assert co_frame.running, "yield() only works for running coroutines"

        yield_to = co_frame.yield_or_resume_to
        resume_to = vm.frame
        co_frame.yield_or_resume_to = resume_to
        co_frame.running = False

        vm.frame = yield_to
        vm.frame.push(value)


@dataclass
class Resume:
    def invoke(self, vm, co_frame, value):
        assert isinstance(co_frame, CoStart), "resume() only works for coroutines"
        assert not co_frame.running, "Cannot resume running coroutine"

        yield_to = vm.frame
        resume_to = co_frame.yield_or_resume_to

        assert resume_to.pc == 0 or resume_to.parent is not co_frame, "Cannot resume finished coroutine"

        co_frame.yield_or_resume_to = yield_to
        co_frame.running = True

        vm.frame = resume_to
        vm.frame.push(value)
        return value


class VM:
    def __init__(self, vm_func):
        self.global_scope = {
            'print': Print(),
            'is_empty': IsEmpty(),
            'pop': Pop(),
            'contains': Contains(),
            'push': Push(),
            'concat': Concat(),
            'get': Get(),
            'set': Set(),
            'list_of': ListOf(),
            'size': Size(),
            'start': Start(),
            'yield': Yield(),
            'resume': Resume(),
        }
        self.frame = Frame(vm_func.instructions, 0, None, self.global_scope, [])

    def run(self):
        while True:
            if self.frame.pc < 0 or len(self.frame.instructions) <= self.frame.pc:
                break

            ins = self.frame.instructions[self.frame.pc]
            self.frame.pc += 1

            #print(ins[0], self.frame)
            match ins:
                case ('JMP', Label(target=target)):
                    self.frame.pc = target
                case ('DEFINE', var_name):
                    value = self.frame.pop()
                    self.frame.local_scope[var_name] = value
                case ('LOAD', var_name):
                    if var_name in self.frame.local_scope:
                        value = self.frame.local_scope[var_name]
                    else:
                        value = self.global_scope[var_name]
                    self.frame.push(value)
                case ('PUSH', value):
                    self.frame.push(value)
                case ('CREATE_ARRAY', num_elems):
                    value = []
                    for i in range(num_elems):
                        value.insert(0, self.frame.pop())
                    self.frame.push(value)
                case ('CALL', num_args):
                    args = []
                    for i in range(num_args):
                        args.insert(0, self.frame.pop())
                    func = self.frame.pop()

                    if isinstance(func, VMFunc):
                        self.frame = Frame(func.instructions, 0, self.frame, {}, args)
                    else:
                        func.invoke(self, *args)
                case ('UNOP', 'not'):
                    self.frame.push(not self.frame.pop())
                case ('UNOP', '-'):
                    self.frame.push(-self.frame.pop())
                case ('JMP_IF_FALSE', Label(target=target)):
                    if self.frame.pop() == False:
                        self.frame.pc = target
                case ('JMP_IF_TRUE', Label(target=target)):
                    if self.frame.pop() == True:
                        self.frame.pc = target
                case ('DROP',):
                    self.frame.pop()
                case ('RETURN',):
                    result = self.frame.pop()
                    self.frame = self.frame.parent
                    self.frame.push(result)
                case ('BINOP', '>='):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs <= rhs)
                case ('BINOP', '<='):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs <= rhs)
                case ('BINOP', '>'):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs > rhs)
                case ('BINOP', '<'):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs < rhs)
                case ('BINOP', '+'):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs + rhs)
                case ('BINOP', '-'):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs - rhs)
                case ('BINOP', '=='):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs == rhs)
                case ('BINOP', '%'):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs % rhs)
                case ('ASSIGN', var_name):
                    value = self.frame.pop()
                    if var_name in self.frame.local_scope:
                        self.frame.local_scope[var_name] = value
                    elif var_name in self.global_scope:
                        self.global_scope[var_name] = value
                    else:
                        print("UNDEFINED", var_name)
                        break
                    self.frame.push(value)
                case ('DUP',):
                    value = self.frame.pop()
                    self.frame.push(value)
                    self.frame.push(value)
                case _:
                    print('UNKNOWN', ins)
                    break