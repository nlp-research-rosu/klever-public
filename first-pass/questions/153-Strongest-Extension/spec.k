// spec.k — Strongest_Extension: REFERENCE statement of all 7 claims.
// The proof RUNS STAGED (each stage < the 500s cap; the single module
// times out): spec1.k (4 inner comp claims) -> spec2.k (2 outer argmax
// claims, inners [trusted]) -> spec3.k (entry, all 6 [trusted]).
// F1 reverify must run the three staged modules, in order.

requires "verification.k"

module STRONGEST-EXTENSION-SPEC
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
  claim
    <k>
      #loop(list(VS:ValSeq), Name("s"),
        Assign(
          Name("val"),
          BinOp(
            "-",
            Call(
              Name("len"),
              ListComp(Name("x"),
                CompFor(
                  Name("x"),
                  Name("s"),
                  BoolOp(
                    "and",
                    Call(Attribute(Name("x"), "isalpha"), .Exprs),
                    Call(Attribute(Name("x"), "isupper"), .Exprs))))),
            Call(
              Name("len"),
              ListComp(Name("x"),
                CompFor(
                  Name("x"),
                  Name("s"),
                  BoolOp(
                    "and",
                    Call(Attribute(Name("x"), "isalpha"), .Exprs),
                    Call(Attribute(Name("x"), "islower"), .Exprs)))))))
        If(Compare(Name("val"), CmpOp(">", Name("my_val"))),
          Assign(Name("strong"), Name("s"))
          Assign(Name("my_val"), Name("val")),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "Strongest_Extension" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "class_name" <- CNV:Val ] [ "extensions" <- EXV:Val ]
                    [ "strong" <- SV:Val ] [ "my_val" <- MV:Int ]
                    [ "s" <- _:Val ] [ "val" <- _:Val ], parent(0)) =>
         scope((.Map [ "class_name" <- CNV ] [ "extensions" <- EXV ]
                    [ "strong" <- selSV(VS, SV, MV) ]
                    [ "my_val" <- selMV(VS, MV) ]) [ "s" <- ?_:Val ] [ "val" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HP:Map => ?_:Map </heap>
    <heapLoc> HL:Int => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStrV(VS) andBool 0 <=Int HL andBool keysBelow(HP, HL)
    ensures true
    [all-path]

  // ---- Outer argmax invariant, variant A (pre-first-iteration).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("s"),
        Assign(
          Name("val"),
          BinOp(
            "-",
            Call(
              Name("len"),
              ListComp(Name("x"),
                CompFor(
                  Name("x"),
                  Name("s"),
                  BoolOp(
                    "and",
                    Call(Attribute(Name("x"), "isalpha"), .Exprs),
                    Call(Attribute(Name("x"), "isupper"), .Exprs))))),
            Call(
              Name("len"),
              ListComp(Name("x"),
                CompFor(
                  Name("x"),
                  Name("s"),
                  BoolOp(
                    "and",
                    Call(Attribute(Name("x"), "isalpha"), .Exprs),
                    Call(Attribute(Name("x"), "islower"), .Exprs)))))))
        If(Compare(Name("val"), CmpOp(">", Name("my_val"))),
          Assign(Name("strong"), Name("s"))
          Assign(Name("my_val"), Name("val")),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "Strongest_Extension" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "class_name" <- CNV:Val ] [ "extensions" <- EXV:Val ]
                    [ "strong" <- SV:Val ] [ "my_val" <- MV:Int ], parent(0)) =>
         scope((.Map [ "class_name" <- CNV ] [ "extensions" <- EXV ]
                    [ "strong" <- selSV(VS, SV, MV) ]
                    [ "my_val" <- selMV(VS, MV) ])
                    [ "s" <- ?_:Val ] [ "val" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HP:Map => ?_:Map </heap>
    <heapLoc> HL:Int => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStrV(VS) andBool 0 <Int vsLen(VS)
     andBool 0 <=Int HL andBool keysBelow(HP, HL)
    ensures true
    [all-path]

  // ---- Entry claim -- the REAL canonical code, verbatim .mpy. The head
  // extension is cons-form structural so extensions[0] reduces; result is the
  // real two-step concat.
  claim
    <k>
      FuncDef("Strongest_Extension", Params("class_name", "extensions"),
        Assign(Name("strong"), Subscript(Name("extensions"), Int(0)))
        Assign(
          Name("my_val"),
          BinOp(
            "-",
            Call(
              Name("len"),
              ListComp(Name("x"),
                CompFor(
                  Name("x"),
                  Subscript(Name("extensions"), Int(0)),
                  BoolOp(
                    "and",
                    Call(Attribute(Name("x"), "isalpha"), .Exprs),
                    Call(Attribute(Name("x"), "isupper"), .Exprs))))),
            Call(
              Name("len"),
              ListComp(Name("x"),
                CompFor(
                  Name("x"),
                  Subscript(Name("extensions"), Int(0)),
                  BoolOp(
                    "and",
                    Call(Attribute(Name("x"), "isalpha"), .Exprs),
                    Call(Attribute(Name("x"), "islower"), .Exprs)))))))
        For(Name("s"), Name("extensions"),
          Assign(
            Name("val"),
            BinOp(
              "-",
              Call(
                Name("len"),
                ListComp(Name("x"),
                  CompFor(
                    Name("x"),
                    Name("s"),
                    BoolOp(
                      "and",
                      Call(Attribute(Name("x"), "isalpha"), .Exprs),
                      Call(Attribute(Name("x"), "isupper"), .Exprs))))),
              Call(
                Name("len"),
                ListComp(Name("x"),
                  CompFor(
                    Name("x"),
                    Name("s"),
                    BoolOp(
                      "and",
                      Call(Attribute(Name("x"), "isalpha"), .Exprs),
                      Call(Attribute(Name("x"), "islower"), .Exprs)))))))
          If(Compare(Name("val"), CmpOp(">", Name("my_val"))),
            Assign(Name("strong"), Name("s"))
            Assign(Name("my_val"), Name("val")),
            .Stmts))
        Return(
          BinOp(
            "+",
            BinOp("+", Name("class_name"), Str(".")),
            Name("strong"))))
      Assign(Name("result"),
        Call(Name("Strongest_Extension"), str(CNS:IntSeq), list(vCons(str(CS0:IntSeq), VS:ValSeq))))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "Strongest_Extension" <- ?_:Val ]
                       [ "result" <-
                           str(seqConcat(CNS, seqConcat(iCons(46, .IntSeq),
                             codesProj(selSV(vCons(str(CS0), VS), str(CS0), stCS(CS0)))))) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStrV(VS)
    [all-path]
endmodule
