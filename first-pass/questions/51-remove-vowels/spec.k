// spec.k — remove_vowels proof on the UNIFIED semantics (src/).
// The canonical is "".join([s for s in text if s.lower() not in "aeiou"]) — join +
// .lower() unmodeled; solution.py is the equivalent explicit non-vowel filter loop.

requires "verification.k"

module REMOVE-VOWELS-SPEC
  imports REMOVE-VOWELS-VERIFICATION

  // ---- Loop invariant (circularity) — string FILTER. From result=str(R) the loop
  // appends each non-vowel char, leaving result := str(seqConcat(R, filterSeq(CS))).
  // Induction on CS; the 10-way `and` of `!=` keeps iff notBool isVowel(code).
  claim
    <k>
      #loop(str(CS:IntSeq), Name("s"),
        Assign(Name("code"), Call(Name("ord"), Name("s")))
        If(BoolOp("and",
             Compare(Name("code"), CmpOp("!=", Int(97))),
             Compare(Name("code"), CmpOp("!=", Int(101))),
             Compare(Name("code"), CmpOp("!=", Int(105))),
             Compare(Name("code"), CmpOp("!=", Int(111))),
             Compare(Name("code"), CmpOp("!=", Int(117))),
             Compare(Name("code"), CmpOp("!=", Int(65))),
             Compare(Name("code"), CmpOp("!=", Int(69))),
             Compare(Name("code"), CmpOp("!=", Int(73))),
             Compare(Name("code"), CmpOp("!=", Int(79))),
             Compare(Name("code"), CmpOp("!=", Int(85)))),
           Assign(Name("result"), BinOp("+", Name("result"), Name("s"))),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "remove_vowels" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "text" <- TV:Val ] [ "result" <- str(R:IntSeq) ] [ "s" <- _:Val ] [ "code" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "text" <- TV ] [ "result" <- str(seqConcat(R, filterSeq(CS))) ] [ "s" <- ?_:Val ] [ "code" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = remove_vowels(str(CS)) == str(filterSeq(CS)).
  claim
    <k>
      FuncDef("remove_vowels", Params("text"),
        Assign(Name("result"), Str(""))
        Assign(Name("s"), Str(""))
        Assign(Name("code"), Int(0))
        For(Name("s"), Name("text"),
          Assign(Name("code"), Call(Name("ord"), Name("s")))
          If(BoolOp("and",
               Compare(Name("code"), CmpOp("!=", Int(97))),
               Compare(Name("code"), CmpOp("!=", Int(101))),
               Compare(Name("code"), CmpOp("!=", Int(105))),
               Compare(Name("code"), CmpOp("!=", Int(111))),
               Compare(Name("code"), CmpOp("!=", Int(117))),
               Compare(Name("code"), CmpOp("!=", Int(65))),
               Compare(Name("code"), CmpOp("!=", Int(69))),
               Compare(Name("code"), CmpOp("!=", Int(73))),
               Compare(Name("code"), CmpOp("!=", Int(79))),
               Compare(Name("code"), CmpOp("!=", Int(85)))),
             Assign(Name("result"), BinOp("+", Name("result"), Name("s"))),
             .Stmts))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("remove_vowels"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "remove_vowels" <- ?_:Val ] [ "result" <- str(filterSeq(CS)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
