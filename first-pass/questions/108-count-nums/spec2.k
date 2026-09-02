// spec2.k - stage 2a: callee span POSITIVE branch (leaves trusted)
requires "verification.k"

module COUNT-NUMS-SPEC2
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
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HL2 andBool keysBelow(?HG, ?HL2)
    [trusted, all-path]

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
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HL2 andBool keysBelow(?HG, ?HL2)
    [trusted, all-path]

  // ---- the real sum fold over an all-int list (the P67 claim) --------------

  claim <k> #sumAcc(list(VS2:ValSeq), ACC2:Int) => ?R:Int ... </k>
        requires allInt(VS2)
        ensures  ?R ==Int sumI(VS2, ACC2)
        [trusted, all-path]

  // ---- digits_sum callee span (frame 3; caller is comp1's frame 2) ---------

  claim
    <k>
      (Assign(Name("neg"), Int(1))
       If(Compare(Name("n"), CmpOp("<", Int(0))),
         Assign(
           TupleExpr(Name("n"), Name("neg")),
           TupleExpr(
             BinOp("*", UnaryOp("-", Int(1)), Name("n")),
             UnaryOp("-", Int(1)))),
         .Stmts)
       Assign(Name("n"),
         ListComp(Call(Name("int"), Name("i")),
           CompFor(Name("i"), Call(Name("str"), Name("n")), Bool(true))))
       Assign(Subscript(Name("n"), Int(0)),
         BinOp("*", Subscript(Name("n"), Int(0)), Name("neg")))
       Return(Call(Name("sum"), Name("n")))):Stmts ~> #endcall
    => dsRes(projectIntTotal(NV)) ~> CONT </k>
    <env> 3 => 2 </env>
    <scopes>
      (-1 |-> builtinsScope)
      (0 |-> scope(.Map [ "count_nums" <- CNV:Val ], parent(-1)))
      (3 |-> scope(.Map [ "n" <- NV:Val ] [ "$cells" <- cellsMark(.ParamNames) ], parent(0)))
      SREST:Map
    =>
      (-1 |-> builtinsScope)
      (0 |-> scope(.Map [ "count_nums" <- CNV ], parent(-1)))
      SREST
    </scopes>
    <scopeLoc> 4 => 3 </scopeLoc>
    <heap> (ACN:Int |-> list(ACC:ValSeq)) HREST:Map
        => (ACN |-> list(ACC)) ?HN:Map </heap>
    <heapLoc> HL:Int => ?HL2:Int </heapLoc>
    // CLOSED stack: kore list unification cannot peel a head over two
    // concrete frames plus a symbolic tail (probed), so nested spans pin
    // the exact stack
    <stack> ListItem(frame(CONT:K, 2, 3)) ListItem(frame(CONT1:K, 1, 2))
         => ListItem(frame(CONT1, 1, 2)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isInt(NV) andBool projectIntTotal(NV) >=Int 0
     andBool 0 <=Int ACN andBool ACN <Int HL andBool keysBelow(HREST, HL)
     andBool notBool 3 in_keys(SREST) andBool notBool 4 in_keys(SREST)
    ensures ACN <Int ?HL2 andBool HL <=Int ?HL2
     andBool keysBelow(?HN, ?HL2) andBool notBool ACN in_keys(?HN)
    [all-path]

  // ---- ds-builder comp invariant, variant B (i bound) ----------------------

endmodule
