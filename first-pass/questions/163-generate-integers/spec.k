// spec.k — generate_integers proof on the UNIFIED semantics (src/).
// [i for i in range(lower, upper+1) if i%2==0] desugars to a closure with an inner For
// over the rangeObj folding $acc = $acc + [i]; the loop body reads only i (single-frame).
// lower = max(2, min(a,b)), upper = min(8, max(a,b)).

requires "verification.k"

module GENERATE-INTEGERS-SPEC
  imports GENERATE-INTEGERS-VERIFICATION

  // ---- Comprehension loop invariant (circularity) — over rangeObj(I, HI, 1) from
  // $acc = list(R) the loop appends each even i, leaving $acc := list(valSeqConcat(R,
  // evensV(I, HI))). Induction on the range; the filter If splits on pyMod(I,2)==0.
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        If(BoolOp("and", Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0)))),
           Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Name("i")))),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "$acc" <- ref(HN1_0:Int) ] [ "i" <- _:Val ], P:Parent) =>
        scope(.Map [ "$acc" <- ref(?HN1_0B:Int) ] [ "i" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(?RO:ValSeq)) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    ensures ?RO ==K valSeqConcat(R, evensV(I, HI))
    [all-path]

  // ---- Entry claim — result = generate_integers(A, B) == the even ints in
  // [max(2,min(A,B)), min(8,max(A,B))]. lower = maxInt(2, minInt(A,B)), upper+1 =
  // minInt(8, maxInt(A,B)) +Int 1. Two nested calls -> nextLoc 1 => 3.
  claim
    <k>
      FuncDef("generate_integers", Params("a", "b"),
        Assign(Name("lower"),
          Call(Name("max"), (Int(2), Call(Name("min"), (Name("a"), Name("b"))))))
        Assign(Name("upper"),
          Call(Name("min"), (Int(8), Call(Name("max"), (Name("a"), Name("b"))))))
        Return(
          ListComp(
            Name("i"),
            CompFor(
              Name("i"),
              Call(Name("range"), (Name("lower"), BinOp("+", Name("upper"), Int(1)))),
              Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0)))))))
      Assign(Name("result"), Call(Name("generate_integers"), (Int(A:Int), Int(B:Int))))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "generate_integers" <- ?_:Val ] [ "result" <- ref(?HN2_e:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_e |-> list(evensV(maxInt(2, minInt(A, B)), minInt(8, maxInt(A, B)) +Int 1))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
