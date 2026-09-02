requires "verification.k"

module SPEC-VACUITY-SYMBOLIC
  imports VERIFICATION

  // General loop invariant.  It applies to the literal loop in solution.mpy.
  // The bounds make I = N + 1 the unique exit state.
  claim
    <k>
      #while(Compare(Name("i"), CmpOp("<=", Name("n"))),
        AugAssign(Name("factorial"), "*", Name("i"))
        AugAssign(Name("total"), "+", Name("i"))
        If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
          Expr(Call(Attribute(Name("result"), "append"), Name("factorial"))),
          Expr(Call(Attribute(Name("result"), "append"), Name("total"))))
        AugAssign(Name("i"), "+", Int(1)))
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(MODULE:Map, parent(-1))
      1 |-> scope(
        "factorial" |-> (F:Int => ?FINALF:Int)
        "i"         |-> (I:Int => N +Int 1)
        "n"         |-> N:Int
        "result"    |-> ref(0)
        "total"     |-> (T:Int => ?FINALT:Int),
        parent(0))
    </scopes>
    <heap>
      0 |-> (list(PREFIX:ValSeq)
        => list(valSeqConcat(PREFIX, ?OUTPUT:ValSeq)))
    </heap>
    requires 1 <=Int I andBool I <=Int N +Int 1
    ensures outputOK(?OUTPUT, I, N, F, T)
    [label(loop-correct)]

  // Complete symbolic call.  prove.sh first proves loop-correct, then makes
  // that proved invariant available as a lemma while proving this claim.
  claim
    <k> Call(Name("f"), Int(N)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "f" |-> closureVal("n", .ParamNames,
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("factorial"), Int(1))
          Assign(Name("total"), Int(0))
          Assign(Name("i"), Int(1))
          While(Compare(Name("i"), CmpOp("<=", Name("n"))),
            AugAssign(Name("factorial"), "*", Name("i"))
            AugAssign(Name("total"), "+", Name("i"))
            If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
              Expr(Call(Attribute(Name("result"), "append"), Name("factorial"))),
              Expr(Call(Attribute(Name("result"), "append"), Name("total"))))
            AugAssign(Name("i"), "+", Int(1)))
          Return(Name("result")), 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(?OUTPUT:ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    requires N >=Int 0
    ensures outputOK(?OUTPUT, 1, N, 1, 1)
    [label(f-symbolic-false-total)]

  // End-to-end base case: evaluate the actual f closure on n = 0.
  claim
    <k> Call(Name("f"), Int(0)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "f" |-> closureVal("n", .ParamNames,
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("factorial"), Int(1))
          Assign(Name("total"), Int(0))
          Assign(Name("i"), Int(1))
          While(Compare(Name("i"), CmpOp("<=", Name("n"))),
            AugAssign(Name("factorial"), "*", Name("i"))
            AugAssign(Name("total"), "+", Name("i"))
            If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
              Expr(Call(Attribute(Name("result"), "append"), Name("factorial"))),
              Expr(Call(Attribute(Name("result"), "append"), Name("total"))))
            AugAssign(Name("i"), "+", Int(1)))
          Return(Name("result")), 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    requires true
    [label(f-zero)]

  // End-to-end prompt example.
  claim
    <k> Call(Name("f"), Int(5)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "f" |-> closureVal("n", .ParamNames,
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("factorial"), Int(1))
          Assign(Name("total"), Int(0))
          Assign(Name("i"), Int(1))
          While(Compare(Name("i"), CmpOp("<=", Name("n"))),
            AugAssign(Name("factorial"), "*", Name("i"))
            AugAssign(Name("total"), "+", Name("i"))
            If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
              Expr(Call(Attribute(Name("result"), "append"), Name("factorial"))),
              Expr(Call(Attribute(Name("result"), "append"), Name("total"))))
            AugAssign(Name("i"), "+", Int(1)))
          Return(Name("result")), 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
        vCons(1, vCons(2, vCons(6, vCons(24, vCons(15, .ValSeq))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    requires true
    [label(f-five)]
endmodule
