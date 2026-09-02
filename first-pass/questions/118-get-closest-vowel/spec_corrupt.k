// spec.k — get_closest_vowel proof on the UNIFIED semantics (src/).
// Width-2 window over the codes: the rightmost vowel flanked by consonants (positions
// 1..len-2). Inlined vowel membership + chr(p1) result. The canonical indexes word[i+-1].

requires "verification.k"

module GCV-CORRUPT
  imports GET-CLOSEST-VOWEL-VERIFICATION

  // ---- Loop invariant (circularity) — from (result=RES, p1=P1, p2=P2, i=IDX) the loop
  // leaves result := closeVowel(CS, IDX, P1, P2, RES) and i := IDX +Int isLen(CS).
  // Induction on CS.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("c"),
        Assign(Name("code"), Call(Name("ord"), Name("c")))
      If(Compare(Name("i"), CmpOp(">=", Int(2))),
        If(BoolOp(
          "and",
          BoolOp(
            "or",
            Compare(Name("p1"), CmpOp("==", Int(97))),
            Compare(Name("p1"), CmpOp("==", Int(101))),
            Compare(Name("p1"), CmpOp("==", Int(105))),
            Compare(Name("p1"), CmpOp("==", Int(111))),
            Compare(Name("p1"), CmpOp("==", Int(117))),
            Compare(Name("p1"), CmpOp("==", Int(65))),
            Compare(Name("p1"), CmpOp("==", Int(69))),
            Compare(Name("p1"), CmpOp("==", Int(73))),
            Compare(Name("p1"), CmpOp("==", Int(79))),
            Compare(Name("p1"), CmpOp("==", Int(85)))),
          UnaryOp(
            "not",
            BoolOp(
              "or",
              Compare(Name("p2"), CmpOp("==", Int(97))),
              Compare(Name("p2"), CmpOp("==", Int(101))),
              Compare(Name("p2"), CmpOp("==", Int(105))),
              Compare(Name("p2"), CmpOp("==", Int(111))),
              Compare(Name("p2"), CmpOp("==", Int(117))),
              Compare(Name("p2"), CmpOp("==", Int(65))),
              Compare(Name("p2"), CmpOp("==", Int(69))),
              Compare(Name("p2"), CmpOp("==", Int(73))),
              Compare(Name("p2"), CmpOp("==", Int(79))),
              Compare(Name("p2"), CmpOp("==", Int(85))))),
          UnaryOp(
            "not",
            BoolOp(
              "or",
              Compare(Name("code"), CmpOp("==", Int(97))),
              Compare(Name("code"), CmpOp("==", Int(101))),
              Compare(Name("code"), CmpOp("==", Int(105))),
              Compare(Name("code"), CmpOp("==", Int(111))),
              Compare(Name("code"), CmpOp("==", Int(117))),
              Compare(Name("code"), CmpOp("==", Int(65))),
              Compare(Name("code"), CmpOp("==", Int(69))),
              Compare(Name("code"), CmpOp("==", Int(73))),
              Compare(Name("code"), CmpOp("==", Int(79))),
              Compare(Name("code"), CmpOp("==", Int(85)))))),
          Assign(Name("result"), Call(Name("chr"), Name("p1"))),
          .Stmts),
        .Stmts)
      Assign(Name("p2"), Name("p1"))
      Assign(Name("p1"), Name("code"))
      Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
    => .K ... </k>
    <env> L:Int </env>
    <store>
      ... L |-> (
        scope(.Map [ "word" <- WV:Val ] [ "result" <- RES:Str ] [ "p1" <- P1:Int ] [ "p2" <- P2:Int ] [ "i" <- IDX:Int ] [ "c" <- _:Val ] [ "code" <- _:Val ], P:Parent) =>
        scope(.Map [ "word" <- WV ] [ "result" <- closeVowel(CS, IDX, P1, P2, RES) ] [ "p1" <- ?_:Int ] [ "p2" <- ?_:Int ] [ "i" <- IDX +Int isLen(CS) ] [ "c" <- ?_:Val ] [ "code" <- ?_:Val ], P)
      ) ...
    </store>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = get_closest_vowel(str(CS)) == closeVowel(CS, 0, 0, 0, str(iCons(122, .IntSeq))).
  claim
    <k>
      FuncDef("get_closest_vowel", Params("word"),
        Assign(Name("result"), Str(""))
        Assign(Name("p1"), Int(0))
        Assign(Name("p2"), Int(0))
        Assign(Name("i"), Int(0))
        Assign(Name("c"), Str(""))
        Assign(Name("code"), Int(0))
        For(Name("c"), Name("word"),
          Assign(Name("code"), Call(Name("ord"), Name("c")))
      If(Compare(Name("i"), CmpOp(">=", Int(2))),
        If(BoolOp(
          "and",
          BoolOp(
            "or",
            Compare(Name("p1"), CmpOp("==", Int(97))),
            Compare(Name("p1"), CmpOp("==", Int(101))),
            Compare(Name("p1"), CmpOp("==", Int(105))),
            Compare(Name("p1"), CmpOp("==", Int(111))),
            Compare(Name("p1"), CmpOp("==", Int(117))),
            Compare(Name("p1"), CmpOp("==", Int(65))),
            Compare(Name("p1"), CmpOp("==", Int(69))),
            Compare(Name("p1"), CmpOp("==", Int(73))),
            Compare(Name("p1"), CmpOp("==", Int(79))),
            Compare(Name("p1"), CmpOp("==", Int(85)))),
          UnaryOp(
            "not",
            BoolOp(
              "or",
              Compare(Name("p2"), CmpOp("==", Int(97))),
              Compare(Name("p2"), CmpOp("==", Int(101))),
              Compare(Name("p2"), CmpOp("==", Int(105))),
              Compare(Name("p2"), CmpOp("==", Int(111))),
              Compare(Name("p2"), CmpOp("==", Int(117))),
              Compare(Name("p2"), CmpOp("==", Int(65))),
              Compare(Name("p2"), CmpOp("==", Int(69))),
              Compare(Name("p2"), CmpOp("==", Int(73))),
              Compare(Name("p2"), CmpOp("==", Int(79))),
              Compare(Name("p2"), CmpOp("==", Int(85))))),
          UnaryOp(
            "not",
            BoolOp(
              "or",
              Compare(Name("code"), CmpOp("==", Int(97))),
              Compare(Name("code"), CmpOp("==", Int(101))),
              Compare(Name("code"), CmpOp("==", Int(105))),
              Compare(Name("code"), CmpOp("==", Int(111))),
              Compare(Name("code"), CmpOp("==", Int(117))),
              Compare(Name("code"), CmpOp("==", Int(65))),
              Compare(Name("code"), CmpOp("==", Int(69))),
              Compare(Name("code"), CmpOp("==", Int(73))),
              Compare(Name("code"), CmpOp("==", Int(79))),
              Compare(Name("code"), CmpOp("==", Int(85)))))),
          Assign(Name("result"), Call(Name("chr"), Name("p1"))),
          .Stmts),
        .Stmts)
      Assign(Name("p2"), Name("p1"))
      Assign(Name("p1"), Name("code"))
      Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("get_closest_vowel"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <store>
      0 |-> scope(.Map, root)
    =>
      0 |-> scope(.Map [ "get_closest_vowel" <- ?_:Val ] [ "result" <- closeVowel(CS, 0, 0, 0, str(iCons(122, .IntSeq))) ], root)
      1 |-> scope(?_:Map, parent(0))
    </store>
    <nextLoc> 1 => 2 </nextLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
