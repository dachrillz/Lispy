# imports.
from collections import deque  # used for the parsing tree
import sys  # used for reading other files.

from pdb import set_trace as bp  # debugging

#imports from the same folder
#from AST import AST as AST


#############################
# Classes
#############################

class Environment():
    def __init__(self, outer=None):
        self.outer = outer
        self.variables = {}


    def __str__(self, i=0):
        list = ['|Items in env ' + str(i) + '|']
        for item in self.variables:
            list.append(item)
            list.append(':')

        if self.outer != None:
            i += 1
            list.append(self.outer.__str__(i))

        return ' '.join(list)

    def addVar(self, key, variable):
        if self.isMember(key):
            return None
        else:
            self.variables[key] = variable
            return variable

    def remVar(self, key):
        del self.variables[key]

    def isMember(self, key):
        if key in self.variables:
            return True
        else:
            return False

    def getMember(self, key):
        if self.isMember(key) == True:
            return self.variables[key]
        else:
            if self.outer == None:
                print('member not found in getMember key: ' + str(key))
                return None
            else:
                return self.outer.getMember(key)

    def define(self, name, value):
        '''
        Support function for the environment function, define.
        '''
        if (self.isMember(name)):
            print('Variable already bound! Change to expection later!')
            return name

        else:
            self.addVar(name, value)

        return value


def EnvFact():
    Env = Environment()

    # Env.addVar('+',(lambda x,y: x+y))
    Env.addVar('+', (lambda x, y: x + y))
    Env.addVar('-', (lambda x, y: x - y))
    Env.addVar('*', (lambda x, y: x * y))
    Env.addVar('/', (lambda x, y: x / y))
    Env.addVar('list', (lambda x, y: createList(x, y)))
    Env.addVar('head', (lambda x, y: y[0]))
    Env.addVar('tail', (lambda x, y: y[1:]))
    Env.addVar('def', lambda x, y: Env.define(x, y))
    Env.addVar('let', lambda x, y: bindEnv(x, y))
    Env.addVar('print', lambda x, y: LispPrint(y, Env))
    Env.addVar('if',lambda x: print('dummyfunction'))

    return Env


#############################
# Functions
#############################

characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z',
              'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
keywords = ['def', 'let']

def AST(stringDeque):
    """ Return the abstract Syntax tree. (String -> AST)"""

    parentMem = False
    symbolParsed = False
    neg = False
    syntaxList = deque([])

    while len(stringDeque) != 0:
        s = stringDeque.popleft()

        if s == '(' and parentMem == True:
            # recursive call.
            stringDeque.appendleft('(')
            syntaxList.append(AST(stringDeque))

        if s == '(':
            parentMem = True

        elif s == ')' and parentMem == True:
            parentMem = False
            return syntaxList

        elif (s == '+' or s == '-' or s == '*' or s == '/') and (symbolParsed == False):
            syntaxList.append('Sym:' + s)
            symbolParsed = True
            
        elif(s == '-') and (symbolParsed == True): #check for negative numbers
            neg = True

        elif s in numbers or neg == True:
            space = False
            if neg == True: #neg was found
                localList = ['Num:', '-' + s]
                neg = False
            else:
                localList = ['Num:', s]
            while space == False:
                if len(stringDeque) == 0:  # if only one element (that is a)
                    syntaxList.append(''.join(localList))
                    return syntaxList
                else:
                    if stringDeque[0] in numbers:
                        localList.append(stringDeque.popleft())
                    else:
                        space = True

            syntaxList.append(''.join(localList))
            del localList

        elif s in characters:
            space = False
            localList = ['Sym:', s]
            while space == False:
                if len(stringDeque) == 0:  # if only one element (that is a)
                    syntaxList.append(''.join(localList))
                    return syntaxList
                else:
                    if stringDeque[0] in characters:
                        localList.append(stringDeque.popleft())
                    else:
                        space = True
            syntaxList.append(''.join(localList))
            del localList


def generateFunction(eval, Environment, ast, env, params):
    def fn(*args):
        return eval(ast, Environment(env, params, args))

    return fn


def bindEnv(x, y):
    x = Environment(y)


def LispPrint(y, env):
    '''
    Support function for print.
    '''
    print(y)
    return y


def defVar(evaluatedSymbol, AST, env):
    boundFunction = evaluatedSymbol
    if env.isMember(
            AST[0][4:]):  # if s is def, and the next value in AST i already defined -> the variable was already bound.
        return AST[0][4:]
    else:  # else bind the variable.
        s1 = AST.popleft()
        s2 = AST.popleft()
        s1 = s1[4:]
        if type(s2) == deque:
            s2 = eval(s2, env)
        else:
            s2 = eval_AST(s2, env)
        evaluatedValue = boundFunction(s1, s2)
        boundFunction = None
        return evaluatedValue


def createList(x, y):
    '''
    This is a support function for the Environment Function Factory, 'list'
    '''
    if type(x) == int:
        x = [x]
    return x + [y]


def convertStringToQueue(string):
    stringDeque = deque([])
    for s in string:
        stringDeque.append(s)

    return stringDeque


