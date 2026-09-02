requires "verification.k"

module RESCALE-TO-UNIT-SPEC
  imports RESCALE-TO-UNIT-VERIFICATION

  // ---- The REAL shared min/max folds, proven (not intercepted). The seed
  // rules take the first yield; the Float-headed folds step via minFloat/
  // maxFloat exactly as float.k executes them.
  claim <k> #minAccF(list(VS:ValSeq), M:Float) => ?R:Float ... </k>
        requires allFloatN(VS)
        ensures  ?R ==K minF2(VS, M)
        [all-path]
  claim <k> #minAcc0(list(VS:ValSeq)) => ?R:Float ... </k>
        requires allFloatN(VS) andBool 0 <Int vsLen(VS)
        ensures  ?R ==K minSeed(VS)
        [all-path]
  claim <k> #maxAccF(list(VS:ValSeq), M:Float) => ?R:Float ... </k>
        requires allFloatN(VS)
        ensures  ?R ==K maxF2(VS, M)
        [all-path]
  claim <k> #maxAcc0(list(VS:ValSeq)) => ?R:Float ... </k>
        requires allFloatN(VS) andBool 0 <Int vsLen(VS)
        ensures  ?R ==K maxSeed(VS)
        [all-path]

  // ---- Listcomp-loop invariant (circularity), variant B: x bound. Frame 1
  // pins the two free-var floats; $acc is a plus-builder (moving ref).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(BoolOp("and", Bool(true)),
           Assign(Name("$acc"),
             BinOp("+", Name("$acc"),
               ListExpr(BinOp(
                 "/",
                 BinOp("-", Name("x"), Name("min_number")),
                 BinOp("-", Name("max_number"), Name("min_number")))))),
           .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "rescale_to_unit" <- _:Val ], parent(-1))
       1 |-> scope(.Map [ "numbers" <- _:Val ]
                        [ "min_number" <- MN:Float ]
                        [ "max_number" <- MX:Float ], parent(0))
       2 |-> (
         scope(.Map [ "$acc" <- ref(AN:Int) ] [ "x" <- _:Val ], parent(1)) =>
         scope(.Map [ "$acc" <- ref(?AN2:Int) ] [ "x" <- ?_:Val ], parent(1))
       )
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?_:Map </heap>
    <heapLoc> HLM:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloatN(VS)
     andBool 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K rescSeq(VS, MN, MX, R)
    [all-path]

  // ---- Variant A: pre-first-iteration (x unbound; nonempty from the entry).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(BoolOp("and", Bool(true)),
           Assign(Name("$acc"),
             BinOp("+", Name("$acc"),
               ListExpr(BinOp(
                 "/",
                 BinOp("-", Name("x"), Name("min_number")),
                 BinOp("-", Name("max_number"), Name("min_number")))))),
           .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "rescale_to_unit" <- _:Val ], parent(-1))
       1 |-> scope(.Map [ "numbers" <- _:Val ]
                        [ "min_number" <- MN:Float ]
                        [ "max_number" <- MX:Float ], parent(0))
       2 |-> (
         scope(.Map [ "$acc" <- ref(AN:Int) ], parent(1)) =>
         scope(.Map [ "$acc" <- ref(?AN2:Int) ] [ "x" <- ?_:Val ], parent(1))
       )
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?_:Map </heap>
    <heapLoc> HLM:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloatN(VS) andBool 0 <Int vsLen(VS)
     andBool 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K rescSeq(VS, MN, MX, R)
    [all-path]

  // ---- Entry claim -- the REAL canonical code, verbatim .mpy. The result
  // list escapes by ref.
  claim
    <k>
      FuncDef("rescale_to_unit", Params("numbers"),
        Assign(Name("min_number"), Call(Name("min"), Name("numbers")))
        Assign(Name("max_number"), Call(Name("max"), Name("numbers")))
        Return(
          ListComp(BinOp(
            "/",
            BinOp("-", Name("x"), Name("min_number")),
            BinOp("-", Name("max_number"), Name("min_number"))),
            CompFor(Name("x"), Name("numbers"), Bool(true)))))
      Assign(Name("result"), Call(Name("rescale_to_unit"), list(NS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "rescale_to_unit" <- ?_:Val ]
                       [ "result" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(rescSeq(NS, minSeed(NS), maxSeed(NS), .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloatN(NS) andBool 0 <Int vsLen(NS)
    [all-path]
endmodule
