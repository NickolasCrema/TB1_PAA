import struct
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
import codecs

def compressFile(inputPath, outputPath, list):
    inputFile = open(inputPath, encoding='utf-8', mode='r')
    outputFile = open(outputPath, mode='bw')
    
    size = len(list)
    print(size)
    outputFile.write(bytes(str(size) + '\n', encoding='utf-8'))
    header = {}
    for symbol in list:
        outputFile.write(bytes(symbol.symbol + '¨' + symbol.binary + '\n', encoding='utf-8'))
        header[symbol.symbol] = symbol.binary
    buf = inputFile.read()
    binaryString = ''
    for letter in buf:
        if letter == '\n':
            binaryString += header['@']
        else:
            binaryString += header[letter]
    buffer = bytearray()
    i = 0
    
    while i < len(binaryString):
        buffer.append(int(binaryString[i:i+8], base=2))
        i += 8
    
    outputFile.write(buffer)

    inputFile.close()
    outputFile.close()
    

def uncompressFile(inputPath, outputPath):
    inputFile = open(inputPath, mode='rb')
    outputFile = open(outputPath, encoding='utf-8', mode='w')
    size = inputFile.readline()
    size = str(size)[2:-3]
    size = int(size)
    # print(size)
    header = {}
    for i in range(size):
        aux = inputFile.readline().decode('utf-8')
        aux = aux.split('¨')
        header[aux[1][:-1]] = aux[0]
    
    buffer = inputFile.read()    
    binaryStr = ''
    for byte in buffer:
        binary = format(byte, '08b')
        for bit in binary:
            binaryStr = binaryStr + bit
            if binaryStr in header.keys():
                if header[binaryStr] == '@':
                    outputFile.write('\n')
                else:
                    outputFile.write(header[binaryStr])
                binaryStr = ''

    inputFile.close()
    outputFile.close()


# a = readFile("reliquias.txt", 0)
# b = createNode(a)
# list = []
# processNode(b, '', list)
# compressFile("reliquias.txt", "reliquiasComprimida.bin", list)
# uncompressFile('reliquiasComprimida.bin', 'reliquiasDescomprimidas.txt')

a = readFile("arquivogerado.txt", 0)
b = createNode(a)
list = []
processNode(b, '', list)
compressFile("arquivogerado.txt", "arquivogeradoComprimida.bin", list)
uncompressFile('arquivogeradoComprimida.bin', 'arquivogeradoDescomprimidas.txt')