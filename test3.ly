;; Testing REPL_ENV
(+ 1 2)
;;=>3
(/ (- (+ 5 (* 2 3)) 3) 4)
;;=>2

(* 2 3)
(+ 5 (* 2 3))
(- (+ 5 (* 2 3)) 3)
(/ (- (+ 5 (* 2 3)) 3) 4)


;; Testing def!
(def x 3)
;;=>3
x
;;=>3
(def x 4)
;;=>4
x
;;=>4
(def y (+ 1 7))
;;=>8
y
;;=>8

;; Verifying symbols are case-sensitive
(def mynum 111)
;;=>111
(def MYNUM 222)
;;=>222
mynum
;;=>111
MYNUM
;;=>222

(print hej)

;; Check env lookup non-fatal error
(abc 1 2 3)
;; .*\'abc\' not found.*
;; Check that error aborts def!
(print hej)
(def w 123)
(def w (abc))
w
;;=>123

(print hej)

;; Testing let*
(let ((z 9)) (z))
;;=>9
(let ((x 9)) (x))
;;=>9
x
;;=>4
(print hej)
z
(let ((g (+ 2 3))) (+ 1 g)) ;;??
;;=>6
(let ((p (+ 2 3) q (+ 2 p))) (+ p q))
;;=>12
(def g (let ((z 7)) (z)))
g
;;=>7

;; Testing outer environment
(def a 4)
;;=>4
(let ((q 9)) q)
;;=>9
(let ((q 9)) a)
;;=>4
(let ((z 2) (let ((q 9)))) a) ;; this one is still bugged.
;;=>4
(let ((x 4)) (def a 5))
;;=>5
a
;;=>4