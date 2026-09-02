// spec.k — anti_shuffle, TRAP-FREE (W3 P86). The REAL canonical: the mapping
// comprehension over s.split(' '), each word through the composed shared
// atoms (charsOf -> sortVS -> joinCodes), space-joined. P19 template.
//
//   kompile verification.k --backend haskell --main-module ANTI-SHUFFLE-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module ANTI-SHUFFLE-SPEC

requires "verification.k"

module ANTI-SHUFFLE-SPEC
  imports ANTI-SHUFFLE-VERIFICATION

  // ---- Comp-loop invariant, variant B (i bound) ------------------------------
  claim
    <k>
      #loop(list(WS:ValSeq), Name("i"),
        If(BoolOp("and", Bool(true)),
          Assign(Name("$acc"),
            BinOp("+", Name("$acc"),
              ListExpr(Call(
                Attribute(Str(""), "join"),
                Call(Name("sorted"), Call(Name("list"), Name("i"))))))),
          .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "anti_shuffle" <- _:Val ], parent(-1))
      1 |-> scope(.Map [ "s" <- _:Val ], parent(0))
      2 |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ] [ "i" <- _:Val ], parent(1)) =>
        scope(.Map [ "$acc" <- ref(?AN2:Int) ] [ "i" <- ?_:Val ], parent(1))
      )
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?FRESH:Map HREST </heap>
    <heapLoc> HLM:Int => ?HLM2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(WS)
     andBool 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
     andBool notBool (AN in_keys(HREST))
    ensures ?RO ==K mapAcc(WS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HLM2 andBool HLM <=Int ?HLM2
     andBool keysBelow(?FRESH, ?HLM2)
     andBool notBool (?AN2 in_keys(?FRESH))
     andBool notBool (?AN2 in_keys(HREST))
    [all-path]

  // ---- Variant A (i unbound; nonempty spelled structurally — the remainder
  // branch gets the positive equation and finishes the zero case structurally)
  claim
    <k>
      #loop(list(WS:ValSeq), Name("i"),
        If(BoolOp("and", Bool(true)),
          Assign(Name("$acc"),
            BinOp("+", Name("$acc"),
              ListExpr(Call(
                Attribute(Str(""), "join"),
                Call(Name("sorted"), Call(Name("list"), Name("i"))))))),
          .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "anti_shuffle" <- _:Val ], parent(-1))
      1 |-> scope(.Map [ "s" <- _:Val ], parent(0))
      2 |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ], parent(1)) =>
        scope(.Map [ "$acc" <- ref(?AN2:Int) ] [ "i" <- ?_:Val ], parent(1))
      )
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?FRESH:Map HREST </heap>
    <heapLoc> HLM:Int => ?HLM2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(WS) andBool notBool (WS ==K .ValSeq)
     andBool 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
     andBool notBool (AN in_keys(HREST))
    ensures ?RO ==K mapAcc(WS, R)
     andBool 0 <=Int ?AN2 andBool ?AN2 <Int ?HLM2 andBool HLM <=Int ?HLM2
     andBool keysBelow(?FRESH, ?HLM2)
     andBool notBool (?AN2 in_keys(?FRESH))
     andBool notBool (?AN2 in_keys(HREST))
    [all-path]

  // ---- Entry — result = the space-join of the per-word sorted strings.
  claim
    <k>
      FuncDef("anti_shuffle", Params("s"),
        Return(
          Call(
            Attribute(Str(" "), "join"),
            ListComp(Call(
              Attribute(Str(""), "join"),
              Call(Name("sorted"), Call(Name("list"), Name("i")))),
              CompFor(
                Name("i"),
                Call(Attribute(Name("s"), "split"), Str(" ")),
                Bool(true))))))
      Assign(Name("result"), Call(Name("anti_shuffle"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "anti_shuffle" <- ?_:Val ]
                       [ "result" <-
                           str(joinCodes(iCons(32, .IntSeq),
                             mapAcc(splitSep(CS, 32, .IntSeq), .ValSeq))) ], parent(-1))
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
