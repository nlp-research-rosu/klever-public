requires "verification.k"

module PARSE-MUSIC-SPEC
  imports PARSE-MUSIC-VERIFICATION

  // ---- Listcomp-loop invariant (circularity), variant B: x bound. Frame 1
  // pins note_map (concrete dictV) + music_string; $acc is a plus-builder.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(BoolOp("and", Name("x")),
           Assign(Name("$acc"),
             BinOp("+", Name("$acc"),
               ListExpr(Subscript(Name("note_map"), Name("x"))))),
           .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "parse_music" <- _:Val ], parent(-1))
       1 |-> scope(.Map [ "music_string" <- _:Val ]
                        [ "note_map" <- dictV(vCons(str(iCons(111, .IntSeq)), vCons(str(iCons(111, iCons(124, .IntSeq))), vCons(str(iCons(46, iCons(124, .IntSeq))), .ValSeq))), vCons(4, vCons(2, vCons(1, .ValSeq)))) ], parent(0))
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
    requires validToks(VS)
     andBool 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K musicFold(VS, R)
    [all-path]

  // ---- Variant A: pre-first-iteration (x unbound; split yields >= 1 token).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(BoolOp("and", Name("x")),
           Assign(Name("$acc"),
             BinOp("+", Name("$acc"),
               ListExpr(Subscript(Name("note_map"), Name("x"))))),
           .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "parse_music" <- _:Val ], parent(-1))
       1 |-> scope(.Map [ "music_string" <- _:Val ]
                        [ "note_map" <- dictV(vCons(str(iCons(111, .IntSeq)), vCons(str(iCons(111, iCons(124, .IntSeq))), vCons(str(iCons(46, iCons(124, .IntSeq))), .ValSeq))), vCons(4, vCons(2, vCons(1, .ValSeq)))) ], parent(0))
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
    requires validToks(VS) andBool 0 <Int vsLen(VS)
     andBool 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K musicFold(VS, R)
    [all-path]

  // ---- Entry claim -- the REAL canonical code, verbatim .mpy. The result
  // list escapes by ref; tokens-list and $acc garbage stay existential.
  claim
    <k>
      FuncDef("parse_music", Params("music_string"),
        Assign(
          Name("note_map"),
          DictExpr(
            Entry(Str("o"), Int(4)),
            Entry(Str("o|"), Int(2)),
            Entry(Str(".|"), Int(1))))
        Return(
          ListComp(Subscript(Name("note_map"), Name("x")),
            CompFor(
              Name("x"),
              Call(Attribute(Name("music_string"), "split"), Str(" ")),
              Name("x")))))
      Assign(Name("result"), Call(Name("parse_music"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "parse_music" <- ?_:Val ]
                       [ "result" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(musicFold(splitSep(CS, 32, .IntSeq), .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validToks(splitSep(CS, 32, .IntSeq))
    [all-path]
endmodule
