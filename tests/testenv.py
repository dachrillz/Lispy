import sys
sys.path.append(sys.path[0][:-6]) #this is incredibly hacky and breaks if the folder name changes, or if the current folder does not happen to be att index 0.
from Language import *
from testFunctions import *

print('\n \t Resets Env and gets Core Library \n')
resetEnv()
importCore()

print('\n \t testing ENV \n')

'''                 
;; Testing REPL_ENV
(+ 1 2)
;=>3
(/ (- (+ 5 (* 2 3)) 3) 4)
;=>2
'''
expr = ['(+ 1 2)', '(/ (- (+ 5 (* 2 3)) 3) 4)']
ans = [3,2]

testFunction(expr,ans)

print('\n \t testing def! \n')

'''
;; Testing def!
(def! x 3)
;=>3
x
;=>3
(def! x 4)
;=>4
x
;=>4
(def! y (+ 1 7))
;=>8
y
;=>8
'''
expr = ['(def x 3)', '(def y (+ 1 7))', 'y']
ans = [3,8,8]

testFunction(expr,ans)

print('\n \t testing Case sensitiveness \n')

'''
;; Verifying symbols are case-sensitive
(def! mynum 111)
;=>111
(def! MYNUM 222)
;=>222
mynum
;=>111
MYNUM
;=>222
'''

expr = ['(def mynum 111)', '(def MYNUM 222)', 'mynum', 'MYNUM']
ans = [111,222,111,222]

testFunction(expr,ans)

'''
;; Check env lookup non-fatal error
(abc 1 2 3)
; .*\'abc\' not found.*
;; Check that error aborts def!
(def! w 123)
(def! w (abc))
w
;=>123
'''

print('\n \t testing some Errors \n')

expr = ['(abc 1 2 3)', '(def w 123)', '(def w (abc))', 'w']
ans = [None,123,None,123]

testFunction(expr,ans)

'''
;; Testing let*
(let* (z 9) z)
;=>9
(let* (x 9) x)
;=>9
x
;=>4
(let* (z (+ 2 3)) (+ 1 z))
;=>6
(let* (p (+ 2 3) q (+ 2 p)) (+ p q))
;=>12
(def! y (let* (z 7) z))
y
;=>7
'''
print('\n \t testing lets \n')


expr = ['(let ((z 9)) z)',
        '(let ((x 9)) x)',
        'x',
        '(let ((z (+ 2 3))) (+ 1 z))',
        '(let ((p (+ 2 3)) (q (+ 2 p))) (+ p q))',
        '(def t (let ((z 7)) z))',
        't']
        
ans = [9,9,3,6,12,7,7]

testFunction(expr,ans)

'''
;; Testing outer environment
(def! a 4)
;=>4
(let* (q 9) q)
;=>9
(let* (q 9) a)
;=>4
(let* (z 2) (let* (q 9) a))
;=>4
(let* (x 4) (def! a 5))
;=>5
a
;=>4
'''

print('\n \t testing outer environment \n')

expr = ['(def a 4)','(let ((q 9)) q)','(let ((q 9)) a)','(let ((z 2)) (let ((q 9)) a))','(let ((x 4)) (def u 5))','u']
ans = [4,9,4,4,5,4]

testFunction(expr,ans)

'''
;>>> deferrable=True
;>>> optional=True
;;
;; -------- Deferrable/Optional Functionality --------

;; Testing let* with vector bindings
(let* [z 9] z)
;=>9
(let* [p (+ 2 3) q (+ 2 p)] (+ p q))
;=>12

;; Testing vector evaluation
(let* (a 5 b 6) [3 4 a [b 7] 8])
;=>[3 4 5 [6 7] 8]
'''