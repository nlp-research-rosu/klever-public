// spec.k — sort_numbers, TRAP-FREE (W3 P19). The REAL canonical: dict
// value_map (a cell captured by the key lambda), the filtering comprehension
// over numbers.split(' '), the SHARED opaque keyed sort with the closure
// inside the atom (P145), and ' '.join as the shared joinCodes.
//
//   kompile verification.k --backend haskell --main-module SORT-NUMBERS-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module SORT-NUMBERS-SPEC

requires "verification.k"

module SORT-NUMBERS-SPEC
  imports SORT-NUMBERS-VERIFICATION

  // ---- Comp-loop invariant (circularity), variant B: x bound. Frame 1 is the
  // function frame ($cells value_map -> cellRef(MH), numbers); frame 2 the comp
  // closure ($acc plus-builder, x). The Q4 discipline: symbolic MH cell pin.
  claim
    <k>
      #loop(list(WS:ValSeq), Name("x"),
        If(BoolOp("and", Name("x")),
          Assign(Name("$acc"),
            BinOp("+", Name("$acc"), ListExpr(Name("x")))),
          .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sort_numbers" <- _:Val ], parent(-1))
      1 |-> scope(.Map [ "$cells" <- cellsMark("value_map") ]
                       [ "value_map" <- cellRef(MH:Int) ]
                       [ "numbers" <- _:Val ], parent(0))
      2 |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ] [ "x" <- _:Val ], parent(1)) =>
        scope(.Map [ "$acc" <- ref(?AN2:Int) ] [ "x" <- ?_:Val ], parent(1))
      )
    </scopes>
    <heap> (MH |-> cellV(MV:Val)) (AN |-> list(R:ValSeq)) HREST:Map
        => (MH |-> cellV(MV)) (?AN2 |-> list(?RO:ValSeq)) ?FRESH:Map HREST </heap>
    <heapLoc> HLM:Int => ?HLM2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(WS)
     andBool 0 <=Int MH andBool MH <Int AN
     andBool AN <Int HLM andBool keysBelow(HREST, HLM)
     andBool notBool (AN in_keys(HREST))
     andBool notBool (MH in_keys(HREST))
    ensures ?RO ==K ftAcc(WS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HLM2 andBool HLM <=Int ?HLM2
     andBool notBool (?AN2 ==Int MH)
     andBool keysBelow(?FRESH, ?HLM2)
     andBool notBool (?AN2 in_keys(?FRESH))
     andBool notBool (?AN2 in_keys(HREST))
    [all-path]

  // ---- Variant A: the pre-first-iteration frame (x not yet bound).
  claim
    <k>
      #loop(list(WS:ValSeq), Name("x"),
        If(BoolOp("and", Name("x")),
          Assign(Name("$acc"),
            BinOp("+", Name("$acc"), ListExpr(Name("x")))),
          .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sort_numbers" <- _:Val ], parent(-1))
      1 |-> scope(.Map [ "$cells" <- cellsMark("value_map") ]
                       [ "value_map" <- cellRef(MH:Int) ]
                       [ "numbers" <- _:Val ], parent(0))
      2 |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ], parent(1)) =>
        scope(.Map [ "$acc" <- ref(?AN2:Int) ] [ "x" <- ?_:Val ], parent(1))
      )
    </scopes>
    <heap> (MH |-> cellV(MV:Val)) (AN |-> list(R:ValSeq)) HREST:Map
        => (MH |-> cellV(MV)) (?AN2 |-> list(?RO:ValSeq)) ?FRESH:Map HREST </heap>
    <heapLoc> HLM:Int => ?HLM2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(WS) andBool notBool (WS ==K .ValSeq)
     andBool 0 <=Int MH andBool MH <Int AN
     andBool AN <Int HLM andBool keysBelow(HREST, HLM)
     andBool notBool (AN in_keys(HREST))
     andBool notBool (MH in_keys(HREST))
    ensures ?RO ==K ftAcc(WS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HLM2 andBool HLM <=Int ?HLM2
     andBool notBool (?AN2 ==Int MH)
     andBool keysBelow(?FRESH, ?HLM2)
     andBool notBool (?AN2 in_keys(?FRESH))
     andBool notBool (?AN2 in_keys(HREST))
    [all-path]

  // ---- Entry claim — the REAL canonical code, verbatim .mpy. The result is
  // a str VALUE: join over the keyed sort of the filtered tokens, the lambda
  // closure (capturing the value_map cell) verbatim inside the opaque atom.
  claim
    <k>
      FuncDef("sort_numbers", Params("numbers"), CellVars("value_map"), FreeVars(.ParamNames),
        Assign(
          Name("value_map"),
          DictExpr(
            Entry(Str("zero"), Int(0)),
            Entry(Str("one"), Int(1)),
            Entry(Str("two"), Int(2)),
            Entry(Str("three"), Int(3)),
            Entry(Str("four"), Int(4)),
            Entry(Str("five"), Int(5)),
            Entry(Str("six"), Int(6)),
            Entry(Str("seven"), Int(7)),
            Entry(Str("eight"), Int(8)),
            Entry(Str("nine"), Int(9))))
        Return(
          Call(
            Attribute(Str(" "), "join"),
            Call(
              Name("sorted"),
              ListComp(Name("x"),
                CompFor(
                  Name("x"),
                  Call(Attribute(Name("numbers"), "split"), Str(" ")),
                  Name("x"))),
              KwArg(
                "key",
                Lambda(
                  Params("x"),
                  CellVars(.ParamNames),
                  FreeVars("value_map"),
                  Subscript(Name("value_map"), Name("x"))))))))
      Assign(Name("result"), Call(Name("sort_numbers"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sort_numbers" <- ?_:Val ]
                       [ "result" <-
                           str(joinCodes(iCons(32, .IntSeq),
                             sortKeyVS(ftAcc(splitSep(CS, 32, .IntSeq), .ValSeq),
                               closureValC(("x", .ParamNames), .ParamNames,
                                 Return(Subscript(Name("value_map"), Name("x"))) .Stmts,
                                 "value_map" |-> cellRef(0))))) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
