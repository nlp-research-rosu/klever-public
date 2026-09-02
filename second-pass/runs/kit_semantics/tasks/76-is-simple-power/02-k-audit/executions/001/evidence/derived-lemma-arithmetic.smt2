(set-logic NIA)

; K's supplied Python-remainder helper:
; pyMod(x,n) = ((x %Int n) + n) %Int n.
(define-fun pyMod ((x Int) (n Int)) Int
  (mod (+ (mod x n) n) n))

(echo "counterexample: exact-divisibility guard permits x=1")
(push)
(declare-const x Int)
(declare-const n Int)
(assert (or (<= n (- 2)) (>= n 2)))
(assert (= (pyMod x n) 0))
(assert (= x 1))
(check-sat)
(pop)

(echo "counterexample: nondivisibility guard permits x=0")
(push)
(declare-const x Int)
(declare-const n Int)
(assert (or (<= n (- 2)) (>= n 2)))
(assert (not (= (pyMod x n) 0)))
(assert (= x 0))
(check-sat)
(pop)
