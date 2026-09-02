requires "verification.k"

module STRONGEST-EXTENSION-SPEC1
  imports STRONGEST-EXTENSION-VERIFICATION
  imports STRONGEST-EXTENSION-VERIFICATION

  // ---- Inner upper-filter comp invariant, variant B (x bound; circularity).
  claim
    <k>
      #loop(str(CS:IntSeq), Name("x"),
        If(BoolOp("and", BoolOp(
          "and",
          Call(Attribute(Name("x"), "isalpha"), .Exprs),
          Call(Attribute(Name("x"), "isupper"), .Exprs))),
          Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Name("x")))),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ] [ "x" <- _:Val ], P:Parent) =>
        scope((.Map [ "$acc" <- ref(?AN2:Int) ]) [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?HG:Map </heap>
    <heapLoc> HLM:Int => ?HL2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K upSeq(CS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HL2 andBool keysBelow(?HG, ?HL2)
    [all-path]

  // ---- Variant A (x unbound at comp start; existential post rest covers
  // both the zero- and nonzero-iteration endings; frame dies at #pop).
  claim
    <k>
      #loop(str(CS:IntSeq), Name("x"),
        If(BoolOp("and", BoolOp(
          "and",
          Call(Attribute(Name("x"), "isalpha"), .Exprs),
          Call(Attribute(Name("x"), "isupper"), .Exprs))),
          Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Name("x")))),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ], P:Parent) =>
        scope((.Map [ "$acc" <- ref(?AN2:Int) ]) ?XM:Map, P)
      ) ...
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?HG:Map </heap>
    <heapLoc> HLM:Int => ?HL2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K upSeq(CS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HL2 andBool keysBelow(?HG, ?HL2)
    [all-path]

  // ---- Inner lower-filter comp invariant, variant B.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("x"),
        If(BoolOp("and", BoolOp(
          "and",
          Call(Attribute(Name("x"), "isalpha"), .Exprs),
          Call(Attribute(Name("x"), "islower"), .Exprs))),
          Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Name("x")))),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ] [ "x" <- _:Val ], P:Parent) =>
        scope((.Map [ "$acc" <- ref(?AN2:Int) ]) [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?HG:Map </heap>
    <heapLoc> HLM:Int => ?HL2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K loSeq(CS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HL2 andBool keysBelow(?HG, ?HL2)
    [all-path]

  // ---- Inner lower-filter comp, variant A.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("x"),
        If(BoolOp("and", BoolOp(
          "and",
          Call(Attribute(Name("x"), "isalpha"), .Exprs),
          Call(Attribute(Name("x"), "islower"), .Exprs))),
          Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Name("x")))),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ], P:Parent) =>
        scope((.Map [ "$acc" <- ref(?AN2:Int) ]) ?XM:Map, P)
      ) ...
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?HG:Map </heap>
    <heapLoc> HLM:Int => ?HL2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K loSeq(CS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HL2 andBool keysBelow(?HG, ?HL2)
    [all-path]

  // ---- Outer argmax invariant, variant B (s/val bound).
endmodule
