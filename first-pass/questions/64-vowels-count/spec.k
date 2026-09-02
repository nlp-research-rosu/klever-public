// spec.k — vowels_count proof on the UNIFIED semantics (src/).
// Dual accumulator: count vowels (10-way code membership) and thread `last` = the
// current code, so the trailing y/Y bump replaces the canonical's s[-1] (intractable).

requires "verification.k"

module VOWELS-COUNT-SPEC
  imports VOWELS-COUNT-VERIFICATION

  // ---- Loop invariant (circularity) — count := CNT +Int vowelCount(CS),
  // last := lastOf(CS, LAST). Induction on CS; the 10-way `or` case-splits per vowel.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("c"),
        Assign(Name("code"), Call(Name("ord"), Name("c")))
        If(BoolOp("or",
             Compare(Name("code"), CmpOp("==", Int(97))),
             Compare(Name("code"), CmpOp("==", Int(101))),
             Compare(Name("code"), CmpOp("==", Int(105))),
             Compare(Name("code"), CmpOp("==", Int(111))),
             Compare(Name("code"), CmpOp("==", Int(117))),
             Compare(Name("code"), CmpOp("==", Int(65))),
             Compare(Name("code"), CmpOp("==", Int(69))),
             Compare(Name("code"), CmpOp("==", Int(73))),
             Compare(Name("code"), CmpOp("==", Int(79))),
             Compare(Name("code"), CmpOp("==", Int(85)))),
           Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
           .Stmts)
        Assign(Name("last"), Name("code")))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "vowels_count" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "s" <- SV:Val ] [ "count" <- CNT:Int ] [ "last" <- LAST:Int ]
                   [ "c" <- _:Val ] [ "code" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "s" <- SV ] [ "count" <- CNT +Int vowelCount(CS) ] [ "last" <- lastOf(CS, LAST) ]
                   [ "c" <- ?_:Val ] [ "code" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = vowels_count(str(CS)) = vowelCount(CS) + (1 if last y/Y).
  claim
    <k>
      FuncDef("vowels_count", Params("s"),
        Assign(Name("count"), Int(0))
        Assign(Name("last"), Int(0))
        Assign(Name("c"), Str(""))
        Assign(Name("code"), Int(0))
        For(Name("c"), Name("s"),
          Assign(Name("code"), Call(Name("ord"), Name("c")))
          If(BoolOp("or",
               Compare(Name("code"), CmpOp("==", Int(97))),
               Compare(Name("code"), CmpOp("==", Int(101))),
               Compare(Name("code"), CmpOp("==", Int(105))),
               Compare(Name("code"), CmpOp("==", Int(111))),
               Compare(Name("code"), CmpOp("==", Int(117))),
               Compare(Name("code"), CmpOp("==", Int(65))),
               Compare(Name("code"), CmpOp("==", Int(69))),
               Compare(Name("code"), CmpOp("==", Int(73))),
               Compare(Name("code"), CmpOp("==", Int(79))),
               Compare(Name("code"), CmpOp("==", Int(85)))),
             Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
             .Stmts)
          Assign(Name("last"), Name("code")))
        If(BoolOp("or",
             Compare(Name("last"), CmpOp("==", Int(121))),
             Compare(Name("last"), CmpOp("==", Int(89)))),
           Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
           .Stmts)
        Return(Name("count")))
      Assign(Name("result"), Call(Name("vowels_count"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "vowels_count" <- ?_:Val ]
                       [ "result" <- vowelCount(CS)
                                     +Int (#if (lastOf(CS, 0) ==Int 121 orBool lastOf(CS, 0) ==Int 89)
                                           #then 1 #else 0 #fi) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
