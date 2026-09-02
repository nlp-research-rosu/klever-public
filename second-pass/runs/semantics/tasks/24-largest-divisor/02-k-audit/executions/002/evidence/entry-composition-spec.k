requires "spec.k"

module ENTRY-COMPOSITION-SPEC
  imports LOOP-SPEC

  // Reviewer-only transitive-composition check.  The function body below is
  // the constructor sequence regenerated from solution.py, written explicitly
  // rather than through largestDivisorBody().
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "largest_divisor",
            Params("n"),
            Expr(
              Str(
                "Return the largest positive divisor of n that is smaller than n."))
            Assign(Name("divisor"), BinOp("-", Name("n"), Int(1)))
            While(
              Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("!=", Int(0))),
              AugAssign(Name("divisor"), "-", Int(1)))
            Return(Name("divisor")))))
      ~> Call(Name("largest_divisor"), Int(N))
      =>
      firstDivisorAtOrBelow(N, N -Int 1) ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "largest_divisor" |->
          closureVal(
            "n",
            Expr(
              Str(
                "Return the largest positive divisor of n that is smaller than n."))
            Assign(Name("divisor"), BinOp("-", Name("n"), Int(1)))
            While(
              Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("!=", Int(0))),
              AugAssign(Name("divisor"), "-", Int(1)))
            Return(Name("divisor")),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 1
    [label(exactEntryComposes)]
endmodule

module GROUND-ENTRY-SPEC
  imports LOOP-SPEC

  // Satisfiable entry-state witnesses with known, distinct results.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "largest_divisor",
            Params("n"),
            Expr(
              Str(
                "Return the largest positive divisor of n that is smaller than n."))
            Assign(Name("divisor"), BinOp("-", Name("n"), Int(1)))
            While(
              Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("!=", Int(0))),
              AugAssign(Name("divisor"), "-", Int(1)))
            Return(Name("divisor")))))
      ~> Call(Name("largest_divisor"), Int(15))
      =>
      5 ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "largest_divisor" |->
          closureVal(
            "n",
            Expr(
              Str(
                "Return the largest positive divisor of n that is smaller than n."))
            Assign(Name("divisor"), BinOp("-", Name("n"), Int(1)))
            While(
              Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("!=", Int(0))),
              AugAssign(Name("divisor"), "-", Int(1)))
            Return(Name("divisor")),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(groundComposite)]

  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "largest_divisor",
            Params("n"),
            Expr(
              Str(
                "Return the largest positive divisor of n that is smaller than n."))
            Assign(Name("divisor"), BinOp("-", Name("n"), Int(1)))
            While(
              Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("!=", Int(0))),
              AugAssign(Name("divisor"), "-", Int(1)))
            Return(Name("divisor")))))
      ~> Call(Name("largest_divisor"), Int(101))
      =>
      1 ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "largest_divisor" |->
          closureVal(
            "n",
            Expr(
              Str(
                "Return the largest positive divisor of n that is smaller than n."))
            Assign(Name("divisor"), BinOp("-", Name("n"), Int(1)))
            While(
              Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("!=", Int(0))),
              AugAssign(Name("divisor"), "-", Int(1)))
            Return(Name("divisor")),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(groundPrime)]
endmodule
