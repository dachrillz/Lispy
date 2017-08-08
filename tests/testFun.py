import sys
sys.path.append(sys.path[0][:-6]) #this is incredibly hacky and breaks if the folder name changes, or if the current folder does not happen to be att index 0.
from Language import *
from testFunctions import *

print('\n \t Resets Env and gets Core Library \n')
resetEnv()
importCore()


print('\n \t testing List functions \n')

print('todo')

print('\n \t testing if \n')

expr = ['(if true 7 8)']
ans = [7]

testFunction(expr,ans)

'''
;; Testing if form
(if true 7 8)
;=>7
(if false 7 8)
;=>8
(if true (+ 1 7) (+ 1 8))
;=>8
(if false (+ 1 7) (+ 1 8))
;=>9
(if nil 7 8)
;=>8
(if 0 7 8)
;=>7
(if "" 7 8)
;=>7
(if (list) 7 8)
;=>7
(if (list 1 2 3) 7 8)
;=>7
(= (list) nil)
;=>false
'''