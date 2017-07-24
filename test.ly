;;Example Program.
;; TODO: Decide if one really should have (a) to evaluate the bound variable a.
;; Maybe only a is necessary.

;; Basic arithmetic. Currently only integer operations are available.
(+ 3 2)
(* 3 2)
(- 3 3)
(/ 2 3) ;; This evaluates to a float currently which is not intended.

;; Values larger than a single digit.
(+ 10 10)

;;Nested arithmetic
(* 2 (+ (+ 3 2) (* 3 2))) ;;22
(+ (* 2 (+ (+ 3 2) (* 3 2))) (* 2 (+ (+ 3 2) (* 3 2)))) ;;44
(* 44 44)
(+ (* 2 (+ (+ 3 2) (* 3 2))) (* 2 (+ (+ 3 2) (+ 3 2))))
(+ (* 2 (+ (+ 3 2) (* 3 2))) (* 2 (+ (+ 3 2) (+ 3 2))))
(+ (+ (* 2 (+ (+ 3 2) (* 3 2))) (* 2 (+ (+ 3 2) (+ 3 2))))(+ (* 2 (+ (+ 3 2) (* 3 2))) (* 2 (+ (+ 3 2) (+ 3 2)))))

;; Basic list operations currently implemented.
(list 1 2 3) ;; This way one evaluates a list.
(def a (list 1 2 3)) ;; Bind the value of the list to the name a.
(head (a)) ;; This way one retrieves the head of a list.
(tail (a)) ;; This way one retrieves the tail of a list.

;;Variable declarations.
(def b 6) ;; Binds the variable b to the value 6 in the current environment.
(b) ;; Recall the value of a bound variable.
(let ((c 2)) (c)) ;; This way one can create a local Environment and bind the variable c in that environment.
(let ((c (+ 2 3))) (c)) ;; Values can be evaluated in the binding.
(let ((c 1)(d 1)) + (c) 2) ;; TODO: THIS STATEMENT IS CURRENTLY BUGGED. :(







