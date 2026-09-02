// spec.k — minSubArraySum (Kadane, minimum) proof on the UNIFIED semantics (src/).
// Whole-list scan seeded from nums[0], skipping the seed via a `first` flag (avoids the
// non-narrowing nums[1:] slice). Coupled cur/best accumulators.

requires "verification.k"

module MIN-SUBARRAY-SPEC
  imports MIN-SUBARRAY-VERIFICATION

  // ---- Loop invariant (circularity) — over any ValSeq VS from (cur=CUR, best=BEST,
  // first=FIRST) the loop leaves cur := curK(VS,CUR,BEST,FIRST), best := bestK(VS,...).
  // Induction on VS; the `if first` splits FIRST, the two inner If's line up with the four
  // branch rules of each summary.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(Name("first"),
          Assign(Name("first"), Bool(false)),
          If(Compare(Name("x"), CmpOp("<", BinOp("+", Name("cur"), Name("x")))),
            Assign(Name("cur"), Name("x")),
            Assign(Name("cur"), BinOp("+", Name("cur"), Name("x"))))
          If(Compare(Name("cur"), CmpOp("<", Name("best"))),
            Assign(Name("best"), Name("cur")),
            .Stmts)))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "nums" <- NV:Val ] [ "cur" <- CUR:Val ] [ "best" <- BEST:Val ] [ "first" <- FIRST:Bool ] [ "x" <- _:Val ], P:Parent) =>
        scope(.Map [ "nums" <- NV ] [ "cur" <- curK(VS, CUR, BEST, FIRST) ] [ "best" <- bestK(VS, CUR, BEST, FIRST) ] [ "first" <- ?_:Bool ] [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool isInt(CUR) andBool isInt(BEST)
    [all-path]

  // ---- Entry claim — for a non-empty list (head H:Int, tail T), after
  // `result = minSubArraySum(...)` the root scope's result is bestK(vCons(H,T), H, H, true)
  // = the minimum non-empty contiguous sub-array sum.
  claim
    <k>
      FuncDef("minSubArraySum", Params("nums"),
        Assign(Name("cur"), Subscript(Name("nums"), Int(0)))
        Assign(Name("best"), Subscript(Name("nums"), Int(0)))
        Assign(Name("first"), Bool(true))
        Assign(Name("x"), Int(0))
        For(Name("x"), Name("nums"),
          If(Name("first"),
            Assign(Name("first"), Bool(false)),
            If(Compare(Name("x"), CmpOp("<", BinOp("+", Name("cur"), Name("x")))),
              Assign(Name("cur"), Name("x")),
              Assign(Name("cur"), BinOp("+", Name("cur"), Name("x"))))
            If(Compare(Name("cur"), CmpOp("<", Name("best"))),
              Assign(Name("best"), Name("cur")),
              .Stmts)))
        Return(Name("best")))
      Assign(Name("result"), Call(Name("minSubArraySum"), list(vCons(HV:Val, T:ValSeq))))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "minSubArraySum" <- ?_:Val ] [ "result" <- bestK(vCons(HV, T), HV, HV, true) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isInt(HV) andBool allInt(T)
    [all-path]
endmodule
