#imports.
from collections import deque # used for the parsing tree
import sys # used for reading other files.

#############################
# Classes
#############################

class Environment():
    def __init__(self,outer = None):
        self.outer = outer
        self.variables = {}
        
        
    def __str__(self, i = 0):
        list = ['|Items in env ' + str(i) + '|']
        for item in self.variables:
            list.append(item)
            list.append(':')
            
        if self.outer != None:
            i += 1
            list.append(self.outer.__str__(i))
            

        return ' '.join(list)
        
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
        if self.isMember(key) == True:
            return self.variables[key]
        else:
            if self.outer == None:
                return None
            else:
                return self.outer.getMember(key)
            
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
    
       
def EnvFact():
    Env = Environment()
    
    #Env.addVar('+',(lambda x,y: x+y))
    Env.addVar('+',(lambda x,y: x+y))
    Env.addVar('-',(lambda x,y: x-y))
    Env.addVar('*',(lambda x,y: x*y))
    Env.addVar('/',(lambda x,y: x/y))
    Env.addVar('list', (lambda x,y: createList(x,y)))
    Env.addVar('head', (lambda x,y: y[0]))
    Env.addVar('tail', (lambda x,y: y[1:]))
    Env.addVar('def', lambda x,y: Env.define(x,y))
    Env.addVar('let', lambda x,y: bindEnv(x,y))
    Env.addVar('print', lambda x,y: LispPrint(y))

    return Env

#############################
# Functions
#############################

characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0','1','2','3','4','5','6','7','8','9']
keywords = ['def','let']

def bindEnv(x,y):
    print('hej')
    x = Environment(y)
    
def LispPrint(y):
    '''
    Support function for print.
    '''
    print(y)
    return y

def createList(x,y):
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
                if len(stringDeque) == 0: #if only one element (that is a, or 5)
                    syntaxList.append(''.join(localList))
                    return syntaxList
                else:
                    if stringDeque[0] in characters:
                        localList.append(stringDeque.popleft())
                    else:
                        space = True
            syntaxList.append(''.join(localList))
            del localList
    

def eval(AST,env):
    print('eval')
    boundFunction = None
    first = True
    evaluatedValue = 0
    
    if(len(AST) == 1): #if the length of the expression is only 1, we can evaluate directly.
        s = AST.popleft()
 
        if(env.isMember(s[4:])):
            return eval_AST(s,env)
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
            else:
                evaluatedValue = evaluatedSymbol
                

        else: #if not deque we evaluate
            evaluatedSymbol = eval_AST(s,env) #retrieve the value or function from the AST.
   
            if s == 'Sym:def' and env.isMember(AST[0][4:]): #if s is def, and the next value in AST i already defined -> the variable was already bound.
                return AST[0][4:]
                    
            elif s == 'Sym:let': #let is a special keyword as well.
                #some conditionals so it does this right, pop a deque and do the let while not empty.
                if type(AST[0]) == deque:
                    env = Environment(env) #create the new environment.
                    s = AST.popleft()
                    while(len(s) != 0):
                        letS = s.popleft()
                        s1 = letS[0]
                        s1 = s1[4:]
                        if type(letS[1]) == deque: #calls eval here if element need to be evaluated.
                            s2 = eval(letS[1],env)
                        else:
                            s2 = letS[1]
                            s2 = eval_AST(s2,env)
                            
                        env.define(s1,s2)
                else:
                    print('error here, a deque was not passed to let.')
                
                evaluatedSymbol = None #resets the bound function.
                first = False
                        
            if callable(evaluatedSymbol): #this checks whether evaluated is a callable object. (that is: is it a function?)
                boundFunction = evaluatedSymbol
                
            elif boundFunction != None and first == True and len(AST) == 0: #this means a single argument was passed to function.
                if env.isMember(s[4:]):
                    evaluatedValue = boundFunction(evaluatedValue,evaluatedSymbol)
                else:
                    print('Variable \"', s[4:], '\" was not bound in the evalution of function + 1 argument')
             
            elif boundFunction != None and first == True: #if the first symbol, just assign it.
                evaluatedValue = evaluatedSymbol
                first = False
                
            elif boundFunction != None: #here we evalute the values to a function bound in the environment.
                evaluatedValue = boundFunction(evaluatedValue,evaluatedSymbol)
                
            elif env.isMember(evaluatedSymbol) == False and first == True:
                print('the symbol was not found in the environment')
                return None

    print(evaluatedValue)
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
        evaluated = env.getMember(symbol)    
        if evaluated != None:
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
    
    #Run the repl as no files was passed.
    if(len(sys.argv) == 1):
        print('Argument List:', str(sys.argv))
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Welcome to the Lispy REPL!')

        while(True):

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
                
    
    #else, parse the passed file.
    else:
        with open(sys.argv[1]) as f: #TODO: make this variable. (If one is to be able to pass more than one file that is.)
            for line in f:
                line = line.replace('\n','')
                if bool(line) and not line[0:2] == ';;':
                    try:
                        InputString = convertStringToQueue(line)
                        abstractSyntaxTree = AST(InputString)
                        evaluatedValue = eval(abstractSyntaxTree,glob)
                        print(evaluatedValue)
                    except:
                        print('Error in the parsing of file.' + line)
                    
                    
        f.close()
        

#############################
# Run main 
#############################     
  
RunLanguage()

