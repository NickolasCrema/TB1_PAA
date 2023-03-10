#Main do programa, funciona como um menu
def main():
    import os
    import time
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
            print('3 - Descompressao')
            print('0 - Sair')
            options = input()
        elif options == '1':
            clear()
            print('\nInsira o nome do arquivo original <-------------------------------------------> 0 - Para voltar')
            fileName = input()
            if fileName == '0':
                options = -1
            else:
                buf, flag, error = readFile(fileName, 0)
                if flag == 1:
                    print('Erro ao abrir arquivo!: ' + repr(error) + '\nAperte ENTER para continuar...')
                    input()
                    options = -1
                elif flag == -1:
                    print('Erro durante a leitura do arquivo!: ' + repr(error) + '\nAperte ENTER para continuar...')
                    input()
                    options = -1

                else:
                    print('\nInsira o nome do novo arquivo compactado <------------------------------------> 0 - Para voltar')
                    outputFileName = input()
                    if outputFileName == '0':
                        options = -1
                    else:
                        init = time.time()
                        huffman = createNode(buf)
                        list = []
                        processNode(huffman, '', list)
                        result, error = compressFile(fileName, outputFileName, list, 0)
                        done = time.time()
                        if result == 0:
                            print('Arquivo compactado com sucesso!\nAperte ENTER para continuar...')
                        elif result == 1:
                            print('Erro ao abrir arquivo de entrada!: ' + repr(error) + '\nAperte ENTER para continuar...')
                        elif result == 2:
                            print('Erro ao abrir arquivo de sa??da!: ' + repr(error) + '\nAperte ENTER para continuar...')
                        elif result == -1:
                            print('Erro ao tentar compactar arquivo!: ' + repr(error) + '\nAperte ENTER para continuar...')
                        else:
                            print('Um erro inesperado aconteceu!: ' + repr(error) + '\nAperte ENTER para continuar...')
                        donetime = done - init
                        print('tempo de execu????o: ' + str(donetime))
                        input()
                        options = -1

        elif options == '2':
            clear()
            print('\nInsira o nome do arquivo original <-------------------------------------------> 0 - Para voltar')
            fileName = input()
            if fileName == '0':
                options = -1
            else:
                buf, flag, error = readFile(fileName, 1)
                if flag == 1:
                    print('Erro ao abrir arquivo!: ' + repr(error))
                    input()
                    options = -1
                elif flag == -1:
                    print('Erro durante a leitura do arquivo!: ' + repr(error))
                    input()
                    options = -1
                else:
                    print('\nInsira o nome do novo arquivo compactado <------------------------------------> 0 - Para voltar')
                    outputFileName = input()
                    if outputFileName == '0':
                        options = -1
                    else:
                        init = time.time()
                        huffman = createNode(buf)
                        list = []
                        processNode(huffman, '', list)
                        result, error = compressFile(fileName, outputFileName, list, 1)
                        done = time.time()
                        donetime = done - init
                        if result == 0:
                            print('Arquivo compactado com sucesso!\nAperte ENTER para continuar...')
                        elif result == 1:
                            print('Erro ao abrir arquivo de entrada!: ' + repr(error) + '\nAperte ENTER para continuar...')
                        elif result == 2:
                            print('Erro ao abrir arquivo de sa??da!: ' + repr(error) + '\nAperte ENTER para continuar...')
                        elif result == -1:
                            print('Erro ao tentar compactar arquivo!: ' + repr(error) + '\nAperte ENTER para continuar...')
                        else:
                            print('Um erro inesperado aconteceu!: ' + repr(error) + '\nAperte ENTER para continuar...')
                        print('tempo de execu????o: ' + str(donetime))
                        input()
                        options = -1

        elif options == '3':
            clear()
            print('\nInsira o nome do arquivo compactado <-----------------------------------------> 0 - Para voltar')
            fileName = input()
            if fileName == '0':
                options = -1
            else:
                print('\nInsira o nome do novo arquivo descompactado <---------------------------------> 0 - Para voltar')
                outputFileName = input()
                if outputFileName == '0':
                    options = -1
                else:
                    init = time.time()
                    result, error = uncompressFile(fileName, outputFileName)
                    done = time.time()
                    donetime = done - init
                    if result == 0:
                        print('Arquivo descompactado com sucesso!\nAperte ENTER para continuar...')
                    elif result == 1:
                        print('Erro ao abrir arquivo de entrada!: ' + repr(error) + '\nAperte ENTER para continuar...')
                    elif result == 2:
                        print('Erro ao ler arquivo de sa??da!: ' + repr(error) + '\nAperte ENTER para continuar...')
                    elif result == -1:
                        print('Erro ao descompactar arquivo!: ' + repr(error) + '\nAperte ENTER para continuar...')
                    else:
                        print('Um erro inesperado aconteceu!: ' + repr(error) + '\nAperte ENTER para continuar...')
                    print('tempo de execu????o: ' + str(donetime))
                    input()
                    options = -1

        elif options == '0':
            clear()
            print('\n  Encerrando o programa!')
            time.sleep(1.5)
            return 0    
                    
