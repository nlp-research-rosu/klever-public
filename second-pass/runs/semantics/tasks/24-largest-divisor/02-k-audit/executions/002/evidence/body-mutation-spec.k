requires "spec.k"

module BODY-MUTATION-SPEC
  imports LOOP-SPEC

  // Operational-sensitivity probe: the submitted return is changed from
  // `divisor` to `divisor + 1`, while the expected result for n=15 stays 5.
  // The real mutated body must execute and produce 6.
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
            Return(BinOp("+", Name("divisor"), Int(1))))))
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
            Return(BinOp("+", Name("divisor"), Int(1))),
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
    [label(mutatedBodyMustNotProveOriginalResult)]
endmodule
