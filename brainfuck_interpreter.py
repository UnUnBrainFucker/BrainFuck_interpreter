import sys
import io

def interpret(code, input_data=''):
    tape = [0]
    cell_index = 0

    user_input = []
    loop_table = {}

    loop_stack = []
    for ip, instruction in enumerate(code):
        if instruction == "[":
            loop_stack.append(ip)
        elif instruction == "]":
            loop_beginning_index = loop_stack.pop()
            loop_table[loop_beginning_index] = ip
            loop_table[ip] = loop_beginning_index

    ip = 0
    while ip < len(code):
        instruction = code[ip]
        
        if instruction == "+":
            tape[cell_index] += 1
            if tape[cell_index] == 256:
                tape[cell_index] = 0
        elif instruction == "-":
            tape[cell_index] -= 1
            if tape[cell_index] == -1:
                tape[cell_index] = 255
        elif instruction == "<":
            cell_index -= 1
        elif instruction == ">":
            cell_index += 1
            if cell_index == len(tape):
                tape.append(0)
        elif instruction == ".":
            print(chr(tape[cell_index]), end="")
        elif instruction == ",":
            if user_input == []:
                user_input = list(input() + "\n")
            tape[cell_index] = ord(user_input.pop(0))
        elif instruction == "[":
            if not tape[cell_index]:
                ip = loop_table[ip]
        elif instruction == "]":
            if tape[cell_index]:
                ip = loop_table[ip]
        elif instruction == "*":
            # number_str = str(tape[cell_index])
            if cell_index == len(tape):
                print(f"Error on index {cell_index} of list/array. Cannot multiply value NULL")
                break
            if chr(tape[cell_index]).isnumeric() and chr(tape[cell_index + 1]).isnumeric():
                tape[cell_index] = int(chr(tape[cell_index])) * int(chr(tape[cell_index + 1])) + 48
            else:
                print(f"Error on index {cell_index} of list/array. Cannot multiply with not int type")
                break
            if tape[cell_index] >= 256:
                tape[cell_index] = 0
        ip += 1

    return ''.join(map(chr, tape))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python brainfuck_interpreter.py <file>')
        if len(sys.argv) < 2:
            raise ValueError('Please provide a file as an argument.')

    with open(sys.argv[1], 'r') as f:
        code = f.read()

    output = interpret(code)
    print(output, end='')