#Estrutura para representar um n?? da ??rvore
class Node:
    def __init__(self, symbol, value):
        self._symbol = symbol
        self._value = value
        self._left = None
        self._right = None
    
    def __repr__(self):
        return f"symbol: {self.symbol}; value: {self.value}"

    @property
    def symbol(self):
        return self._symbol
    
    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol
    
    @property 
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

    @property
    def left(self):
        return self._left
    
    @left.setter
    def left(self, left):
        self._left = left
    
    @property
    def right(self):
        return self._right
    
    @right.setter
    def right(self, right):
        self._right = right

#Estrutura para representar os s??mbolos comprimidos
class compressedSymbol:
    def __init__(self, symbol, binary):
        self.symbol = symbol
        self.binary = binary
    
    def __repr__(self):
        return f"symbol: {self.symbol}; binary: {self.binary} "

#Gera o n?? pai com base em seus filhos
#Params:
#   N?? da esquerda
#   N?? da direita
#Return:
#   Retorna o n?? pai completo
#Pr??-Condi????o: Nenhuma
#P??s-Condi????o: Gera o n?? pai
def fillNode(left, right):
    node = Node(None, 0)
    node.left = left
    node.right = right
    node.value = left.value + right.value
    return node

#Monta a ??rvore de acordo com o algoritmo de Huffman
#Params:
#   queue: Uma lista para servir como fila de prioridade
#Return:
#   Retorna a raiz da ??rvore
#Pr??-Condi????o: Necessita da lista montada corretamente
#P??s-Condi????o: Monta a ??rvore
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

#Percorre a ??rvore codificando os s??mbolos
#Params:
#   ??rvore bin??ria
#   Uma string vazia para armazenar a string bin??ria ao longo da recurs??o
#   Uma lista vazia para armazenar os s??mbolos codificados ao longo da recurs??o
#Return:
#   N??o retorna nada
#Pr??-Condi????o: Gera????o correta da ??rvore
#P??s-Condi????o: Preenche a lista com os s??mbolos comprimidos
def processNode(node, binary, list):
    if node == None:
        return
    elif node.symbol != None:
        list.append(compressedSymbol(node.symbol, binary))
    processNode(node.left, binary + "0", list)
    processNode(node.right, binary + "1", list)

#Realiza a leitura do arquivo fonte e conta a frequencia de cada simbolo, 
#sendo a contagem por letra ou por palavra
#Params: 
#   f: Caminho do arquivo fonte 
#   wordOrLetter: Flag que seta como ser?? feita a contagem de frequencias:
#       0 - Por letra
#       1 - Por palavra
#Return: Retorna uma tupla;
#   Uma lista contendo os n??s da ??rvore, em caso de erro retorna uma lista vazia
#   Uma flag que sinaliza se houve erro ou n??o:
#       0 - Sucesso
#       1 - Falha na abertura do arquivo
#      -1 - Falha na leitura do arquivo 
#Pr??-Condi????o: Arquivo fonte precisa existir
#P??s-Condi????o: Faz a leitura do arquivo e armazena os n??s em uma lista
def readFile(f, wordOrLetter):
    try:
        file = open(f, encoding='utf-8', mode='r')

    except Exception as error:
        return [], 1, error

    try:
        if wordOrLetter == 0:
            buf = file.read()
            list = []
            flag = 0
            list.append(Node(str('@'), 0))
            list.append(Node('<EOF>', 1))
            for symbol in buf:
                if symbol == '\n':
                    for s in list:
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
            list.append(Node('<EOF>', 1))
            for lineCount, line in enumerate(buf):
                aux = ''.join(line.split('\n')).split(' ')
                header['@'] += 1
                if len(aux) == 1 and aux[0] == '':
                    header['@'] += 1
                else:
                    for i, word in enumerate(aux):
                        symbols = []
                        if word != '':
                            if len(word) > 1:
                                while not word[-1:].isalnum():
                                    if len(word) == 1:
                                        break
                                    else:
                                        if header.get(word[-1:]) is not None:
                                            header[word[-1:]] += 1
                                        else:
                                            header[word[-1:]] = 1
                                        # symbols.append(word[-1:])
                                        word = word[:-1]
                                if header.get(word) is not None:
                                    header[word] += 1
                                else:
                                    header[word] = 1
                                if i != len(aux)-1:
                                    header[' '] += 1
                            else:
                                if header.get(word) is not None:
                                    header[word] += 1
                                    header[' '] += 1
                                else:
                                    header[word] = 1
                                    header[' '] += 1
                    if lineCount != len(line)-1:
                        header['@'] += 1
            for word in header.keys():
                list.append(Node(symbol=word, value=header[word]))

    except Exception as error:
        file.close()
        return [], -1, error

    file.close()
    
    return list, 0, ''

