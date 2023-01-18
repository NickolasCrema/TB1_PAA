class Node:
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value
        self.left = None
        self.right = None
    
    def __repr__(self):
        return f"symbol: {self.symbol}; value: {self.value}"

    def setValue(self, value):
        self.value = value
    
    def incValue(self):
        self.value+=1
    
    def setLeft(self, left):
        self.left = left
    
    def setRight(self, right):
        self.right = right

class compressedSymbol:
    def __init__(self, symbol, binary):
        self.symbol = symbol
        self.binary = binary
    
    def __repr__(self):
        return f"symbol: {self.symbol}; binary: {self.binary} "

def fillNode(left, right):
    node = Node(None, 0)
    node.setLeft(left)
    node.setRight(right)
    node.setValue(left.value + right.value)
    return node

def createNode(queue):
    n = len(queue)
    node = 0
    for i in range(n-1):
        queue.sort(key=lambda x: x.value)
        left = queue.pop(0)
        right = queue.pop(0)
        node = fillNode(left, right)
        queue.append(node)
    return node

def processNode(node, binary, list):
    if node == None:
        return
    elif node.symbol != None:
        list.append(compressedSymbol(node.symbol, binary))
    processNode(node.left, binary + "0", list)
    processNode(node.right, binary + "1", list)

def readFile(f, wordOrLetter):
    file = open(f, encoding='utf-8', mode='r')
    buf = file.read()
    list = []
    flag = 0
    string = ''
    list.append(Node(str('@'), 0))
    # if wordOrLetter == 0:
    for symbol in buf:
        # print(symbol)
        if symbol == '\n':
            for s in list:   #TODO ARRUMAR O BARRA N
                if s.symbol == '@':
                    s.value+=1
                    break
                break
            pass
        else:
            flag = 0
            for s in list:
                if str(s.symbol) == str(symbol):
                    flag = 1
                    s.value+=1
            if flag == 0:
                list.append(Node(str(symbol), value=1))
    # else:
    #     list.append(Node(str(' '), 0))
    #     for symbol in buf:
    #         string = string + symbol
    #         if symbol == '\n':
    #             for s in list:   #TODO ARRUMAR O BARRA N
    #                 if s.symbol == '@':
    #                     s.value+=1
    #                     break
    #                 break
    #             pass
    #         elif symbol == ' ':
    #             flag = 0
    #             for s in list:
    #                 if str(s.symbol) == str(string):
    #                     flag = 1
    #                     s.value += 1
    #             if flag == 0:
    #                 list.append()


    file.close()
    return list

def compressFile(inputPath, outputPath, list):
    size = len(list)
    inputFile = open(inputPath, encoding='utf-8', mode='r')
    outputFile = open(outputPath, mode='wb')
    outputFile.write(bytes(str(size) + '\n', encoding='utf-8'))
    header = {}
    for compressedSymbol in list:
        outputFile.write(bytes(str(compressedSymbol.symbol), encoding='utf-8') + bytes('¨', encoding='utf-8') + int(compressedSymbol.binary[::-1], 2).to_bytes(4, 'little') + bytes('\n', encoding='utf-8'))
        header[compressedSymbol.symbol] = compressedSymbol.binary
    # print(header)
    buf = inputFile.read()
    bits = ''
    binaries = []
    for symbol in buf:
        if symbol == '\n':
            binary = header['@']
            # binary = bytearray(binary, encoding='utf-8')
            binaries.append(binary)
        else:
            if symbol in header:
                binary = header[symbol]
                # binary = bytearray(binary, encoding='utf-8')
                binaries.append(binary)
    # print(bits)
    # outputFile.write(int(bits[::-1], 2).to_bytes(4, 'little'))
    for binary in binaries:
        outputFile.write(int(binary[::-1], 2).to_bytes(4, 'little'))
    inputFile.close()
    outputFile.close()

def uncompressFile(inputPath, outputPath):
    inputFile = open(inputPath, mode='rb')
    outputFile = open(outputPath, encoding='utf-8', mode='w')
    size = inputFile.readline()
    # size = int.from_bytes(size, 'little')
    size = str(size)[2:-3]
    size = int(size)
    print(size)
    header = {}
    aux = ''
    for i in range(size):
        aux = inputFile.readline()
        letter = aux[0:1]
        letter = str(letter)
        letter = letter[2:3]
        rest = aux[1:-1]
        header[rest] = letter
        # rest = bytearray(rest)
        # print([i for i in rest])
        # print(rest)
        # print(letter)
        # # print(aux)
        # aux = aux.split('¨')
        # header[aux[1]] = aux[0]
    # print(header)
    buf = inputFile.read()
    buf = buf.decode('ansi')
    buf = buf.encode('utf-8')
    # buf = buf.decode('utf-8')
    # print(buf)
    string = ''
    
    for symbol in buf:
        simbolo = bytearray(symbol)
        string = str(string) + str(simbolo)
        print(str(string))
        if string in header.keys():
            print('si')
            if header[string] == '@':
                outputFile.write('\n')
                string = 0
            else:
                outputFile.write(header[string])
                string = ''
    inputFile.close()
    outputFile.close()

# a = readFile("reliquias.txt", 0)
# b = createNode(a)
# list = []
# processNode(b, '', list)
# compressFile("reliquias.txt", "reliquiasComprimida.bin", list)
uncompressFile('reliquiasComprimida.bin', 'reliquiasDescomprimidas.txt')