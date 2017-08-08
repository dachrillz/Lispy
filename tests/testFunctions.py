import sys
sys.path.append(sys.path[0][:-6]) #this is incredibly hacky and breaks if the folder name changes, or if the current folder does not happen to be att index 0.
from Language import *

print('Setting up Environment for testing in testFunctions.py')
glob = EnvFact() #called from language

def resetEnv():
    print('Setting up Environment for testing in testFunctions.py')
    global glob
    glob = EnvFact()
    
    
def importCore():
    ''' temporart function'''
    global glob
    
    with open('../core.ly') as f:  
        for line in f:
            line = line.replace('\n', '')
            if bool(line) and not line[0:2] == ';;':
                try:
                    InputString = convertStringToQueue(line)
                    abstractSyntaxTree = AST(InputString)
                    evaluatedValue = eval(abstractSyntaxTree, glob)
                    print(evaluatedValue)
                except:
                    print('Error in the parsing of file.' + line)

    print(glob)
    f.close()


def testExpression(inputString):
    inputString = convertStringToQueue(inputString)
    parsedTree = AST(inputString)
    evaluatedValue = eval(parsedTree,glob)
    
    
    return evaluatedValue
    
    
    
def testFunction(expressionList,expectedValueList):
    for i in range (len(expectedValueList)):
        print(expressionList[i], '=>' ,expectedValueList[i])
        try:
            assert testExpression(expressionList[i]) == expectedValueList[i]
        except:
            print('ERROR IN EXPRESSION: ' + expressionList[i])