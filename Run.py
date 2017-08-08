def RunLanguage():
    # create the global environment.
    glob = EnvFact()

    # Run the repl as no files was passed.
    if (len(sys.argv) == 1):
        print('Argument List:', str(sys.argv))
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Welcome to the Lispy REPL!')

        while (True):

            InputString = input("Input> ")

            if InputString == 'bajs':
                for item in glob.variables:
                    print(item)

            else:
                print("To be passed to AST " + InputString)

                InputString = convertStringToQueue(InputString)  # convert to a deque

                abstractSyntaxTree = AST(InputString)

                print('abstractSyntaxTree')
                print(abstractSyntaxTree)

                evaluatedValue = eval(abstractSyntaxTree, glob)

                print('evaluated value')
                print(evaluatedValue)


    # else, parse the passed file.
    else:
        with open(sys.argv[
                      1]) as f:  # TODO: make this variable. (If one is to be able to pass more than one file that is.)
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

        f.close()


#############################
# Run main 
#############################     

RunLanguage()

