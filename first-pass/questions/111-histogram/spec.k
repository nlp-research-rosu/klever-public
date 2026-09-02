// spec.k — histogram, TRAP-FREE (P111). Element-loop invariants over the
// heap-ref'd split list (fixed-ref heap shape; the body reads list1.count(i)
// through the ref each iteration); the value dict folds via dictSet. Closed-
// frame pairs; entry over the real single FuncDef.
//
//   kompile verification.k --backend haskell --main-module HISTOGRAM-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module HISTOGRAM-SPEC

requires "verification.k"

module HISTOGRAM-SPEC
  imports HISTOGRAM-VERIFICATION

  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        If(BoolOp("and",
            Compare(Call(Attribute(Name("list1"), "count"), Name("i")), CmpOp(">", Name("t"))),
            Compare(Name("i"), CmpOp("!=", Str("")))),
          Assign(Name("t"), Call(Attribute(Name("list1"), "count"), Name("i"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "histogram" <- HGV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "test" <- TV:Val ] [ "dict1" <- D:Val ] [ "list1" <- ref(LR:Int) ] [ "t" <- T:Int ], parent(0))
           => scope(.Map [ "test" <- TV ] [ "dict1" <- D ] [ "list1" <- ref(LR) ]
                [ "t" <- maxCnt(VS, FULL, T) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(FULL:ValSeq)) HREST:Map
        => (LR |-> list(FULL)) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool isRefV(D)
     andBool notBool (VS ==K .ValSeq)
     andBool allStr(VS) andBool allStr(FULL)
    [all-path]

  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        If(BoolOp("and",
            Compare(Call(Attribute(Name("list1"), "count"), Name("i")), CmpOp(">", Name("t"))),
            Compare(Name("i"), CmpOp("!=", Str("")))),
          Assign(Name("t"), Call(Attribute(Name("list1"), "count"), Name("i"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "histogram" <- HGV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "test" <- TV:Val ] [ "dict1" <- D:Val ] [ "list1" <- ref(LR:Int) ] [ "t" <- T:Int ] [ "i" <- _:Val ], parent(0))
           => scope(.Map [ "test" <- TV ] [ "dict1" <- D ] [ "list1" <- ref(LR) ]
                [ "t" <- maxCnt(VS, FULL, T) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(FULL:ValSeq)) HREST:Map
        => (LR |-> list(FULL)) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool isRefV(D)
     andBool allStr(VS) andBool allStr(FULL)
    [all-path]

  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        If(Compare(Call(Attribute(Name("list1"), "count"), Name("i")), CmpOp("==", Name("t"))),
          Assign(Subscript(Name("dict1"), Name("i")), Name("t")),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "histogram" <- HGV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "test" <- TV:Val ] [ "dict1" <- dictV(DKS:ValSeq, DVS:ValSeq) ] [ "list1" <- ref(LR:Int) ] [ "t" <- T:Int ] [ "i" <- _:Val ], parent(0))
           => scope(.Map [ "test" <- TV ] [ "dict1" <- buildD(VS, FULL, T, dictV(DKS, DVS)) ] [ "list1" <- ref(LR) ]
                [ "t" <- T ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(FULL:ValSeq)) HREST:Map
        => (LR |-> list(FULL)) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS) andBool allStr(FULL)
    [all-path]

  // ---- entry (some non-empty word): result == buildD over the split at the max count.
  // Deciding premise spelled as the executed If(t > 0) atom.
  claim
    <k>
      FuncDef("histogram", Params("test"),
        Assign(Name("dict1"), DictExpr(.Entries))
        Assign(Name("list1"), Call(Attribute(Name("test"), "split"), Str(" ")))
        Assign(Name("t"), Int(0))
        For(Name("i"), Name("list1"),
          If(BoolOp("and",
            Compare(Call(Attribute(Name("list1"), "count"), Name("i")), CmpOp(">", Name("t"))),
            Compare(Name("i"), CmpOp("!=", Str("")))),
          Assign(Name("t"), Call(Attribute(Name("list1"), "count"), Name("i"))),
          .Stmts))
        If(Compare(Name("t"), CmpOp(">", Int(0))),
          For(Name("i"), Name("list1"),
            If(Compare(Call(Attribute(Name("list1"), "count"), Name("i")), CmpOp("==", Name("t"))),
          Assign(Subscript(Name("dict1"), Name("i")), Name("t")),
          .Stmts)),
          .Stmts)
        Return(Name("dict1")))
      Assign(Name("result"), Call(Name("histogram"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "histogram" <- ?_:Val ] [ "result" <-
          buildD(splitSep(CS, 32, .IntSeq), splitSep(CS, 32, .IntSeq),
            maxCnt(splitSep(CS, 32, .IntSeq), splitSep(CS, 32, .IntSeq), 0), dictV(.ValSeq, .ValSeq)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires maxCnt(splitSep(CS, 32, .IntSeq), splitSep(CS, 32, .IntSeq), 0) >Int 0
    [all-path]

  // ---- entry (all-empty split): result == the empty dict, complementary premise.
  claim
    <k>
      FuncDef("histogram", Params("test"),
        Assign(Name("dict1"), DictExpr(.Entries))
        Assign(Name("list1"), Call(Attribute(Name("test"), "split"), Str(" ")))
        Assign(Name("t"), Int(0))
        For(Name("i"), Name("list1"),
          If(BoolOp("and",
            Compare(Call(Attribute(Name("list1"), "count"), Name("i")), CmpOp(">", Name("t"))),
            Compare(Name("i"), CmpOp("!=", Str("")))),
          Assign(Name("t"), Call(Attribute(Name("list1"), "count"), Name("i"))),
          .Stmts))
        If(Compare(Name("t"), CmpOp(">", Int(0))),
          For(Name("i"), Name("list1"),
            If(Compare(Call(Attribute(Name("list1"), "count"), Name("i")), CmpOp("==", Name("t"))),
          Assign(Subscript(Name("dict1"), Name("i")), Name("t")),
          .Stmts)),
          .Stmts)
        Return(Name("dict1")))
      Assign(Name("result"), Call(Name("histogram"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "histogram" <- ?_:Val ] [ "result" <- dictV(.ValSeq, .ValSeq) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool (maxCnt(splitSep(CS, 32, .IntSeq), splitSep(CS, 32, .IntSeq), 0) >Int 0)
    [all-path]
endmodule
