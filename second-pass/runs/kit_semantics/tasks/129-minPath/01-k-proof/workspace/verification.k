requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // -----------------------------------------------------------------------
  // A row-major mathematical representation of every valid input grid.
  // The [concrete] equations give the selectors a fixed denotation without
  // forcing symbolic P or N to unroll during proof.
  // -----------------------------------------------------------------------

  syntax Bool ::= intMember(Int, IntSeq) [function, total]
  rule intMember(_:Int, .IntSeq) => false
  rule intMember(X:Int, iCons(Y:Int, R:IntSeq))
    => (X ==Int Y) orBool intMember(X, R)

  syntax Bool ::= allInRange(IntSeq, Int) [function, total]
  rule allInRange(.IntSeq, _:Int) => true
  rule allInRange(iCons(X:Int, R:IntSeq), M:Int)
    => (1 <=Int X andBool X <=Int M) andBool allInRange(R, M)

  syntax Bool ::= uniqueInts(IntSeq) [function, total]
  rule uniqueInts(.IntSeq) => true
  rule uniqueInts(iCons(X:Int, R:IntSeq))
    => notBool intMember(X, R) andBool uniqueInts(R)

  syntax Bool ::= validPerm(IntSeq, Int)
    [function, total, symbol(validPerm), no-evaluators]
  rule validPerm(P:IntSeq, M:Int)
    => (isLen(P) ==Int M) andBool allInRange(P, M) andBool uniqueInts(P)
    [concrete]

  syntax ValSeq ::= gridRows(IntSeq, Int)
    [function, total, symbol(gridRows), no-evaluators]
  syntax ValSeq ::= gridRowsFrom(IntSeq, Int, Int)
    [function, total, symbol(gridRowsFrom), no-evaluators]
  syntax ValSeq ::= gridRow(IntSeq, Int, Int)
    [function, total, symbol(gridRow), no-evaluators]
  syntax ValSeq ::= gridRowFrom(IntSeq, Int, Int, Int)
    [function, total, symbol(gridRowFrom), no-evaluators]

  syntax Int ::= pAtTotal(IntSeq, Int) [function, total]
  rule pAtTotal(.IntSeq, _:Int) => 0
  rule pAtTotal(iCons(X:Int, _:IntSeq), 0) => X
  rule pAtTotal(iCons(_:Int, R:IntSeq), I:Int) => pAtTotal(R, I -Int 1)
    requires I >Int 0
  rule pAtTotal(iCons(_:Int, _:IntSeq), I:Int) => 0
    requires I <Int 0

  rule gridRows(P:IntSeq, N:Int) => gridRowsFrom(P, N, 0) [concrete]
  rule gridRowsFrom(_:IntSeq, N:Int, I:Int) => .ValSeq
    requires I >=Int N
    [concrete]
  rule gridRowsFrom(P:IntSeq, N:Int, I:Int)
    => vCons(list(gridRow(P, N, I)), gridRowsFrom(P, N, I +Int 1))
    requires I <Int N
    [concrete]

  rule gridRow(P:IntSeq, N:Int, I:Int) => gridRowFrom(P, N, I, 0)
    [concrete]
  rule gridRowFrom(_:IntSeq, N:Int, _:Int, J:Int) => .ValSeq
    requires J >=Int N
    [concrete]
  rule gridRowFrom(P:IntSeq, N:Int, I:Int, J:Int)
    => vCons(pAtTotal(P, I *Int N +Int J),
             gridRowFrom(P, N, I, J +Int 1))
    requires J <Int N
    [concrete]

  syntax Int ::= gridAt(IntSeq, Int, Int, Int)
    [function, total, symbol(gridAt), no-evaluators]
  rule gridAt(P:IntSeq, N:Int, I:Int, J:Int)
    => pAtTotal(P, I *Int N +Int J)
    [concrete]

  syntax Int ::= findOne(IntSeq, Int) [function, total]
  rule findOne(.IntSeq, _:Int) => -1
  rule findOne(iCons(1, _:IntSeq), A:Int) => A
  rule findOne(iCons(X:Int, R:IntSeq), A:Int) => findOne(R, A +Int 1)
    requires X =/=Int 1

  syntax Int ::= oneIndex(IntSeq)
    [function, total, symbol(oneIndex), no-evaluators]
  rule oneIndex(P:IntSeq) => findOne(P, 0) [concrete]

  syntax Int ::= oneRow(IntSeq, Int)
    [function, total, symbol(oneRow), no-evaluators]
  syntax Int ::= oneCol(IntSeq, Int)
    [function, total, symbol(oneCol), no-evaluators]
  rule oneRow(P:IntSeq, N:Int) => oneIndex(P) /Int N
    requires N >Int 0
    [concrete]
  rule oneRow(_:IntSeq, N:Int) => 0
    requires N <=Int 0
    [concrete]
  rule oneCol(P:IntSeq, N:Int) => pyMod(oneIndex(P), N)
    requires N >Int 0
    [concrete]
  rule oneCol(_:IntSeq, N:Int) => 0
    requires N <=Int 0
    [concrete]

  // Guarded functional access lemmas.  They expose only the fixed grid
  // selectors at valid indices; Python's evaluation and control remain intact.
  rule vsLen(gridRows(P:IntSeq, N:Int)) => N
    requires N >=Int 2 andBool validPerm(P, N *Int N)
    [simplification]

  rule valSeqAt(gridRows(P:IntSeq, N:Int), I:Int)
    => list(gridRow(P, N, I))
    requires N >=Int 2 andBool validPerm(P, N *Int N)
      andBool I >=Int 0 andBool I <Int N
    [simplification]

  rule valSeqAt(gridRow(P:IntSeq, N:Int, I:Int), J:Int)
    => gridAt(P, N, I, J)
    requires N >=Int 2 andBool validPerm(P, N *Int N)
      andBool I >=Int 0 andBool I <Int N
      andBool J >=Int 0 andBool J <Int N
    [simplification]

  rule (gridAt(P:IntSeq, N:Int, I:Int, J:Int) ==Int 1)
    => (I ==Int oneRow(P, N) andBool J ==Int oneCol(P, N))
    requires N >=Int 2 andBool validPerm(P, N *Int N)
      andBool I >=Int 0 andBool I <Int N
      andBool J >=Int 0 andBool J <Int N
    [simplification]

  rule (gridAt(P:IntSeq, N:Int, I:Int, J:Int) <Int N *Int N +Int 1)
    => true
    requires N >=Int 2 andBool validPerm(P, N *Int N)
      andBool I >=Int 0 andBool I <Int N
      andBool J >=Int 0 andBool J <Int N
    [simplification]

  // -----------------------------------------------------------------------
  // Pure summaries used by the loop claims and final postcondition.
  // -----------------------------------------------------------------------

  syntax Int ::= chooseMin(Int, Int, Bool) [function, total]
  rule chooseMin(B:Int, _:Int, false) => B
  rule chooseMin(B:Int, V:Int, true) => V requires V <Int B
  rule chooseMin(B:Int, V:Int, true) => B requires V >=Int B

  syntax Int ::= bestUp(IntSeq, Int, Int, Int) [function, total]
  syntax Int ::= bestDown(IntSeq, Int, Int, Int) [function, total]
  syntax Int ::= bestLeft(IntSeq, Int, Int, Int) [function, total]
  syntax Int ::= neighborMin(IntSeq, Int, Int, Int)
    [function, total, symbol(neighborMin), no-evaluators]

  syntax Int ::= afterUp(Int, IntSeq, Int, Int, Int) [function, total]
  syntax Int ::= afterDown(Int, IntSeq, Int, Int, Int) [function, total]
  syntax Int ::= afterLeft(Int, IntSeq, Int, Int, Int) [function, total]
  syntax Int ::= afterRight(Int, IntSeq, Int, Int, Int) [function, total]

  rule afterUp(B:Int, P:IntSeq, N:Int, R:Int, C:Int)
    => chooseMin(B, gridAt(P, N, R -Int 1, C), R >Int 0)
  rule afterDown(B:Int, P:IntSeq, N:Int, R:Int, C:Int)
    => chooseMin(B, gridAt(P, N, R +Int 1, C), R +Int 1 <Int N)
  rule afterLeft(B:Int, P:IntSeq, N:Int, R:Int, C:Int)
    => chooseMin(B, gridAt(P, N, R, C -Int 1), C >Int 0)
  rule afterRight(B:Int, P:IntSeq, N:Int, R:Int, C:Int)
    => chooseMin(B, gridAt(P, N, R, C +Int 1), C +Int 1 <Int N)

  rule bestUp(P:IntSeq, N:Int, R:Int, C:Int)
    => afterUp(N *Int N +Int 1, P, N, R, C)
  rule bestDown(P:IntSeq, N:Int, R:Int, C:Int)
    => afterDown(bestUp(P, N, R, C), P, N, R, C)
  rule bestLeft(P:IntSeq, N:Int, R:Int, C:Int)
    => afterLeft(bestDown(P, N, R, C), P, N, R, C)
  // Definitional expansion of the four conditional minima.  This is a
  // functional data equation only: it exposes the same guarded selectors as
  // the source conditionals and never rewrites program control.
  rule neighborMin(P:IntSeq, N:Int, R:Int, C:Int)
    => chooseMin(
         chooseMin(
           chooseMin(
             chooseMin(N *Int N +Int 1,
                       gridAt(P, N, R -Int 1, C),
                       R >Int 0),
             gridAt(P, N, R +Int 1, C),
             R +Int 1 <Int N),
           gridAt(P, N, R, C -Int 1),
           C >Int 0),
         gridAt(P, N, R, C +Int 1),
         C +Int 1 <Int N)
    requires N >=Int 2 andBool validPerm(P, N *Int N)
      andBool R >=Int 0 andBool R <Int N
      andBool C >=Int 0 andBool C <Int N
    [simplification]

  // Structurally exact singleton append.  The simplification lemma below is
  // the functional selector for the symbolic-prefix access at list.append;
  // on concrete sequences its equations compute the identical ValSeq.
  syntax ValSeq ::= snocVS(ValSeq, Val)
    [function, total, symbol(snocVS), no-evaluators]
  rule snocVS(.ValSeq, V:Val) => vCons(V, .ValSeq) [simplification]
  rule snocVS(vCons(X:Val, R:ValSeq), V:Val)
    => vCons(X, snocVS(R, V))
    [concrete]

  // This is the only nonempty symbolic shape needed at the zero/one-pair
  // boundary.  Keeping the general recursive equation [concrete] prevents
  // case-splitting an opaque accumulated prefix during symbolic proof.
  rule snocVS(vCons(X:Val, .ValSeq), V:Val)
    => vCons(X, vCons(V, .ValSeq))
    [simplification]
  rule snocVS(vCons(X:Val, vCons(Y:Val, .ValSeq)), V:Val)
    => vCons(X, vCons(Y, vCons(V, .ValSeq)))
    [simplification]

  rule valSeqConcat(A:ValSeq, vCons(V:Val, .ValSeq)) => snocVS(A, V)
    [simplification]

  syntax Bool ::= pairDone(ValSeq, ValSeq, Int, Int)
    [function, total, symbol(pairDone), no-evaluators]
  rule pairDone(A:ValSeq, O:ValSeq, R:Int, _:Int) => A ==K O
    requires R <=Int 0
    [simplification]
  rule pairDone(A:ValSeq, O:ValSeq, R:Int, M:Int)
    => pairDone(snocVS(snocVS(A, 1), M), O, R -Int 1, M)
    requires R >Int 0
    [simplification]

  // Odd-length counterpart: R pairs followed by the final 1.
  syntax Bool ::= oddDone(ValSeq, ValSeq, Int, Int)
    [function, total, symbol(oddDone), no-evaluators]
  rule oddDone(A:ValSeq, O:ValSeq, R:Int, _:Int)
    => (O ==K snocVS(A, 1))
    requires R <=Int 0
    [simplification]
  rule oddDone(A:ValSeq, O:ValSeq, R:Int, M:Int)
    => oddDone(snocVS(snocVS(A, 1), M), O, R -Int 1, M)
    requires R >Int 0
    [simplification]

  // Appending the odd tail to a completed pair prefix connects the two exact
  // recursive relations without solving backward through a summary function.
  rule oddDone(A:ValSeq, snocVS(P:ValSeq, 1), R:Int, M:Int)
    => pairDone(A, P, R, M)
    requires R >=Int 0
    [simplification]

  syntax Bool ::= finishRel(ValSeq, ValSeq, Int, Int, Int)
    [function, total, symbol(finishRel), no-evaluators]
  // Both parity branches consume one completed pair in the same way.  This
  // guarded fold lets the generalized loop circularity retain the odd-tail
  // continuation without prematurely splitting on the symbolic parity of K.
  rule finishRel(A:ValSeq, O:ValSeq, R:Int, M:Int, K:Int)
    => finishRel(snocVS(snocVS(A, 1), M), O, R -Int 1, M, K)
    requires R >Int 0
    [simplification]
  rule finishRel(A:ValSeq, O:ValSeq, R:Int, M:Int, K:Int)
    => oddDone(A, O, R, M)
    requires R <=Int 0 andBool pyMod(K, 2) ==Int 1
    [simplification]
  rule finishRel(A:ValSeq, O:ValSeq, R:Int, M:Int, K:Int)
    => pairDone(A, O, R, M)
    requires R <=Int 0 andBool pyMod(K, 2) =/=Int 1
    [simplification]

  syntax Bool ::= pathRel(ValSeq, Int, Int)
    [function, total, symbol(pathRel), no-evaluators]
  rule pathRel(O:ValSeq, K:Int, M:Int)
    => finishRel(.ValSeq, O,
                 (K -Int pyMod(K, 2)) /Int 2, M, K)
    [simplification]

  // -----------------------------------------------------------------------
  // Exact AST abbreviations for solution.py.  These are syntax macros only.
  // -----------------------------------------------------------------------

  syntax Stmt ::= "innerLoop" [macro]
  rule innerLoop =>
    While(Compare(Name("j"), CmpOp("<", Name("n"))),
      If(Compare(Subscript(Subscript(Name("grid"), Name("i")), Name("j")),
                 CmpOp("==", Int(1))),
        Assign(Name("row"), Name("i"))
        Assign(Name("col"), Name("j")),
        .Stmts)
      Assign(Name("j"), BinOp("+", Name("j"), Int(1))))

  syntax KItem ::= "innerWhile" [macro]
  rule innerWhile =>
    #while(Compare(Name("j"), CmpOp("<", Name("n"))),
      If(Compare(Subscript(Subscript(Name("grid"), Name("i")), Name("j")),
                 CmpOp("==", Int(1))),
        Assign(Name("row"), Name("i"))
        Assign(Name("col"), Name("j")),
        .Stmts)
      Assign(Name("j"), BinOp("+", Name("j"), Int(1))))

  syntax Stmt ::= "outerLoop" [macro]
  rule outerLoop =>
    While(Compare(Name("i"), CmpOp("<", Name("n"))),
      Assign(Name("j"), Int(0))
      innerLoop
      Assign(Name("i"), BinOp("+", Name("i"), Int(1))))

  syntax KItem ::= "outerWhile" [macro]
  rule outerWhile =>
    #while(Compare(Name("i"), CmpOp("<", Name("n"))),
      Assign(Name("j"), Int(0))
      innerLoop
      Assign(Name("i"), BinOp("+", Name("i"), Int(1))))

  syntax Stmt ::= "upIf" [macro]
  rule upIf =>
    If(Compare(Name("row"), CmpOp(">", Int(0))),
      If(Compare(Subscript(Subscript(Name("grid"),
                                      BinOp("-", Name("row"), Int(1))),
                            Name("col")),
                 CmpOp("<", Name("neighbor"))),
        Assign(Name("neighbor"),
               Subscript(Subscript(Name("grid"),
                                   BinOp("-", Name("row"), Int(1))),
                         Name("col"))),
        .Stmts),
      .Stmts)

  syntax Stmt ::= "downIf" [macro]
  rule downIf =>
    If(Compare(BinOp("+", Name("row"), Int(1)), CmpOp("<", Name("n"))),
      If(Compare(Subscript(Subscript(Name("grid"),
                                      BinOp("+", Name("row"), Int(1))),
                            Name("col")),
                 CmpOp("<", Name("neighbor"))),
        Assign(Name("neighbor"),
               Subscript(Subscript(Name("grid"),
                                   BinOp("+", Name("row"), Int(1))),
                         Name("col"))),
        .Stmts),
      .Stmts)

  syntax Stmt ::= "leftIf" [macro]
  rule leftIf =>
    If(Compare(Name("col"), CmpOp(">", Int(0))),
      If(Compare(Subscript(Subscript(Name("grid"), Name("row")),
                            BinOp("-", Name("col"), Int(1))),
                 CmpOp("<", Name("neighbor"))),
        Assign(Name("neighbor"),
               Subscript(Subscript(Name("grid"), Name("row")),
                         BinOp("-", Name("col"), Int(1)))),
        .Stmts),
      .Stmts)

  syntax Stmt ::= "rightIf" [macro]
  rule rightIf =>
    If(Compare(BinOp("+", Name("col"), Int(1)), CmpOp("<", Name("n"))),
      If(Compare(Subscript(Subscript(Name("grid"), Name("row")),
                            BinOp("+", Name("col"), Int(1))),
                 CmpOp("<", Name("neighbor"))),
        Assign(Name("neighbor"),
               Subscript(Subscript(Name("grid"), Name("row")),
                         BinOp("+", Name("col"), Int(1)))),
        .Stmts),
      .Stmts)

  syntax Stmts ::= "neighborUpdates" [macro]
  rule neighborUpdates =>
    upIf
    downIf
    leftIf
    rightIf

  syntax Stmts ::= "resultBody" [macro]
  rule resultBody =>
    Expr(Call(Attribute(Name("result"), "append"), (Int(1), .Exprs)))
    Expr(Call(Attribute(Name("result"), "append"),
              (Name("neighbor"), .Exprs)))
    Assign(Name("pairs"), BinOp("-", Name("pairs"), Int(1)))

  syntax Stmt ::= "resultLoop" [macro]
  rule resultLoop =>
    While(Compare(Name("pairs"), CmpOp(">", Int(0))), resultBody)

  syntax KItem ::= "resultWhile" [macro]
  rule resultWhile =>
    #while(Compare(Name("pairs"), CmpOp(">", Int(0))), resultBody)

  syntax Stmt ::= "oddTail" [macro]
  rule oddTail =>
    If(Compare(BinOp("%", Name("k"), Int(2)), CmpOp("==", Int(1))),
      Expr(Call(Attribute(Name("result"), "append"), (Int(1), .Exprs))),
      .Stmts)

  syntax Stmts ::= "resultFinish" [macro]
  rule resultFinish =>
    resultLoop
    oddTail

  syntax Stmts ::= "minPathBody" [macro]
  rule minPathBody =>
    Assign(Name("n"), Call(Name("len"), (Name("grid"), .Exprs)))
    Assign(Name("row"), Int(0))
    Assign(Name("col"), Int(0))
    Assign(Name("i"), Int(0))
    outerLoop
    Assign(Name("neighbor"),
           BinOp("+", BinOp("*", Name("n"), Name("n")), Int(1)))
    upIf
    downIf
    leftIf
    rightIf
    Assign(Name("result"), ListExpr(.Exprs))
    Assign(Name("pairs"), BinOp("//", Name("k"), Int(2)))
    resultLoop
    oddTail
    Return(Name("result"))

endmodule
