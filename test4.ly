;; function tests.

(def name (fun (a b) (+ 1 a b) a b))

(def hej (fun (a b) (+ b a) a b))

(print (name 1 2))