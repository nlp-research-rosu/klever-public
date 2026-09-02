// spec.k — sum_squares on the UNIFIED semantics. List-fold over the elements, ceil(i)^2 into an
// int accumulator. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module SUM-SQUARES-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module SUM-SQUARES-SPEC

requires "verification.k"

module SUM-SQUARES-SPEC
  imports SUM-SQUARES-VERIFICATION

  // ---- Loop invariant — for i in lst: squared += ceil(i)**2 leaves squared := sqFold(VS, SQ). ---
  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        AugAssign(Name("squared"), "+", BinOp("**", Call(Attribute(Name("math"), "ceil"), Name("i")), Int(2))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "lst" <- LV:Val ] [ "squared" <- SQ:Int ] [ "i" <- _:Val ], PR:Parent)
               => scope(.Map [ "lst" <- LV ] [ "squared" <- sqFold(VS, SQ) ] [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNum(VS)
    [all-path]

  // ---- Entry claim — result == sqRes(VS) = sqFold(VS, 0). --------------------
  claim
    <k>
      FuncDef("sum_squares", Params("lst"),
        Import("math")
        Assign(Name("squared"), Int(0))
        Assign(Name("i"), Int(0))
        For(Name("i"), Name("lst"),
          AugAssign(Name("squared"), "+", BinOp("**", Call(Attribute(Name("math"), "ceil"), Name("i")), Int(2))))
        Return(Name("squared")))
      Assign(Name("result"), Call(Name("sum_squares"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sum_squares" <- ?_:Val ] [ "result" <- sqRes(VS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNum(VS)
    [all-path]
endmodule
