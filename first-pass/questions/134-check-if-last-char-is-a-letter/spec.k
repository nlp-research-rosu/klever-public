// spec.k — check_if_last_char_is_a_letter proof on the UNIFIED semantics (src/).
// WIDTH-2 window (last/prev codes + count n) replaces the canonical split(' ')[-1].

requires "verification.k"

module CHECK-LAST-LETTER-SPEC
  imports CHECK-LAST-LETTER-VERIFICATION

  // ---- Loop invariant (circularity) — over any IntSeq CS from (last=LAST, prev=PREV, n=N)
  // the loop leaves last := lastOf(CS,LAST), prev := prevOf(CS,LAST,PREV), n := N + isLen(CS).
  // Each step does prev:=last, last:=ord(ch), n:=n+1. Induction on CS.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("ch"),
        Assign(Name("prev"), Name("last"))
        Assign(Name("last"), Call(Name("ord"), Name("ch")))
        Assign(Name("n"), BinOp("+", Name("n"), Int(1))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "check_if_last_char_is_a_letter" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "txt" <- TV:Val ] [ "last" <- LAST:Int ] [ "prev" <- PREV:Int ] [ "n" <- N:Int ] [ "ch" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "txt" <- TV ] [ "last" <- lastOf(CS, LAST) ] [ "prev" <- prevOf(CS, LAST, PREV) ] [ "n" <- N +Int isLen(CS) ] [ "ch" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = check_if_last_char_is_a_letter(str(CS)) is True iff the last
  // char is a letter (a-z or A-Z) AND isolated (only char, or preceded by a space).
  claim
    <k>
      FuncDef("check_if_last_char_is_a_letter", Params("txt"),
        Assign(Name("last"), Int(0))
        Assign(Name("prev"), Int(0))
        Assign(Name("n"), Int(0))
        Assign(Name("ch"), Str(""))
        For(Name("ch"), Name("txt"),
          Assign(Name("prev"), Name("last"))
          Assign(Name("last"), Call(Name("ord"), Name("ch")))
          Assign(Name("n"), BinOp("+", Name("n"), Int(1))))
        Assign(Name("isletter"),
          BoolOp("or",
            BoolOp("and", Compare(Int(97), CmpOp("<=", Name("last"))),
                          Compare(Name("last"), CmpOp("<=", Int(122)))),
            BoolOp("and", Compare(Int(65), CmpOp("<=", Name("last"))),
                          Compare(Name("last"), CmpOp("<=", Int(90))))))
        Assign(Name("isolated"),
          BoolOp("or", Compare(Name("n"), CmpOp("==", Int(1))),
                       Compare(Name("prev"), CmpOp("==", Int(32)))))
        Return(BoolOp("and", Name("isletter"), Name("isolated"))))
      Assign(Name("result"), Call(Name("check_if_last_char_is_a_letter"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "check_if_last_char_is_a_letter" <- ?_:Val ]
                       [ "result" <- ( ( 97 <=Int lastOf(CS, 0) andBool lastOf(CS, 0) <=Int 122 )
                                 orBool ( 65 <=Int lastOf(CS, 0) andBool lastOf(CS, 0) <=Int 90 ) )
                              andBool ( isLen(CS) ==Int 1 orBool prevOf(CS, 0, 0) ==Int 32 ) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
