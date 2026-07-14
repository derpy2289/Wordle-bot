code = ["0010101", "0123456"]
code2 = ["0010101", "1111011", "0101101", "0001000", "1000110", "1101111", "0111101", "0111001", "0000010", "0110001", "1101001", "1100111", "0011010", "0111010" , "0000010", "1110011", "1101110", "1100101"]
2345601
key = 0
key_letter = [2, 1, 4, 2, 7, 7]
for i in range(len(code2)):
    #print(f"Code {i}: {code2[i]}")  # Print each code with its index
    letter = ""
    code_letters = code2[i]
    letter += code_letters[(key_letter[key]):]
    letter += code_letters[:(key_letter[key])]
    print("0" + letter, end= ", ")

    key = (key+1) % 6

    #print(f"Decoded letter for Code {i}: {letter}")  # Print the decoded letter