// spec.k — is_simple_power proof on the UNIFIED semantics (src/).
//
//   kompile verification.k --backend haskell \
//     --main-module IS-SIMPLE-POWER-VERIFICATION --syntax-module IS-SIMPLE-POWER-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module IS-SIMPLE-POWER-SPEC

requires "verification.k"

module IS-SIMPLE-POWER-SPEC
  imports IS-SIMPLE-POWER-VERIFICATION
  imports K-EQUAL

  // ---- Loop invariant (the circularity) — see ../13-greatest-common-divisor + NOTES.md
  // GROWING while loop:  while power < x: power = power * n.
  // From (power=P, n=N, x=X) the loop terminates with  power := powUp(P, N, X)  (n, x
  // unchanged).  By induction on the GAP `x - power` shrinking: the condition `power < x`
  // splits P into  P >= X (stop; power already holds the final value)  /  P < X (run the
  // body so power := P*N, then loop again — the smaller-gap instance powUp(P*N, N, X),
  // which equals powUp(P, N, X) by the recurrence).  Restricted to N > 1, the loop's real
  // domain (n=1 is the early-return guard; n<=0 would not converge) so power strictly
  // grows toward x and the recurrence is well-founded.
  claim
    <k>
      #while(Compare(Name("power"), CmpOp("<", Name("x"))),
        Assign(Name("power"), BinOp("*", Name("power"), Name("n"))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "x" <- X:Int ] [ "n" <- N:Int ] [ "power" <- P:Int ], PAR:Parent)
               => scope(.Map [ "x" <- X ] [ "n" <- N ] [ "power" <- powUp(P, N, X) ], PAR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 1
    [all-path]

  // ---- Entry claim — see ../3-below-zero/PROOF.md ----------------------------
  // After `result = is_simple_power(X, N)`, the root scope's result is
  //   N == 1  ?  X == 1  :  powUp(1, N, X) == X
  // the program's early-return guard composed with the growing-loop summary.  kprove
  // case-splits on the program's `if n == 1` (N == 1 -> Return(x==1) -> X==1; else ->
  // power=1, the while loop closed by the loop-invariant circularity giving
  // power := powUp(1, N, X), then Return(power==x) -> powUp(1,N,X)==X).
  // Restricted to the function's real (HumanEval) domain X >= 1, N >= 1 (positive ints);
  // the loop only converges for n >= 2, and the n==1 / n<=0 edges are handled by the guard
  // / excluded by the domain.  See PROOF.md.
  claim
    <k>
      FuncDef("is_simple_power", Params("x", "n"),
        If(Compare(Name("n"), CmpOp("==", Int(1))),
           Return(Compare(Name("x"), CmpOp("==", Int(1)))),
           .Stmts)
        Assign(Name("power"), Int(1))
        While(Compare(Name("power"), CmpOp("<", Name("x"))),
          Assign(Name("power"), BinOp("*", Name("power"), Name("n"))))
        Return(Compare(Name("power"), CmpOp("==", Name("x")))))
      Assign(Name("result"), Call(Name("is_simple_power"), (X:Int, N:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_simple_power" <- ?_:Val ]
                       [ "result" <- #if N ==Int 1
                                      #then X ==Int 1
                                      #else powUp(1, N, X) ==Int X #fi ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires X >=Int 1 andBool N >=Int 1
    [all-path]
endmodule
