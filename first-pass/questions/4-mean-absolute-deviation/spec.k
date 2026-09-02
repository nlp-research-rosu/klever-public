requires "verification.k"

module MEAN-ABSOLUTE-DEVIATION-SPEC
  imports MEAN-ABSOLUTE-DEVIATION-VERIFICATION

  // ---- The REAL shared sum folds, proven (not intercepted). The Int-headed
  // #sumAcc switches to the Float-headed #sumAccF on the first yield.
  claim <k> #sumAccF(list(VS:ValSeq), ACC:Float) => ?R:Float ... </k>
        requires allFloatN(VS)
        ensures  ?R ==K sumF2(VS, ACC)
        [all-path]

  claim <k> #sumAcc(list(VS:ValSeq), 0) => ?R:Float ... </k>
        requires allFloatN(VS) andBool 0 <Int vsLen(VS)
        ensures  ?R ==K sumF2(VS, 0.0)
        [all-path]

  // ---- Genexp-loop invariant (circularity), frame variant B: x already bound.
  // Two-frame shape: frame 2 is the comprehension closure (plain closureVal,
  // parent(1)); frame 1 is the annotated function frame whose cellvar mean
  // lives in the HEAP CELL at loc 0 (first allocation of the run). $acc is a
  // plus-builder (moving ref); the loop body reads mean through cellRef(0) and
  // abs through the builtins frame, so every frame on the walk is pinned.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(BoolOp("and", Bool(true)),
           Assign(Name("$acc"),
             BinOp("+", Name("$acc"),
               ListExpr(Call(Name("abs"), BinOp("-", Name("x"), Name("mean")))))),
           .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "mean_absolute_deviation" <- _:Val ], parent(-1))
       1 |-> scope(.Map [ "$cells" <- cellsMark("mean") ]
                        [ "mean" <- cellRef(MH:Int) ]
                        [ "numbers" <- _:Val ], parent(0))
       2 |-> (
         scope(.Map [ "$acc" <- ref(AN:Int) ] [ "x" <- _:Val ], parent(1)) =>
         scope(.Map [ "$acc" <- ref(?AN2:Int) ] [ "x" <- ?_:Val ], parent(1))
       )
    </scopes>
    <heap> (MH |-> cellV(MEANT:Float)) (AN |-> list(R:ValSeq)) HREST:Map
        => (MH |-> cellV(MEANT)) (?AN2 |-> list(?RO:ValSeq)) ?FRESH:Map HREST </heap>
    <heapLoc> HLM:Int => ?HLM2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloatN(VS)
     andBool 0 <=Int MH andBool MH <Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
     andBool notBool (AN in_keys(HREST))
     andBool notBool (MH in_keys(HREST))
    ensures ?RO ==K sadSeq(VS, MEANT, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HLM2 andBool HLM <=Int ?HLM2
     andBool notBool (?AN2 ==Int MH)
     andBool keysBelow(?FRESH, ?HLM2)
     andBool notBool (?AN2 in_keys(?FRESH))
     andBool notBool (?AN2 in_keys(HREST))
     andBool notBool (MH in_keys(?FRESH))
    [all-path]

  // ---- Variant A: the pre-first-iteration frame (x not yet bound; the entry
  // premise vsLen > 0 guarantees x binds, so the post frame has it).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(BoolOp("and", Bool(true)),
           Assign(Name("$acc"),
             BinOp("+", Name("$acc"),
               ListExpr(Call(Name("abs"), BinOp("-", Name("x"), Name("mean")))))),
           .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "mean_absolute_deviation" <- _:Val ], parent(-1))
       1 |-> scope(.Map [ "$cells" <- cellsMark("mean") ]
                        [ "mean" <- cellRef(MH:Int) ]
                        [ "numbers" <- _:Val ], parent(0))
       2 |-> (
         scope(.Map [ "$acc" <- ref(AN:Int) ], parent(1)) =>
         scope(.Map [ "$acc" <- ref(?AN2:Int) ] [ "x" <- ?_:Val ], parent(1))
       )
    </scopes>
    <heap> (MH |-> cellV(MEANT:Float)) (AN |-> list(R:ValSeq)) HREST:Map
        => (MH |-> cellV(MEANT)) (?AN2 |-> list(?RO:ValSeq)) ?FRESH:Map HREST </heap>
    <heapLoc> HLM:Int => ?HLM2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloatN(VS) andBool 0 <Int vsLen(VS)
     andBool 0 <=Int MH andBool MH <Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
     andBool notBool (AN in_keys(HREST))
     andBool notBool (MH in_keys(HREST))
    ensures ?RO ==K sadSeq(VS, MEANT, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HLM2 andBool HLM <=Int ?HLM2
     andBool notBool (?AN2 ==Int MH)
     andBool keysBelow(?FRESH, ?HLM2)
     andBool notBool (?AN2 in_keys(?FRESH))
     andBool notBool (?AN2 in_keys(HREST))
     andBool notBool (MH in_keys(?FRESH))
    [all-path]

  // ---- Entry claim — the REAL canonical code, verbatim .mpy. result is a
  // Float value (no ref), so the heap post is fully existential; both frames
  // deallocate and scopeLoc winds back.
  claim
    <k>
      FuncDef("mean_absolute_deviation", Params("numbers"), CellVars("mean"), FreeVars(.ParamNames),
        Assign(
          Name("mean"),
          BinOp(
            "/",
            Call(Name("sum"), Name("numbers")),
            Call(Name("len"), Name("numbers"))))
        Return(
          BinOp(
            "/",
            Call(
              Name("sum"),
              GenExp(Call(Name("abs"), BinOp("-", Name("x"), Name("mean"))),
                CompFor(Name("x"), Name("numbers"), Bool(true)))),
            Call(Name("len"), Name("numbers")))))
      Assign(Name("result"), Call(Name("mean_absolute_deviation"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "mean_absolute_deviation" <- ?_:Val ]
                       [ "result" <-
                           divFloatIntV(
                             sumF2(sadSeq(VS, divFloatIntV(sumF2(VS, 0.0), vsLen(VS)), .ValSeq), 0.0),
                             vsLen(VS)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloatN(VS) andBool 0 <Int vsLen(VS)
    [all-path]
endmodule
