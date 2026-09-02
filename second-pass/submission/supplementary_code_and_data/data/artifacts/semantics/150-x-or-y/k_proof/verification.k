requires "reference-semantics/semantics.k"

module X-OR-Y-VERIFICATION
  imports MPY

  // The translated body of solution.py, named here so the claims remain
  // readable.  These are syntax macros, not additional execution semantics.
  syntax Stmts ::= "xOrYLoopBody" [macro]
  rule xOrYLoopBody
    => If(
         Compare(BinOp("%", Name("n"), Name("divisor")),
                 CmpOp("==", Int(0))),
         Return(Name("y")),
         .Stmts)

  syntax Stmts ::= "xOrYBody" [macro]
  rule xOrYBody
    => If(Compare(Name("n"), CmpOp("<", Int(2))),
          Return(Name("y")),
          .Stmts)
       For(Name("divisor"), Call(Name("range"), (Int(2), Name("n"))),
           xOrYLoopBody)
       Return(Name("x"))

  // A call of the actual translated function body in a clean module frame.
  syntax KItem ::= "#xOrY" "(" Int "," Val "," Val ")" [macro]
  rule #xOrY(N:Int, X:Val, Y:Val)
    => Call(closureVal(("n", "x", "y"), xOrYBody, 0), (N, X, Y))

  // Mathematical trial-division specification.  primeSelect(N,D,X,Y) is X
  // exactly when N >= 2 and none of D,D+1,...,N-1 divides N; otherwise it is Y.
  // In particular primeSelect(N,2,X,Y) is the contract of x_or_y.
  syntax Val ::= primeSelect(Int, Int, Val, Val) [function]

  rule primeSelect(N:Int, D:Int, X:Val, Y:Val) => Y
    requires D >=Int 2 andBool N <Int 2

  rule primeSelect(N:Int, D:Int, X:Val, Y:Val) => X
    requires D >=Int 2 andBool N >=Int 2 andBool D >=Int N

  rule primeSelect(N:Int, D:Int, X:Val, Y:Val) => Y
    requires D >=Int 2 andBool N >=Int 2 andBool D <Int N
      andBool pyMod(N, D) ==Int 0

  rule primeSelect(N:Int, D:Int, X:Val, Y:Val)
    => primeSelect(N, D +Int 1, X, Y)
    requires D >=Int 2 andBool N >=Int 2 andBool D <Int N
      andBool pyMod(N, D) =/=Int 0

  // The corresponding final value of the Python local `divisor`.  Tracking
  // this small piece of mutable frame state makes the loop invariant exact.
  syntax Int ::= scanLast(Int, Int, Int) [function]

  rule scanLast(N:Int, D:Int, OLD:Int) => OLD
    requires N >=Int 2 andBool D >=Int 2 andBool D >=Int N

  rule scanLast(N:Int, D:Int, OLD:Int) => D
    requires N >=Int 2 andBool D >=Int 2 andBool D <Int N
      andBool pyMod(N, D) ==Int 0

  rule scanLast(N:Int, D:Int, OLD:Int)
    => scanLast(N, D +Int 1, D)
    requires N >=Int 2 andBool D >=Int 2 andBool D <Int N
      andBool pyMod(N, D) =/=Int 0
endmodule

// Modular proof layer.  The rule below is byte-for-byte the reachability
// summary proved as loop_correct in X-OR-Y-LOOP-SPEC.  It is kept out of the
// base module used for that proof, then imported only for the top-level proof.
module X-OR-Y-SUMMARY
  imports X-OR-Y-VERIFICATION

  rule
    <k>
      #loop(rangeObj(D:Int, N:Int, 1), Name("divisor"), xOrYLoopBody)
      ~> (Return(Name("x")) .Stmts)
      ~> #endcall
      => #pop
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> BS:Scope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        "divisor" |-> (OLD:Int => scanLast(N, D, OLD))
        "n" |-> N:Int
        "x" |-> X:Val
        "y" |-> Y:Val,
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet => retV(primeSelect(N, D, X:Val, Y:Val)) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 2
      andBool D >=Int 2
    [priority(40)]
endmodule
