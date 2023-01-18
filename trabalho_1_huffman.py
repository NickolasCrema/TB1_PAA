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

def readFile(f):
    file = open(f, encoding='utf-8', mode='r')
    buf = file.read()
    list = []
    flag = 0
    list.append(Node(str('\0'), 0))
    for symbol in buf:
        if symbol == '\0':
            for s in list:   #TODO ARRUMAR O BARRA N
                if s.symbol == '\0':
                    s.value+=1
                    break
                break
            pass
        flag = 0
        for s in list:
            if str(s.symbol) == str(symbol):
                flag = 1
                s.value+=1
        if flag == 0:
            list.append(Node(str(symbol), value=1))
    file.close()
    print(list)
    return list

def compressFile(inputPath, outputPath, list):
    size = len(list)
    inputFile = open(inputPath, encoding='utf-8', mode='r')
    outputFile = open(outputPath, mode='wb')
    outputFile.write(bytes(str(size) + '\n', encoding='utf-8'))
    for compressedSymbol in list:
        outputFile.write(bytearray(str(compressedSymbol.symbol), encoding='utf-8') + ';'.encode('utf-8') + str(compressedSymbol.binary).encode('utf-8') + '\n'.encode('utf-8'))
    buf = inputFile.read()
    for symbol in buf:
        for compressedSymbol in list:
            if str(symbol) == str(compressedSymbol.symbol):
                binary = compressedSymbol.binary
                binary = bytes(binary, encoding='utf-8')
                outputFile.write(binary)
                break
    inputFile.close()
    outputFile.close()

def uncompressFile(inputPath, outputPath):
    inputFile = open(inputPath, encoding='utf-8', mode='r')
    outputFile = open(outputPath, encoding='utf-8', mode='w')
    size = int(inputFile.readline())
    header = []
    aux = ''
    for i in range(size):
        aux = str(inputFile.readline())
        aux = aux.split(';')
        header.append(compressedSymbol(aux[0], aux[1]))
    # for i in header:
    #     print(i)
        # aux = bytes(i.symbol[2:], encoding='utf-8')
        # i.symbol = aux.decode('utf-8')
        # print(aux)
    buf = str(inputFile.read())
    # buf = ''.join(buf.split('b\''))
    string = ''
    for symbol in buf:
        # print(string)
        string = string + symbol
        for compressed in header:
            # print(str(compressed.binary) == str(string))
            # print(compressed.binary + " " + string)
            if string == compressed.binary[:-1]:
                # print(compressed.binary)
                outputFile.write(compressed.symbol)
                string = ''
                break
    inputFile.close()
    outputFile.close()

# a = readFile("reliquias.txt")
# b = createNode(a)
# list = []
# processNode(b, '', list)
# compressFile("reliquias.txt", "reliquiasComprimida.bin", list)
uncompressFile('reliquiasComprimida.bin', 'reliquiasDescomprimidas.txt')