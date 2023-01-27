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
            print('\nInsira o nome do arquivo original <-------------------------------------------> 0 - Para voltar')            # print('0 - Voltar')
            fileName = input()
            if fileName == '0':
                options = -1
            else:
                buf, flag = readFile(fileName, 0)
                if flag == 1:
                    print('Erro ao abrir arquivo! Aperte qualquer tecla para continuar')
                    input()
                    options = -1
                elif flag == -1:
                    print('Erro durante a leitura do arquivo! Aperte qualquer tecla para continuar')
                    input()
                    options = -1
                else:
                    print('\nInsira o nome do novo arquivo compactado <------------------------------------> 0 - Para voltar')
                    outputFileName = input()
                    if outputFileName == '0':
                        options = -1
                    else:
                        huffman = createNode(buf)
                        list = []
                        processNode(huffman, '', list)
                        result = compressFile(fileName, outputFileName, list, 0)
                        if result == 0:
                            print('Arquivo compactado com sucesso! Aperte qualquer tecla para continuar')
                        elif result == 1:
                            print('Erro ao abrir arquivo de entrada! Aperte qualquer tecla para continuar')
                        elif result == 2:
                            print('Erro ao abrir arquivo de saída! Aperte qualquer tecla para continuar')
                        elif result == -1:
                            print('Erro ao tentar compactar arquivo! Aperte qualquer tecla para continuar')
                        else:
                            print('Um erro inesperado aconteceu! Aperte qualquer tecla para continuar')
                        input()
                        options = -1

        elif options == '2':
            clear()
            print('\nInsira o nome do arquivo original <-------------------------------------------> 0 - Para voltar')
            fileName = input()
            if fileName == '0':
                options = -1
            else:
                buf, flag = readFile(fileName, 1)
                if flag == 1:
                    print('Erro ao abrir arquivo!')
                elif flag == -1:
                    print('Erro durante a leitura do arquivo!')
                else:
                    print('\nInsira o nome do novo arquivo compactado <------------------------------------> 0 - Para voltar')
                    outputFileName = input()
                    if outputFileName == '0':
                        options = -1
                    else:
                        huffman = createNode(buf)
                        list = []
                        processNode(huffman, '', list)
                        result = compressFile(fileName, outputFileName, list, 1)
                        if result == 0:
                            print('Arquivo compactado com sucesso! Aperte qualquer tecla para continuar')
                        elif result == 1:
                            print('Erro ao abrir arquivo de entrada! Aperte qualquer tecla para continuar')
                        elif result == 2:
                            print('Erro ao abrir arquivo de saída! Aperte qualquer tecla para continuar')
                        elif result == -1:
                            print('Erro ao tentar compactar arquivo! Aperte qualquer tecla para continuar')
                        else:
                            print('Um erro inesperado aconteceu! Aperte qualquer tecla para continuar')
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
                    result = uncompressFile(fileName, outputFileName)
                    if result == 0:
                        print('Arquivo descompactado com sucesso! Aperte qualquer tecla para continuar')
                    elif result == 1:
                        print('Erro ao abrir arquivo de entrada! Aperte qualquer tecla para continuar')
                    elif result == 2:
                        print('Erro ao ler arquivo de saída! Aperte qualquer tecla para continuar')
                    elif result == -1:
                        print('Erro ao descompactar arquivo! Aperte qualquer tecla para continuar')
                    else:
                        print('Um erro inesperado aconteceu! Aperte qualquer tecla para continuar')
                    input()
                    options = -1

        elif options == '0':
            clear()
            print('\n  Encerrando o programa!')
            time.sleep(1.5)
            return 0    
                    
#Estrutura para representar um nó da árvore
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

#Estrutura para representar os símbolos comprimidos
class compressedSymbol:
    def __init__(self, symbol, binary):
        self.symbol = symbol
        self.binary = binary
    
    def __repr__(self):
        return f"symbol: {self.symbol}; binary: {self.binary} "

#Gera o nó pai com base em seus filhos
#Params:
#   Nó da esquerda
#   Nó da direita
#Return:
#   Retorna o nó pai completo
#Pré-Condição: Nenhuma
#Pós-Condição: Gera o nó pai
def fillNode(left, right):
    node = Node(None, 0)
    node.setLeft(left)
    node.setRight(right)
    node.setValue(left.value + right.value)
    return node

