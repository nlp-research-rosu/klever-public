// spec.k — make_a_pile proof on the UNIFIED semantics (src/).
// [n + 2*i for i in range(n)] desugars to a closure with an inner For over range(n)
// folding $acc = $acc + [n + 2*i]; the free `n` resolves through the parent frame.

requires "verification.k"

module MAKE-A-PILE-SPEC
  imports MAKE-A-PILE-VERIFICATION

  // ---- Loop invariant (circularity) — over rangeObj(I, N, 1) the comprehension loop
  // right-conses n + 2*i per index, leaving $acc := list(valSeqConcat(R, pileV(I, N, NV))).
  // NV = the parent frame's `n`. Induction on the range via inRange.
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        If(BoolOp("and", Bool(true)),
           Assign(Name("$acc"),
             BinOp("+", Name("$acc"),
               ListExpr(BinOp("+", Name("n"), BinOp("*", Int(2), Name("i")))))),
           .Stmts))
    => .K ... </k>
    <env> LC:Int </env>
    <scopes>
      ... LC |-> (
        scope(.Map [ "$acc" <- ref(HN1_0:Int) ] [ "i" <- _:Val ], parent(LP:Int)) =>
        scope(.Map [ "$acc" <- ref(?HN1_0B:Int) ] [ "i" <- ?_:Val ], parent(LP))
      )
      LP |-> scope(.Map [ "n" <- NV:Int ], _PP:Parent)
      ...
    </scopes>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(?RO:ValSeq)) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires LC =/=Int LP
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    ensures ?RO ==K valSeqConcat(R, pileV(I, N -Int I, NV))
    [all-path]

  // ---- Entry claim — result = make_a_pile(N) == list(pileV(0, N, N)). Two nested calls
  // (make_a_pile scope 1, comprehension closure scope 2), so nextLoc runs 1 => 3.
  claim
    <k>
      FuncDef("make_a_pile", Params("n"),
        Return(
          ListComp(BinOp("+", Name("n"), BinOp("*", Int(2), Name("i"))),
            CompFor(Name("i"), Call(Name("range"), Name("n")), Bool(true)))))
      Assign(Name("result"), Call(Name("make_a_pile"), Int(N:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "make_a_pile" <- ?_:Val ] [ "result" <- ref(?HN2_e:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_e |-> list(pileV(0, N, N))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
