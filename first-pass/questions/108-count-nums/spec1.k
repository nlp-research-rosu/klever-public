// spec1.k - stage 1: leaf claims (digit-comp x2, sum, filter-comp x2)
requires "verification.k"

module COUNT-NUMS-SPEC1
  imports COUNT-NUMS-VERIFICATION

  claim
    <k>
      #loop(str(CS:IntSeq), Name("i"),
        If(BoolOp("and", Bool(true)),
          Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Call(Name("int"), Name("i"))))),
          .Stmts))
    => .K ... </k>
    <env> 4 </env>
    <scopes>
      ... -1 |-> builtinsScope
          0 |-> scope(.Map [ "count_nums" <- _:Val ], parent(-1))
          3 |-> scope(.Map [ "n" <- _:Val ] [ "$cells" <- cellsMark(.ParamNames) ]
                          [ "neg" <- _:Val ], parent(0))
          4 |-> (
            scope(.Map [ "$acc" <- ref(AN:Int) ] [ "i" <- _:Val ], parent(3)) =>
            scope(.Map [ "$acc" <- ref(?AN2:Int) ] [ "i" <- ?_:Val ], parent(3))
          ) ...
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?HG:Map HREST </heap>
    <heapLoc> HLM:Int => ?HL2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K intFold(CS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HL2 andBool HLM <=Int ?HL2
     andBool keysBelow(?HG, ?HL2)
     andBool notBool (?AN2 in_keys(?HG)) andBool notBool (?AN2 in_keys(HREST))
    [all-path]

  // ---- digit-comp invariant, variant A (i unbound at comp start) -----------

  claim
    <k>
      #loop(str(CS:IntSeq), Name("i"),
        If(BoolOp("and", Bool(true)),
          Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Call(Name("int"), Name("i"))))),
          .Stmts))
    => .K ... </k>
    <env> 4 </env>
    <scopes>
      ... -1 |-> builtinsScope
          0 |-> scope(.Map [ "count_nums" <- _:Val ], parent(-1))
          3 |-> scope(.Map [ "n" <- _:Val ] [ "$cells" <- cellsMark(.ParamNames) ]
                          [ "neg" <- _:Val ], parent(0))
          4 |-> (
            scope(.Map [ "$acc" <- ref(AN:Int) ], parent(3)) =>
            scope((.Map [ "$acc" <- ref(?AN2:Int) ]) ?XM:Map, parent(3))
          ) ...
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?HG:Map HREST </heap>
    <heapLoc> HLM:Int => ?HL2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K intFold(CS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HL2 andBool HLM <=Int ?HL2
     andBool keysBelow(?HG, ?HL2)
     andBool notBool (?AN2 in_keys(?HG)) andBool notBool (?AN2 in_keys(HREST))
    [all-path]

  // ---- the real sum fold over an all-int list (the P67 claim) --------------

  claim <k> #sumAcc(list(VS2:ValSeq), ACC2:Int) => ?R:Int ... </k>
        requires allInt(VS2)
        ensures  ?R ==Int sumI(VS2, ACC2)
        [all-path]

  // ---- digits_sum callee span (frame 3; caller is comp1's frame 2) ---------

  claim
    <k>
      #loop(list(VS:ValSeq), Name("v"),
        If(BoolOp("and", Compare(Name("v"), CmpOp(">", Int(0)))),
          Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Name("v")))),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ] [ "v" <- _:Val ], P:Parent) =>
        scope(.Map [ "$acc" <- ref(?AN2:Int) ] [ "v" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?HG:Map </heap>
    <heapLoc> HLM:Int => ?HL2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
     andBool 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K posFilt(VS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HL2 andBool keysBelow(?HG, ?HL2)
    [all-path]

  // ---- positive-filter comp invariant, variant A (v unbound) ---------------

  claim
    <k>
      #loop(list(VS:ValSeq), Name("v"),
        If(BoolOp("and", Compare(Name("v"), CmpOp(">", Int(0)))),
          Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Name("v")))),
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
    requires allInt(VS)
     andBool 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K posFilt(VS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HL2 andBool keysBelow(?HG, ?HL2)
    [all-path]

  // ---- entry ----------------------------------------------------------------

endmodule
