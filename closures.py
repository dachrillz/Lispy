def functionGenerator(variables,body):
    boundedVariables = variables
    boundedBody = body

    def func1(*args):
        print(boundedVariables)
        print(boundedBody)
        
        return body(*boundedVariables)
        
        
    return func1    
test = lambda x,y: x+y


hej = functionGenerator(('x','y'),test)

print(hej)
print(hej(1))
print(hej(1))