def eval(AST, env):

    boundFunction = None
    first = True
    evaluatedValue = 0

    if (isinstance(AST, str)):
        return eval_AST(AST, env)

    if (len(AST) == 1):  # if the length of the expression is only 1, we can evaluate directly.
        s = AST.popleft()

        if (env.getMember(s[4:]) != None or s[:4] == 'Num:'):
            return eval_AST(s, env)
        else:
            print('Variable is not member of environment. Change to expection class later1')
            return None

    while (len(AST) != 0):
        s = AST.popleft()

        if (type(s) == deque):  # if deque call recursively
            evaluatedSymbol = eval(s, env)
            argumentList = []
            if boundFunction != None:  # if a function is already bound use it to calculate.
                evaluatedValue = boundFunction(evaluatedValue, evaluatedSymbol)
                first = False
            elif callable(evaluatedSymbol):
                if (type(AST[0]) == deque):
                    argumentList.append(eval(AST.popleft(), env))
                else:
                    while (len(AST) != 0):
                        argumentList.append(eval_AST(AST.popleft(), env))
                # evaluatedValue = evaluatedSymbol(evaluatedValue)
                evaluatedValue = evaluatedSymbol(*argumentList)
                # evaluatedValue = evaluatedSymbol(evaluatedValue)
                return evaluatedValue
            else:
                evaluatedValue = evaluatedSymbol


        else:  # if not deque we evaluate
            evaluatedSymbol = eval_AST(s, env)  # retrieve the value or function from the AST.

            if s == 'Sym:def':
                evaluatedValue = defVar(evaluatedSymbol, AST, env)


            elif s == 'Sym:let':  # let is a special keyword as well.
                # some conditionals so it does this right, pop a deque and do the let while not empty.
                if type(AST[0]) == deque:
                    env = Environment(env)  # create the new environment.
                    s = AST.popleft()
                    while (len(s) != 0):
                        letS = s.popleft()
                        s1 = letS[0]
                        s1 = s1[4:]
                        if type(letS[1]) == deque:  # calls eval here if element need to be evaluated.
                            s2 = eval(letS[1], env)
                        else:
                            s2 = letS[1]
                            s2 = eval_AST(s2, env)

                        env.define(s1, s2)
                    if (type(AST[0]) == deque):
                        evaluatedValue = eval(AST.popleft(), env)
                    else:
                        evaluatedValue = eval(AST, env)

                else:
                    print('error here, a deque was not passed to let.')

                evaluatedSymbol = None  # resets the bound function.
                first = False

            elif s == 'Sym:if':
                s = AST.popleft()
                s = eval_AST(s, env)
                if s == 0:
                    return eval(AST[1], env)
                else:
                    return eval(AST[0], env)


            elif s == 'Sym:fun':
                s1 = AST.popleft()
                s2 = AST.popleft()

                def GenerateFunction(name, variables, body):
                    variablesList = deque([])
                    for var in variables:
                        variablesList.append(var)

                    def func1(*args):
                        nonlocal variablesList
                        localEnv = Environment(env)
                        i = 0

                        variablesListCopy = deque([]) #because deque
                        for item in variablesList:
                            variablesListCopy.append(item)

                        for arg in args: #copy over values to the bounded variables.
                            if type(variables[i] == int):
                                variablesListCopy.insert(2 * (i) + 1, 'Num:' + str(arg))
                            else:
                                print('no int passed to generateFunction function, error')
                            i += 1

                        while len(variablesListCopy) != 0:
                            defVar(localEnv.define, variablesListCopy, localEnv)

                        del(variablesListCopy)

                        bodyCopy = deque([]) #because it is a deque!
                        for item in body:
                            bodyCopy.append(item)
                        return eval(bodyCopy, localEnv)

                    func1.__name__ = name
                    return func1

                GeneratedFunction = GenerateFunction('hej', s1, s2)
                return GeneratedFunction
                # print(inspect.getsource(test))
                # print(test(0))
                # return generateFunction(eval,Environment,s2,env,s1)

            if callable(
                    evaluatedSymbol):  # this checks whether evaluated is a callable object. (that is: is it a function?)
                boundFunction = evaluatedSymbol
                while (len(AST) != 0):
                    s = AST.popleft()
                    if first == True and len(AST) != 0:
                        if (type(s) == deque):
                            evaluatedSymbol = eval(s, env)
                        else:
                            evaluatedSymbol = eval_AST(s, env)
                        evaluatedValue = evaluatedSymbol
                        first = False
                    else:
                        if (type(s) == deque):
                            evaluatedSymbol = eval(s, env)
                        else:
                            evaluatedSymbol = eval_AST(s, env)
                        evaluatedValue = boundFunction(evaluatedValue, evaluatedSymbol)


            elif env.isMember(evaluatedSymbol) == False and first == True:
                print('the symbol was not found in the environment')
                return None

    return evaluatedValue


def eval_AST(s, env):
    '''
    Support function for the EVAL function.
    Three cases, list, symbol or otherwise.
    Otherwise not implemented currently.
    '''

    # case of symbol
    if 'Sym:' in s:
        symbol = s[4:]
        evaluated = env.getMember(symbol)
        if evaluated != None:
            return evaluated

        else:
            return symbol

    # case of number.
    elif 'Num:' in s:
        return int(s[4:])


        # case of float?

        # case of string?





