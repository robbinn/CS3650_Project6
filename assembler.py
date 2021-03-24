ac1toc6 = {
    "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000", "!D": "0001101",
    "!A": "0110001", "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011", "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000", "D|M": "1010101"
}

d1tod3 = {
    "null": "000", "M": "001", "D": "010", "A": "100", "MD": "011", "AM": "101", "AD": "110", "AMD": "111"
}

j1toj3 = {
    "null": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

symbol_table = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5,
    "R6": 6, "R7": 7, "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
    "SCREEN": 16384, "KBD": 24576, "OUTPUT_FIRST": 17000, "OUTPUT_D": 18000, "INFINITE_LOOP": 19000
}

# 0-15 are used, so next available address will be 16
nextPointer = 16

filename = input('Enter the filename: ')
temp_filename = filename.split('.')[0] + '.txt'
out_filename = filename.split('.')[0] + '.hack'

infile = open(filename)
outfile = open(temp_filename, "w")

lineCounter = 0
# Cleaning the file
for line in infile:
    new_line = line.lstrip().rstrip()
    if "//" in new_line:
        new_line = new_line.split("//")[0]
    if new_line != "":
        if new_line[0] != '/' and new_line[0] != '\n':
            if new_line[0] == "(":
                symbol_table[new_line[1:-1]] = lineCounter
            else:
                lineCounter += 1
                outfile.write(new_line + "\n")

infile = open(temp_filename)
outfile = open(out_filename, "w")

# Decoding the file
for line in infile:
    line.lstrip().rstrip()
    if line[0] == "@":
        if line[1].isdigit():
            temp = int(line[1:])
        else:
            label = line[1:-1]
            temp = symbol_table.get(label, -1)
            if temp == -1:
                symbol_table[label] = nextPointer
                temp = symbol_table[label]
                nextPointer += 1
        binValue = bin(temp)[2:].zfill(16)
        outfile.write(binValue + '\n')
    else:
        line = line[:-1]
        if "=" not in line:
            line = "null=" + line
        if ";" not in line:
            line = line + ";null"

        temp = line.split("=")[1].split(";")
        compCode = ac1toc6.get(temp[0].rstrip())
        destCode = d1tod3.get(line.split("=")[0].rstrip())
        jumpCode = j1toj3.get(temp[1].rstrip())
        outfile.write('111' + compCode + destCode + jumpCode + '\n')

infile.close()
outfile.close()
