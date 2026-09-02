// spec.k — sum_to_n proof on the UNIFIED semantics (src/).
// sum(range(n+1)) is a <k>-cell fold (#sumAcc over the rangeObj); the loop invariant
// lives entirely in the <k> cell (sum is an expression, touches no other cell).

requires "verification.k"

module SUM-TO-N-SPEC
  imports SUM-TO-N-VERIFICATION

  // ---- Loop invariant (circularity, <k>-cell only) — the reference's #sumAcc fold over
  // rangeObj(I, HI, 1) from ACC reduces to sumRange(I, HI, ACC). Induction on the range:
  // #iterNext splits inRange(I,HI,1) = I<HI (yield I, recurse #sumAcc(rangeObj(I+1,HI,1),
  // ACC+I)) vs I>=HI (done, ACC).
  claim
    <k> #sumAcc(rangeObj(I:Int, HI:Int, 1), ACC:Int) => sumRange(I, HI, ACC) ... </k>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = sum_to_n(N) == sumRange(0, N+1, 0) = 0+1+...+N. range(N+1)
  // = rangeObj(0, N+1, 1), empty for N <= -1 (base gives 0). N symbolic Int.
  claim
    <k>
      FuncDef("sum_to_n", Params("n"),
        Return(
          Call(Name("sum"),
            Call(Name("range"), BinOp("+", Name("n"), Int(1))))))
      Assign(Name("result"), Call(Name("sum_to_n"), Int(N:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sum_to_n" <- ?_:Val ] [ "result" <- sumRange(0, N +Int 1, 0) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
