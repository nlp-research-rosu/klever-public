// spec.k — split_words on the UNIFIED semantics, TRAP-FREE (P125). Count-branch
// loop invariant over the REAL inline body + one entry claim per branch of the
// 3-way (the membership atoms are irreducible, so each claim carries its branch
// premise; the split branches return heap refs, the count branch an Int).
//
//   kompile verification.k --backend haskell --main-module SPLIT-WORDS-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module SPLIT-WORDS-SPEC

requires "verification.k"

module SPLIT-WORDS-SPEC
  imports SPLIT-WORDS-VERIFICATION

  // ---- COUNT loop invariant — the real inline body; per-char atoms reduce to
  // isLowerC(atI(CS,I)) / pyMod(atI(CS,I),2)==0 and the fold case-splits.
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        If(BoolOp("and",
            Call(Attribute(Subscript(Name("txt"), Name("i")), "islower"), .Exprs),
            Compare(BinOp("%", Call(Name("ord"), Subscript(Name("txt"), Name("i"))), Int(2)),
              CmpOp("==", Int(0)))),
          Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
          .Stmts))
    => .K ... </k>
    <env> L0:Int </env>
    <scopes>
      ... -1 |-> builtinsScope
          GLB |-> scope(.Map [ "split_words" <- FB0:Val ], parent(-1))
          L0 |-> ( scope(.Map [ "txt" <- str(CS:IntSeq) ] [ "count" <- C:Int ] [ "i" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "txt" <- str(CS) ] [ "count" <- evenLowerCount(str(CS), I, N, C) ] [ "i" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool N ==Int isLen(CS)
    [all-path]

  // ---- entry (whitespace-split branch)
  claim
    <k>
      FuncDef("split_words", Params("txt"),
        If(Compare(Str(" "), CmpOp("in", Name("txt"))),
          Return(Call(Attribute(Name("txt"), "split"), .Exprs)),
          If(Compare(Str(","), CmpOp("in", Name("txt"))),
            Return(Call(Attribute(Call(Attribute(Name("txt"), "replace"), Str(","), Str(" ")), "split"), .Exprs)),
            Assign(Name("count"), Int(0))
            Assign(Name("i"), Int(0))
            For(Name("i"), Call(Name("range"), Call(Name("len"), Name("txt"))),
              If(BoolOp("and",
                  Call(Attribute(Subscript(Name("txt"), Name("i")), "islower"), .Exprs),
                  Compare(BinOp("%", Call(Name("ord"), Subscript(Name("txt"), Name("i"))), Int(2)),
                    CmpOp("==", Int(0)))),
                Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
                .Stmts))
            Return(Name("count")))))
      Assign(Name("result"), Call(Name("split_words"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "split_words" <- ?_:Val ] [ "result" <- ref(?NW:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => (?NW |-> list(splitWS(CS, .IntSeq, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires strContains(iCons(32, .IntSeq), CS)
    [all-path]

  // ---- entry (comma-split branch)
  claim
    <k>
      FuncDef("split_words", Params("txt"),
        If(Compare(Str(" "), CmpOp("in", Name("txt"))),
          Return(Call(Attribute(Name("txt"), "split"), .Exprs)),
          If(Compare(Str(","), CmpOp("in", Name("txt"))),
            Return(Call(Attribute(Call(Attribute(Name("txt"), "replace"), Str(","), Str(" ")), "split"), .Exprs)),
            Assign(Name("count"), Int(0))
            Assign(Name("i"), Int(0))
            For(Name("i"), Call(Name("range"), Call(Name("len"), Name("txt"))),
              If(BoolOp("and",
                  Call(Attribute(Subscript(Name("txt"), Name("i")), "islower"), .Exprs),
                  Compare(BinOp("%", Call(Name("ord"), Subscript(Name("txt"), Name("i"))), Int(2)),
                    CmpOp("==", Int(0)))),
                Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
                .Stmts))
            Return(Name("count")))))
      Assign(Name("result"), Call(Name("split_words"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "split_words" <- ?_:Val ] [ "result" <- ref(?NC:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => (?NC |-> list(splitWS(replaceC(CS, 44, 32), .IntSeq, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool strContains(iCons(32, .IntSeq), CS)
     andBool strContains(iCons(44, .IntSeq), CS)
    [all-path]

  // ---- entry (count branch)
  claim
    <k>
      FuncDef("split_words", Params("txt"),
        If(Compare(Str(" "), CmpOp("in", Name("txt"))),
          Return(Call(Attribute(Name("txt"), "split"), .Exprs)),
          If(Compare(Str(","), CmpOp("in", Name("txt"))),
            Return(Call(Attribute(Call(Attribute(Name("txt"), "replace"), Str(","), Str(" ")), "split"), .Exprs)),
            Assign(Name("count"), Int(0))
            Assign(Name("i"), Int(0))
            For(Name("i"), Call(Name("range"), Call(Name("len"), Name("txt"))),
              If(BoolOp("and",
                  Call(Attribute(Subscript(Name("txt"), Name("i")), "islower"), .Exprs),
                  Compare(BinOp("%", Call(Name("ord"), Subscript(Name("txt"), Name("i"))), Int(2)),
                    CmpOp("==", Int(0)))),
                Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
                .Stmts))
            Return(Name("count")))))
      Assign(Name("result"), Call(Name("split_words"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "split_words" <- ?_:Val ] [ "result" <- evenLowerCount(str(CS), 0, isLen(CS), 0) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool strContains(iCons(32, .IntSeq), CS)
     andBool notBool strContains(iCons(44, .IntSeq), CS)
    [all-path]
endmodule
