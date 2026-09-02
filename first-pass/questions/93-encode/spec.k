// spec.k — encode proof on the UNIFIED semantics (src/).
// The canonical uses message.swapcase() + a dict comprehension + ''.join (all
// unmodeled); solution.py is the equivalent explicit swapcase+vowel-shift char-map.

requires "verification.k"

module ENCODE-SPEC
  imports ENCODE-VERIFICATION

  // ---- Loop invariant (circularity) — string map. From result=str(R) the loop
  // appends chr(encChar(code)) per char, leaving result := str(seqConcat(R, encMap(CS))).
  // Induction on CS; the if/elif (swapcase) then 10-way vowel `or` line up with encChar.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("c"),
        Assign(Name("code"), Call(Name("ord"), Name("c")))
        Assign(Name("new"), Name("code"))
        If(BoolOp("and", Compare(Name("code"), CmpOp(">=", Int(65))), Compare(Name("code"), CmpOp("<=", Int(90)))),
          Assign(Name("new"), BinOp("+", Name("code"), Int(32))),
          If(BoolOp("and", Compare(Name("code"), CmpOp(">=", Int(97))), Compare(Name("code"), CmpOp("<=", Int(122)))),
            Assign(Name("new"), BinOp("-", Name("code"), Int(32))),
            .Stmts))
        If(BoolOp("or",
             Compare(Name("new"), CmpOp("==", Int(97))),
             Compare(Name("new"), CmpOp("==", Int(101))),
             Compare(Name("new"), CmpOp("==", Int(105))),
             Compare(Name("new"), CmpOp("==", Int(111))),
             Compare(Name("new"), CmpOp("==", Int(117))),
             Compare(Name("new"), CmpOp("==", Int(65))),
             Compare(Name("new"), CmpOp("==", Int(69))),
             Compare(Name("new"), CmpOp("==", Int(73))),
             Compare(Name("new"), CmpOp("==", Int(79))),
             Compare(Name("new"), CmpOp("==", Int(85)))),
           Assign(Name("new"), BinOp("+", Name("new"), Int(2))),
           .Stmts)
        Assign(Name("result"), BinOp("+", Name("result"), Call(Name("chr"), Name("new")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "encode" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "message" <- SV:Val ] [ "result" <- str(R:IntSeq) ]
                   [ "c" <- _:Val ] [ "code" <- _:Val ] [ "new" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "message" <- SV ] [ "result" <- str(seqConcat(R, encMap(CS))) ]
                   [ "c" <- ?_:Val ] [ "code" <- ?_:Val ] [ "new" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = encode(str(CS)) == str(encMap(CS)).
  claim
    <k>
      FuncDef("encode", Params("message"),
        Assign(Name("result"), Str(""))
        Assign(Name("c"), Str(""))
        Assign(Name("code"), Int(0))
        Assign(Name("new"), Int(0))
        For(Name("c"), Name("message"),
          Assign(Name("code"), Call(Name("ord"), Name("c")))
          Assign(Name("new"), Name("code"))
          If(BoolOp("and", Compare(Name("code"), CmpOp(">=", Int(65))), Compare(Name("code"), CmpOp("<=", Int(90)))),
            Assign(Name("new"), BinOp("+", Name("code"), Int(32))),
            If(BoolOp("and", Compare(Name("code"), CmpOp(">=", Int(97))), Compare(Name("code"), CmpOp("<=", Int(122)))),
              Assign(Name("new"), BinOp("-", Name("code"), Int(32))),
              .Stmts))
          If(BoolOp("or",
               Compare(Name("new"), CmpOp("==", Int(97))),
               Compare(Name("new"), CmpOp("==", Int(101))),
               Compare(Name("new"), CmpOp("==", Int(105))),
               Compare(Name("new"), CmpOp("==", Int(111))),
               Compare(Name("new"), CmpOp("==", Int(117))),
               Compare(Name("new"), CmpOp("==", Int(65))),
               Compare(Name("new"), CmpOp("==", Int(69))),
               Compare(Name("new"), CmpOp("==", Int(73))),
               Compare(Name("new"), CmpOp("==", Int(79))),
               Compare(Name("new"), CmpOp("==", Int(85)))),
             Assign(Name("new"), BinOp("+", Name("new"), Int(2))),
             .Stmts)
          Assign(Name("result"), BinOp("+", Name("result"), Call(Name("chr"), Name("new")))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("encode"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "encode" <- ?_:Val ] [ "result" <- str(encMap(CS)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
