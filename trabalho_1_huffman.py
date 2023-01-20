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
    if wordOrLetter == 0:
        buf = file.read()
        list = []
        flag = 0
        string = ''
        list.append(Node(str('@'), 0))
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
    else:
        list = []
        buf = file.readlines()
        # print(buf)
        header = {}
        header['@'] = 0
        header[' '] = 0
        for line in buf:
            
            aux = line.split(' ')
            # print(line)
            # print(aux)
            header[' '] += len(aux)-1
            header['@'] += 1
            # print(aux)
            for word in aux:
                if word != '' and word != '\n' and word != ' ':
                    # print(word)
                    # print(ord(word[-1:]))
                    # print(header)
                    if  (ord(word[-1:]) != 10 or ord(word[-1:]) != 8) and word != ' ':
                        if ord(word[-1:]) < 65 or ord(word[-1:]) > 122:
                            if word[-1:] in header.keys():
                                header[word[-1:]] += 1
                            else:
                                header[word[-1:]] = 0
                            word = word[:-1]
                        if word in header.keys():
                            header[word] += 1
                        else:
                            header[word] = 1

        for word in header.keys():
            list.append(Node(symbol=word, value=header[word]))

    file.close()
    return list
import codecs

def compressFile(inputPath, outputPath, list, wordOrLetter):
    inputFile = open(inputPath, encoding='utf-8', mode='r')
    outputFile = open(outputPath, mode='bw')
    size = len(list)
    print(size)
    outputFile.write(bytes(str(size) + '\n', encoding='utf-8'))
    header = {}
    for symbol in list:
        buffer = bytearray()
        string = bytes(symbol.symbol + '¨' + symbol.binary + '\n', encoding='utf-8')
        i=0
        while i < len(string):
            buffer.append(int(string[i:i+8], base=2)) 
            i+=8
        header[symbol.symbol] = symbol.binary
    outputFile.write(buffer)
    buf = inputFile.read()
    binaryString = ''
    if wordOrLetter == 0:
        for letter in buf:
            if letter == '\n':
                binaryString += header['@']
            else:
                binaryString += header[letter]
        buffer = bytearray()
        i = 0
        
        while i < len(binaryString):
            buffer.append(int(binaryString[i:i+8], base=16))
            i += 8
    else:
        buffer = bytearray()
        binaryString = ''
        string = ''
        for letter in buf:
            print(ord(letter))
            if ord(letter) < 65 or (ord(letter) > 122 and ord(letter) < 192):
                binaryString += header[string]
                if letter == '\n':
                    binaryString += header['@']
                else:
                    binaryString += header[letter]
                string = ''
            else:
                string += letter
        
        buffer = bytearray()
        i=0
        while i < len(binaryString):
            buffer.append(int(binaryString[i:i+8], base=2))
            i+=8


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


a = readFile("reliquias.txt", 1)
b = createNode(a)
list = []
processNode(b, '', list)
compressFile("reliquias.txt", "reliquiasComprimida.bin", list, 1)
# uncompressFile('reliquiasComprimida.bin', 'reliquiasDescomprimidas.txt')

# a = readFile("arquivogerado.txt", 0)
# b = createNode(a)
# list = []
# processNode(b, '', list)
# compressFile("arquivogerado.txt", "arquivogeradoComprimida.bin", list)
# uncompressFile('arquivogeradoComprimida.bin', 'arquivogeradoDescomprimidas.txt')