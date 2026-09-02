module MPY-VERIFICATION
  imports MPY

  // The postcondition is stated separately from expression evaluation.
  // Empty input is fixed; nonempty input selects ascending or descending
  // according to the parity of its first and last elements.
  syntax IntList ::= expectedSort(IntList) [function, total]

  rule expectedSort(nil) => nil
  rule expectedSort(cons(I, IS))
    => sortFlag(cons(I, IS), endpointEven(cons(I, IS)))

  syntax Bool ::= endpointEven(IntList) [function]
  rule endpointEven(cons(I, IS))
    => ((I +Int ilast(cons(I, IS))) %Int 2) ==Int 0

  // Executable domain and ordering observers.  nonnegative is used as the
  // symbolic claim's HumanEval-domain precondition; the order observers make
  // the mathematical post-state directly inspectable with krun/kast.
  syntax Bool ::= nonnegative(IntList) [function, total]
                | ascending(IntList) [function, total]
                | descending(IntList) [function, total]
  rule nonnegative(nil) => true
  rule nonnegative(cons(I, IS)) => (I >=Int 0) andBool nonnegative(IS)

  rule ascending(nil) => true
  rule ascending(cons(_, nil)) => true
  rule ascending(cons(I, cons(J, JS)))
    => (I <=Int J) andBool ascending(cons(J, JS))

  rule descending(nil) => true
  rule descending(cons(_, nil)) => true
  rule descending(cons(I, cons(J, JS)))
    => (I >=Int J) andBool descending(cons(J, JS))
endmodule
