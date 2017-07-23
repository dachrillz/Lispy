#imports.
from collections import deque # used for the parsing tree

#############################
# Classes
#############################

class Environment():
    def __init__(self,outer = None):
        self.outer = outer
        self.variables = {}
        
    def addVar(self,key,variable):
        if self.isMember(key):
            return None
        else:
            self.variables[key] = variable
            return variable
            
    def remVar(self,key):
        del self.variables[key]
        
    def isMember(self,key):
        if key in self.variables:
            return True
        else:
            return False
        
    def getMember(self,key):
        print('heheh')
        print(key)
        if self.isMember(key) == True:
            return self.variables[key]
        else:
            print('variable not found') # do recursion here!
            
    def define(self,name,value):
        '''
        Support function for the environment function, define.
        '''
        if (self.isMember(name)):
            print('Variable already bound! Change to expection later!')
            return name
        
        else:
            self.addVar(name,value)
            
        return value
    
def createList(x,y):
    '''
    This is a support function for the Environment Function, 'list'
    '''
    if type(x) == int:
        x = [x]
    return x + [y]
    
        
def EnvFact():
    Env = Environment()
    
    #Env.addVar('+',(lambda x,y: x+y))
    Env.addVar('+',(lambda x,y: x+y))
    Env.addVar('-',(lambda x,y: x-y))
    Env.addVar('*',(lambda x,y: x*y))
    Env.addVar('/',(lambda x,y: x/y))
    Env.addVar('list', (lambda x,y: createList(x,y)))
    Env.addVar('head', (lambda x,y: y[0]))
    Env.addVar('tail', (lambda x,y: y[1]))
    Env.addVar('def', lambda x,y: Env.define(x,y))

    return Env

#############################
# Functions
#############################

characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
numbers = ['0','1','2','3','4','5','6','7','8','9']
keywords = ['def','let']


def convertStringToQueue(string):
    stringDeque = deque([])
    for s in string:
        stringDeque.append(s)
        
    return stringDeque

def AST(stringDeque):
    """ Return the abstract Syntax tree. (String -> AST)"""
    
    parentMem = False
    symbolParsed = False
    syntaxList = deque([])

    while len(stringDeque) != 0:
        s = stringDeque.popleft()
        
        if s == '(' and parentMem == True:
                #recursive call.
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
            
        elif s in numbers:
            space = False
            localList = ['Num:', s]
            while space == False:
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
                if stringDeque[0] in characters:
                    localList.append(stringDeque.popleft())
                else:
                    space = True
            syntaxList.append(''.join(localList))
            del localList
    

'''  
def eval(AST,env):
    Symbol = ''
    ArithmeticValue = None #NEEDS A BETTER NAME!
    first = True # helpvariable for multiplication and div

    while len(AST) != 0:
        s = AST.popleft()
        
        
        if type(s) is deque:
            if env.isMember(Symbol) == True:
                ArithmeticValue = env.getMember(Symbol)(ArithmeticValue,eval(s,env))
                

    
        elif env.isMember(Symbol) == True:
            if first:
                if s[:4] == 'Num:':
                    ArithmeticValue = int(s[4:])
                    first = False
                else:
                    ArithmeticValue = s[4:]
                    first = False
                    
            else:
                print(ArithmeticValue)
                if(env.isMember(ArithmeticValue) == True):
                        ArithmeticValue = int(env.getMember(ArithmeticValue))

                ArithmeticValue = env.getMember(Symbol)(ArithmeticValue,int(s[4:]))

            
      
        #interpret different symbols, Double check this one it might be totally unneccessary
        # to have different cases!
        elif s[0:4] == 'Sym:':
                
            if s[4:9] == 'list':
                Symbol = 'list'
                s = AST.popleft()
                s = s[4:]
                s = int(s)
                ArithmeticValue = [s] #here one might have to do a check!
                first = False
                
                
            elif s[4:7] == 'def':
                s1 = AST.popleft()[4:]
                s2 = AST.popleft()[4:]
                Symbol = s[4:]
                ArithmeticValue = env.addVar(s1,s2)

            elif s[4:] in env.variables:
                Symbol = s[4:]
   
            elif env.isMember(s[4:]) == True and s[4:9] != 'list' :
                ArithmeticValue = env.getMember(s[4:])


    return ArithmeticValue
'''

def eval(AST,env):
    boundFunction = None
    first = True
    evaluatedValue = 0
    
    if(len(AST) == 1): #if the length of the expression is only 1, we can evaluate directly.
        evaluatedSymbol = eval_AST(AST.popleft(),env)
        
        if(env.isMember(evaluatedSymbol)):
            return evaluatedSymbol
        else:
            print('Variable is not member of environment. Change to expection class later')
            return None

    while(len(AST) != 0):
        s = AST.popleft()
        
        if(type(s) == deque): #if deque call recursively
            evaluatedSymbol = eval(s,env)
            if boundFunction != None: #if a function is already bound use it to calculate.
                evaluatedValue = boundFunction(evaluatedValue,evaluatedSymbol)
                first = False
                

        else: #if not deque we evaluate
            evaluatedSymbol = eval_AST(s,env) #retrieve the value or function from the AST.
            
            if s == 'Sym:def': #def is a special keyword that we treat specially
                if(env.isMember(AST[0][4:])):
                    return AST[0][4:] #the variable was already defined, this is sloppy hacky code.
                        
            if callable(evaluatedSymbol): #this checks whether evaluated is a callable object. (that is: is it a function?)
                boundFunction = evaluatedSymbol
                
            elif boundFunction != None and first == True: #if the first symbol, just assign it.
                evaluatedValue = evaluatedSymbol
                first = False
                
            elif boundFunction != None: #here we evalute the values to a function bound in the environment.
                evaluatedValue = boundFunction(evaluatedValue,evaluatedSymbol)

    

    return evaluatedValue


def eval_AST(s,env):
    '''
    Support function for the EVAL function.
    Three cases, list, symbol or otherwise.
    Otherwise not implemented currently.
    '''

    #case of symbol
    if 'Sym:' in s:
        symbol = s[4:]
    
        if env.isMember(symbol):
            evaluated = env.getMember(symbol)
            return evaluated
            
        else:
            return symbol
            
    #case of number.    
    elif 'Num:' in s:
        return int(s[4:])
        
        
    #case of float?
    
    #case of string?
        
        

'''
Start the main evaluation loop
'''
def RunLanguage():  
    #create the global environment.
    glob = EnvFact()
    while(True):
        print('fisk')

        InputString = input("Input> ")
        
        if InputString == 'bajs':
            for item in glob.variables:
                print(item)

        else:
            print("To be passed to AST " + InputString)
            
            InputString = convertStringToQueue(InputString) #convert to a deque
            
            abstractSyntaxTree = AST(InputString)
            
            print('abstractSyntaxTree')
            print(abstractSyntaxTree)
            
            evaluatedValue = eval(abstractSyntaxTree,glob)
            
            print('evaluated value')
            print(evaluatedValue)

#############################
# Run main 
#############################     
  
RunLanguage()