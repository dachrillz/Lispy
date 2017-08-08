def AST(stringDeque):
    """ Return the abstract Syntax tree. (String -> AST)"""

    parentMem = False
    symbolParsed = False
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

        elif s in numbers:
            space = False
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