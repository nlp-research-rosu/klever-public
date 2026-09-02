// spec.k — is_nested on the UNIFIED semantics (src/). Single-pass scalar-accumulator loop invariant
// (6 scalars folded via nestFold) + entry. The per-char `string[i]=='['` is intSeqAt(CS,I)==91
// (case-splittable). See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module IS-NESTED-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module IS-NESTED-SPEC

requires "verification.k"

module IS-NESTED-SPEC
  imports IS-NESTED-VERIFICATION

  // ---- LOOP invariant (i-scan) — leaves the 6 scalars := projections of
  // nestFold(CS, I, N, nstate(NO,NC,FO,SO,LC,SLC)). Case-splits on intSeqAt(CS,I)==91 each step.
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        If(Compare(Subscript(Name("string"), Name("i")), CmpOp("==", Str("["))),
          Assign(Name("num_opens"), BinOp("+", Name("num_opens"), Int(1)))
          If(Compare(Name("num_opens"), CmpOp("==", Int(1))), Assign(Name("first_open"), Name("i")), .Stmts)
          If(Compare(Name("num_opens"), CmpOp("==", Int(2))), Assign(Name("second_open"), Name("i")), .Stmts),
          Assign(Name("num_closes"), BinOp("+", Name("num_closes"), Int(1)))
          Assign(Name("second_last_close"), Name("last_close"))
          Assign(Name("last_close"), Name("i"))))
    => .K ... </k>
    <env> L0:Int </env>
    <scopes>
      ... L0 |-> ( scope(.Map [ "string" <- str(CS:IntSeq) ] [ "num_opens" <- NO:Int ] [ "num_closes" <- NC:Int ]
                              [ "first_open" <- FO:Int ] [ "second_open" <- SO:Int ] [ "last_close" <- LC:Int ]
                              [ "second_last_close" <- SLC:Int ] [ "i" <- _:Val ], PR:Parent)
               => scope(.Map [ "string" <- str(CS) ]
                              [ "num_opens" <- nNo(nestFold(CS, I, N, nstate(NO, NC, FO, SO, LC, SLC))) ]
                              [ "num_closes" <- nNc(nestFold(CS, I, N, nstate(NO, NC, FO, SO, LC, SLC))) ]
                              [ "first_open" <- nFo(nestFold(CS, I, N, nstate(NO, NC, FO, SO, LC, SLC))) ]
                              [ "second_open" <- nSo(nestFold(CS, I, N, nstate(NO, NC, FO, SO, LC, SLC))) ]
                              [ "last_close" <- nLc(nestFold(CS, I, N, nstate(NO, NC, FO, SO, LC, SLC))) ]
                              [ "second_last_close" <- nSlc(nestFold(CS, I, N, nstate(NO, NC, FO, SO, LC, SLC))) ]
                              [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool N ==Int isLen(CS) andBool NO >=Int 0
    [all-path]

  // ---- Entry claim — result = is_nested(str(CS)) == isNestedRes(CS). The 6 scalars init (0,0,-1,-1,
  // -1,-1); the loop folds them to isNestState(CS); the Return conjunction is isNestedRes(CS).
  claim
    <k>
      FuncDef("is_nested", Params("string"),
        Assign(Name("num_opens"), Int(0))
        Assign(Name("num_closes"), Int(0))
        Assign(Name("first_open"), UnaryOp("-", Int(1)))
        Assign(Name("second_open"), UnaryOp("-", Int(1)))
        Assign(Name("last_close"), UnaryOp("-", Int(1)))
        Assign(Name("second_last_close"), UnaryOp("-", Int(1)))
        Assign(Name("i"), Int(0))
        For(Name("i"), Call(Name("range"), Call(Name("len"), Name("string"))),
          If(Compare(Subscript(Name("string"), Name("i")), CmpOp("==", Str("["))),
            Assign(Name("num_opens"), BinOp("+", Name("num_opens"), Int(1)))
            If(Compare(Name("num_opens"), CmpOp("==", Int(1))), Assign(Name("first_open"), Name("i")), .Stmts)
            If(Compare(Name("num_opens"), CmpOp("==", Int(2))), Assign(Name("second_open"), Name("i")), .Stmts),
            Assign(Name("num_closes"), BinOp("+", Name("num_closes"), Int(1)))
            Assign(Name("second_last_close"), Name("last_close"))
            Assign(Name("last_close"), Name("i"))))
        Return(BoolOp("and",
          Compare(Name("num_opens"), CmpOp(">=", Int(2))),
          Compare(Name("num_closes"), CmpOp(">=", Int(2))),
          Compare(Name("first_open"), CmpOp("<", Name("last_close"))),
          Compare(Name("second_open"), CmpOp("<", Name("second_last_close"))))))
      Assign(Name("result"), Call(Name("is_nested"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_nested" <- ?_:Val ] [ "result" <- isNestedRes(CS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
