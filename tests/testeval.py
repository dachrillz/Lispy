import sys
sys.path.append(sys.path[0][:-6]) #this is incredibly hacky and breaks if the folder name changes, or if the current folder does not happen to be att index 0.
from Language import *
from testFunctions import *

expressionList = ['(+ 1 2)',
                  '(+ 5 (* 2 3))',
                  '(- (+ 5 (* 2 3)) 3)',
                  '(/ (- (+ 5 (* 2 3)) 3) 4)',
                  '(/ (- (+ 515 (* 87 311)) 302) 27)',
                  '(* -3 6)',
                  '(/ (- (+ 515 (* -87 311)) 296) 27)',
                  '(abc 1 2 3)',
                  '()']
                  
expectedValueList = [3,11,8,2,1010,-18,-994,None,0]


print('\n \t testing evaluation \n')

for i in range (len(expressionList)):
    print(expressionList[i], '=>' ,expectedValueList[i])
    try:
        assert testExpression(expressionList[i]) == expectedValueList[i]
    except:
        print('ERROR')


'''
(+ 5 (* 2 3))
;=>11

(- (+ 5 (* 2 3)) 3)
;=>8

(/ (- (+ 5 (* 2 3)) 3) 4)
;=>2

(/ (- (+ 515 (* 87 311)) 302) 27)
;=>1010

(* -3 6)
;=>-18

(/ (- (+ 515 (* -87 311)) 296) 27)
;=>-994

(abc 1 2 3)
; .*\'abc\' not found.*

;; Testing empty list
()
;=>()

;>>> deferrable=True
;>>> optional=True
;;
;; -------- Deferrable/Optional Functionality --------

;; Testing evaluation within collection literals
[1 2 (+ 1 2)]
;=>[1 2 3]

{"a" (+ 7 8)}
;=>{"a" 15}

{:a (+ 7 8)}
;=>{:a 15}
'''