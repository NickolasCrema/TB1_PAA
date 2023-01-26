def main(args):
    import os
    path = os.getcwd()
    clear = lambda: os.system('cls')
    options = -1
    fileName = ''
    outputFileName = ''
    clear()
    while(True):
        if options == -1:
            clear()
            print('\n1 - Compressao por letra')
            print('2 - Compressao por palavra')
            print('3 - Descompressao por letra')
            print('4 - Descompressao por palavra')
            options = input()
        elif options == '1':
            clear()
            print('\nInsira o nome do arquivo <-------------------------------------------> 0 - Para voltar')
            # print('0 - Voltar')
            fileName = input()
            if fileName == '0':
                options = -1
            else:
                buf = readFile(fileName, 0)
                print('\nInsira o nome do arquivo compactado <--------------------------------> 0 - Para voltar')
                outputFileName = input()
                if outputFileName == '0':
                    options = -1
                else:
                    huffman = createNode(buf)
                    list = []
                    processNode(huffman, '', list)
                    if compressFile(fileName, outputFileName, list, 0) == 0:
                        print('Arquivo compactado com sucesso! Aperte qualquer tecla para continuar')
                    else:
                        print('Erro ao compactar arquivo! Aperte qualquer tecla para continuar')
                    input()
                    options = -1

    return 0
#Estrutura de nó da árvore
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
        header = {}
        header['@'] = 0
        header[' '] = 0
        for line in buf:
            aux = ''.join(line.split('\n')).split(' ')
            header['@'] += 1
            for i, word in enumerate(aux):
                if i == len(aux)-1:
                    if word in header.keys():
                        header[word] += 1
                    else:
                        header[word] = 1
                else:
                    if word in header.keys():
                        header[word] += 1
                        header[' '] += 1
                    else:
                        header[word] = 1
                        header[' '] += 1
            header['@'] += 1
                # if word != '' and word != '\n' and word != ' ' and len(word) > 1:
                #     while ord(word[-1:]) < 48 or (ord(word[-1:]) > 57 and ord(word[-1:]) < 65) or (ord(word[-1:]) > 90 and ord(word[-1:]) < 97) or (ord(word[-1:]) > 122 and ord(word[-1:]) < 192) or ord(word[-1:]) > 256:
                #         if word[-1:] in header.keys():
                #             header[word[-1:]] += 1
                #         else:
                #             header[word[-1:]] = 1
                #         word = word[:-1]
                #     if word in header.keys():
                #         header[word] += 1
                #     else:
                #         header[word] = 1     TODO SE TIVER SACO EU USO ISSO
                # elif word == ' ':
                #     header[' '] += 1
                # elif word == '\n':
                #     header['@'] += 1
                # else:
                #     if word in header.keys():
                #         header[word] += 1
                #     else:
                #         header[word] = 1

        for word in header.keys():
            list.append(Node(symbol=word, value=header[word]))

    file.close()
    return list

def compressFile(inputPath, outputPath, list, wordOrLetter):
    inputFile = open(inputPath, encoding='utf-8', mode='r')
    outputFile = open(outputPath, mode='bw')
    size = len(list)
    print(size)
    outputFile.write(bytes(str(size) + '\n', encoding='utf-8'))
    header = {}
    toWrite = ''
    for symbol in list:
        buffer = bytearray()
        string = symbol.symbol + '¨' + symbol.binary + '\n'
        toWrite = [i.encode('ansi') for i in string]
        string = toWrite[0]
        for i in range(1, len(toWrite)):
            string += toWrite[i]
        header[symbol.symbol] = symbol.binary
        outputFile.write(string)
    binaryString = ''

    if wordOrLetter == 0:
        buf = inputFile.read()
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
    else:
        buffer = bytearray()
        buf = inputFile.readlines()
        binaryString = ''
        string = ''
        for line in buf:
            aux = ''.join(line.split('\n')).split(' ')
            for i, word in enumerate(aux):
                if i == len(aux)-1:
                    if word in header.keys():
                        binaryString += header[word]
                else:
                    if word in header.keys():
                        binaryString += header[word]
                        binaryString += header[' ']
                # if word == '\n':
                #     binaryString += header['@']
                # elif word == ' ':
                #     binaryString += header[' ']
                # elif word != ' ' and word != '\n' and word != '' and len(word) > 1:
                #     while ord(word[-1:]) < 48 or (ord(word[-1:]) > 57 and ord(word[-1:]) < 65) or (ord(word[-1:]) > 90 and ord(word[-1:]) < 97) or (ord(word[-1:]) > 122 and ord(word[-1:]) < 192) or ord(word[-1:]) > 256:   
                #         binaryString += header[word[-1:]]
                #         word = word[:-1]
                #     if word in header.keys():
                #         binaryString += header[word]
                #         binaryString += header[' ']   TODO SE TIVER SACO EU USO ISSO
                # else:
                #     if word in header.keys():
                #         binaryString += header[word]
                #         binaryString += header[' ']
            
            binaryString += header['@']
        
        buffer = bytearray()
        i=0
        while i < len(binaryString):
            buffer.append(int(binaryString[i:i+8], base=2))
            i+=8


    outputFile.write(buffer)

    inputFile.close()
    outputFile.close()
    return 0
    

def uncompressFile(inputPath, outputPath, wordOrLetter):
    inputFile = open(inputPath, mode='rb')
    outputFile = open(outputPath, encoding='utf-8', mode='w')
    size = inputFile.readline()
    size = str(size)[2:-3]
    size = int(size)
    # print(size)
    header = {}
    string = ''
    for i in range(size):
        aux = inputFile.readline().decode('ansi')
        # print(aux)
        # for byte in aux:
            
        #     string += byte
        splitstring = ''.join(aux.split('\n')).split('¨')
        print('str: ' + aux)
        string = ''
        header[splitstring[1]] = splitstring[0]
            
    print(header)
    
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
# compressFile("reliquias.txt", "reliquiasComprimida.bin", list, 0)
# uncompressFile('reliquiasComprimida.bin', 'reliquiasDescomprimidas.txt', 0)

# a = readFile("arquivogerado.txt", 1)
# b = createNode(a)
# list = []
# processNode(b, '', list)
# compressFile("arquivogerado.txt", "arquivogeradoComprimida.bin", list, 1)
# uncompressFile('arquivogeradoComprimida.bin', 'arquivogeradoDescomprimidas.txt', 1)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

