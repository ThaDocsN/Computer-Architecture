"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.sp = 7
        self.pc = 0
        self.equal = 0
        self.greater = 0
        self.less = 0

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, file):
        """Load a program into memory."""

        address = 0

        # # For now, we've just hardcoded a program:
        #
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        program = []

        try:
            with open(file) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num != "":
                        program.append(int(num, 2))

        except FileNotFoundError:
            print(f"{file} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def push(self, reg):
        val = self.reg[reg]
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = val
        self.pc += 2

    def pop(self, reg):
        val = self.ram[self.reg[self.sp]]
        self.reg[reg] = val
        self.reg[self.sp] += 1
        self.pc += 2

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            command = self.ram[self.pc]
            reg_a = self.ram[self.pc + 1]
            reg_b = self.ram[self.pc + 2]

            if command == 0b10000010:
                self.reg[reg_a] = reg_b
                self.pc += 3
            elif command == 0b01000111:
                print(reg_a)
                self.pc += 2
            elif command == 0b10100010:
                self.reg[reg_a] *= self.reg[reg_b]
                self.pc += 3
            elif command == 0b01000101:
                self.sp -= 1
                self.ram[self.sp] = self.reg[reg_a]
                self.pc += 2
            elif command == 0b01000110:
                self.reg[reg_a] = self.ram[self.sp]
                self.sp += 1
                self.pc += 2
            elif command == 0b00010001:
                self.pc = self.ram[self.sp]
                self.sp += 1
            elif command == 0b10100000:
                self.reg[reg_a] += self.reg[reg_b]
                self.pc += 3
            elif command == 0b10100111:
                value1 = reg_a
                value2 = reg_b
                if value1 == value2:
                    self.equal = 1
                elif value1 > value2:
                    self.greater = 1
                elif value1 < value2:
                    self.less = 1
                self.pc += 3
            elif command == 0b01010100:
                self.pc = self.reg[reg_a]
            elif command == 0b01010101:
                if self.equal == 1:
                    self.pc = self.reg[reg_a]
                else:
                    self.pc += 2
            elif command == 0b01010110:
                if self.equal == 0:
                    self.pc = self.reg[reg_a]
                else:
                    self.pc += 2
            elif command == 0b00000001:
                running = False
                self.pc += 1
                print("Stop")
                sys.exit(1)

