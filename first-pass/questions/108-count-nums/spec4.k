// spec4.k - stage 4: entry (all inner trusted)
requires "verification.k"

module COUNT-NUMS-SPEC4
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
    [trusted, all-path]

  // ---- ds-builder comp invariant, variant B (i bound) ----------------------

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
    requires isInt(NV) andBool projectIntTotal(NV) <Int 0
     andBool 0 <=Int ACN andBool ACN <Int HL andBool keysBelow(HREST, HL)
     andBool notBool 3 in_keys(SREST) andBool notBool 4 in_keys(SREST)
    ensures ACN <Int ?HL2 andBool HL <=Int ?HL2
     andBool keysBelow(?HN, ?HL2) andBool notBool ACN in_keys(?HN)
    [trusted, all-path]

  // ---- ds-builder comp invariant, variant B (i bound) ----------------------

  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        If(BoolOp("and", Bool(true)),
          Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Call(Name("digits_sum"), Name("i"))))),
          .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "count_nums" <- _:Val ], parent(-1))
      1 |-> scope(.Map [ "arr" <- AV:Val ]
                       [ "digits_sum" <- closureValC("n", .ParamNames,
              Assign(Name("neg"), Int(1))
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
              Return(Call(Name("sum"), Name("n"))), .Map) ], parent(0))
      2 |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ] [ "i" <- _:Val ], parent(1)) =>
        scope(.Map [ "$acc" <- ref(?AN2:Int) ] [ "i" <- ?_:Val ], parent(1))
      )
    </scopes>
    <scopeLoc> 3 </scopeLoc>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?HG:Map </heap>
    <heapLoc> HLM:Int => ?HL2:Int </heapLoc>
    <stack> ListItem(frame(CONT1:K, 1, 2)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
     andBool 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K dsFold(VS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HL2 andBool keysBelow(?HG, ?HL2)
    [trusted, all-path]

  // ---- ds-builder comp invariant, variant A (i unbound) --------------------

  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        If(BoolOp("and", Bool(true)),
          Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Call(Name("digits_sum"), Name("i"))))),
          .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "count_nums" <- _:Val ], parent(-1))
      1 |-> scope(.Map [ "arr" <- AV:Val ]
                       [ "digits_sum" <- closureValC("n", .ParamNames,
              Assign(Name("neg"), Int(1))
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
              Return(Call(Name("sum"), Name("n"))), .Map) ], parent(0))
      2 |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ], parent(1)) =>
        scope((.Map [ "$acc" <- ref(?AN2:Int) ]) ?XM:Map, parent(1))
      )
    </scopes>
    <scopeLoc> 3 </scopeLoc>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?HG:Map </heap>
    <heapLoc> HLM:Int => ?HL2:Int </heapLoc>
    <stack> ListItem(frame(CONT1:K, 1, 2)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
     andBool 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K dsFold(VS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HL2 andBool keysBelow(?HG, ?HL2)
    [trusted, all-path]

  // ---- positive-filter comp invariant, variant B (v bound) -----------------

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
    [trusted, all-path]

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
    [trusted, all-path]

  // ---- entry ----------------------------------------------------------------

  claim
    <k>
      FuncDef("count_nums", Params("arr"),
        FuncDef("digits_sum", Params("n"), CellVars(.ParamNames), FreeVars(.ParamNames),
          Assign(Name("neg"), Int(1))
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
          Return(Call(Name("sum"), Name("n"))))
        Assign(Name("ds"),
          ListComp(Call(Name("digits_sum"), Name("i")),
            CompFor(Name("i"), Name("arr"), Bool(true))))
        Return(
          Call(Name("len"),
            ListComp(Name("v"),
              CompFor(Name("v"), Name("ds"),
                Compare(Name("v"), CmpOp(">", Int(0))))))))
      Assign(Name("result"), Call(Name("count_nums"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "count_nums" <- ?_:Val ] [ "result" <- cnRes(VS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]

endmodule