#Monta a árvore de acordo com o algoritmo de Huffman
#Params:
#   queue: Uma lista para servir como fila de prioridade
#Return:
#   Retorna a raiz da árvore
#Pré-Condição: Necessita da lista montada corretamente
#Pós-Condição: Monta a árvore
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

#Percorre a árvore codificando os símbolos
#Params:
#   Árvore binária
#   Uma string vazia para armazenar a string binária ao longo da recursão
#   Uma lista vazia para armazenar os símbolos codificados ao longo da recursão
#Return:
#   Não retorna nada
#Pré-Condição: Geração correta da árvore
#Pós-Condição: Preenche a lista com os símbolos comprimidos
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
#   wordOrLetter: Flag que seta como será feita a contagem de frequencias:
#       0 - Por letra
#       1 - Por palavra
#Return: Retorna uma tupla;
#   Uma lista contendo os nós da árvore, em caso de erro retorna uma lista vazia
#   Uma flag que sinaliza se houve erro ou não:
#       0 - Sucesso
#       1 - Falha na abertura do arquivo
#      -1 - Falha na compressão do arquivo 
#Pré-Condição: Arquivo fonte precisa existir
#Pós-Condição: Faz a leitura do arquivo e armazena os nós em uma lista
def readFile(f, wordOrLetter):
    try:
        file = open(f, encoding='utf-8', mode='r')

    except:
        return [], 1

    try:
        if wordOrLetter == 0:
            buf = file.read()
            list = []
            flag = 0
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

    except:
        file.close()
        return [], -1

    file.close()
    
    return list, 0

#Realiza a compressão do arquivo
#Params:
#   inputPath: Caminho do arquivo fonte
#   outputPath: Caminho destinado ao arquivo de saída
#   list: Lista com os símbolos codificados para geração do cabeçalho
#   wordOrLetter: Flag que inidica o tipo de compressão;
#       0 - Por letra;
#       1 - Por palavra;
#Return: 
#   Retorna um inteiro que sinaliza se houve erro ou não;
#       0 - Sucesso
#       1 - Erro na abertura do arquivo fonte
#       2 - Erro na abertura do arquivo de saída
#      -1 - Erro na codificação do arquivo
#Pré-Condição: Sucesso na codificação da árvore
#Pós-Condição: Comprime o arquivo
def compressFile(inputPath, outputPath, list, wordOrLetter):
    try:
        inputFile = open(inputPath, encoding='utf-8', mode='r')
    except:
        return 1
    try:
        outputFile = open(outputPath, mode='bw')
    except: 
        return 2
    try:
        size = len(list)
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


    except:
        inputFile.close()
        outputFile.close()
        return -1

    inputFile.close()
    outputFile.close()

    return 0
    
#Realiza a descompressão do arquivo
#Params:
#   inputPath: Caminho do arquivo a ser descomprimido
#   outputPath: Caminho destinado ao arquivo de saída
#Return:
#   Retorna um inteiro para sinzalização se houve erro ou não:
#       0 - Sucesso
#       1 - Erro na abertura do arquivo a ser descomprimido
#       2 - Erro na abertura do arquivo de saída
#      -1 - Erro na descompressão do arquivo
#Pré-Condição: Arquivo a ser descomprimido precisa estar devidamente montado
#Pós-Condição: Descomprime o arquivo 
def uncompressFile(inputPath, outputPath):
    try:
        inputFile = open(inputPath, mode='rb')

    except:
        return 1

    try:
        outputFile = open(outputPath, encoding='utf-8', mode='w')

    except:
        return 2

    try:
        size = inputFile.readline()
        size = str(size)[2:-3]
        size = int(size)
        header = {}

        for i in range(size):
            aux = inputFile.readline().decode('ansi')
            splitstring = ''.join(aux.split('\n')).split('¨')
            print('str: ' + aux)
            header[splitstring[1]] = splitstring[0]
                        
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
    except:
        inputFile.close()
        outputFile.close()
        return -1

    inputFile.close()
    outputFile.close()
    return 0

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
    sys.exit(main())

