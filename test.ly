;;Example Program.
;; TO RUN THE PROGRAM, Type; in the same folder as the files: python lispy.py test.ly

;; TODO: Decide if one really should have (a) to evaluate the bound variable a.
;; Maybe only a is necessary.

;; Basic arithmetic. Currently only integer operations are available.
(print (+ 3 2))
(print (* 3 2))
(print (- 3 3))
(print (/ 2 3)) ;; This evaluates to a float currently which is not intended.

;; Values larger than a single digit.
(print (+ 10 10))

;;Nested arithmetic
(print (* 2 (+ (+ 3 2) (* 3 2)))) ;;22
(print (+ (* 2 (+ (+ 3 2) (* 3 2))) (* 2 (+ (+ 3 2) (* 3 2))))) ;;44
(print (* 44 44))
(print (+ (* 2 (+ (+ 3 2) (* 3 2))) (* 2 (+ (+ 3 2) (+ 3 2)))))
(print (+ (* 2 (+ (+ 3 2) (* 3 2))) (* 2 (+ (+ 3 2) (+ 3 2)))))
(print (+ (+ (* 2 (+ (+ 3 2) (* 3 2))) (* 2 (+ (+ 3 2) (+ 3 2))))(+ (* 2 (+ (+ 3 2) (* 3 2))) (* 2 (+ (+ 3 2) (+ 3 2))))))

;; Basic list operations currently implemented.
(print (list 1 2 3)) ;; This way one evaluates a list.
(print (def a (list 1 2 3))) ;; Bind the value of the list to the name a.
(print (head (a))) ;; This way one retrieves the head of a list.
(print (tail (a))) ;; This way one retrieves the tail of a list.

(print hej)

;;Variable declarations.
(print (def b 6)) ;; Binds the variable b to the value 6 in the current environment.
(print b) ;; Recall the value of a bound variable.
(print (let ((c 2)) (c))) ;; This way one can create a local Environment and bind the variable c in that environment.
(print (let ((c (+ 2 3))) (c))) ;; Values can be evaluated in the binding.
(print (let ((c 1)(d 1)) (+ c 2))) ;; TODO: THIS STATEMENT IS CURRENTLY BUGGED. :(