#Realiza a compress??o do arquivo
#Params:
#   inputPath: Caminho do arquivo fonte
#   outputPath: Caminho destinado ao arquivo de sa??da
#   list: Lista com os s??mbolos codificados para gera????o do cabe??alho
#   wordOrLetter: Flag que inidica o tipo de compress??o;
#       0 - Por letra;
#       1 - Por palavra;
#Return: 
#   Retorna um inteiro que sinaliza se houve erro ou n??o;
#       0 - Sucesso
#       1 - Erro na abertura do arquivo fonte
#       2 - Erro na abertura do arquivo de sa??da
#      -1 - Erro na codifica????o do arquivo
#Pr??-Condi????o: Sucesso na codifica????o da ??rvore
#P??s-Condi????o: Comprime o arquivo
def compressFile(inputPath, outputPath, list, wordOrLetter):

    try:
        inputFile = open(inputPath, encoding='utf-8', mode='r')
    except Exception as error:
        return 1, error

    try:
        outputFile = open(outputPath, mode='bw')
    except Exception as error: 
        return 2, error

    try:
        size = len(list)
        outputFile.write(bytes(str(size) + '\n', encoding='utf-8'))
        header = {}
        toWrite = ''
        for symbol in list:
            buffer = bytearray()
            string = symbol.symbol + '??' + symbol.binary + '\n'
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
            binaryString += header['<EOF>']
            
            while i < len(binaryString):
                buffer.append(int(binaryString[i:i+8], base=2))
                i += 8
        else:
            buf = inputFile.readlines()
            binaryString = ''
            string = ''
            for lineCount, line in enumerate(buf):
                aux = ''.join(line.split('\n')).split(' ')
                if len(aux) == 1 and aux[0] == '':
                    binaryString += header['@']
                else:
                    for i, word in enumerate(aux):
                        symbols = []
                        if word == '' and i != len(aux)-1:
                            binaryString += header[' ']
                        elif word == '' and i == len(aux)-1:
                            continue
                        else:
                            if len(word) > 1:
            
                                while not word[-1:].isalnum():
                                    if len(word) == 1:
                                        break
                                    else:
                                        symbols.append(word[-1:])
                                        word = word[:-1]
                                if header.get(word) is not None:
                                    binaryString += header[word]
                                    for symbol in symbols:
                                        binaryString += header[symbol]
                                    if i != len(aux)-1:
                                        binaryString += header[' ']
                            else:
                                if header.get(word) is not None:
                                    binaryString += header[word]
                                else:
                                    binaryString += header[word]
                                if i != len(aux)-1:
                                        binaryString += header[' ']

                    if lineCount != len(line)-1:
                        binaryString += header['@']

            binaryString += header['<EOF>']
            buffer = bytearray()
            i=0
            while i < len(binaryString):
                buffer.append(int(binaryString[i:i+8], base=2))
                i+=8

        outputFile.write(buffer)

    except Exception as error:
        inputFile.close()
        outputFile.close()
        return -1, error

    inputFile.close()
    outputFile.close()

    return 0, ''
    
#Realiza a descompress??o do arquivo
#Params:
#   inputPath: Caminho do arquivo a ser descomprimido
#   outputPath: Caminho destinado ao arquivo de sa??da
#Return:
#   Retorna um inteiro para sinaliza????o se houve erro ou n??o:
#       0 - Sucesso
#       1 - Erro na abertura do arquivo a ser descomprimido
#       2 - Erro na abertura do arquivo de sa??da
#      -1 - Erro na descompress??o do arquivo
#Pr??-Condi????o: Arquivo a ser descomprimido precisa estar devidamente montado
#P??s-Condi????o: Descomprime o arquivo 
def uncompressFile(inputPath, outputPath):

    try:
        inputFile = open(inputPath, mode='rb')
    except Exception as error:
        return 1, error

    try:
        outputFile = open(outputPath, encoding='utf-8', mode='w')
    except Exception as error:
        return 2, error

    try:
        size = inputFile.readline()
        size = str(size)[2:-3]
        size = int(size)
        header = {}
        for i in range(size):
            aux = inputFile.readline().decode('ansi')
            splitstring = ''.join(aux.split('\n')).split('??')
            if splitstring[0] == '<EOF>':
                header[splitstring[0]] = splitstring[1]
            else:
                header[splitstring[1]] = splitstring[0]
        buffer = inputFile.read()
        binaryStr = ''
        for byte in buffer:
            binary = format(byte, '08b')
            for bit in binary:
                binaryStr += bit
                if binaryStr == header['<EOF>']:
                    break
                if binaryStr in header.keys():
                    if header[binaryStr] == '@':
                        outputFile.write('\n')
                    else:
                        outputFile.write(header[binaryStr])
                    binaryStr = ''

    except Exception as error:
        inputFile.close()
        outputFile.close()
        return -1, error

    inputFile.close()
    outputFile.close()
    return 0, ''

if __name__ == '__main__':
    import sys
    sys.exit(main())