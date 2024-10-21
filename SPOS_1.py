'''/*************************************************************************** 
Name – Omkar Dnyaneshwar Shinde  
Div - B-39  
Problem Statement : Design suitable Data Structures and Implement Pass - I and Pass - II of a 
two pass assembler for pseudo machine. Implementation should consist of a few instructions 
from each category and few assembler directives. The Output of a Pass - I (Intermediate code 
file and symbol table) should be input for Pass - II. 
***************************************************************************/ 
'''
# Define instruction set (IS), directive set (DL), assembler directives (AD), registers (REG), and conditions (COND)
IS = {
    "STOP" : "00",
    "ADD" : "01",
    "SUB" : "02",
    "MULT" : "03",
    "MOVER" : "04",
    "MOVEM" : "05",
    "COMP" : "06",
    "BC" : "07",
    "DIV" : "08",
    "READ" : "09",
    "PRINT" : "10"
}

DL = {"DC" : "01", "DS" : "02"}

AD = {
    "START" : "01",
    "END" : "02",
    "ORIGIN" : "03",
    "EQU" : "04",
    "LTORG" : "05"
}

REG = {
    "AREG" : "01",
    "BREG" : "02",
    "CREG" : "03",
    "DREG" : "04"
}

COND = {
    "LT" : "1",
    "LE" : "2",
    "EQ" : "3",
    "GT" : "4",
    "GE" : "5",
    "ANY" : "6"
}

# Initialize variables
location_counter = 0  # Keeps track of current location
literals = []  # List to store all literals
literal_table = []  # Table to store literals and their addresses
literal_count = 0  # Counter for number of literals
pool_table = []  # Pool table for literals

symbol_table = []  # Table to store symbols and their addresses
symbol_dict = {}  # Dictionary to map symbol names to their addresses
symbols = []  # List to store all symbols

# Read assembly instructions from file
with open("file.txt", 'r') as f:
    lines = f.read().strip().splitlines()

# Process each line for symbol and literal tables
for line in lines:
    # Split the line into parts and remove commas
    line_parts = line.replace(",", " ").split()

    # Handle START directive
    if line_parts[0] == "START":
        location_counter = int(line_parts[1])  # Set location counter to the starting address

    # Handle instruction set (IS)
    elif line_parts[0] in IS:
        location_counter += 1  # Increment location counter for instruction
        if len(line_parts) > 2 and '=' in line_parts[2]:  # Check if the instruction has a literal
            if not pool_table:
                pool_table.append(1)  # Start first literal pool
            literals.append(line_parts[2])  # Add literal to the list
    
    # Handle assembler directives (AD)
    elif line_parts[0] in AD:
        # Handle LTORG (literal pool origin)
        if line_parts[0] == "LTORG":
            for literal in literals:
                if not any(literal in lit for lit in literal_table):
                    literal_table.append([literal, location_counter])  # Add literal to literal table
                    location_counter += 1
                    literal_count += 1
            pool_table.append(literal_count + 1)  # Update pool table

        # Handle ORIGIN directive
        if line_parts[0] == 'ORIGIN':
            origin_parts = line_parts[1].split("+")
            location_counter = int(symbol_dict[origin_parts[0]]) + int(origin_parts[1])  # Update location counter
    
    # Handle other symbols and literals
    else:
        # If line contains literal
        if len(line_parts) > 3 and '=' in line_parts[3]:
            if not pool_table:
                pool_table.append(1)
            literals.append(line_parts[3])  # Add literal to the list

        # Handle EQU directive for symbols
        if line_parts[1] == "EQU":
            symbol_table.append([line_parts[0], symbol_dict[line_parts[2]]])
            symbol_dict[line_parts[0]] = symbol_dict[line_parts[2]]  # Assign same address as another symbol
            symbols.append(line_parts[0])
        else:
            symbol_table.append([line_parts[0], location_counter])
            symbol_dict[line_parts[0]] = location_counter  # Assign location counter as address
            symbols.append(line_parts[0])

        # Handle DL (declarative statement) - Adjust location counter if needed
        if line_parts[1] in DL:
            if "'" not in line_parts[2]:
                location_counter += (int(line_parts[2]) - 1)
        location_counter += 1

# Add remaining literals to the literal table
for i in range(literal_count, len(literals)):
    literal_table.append([literals[i], location_counter - 1])
    location_counter += 1

# Generate intermediate code and write to files
output = ""

# Process each line for intermediate code generation
for line in lines:
    line_parts = line.replace(",", " ").split()

    # If line is an instruction or STOP command
    if (len(line_parts) > 1 and line_parts[0] not in AD and line_parts[1] not in AD) or line_parts[0] == 'STOP':
        output += f"{location_counter}  "

    # Handle assembler directives
    if line_parts[0] in AD:
        output += f"(AD,{AD[line_parts[0]]})  "
        if line_parts[0] == 'ORIGIN':
            origin_parts = line_parts[1].split("+")
            location_counter = int(symbol_dict[origin_parts[0]]) + int(origin_parts[1])
            output += f"(C,{location_counter})\n"
        if line_parts[0] == 'LTORG':
            output += "\n"
            for lit in literal_table:
                output += f"{location_counter}  (DL,01)   (C,{literal_count})\n"
                location_counter += 1
                literal_count += 1

    # Handle IS and REG for instructions
    elif line_parts[0] in IS:
        location_counter += 1
        output += f"(IS,{IS[line_parts[0]]})  "
        if line_parts[0] == "BC":
            output += f" {COND[line_parts[1]]}        (S,{symbols.index(line_parts[2]) + 1})\n"
        if len(line_parts) > 1 and line_parts[1] in REG:
            output += f"(REG,{REG[line_parts[1]]})  "
            if '=' in line_parts[2]:
                output += f"(L,{literal_count})\n"
                literal_count += 1
            else:
                output += f"(S,{symbols.index(line_parts[2]) + 1})\n"

# Write intermediate code and tables to files
with open('IC.txt', 'w') as f1:
    f1.write(output)

with open('Sym_tab.txt', 'w') as f2:
    for i, symbol in enumerate(symbol_table):
        f2.write(f"{i+1:<8}{symbol[0]:<8}{symbol[1]:<8}\n")

with open('Lit_tab.txt', 'w') as f3:
    for i, literal in enumerate(literal_table):
        f3.write(f"{i+1:<8}{literal[0]:<8}{literal[1]:<8}\n")

with open('Pool_tab.txt', 'w') as f4:
    for pool in pool_table:
        f4.write(f"{pool}\n")


with open('IC.txt', 'r') as f1:
    print(f1.read())

with open('Sym_tab.txt', 'r') as f2:
    print(f2.read())

with open('Lit_tab.txt', 'r') as f3:
    print(f3.read())
with open('Pool_tab.txt', 'r') as f4:
    print(f4.read())