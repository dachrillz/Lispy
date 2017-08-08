#Imports

import sys
sys.path.append(sys.path[0][:-6]) #this is incredibly hacky and breaks if the folder name changes, or if the current folder does not happen to be att index 0.
from Language import AST

print(AST)

'''
;; Testing read of numbers
1
;=>1
7
;=>7
  7   
;=>7
-123
;=>-123


;; Testing read of symbols
+
;=>+
abc
;=>abc
   abc   
;=>abc
abc5
;=>abc5
abc-def
;=>abc-def


;; Testing read of lists
(+ 1 2)
;=>(+ 1 2)
()
;=>()
(nil)
;=>(nil)
((3 4))
;=>((3 4))
(+ 1 (+ 2 3))
;=>(+ 1 (+ 2 3))
  ( +   1   (+   2 3   )   )  
;=>(+ 1 (+ 2 3))
(* 1 2)
;=>(* 1 2)
(** 1 2)
;=>(** 1 2)
(* -3 6)
;=>(* -3 6)

;; Test commas as whitespace
(1 2, 3,,,,),,
;=>(1 2 3)


;>>> deferrable=True

;;
;; -------- Deferrable Functionality --------

;; Testing read of nil/true/false
nil
;=>nil
true
;=>true
false
;=>false

;; Testing read of strings
"abc"
;=>"abc"
   "abc"   
;=>"abc"
"abc (with parens)"
;=>"abc (with parens)"
"abc\"def"
;=>"abc\"def"
;;;"abc\ndef"
;;;;=>"abc\ndef"
""
;=>""

;; Testing reader errors
;;; TODO: fix these so they fail correctly
(1 2
; expected ')', got EOF
[1 2
; expected ']', got EOF
"abc
; expected '"', got EOF
(1 "abc
; expected ')', got EOF

;; Testing read of quoting
'1
;=>(quote 1)
'(1 2 3)
;=>(quote (1 2 3))
`1
;=>(quasiquote 1)
`(1 2 3)
;=>(quasiquote (1 2 3))
~1
;=>(unquote 1)
~(1 2 3)
;=>(unquote (1 2 3))
`(1 ~a 3)
;=>(quasiquote (1 (unquote a) 3))
~@(1 2 3)
;=>(splice-unquote (1 2 3))


;>>> optional=True
;;
;; -------- Optional Functionality --------

;; Testing keywords
:kw
;=>:kw
(:kw1 :kw2 :kw3)
;=>(:kw1 :kw2 :kw3)

;; Testing read of vectors
[+ 1 2]
;=>[+ 1 2]
[]
;=>[]
[[3 4]]
;=>[[3 4]]
[+ 1 [+ 2 3]]
;=>[+ 1 [+ 2 3]]
  [ +   1   [+   2 3   ]   ]  
;=>[+ 1 [+ 2 3]]

;; Testing read of hash maps
{"abc" 1}
;=>{"abc" 1}
{"a" {"b" 2}}
;=>{"a" {"b" 2}}
{"a" {"b" {"c" 3}}}
;=>{"a" {"b" {"c" 3}}}
{  "a"  {"b"   {  "cde"     3   }  }}
;=>{"a" {"b" {"cde" 3}}}
{  :a  {:b   {  :cde     3   }  }}
;=>{:a {:b {:cde 3}}}

;; Testing read of comments
 ;; whole line comment (not an exception)
1 ; comment after expression
;=>1
1; comment after expression
;=>1

;; Testing read of ^/metadata
^{"a" 1} [1 2 3]
;=>(with-meta [1 2 3] {"a" 1})


;; Testing read of @/deref
@a
;=>(deref a)
'''