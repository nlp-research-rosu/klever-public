// spec.k — sorted_list_sum, TRAP-FREE (P149). Even-length filter loop
// invariants (P67 template) + entry: lst arrives as a heap ref (the real
// in-place lst.sort()), the filter builds new_lst by real .append(), and the
// result is the SHARED opaque sortKeyVS keyed by the len builtin.
//
//   kompile verification.k --backend haskell --main-module SORTED-LIST-SUM-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module SORTED-LIST-SUM-SPEC

requires "verification.k"

module SORTED-LIST-SUM-SPEC
  imports SORTED-LIST-SUM-VERIFICATION

  // ---- filter-loop invariant, variant B (i bound; circularity) -------------
  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        If(Compare(BinOp("%", Call(Name("len"), Name("i")), Int(2)), CmpOp("==", Int(0))),
          Expr(Call(Attribute(Name("new_lst"), "append"), Name("i"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sorted_list_sum" <- SLSV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "lst" <- ref(LN:Int) ] [ "new_lst" <- ref(LR:Int) ] [ "i" <- _:Val ], parent(0))
           => scope(.Map [ "lst" <- ref(LN) ] [ "new_lst" <- ref(LR) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(ACC:ValSeq)) HREST:Map
        => (LR |-> list(evenFilt(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS) andBool LN =/=Int LR
    [all-path]

  // ---- filter-loop invariant, variant A (i unbound) -------------------------
  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        If(Compare(BinOp("%", Call(Name("len"), Name("i")), Int(2)), CmpOp("==", Int(0))),
          Expr(Call(Attribute(Name("new_lst"), "append"), Name("i"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sorted_list_sum" <- SLSV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "lst" <- ref(LN:Int) ] [ "new_lst" <- ref(LR:Int) ], parent(0))
           => scope(.Map [ "lst" <- ref(LN) ] [ "new_lst" <- ref(LR) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(ACC:ValSeq)) HREST:Map
        => (LR |-> list(evenFilt(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    // nonempty: the zero-iteration ending executes structurally (no claim),
    // so the post can pin i bound without an abstract map rest (which would
    // poison the later `sorted` lookup in this frame)
    requires allStr(VS) andBool LN =/=Int LR andBool notBool (VS ==K .ValSeq)
    [all-path]

  // ---- entry -----------------------------------------------------------------
  claim
    <k>
      FuncDef("sorted_list_sum", Params("lst"),
        Expr(Call(Attribute(Name("lst"), "sort"), .Exprs))
        Assign(Name("new_lst"), ListExpr(.Exprs))
        For(Name("i"), Name("lst"),
          If(Compare(BinOp("%", Call(Name("len"), Name("i")), Int(2)), CmpOp("==", Int(0))),
            Expr(Call(Attribute(Name("new_lst"), "append"), Name("i"))),
            .Stmts))
        Return(Call(Name("sorted"), Name("new_lst"), KwArg("key", Name("len")))))
      Assign(Name("result"), Call(Name("sorted_list_sum"), ref(0)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sorted_list_sum" <- ?_:Val ] [ "result" <- ref(?H2:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> (0 |-> list(VS:ValSeq))
        => (0 |-> list(sortVS(VS)))
           (?H2 |-> list(sortKeyVS(evenFilt(sortVS(VS), .ValSeq), builtinV("len")))) ?_:Map </heap>
    <heapLoc> 1 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
    [all-path]
endmodule
