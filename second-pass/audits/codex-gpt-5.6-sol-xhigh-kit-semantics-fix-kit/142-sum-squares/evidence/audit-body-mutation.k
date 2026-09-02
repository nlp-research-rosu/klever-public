requires "verification.k"

module AUDIT-BODY-MUTATION
  imports VERIFICATION

  // Reviewer-authored sensitivity probe: the index-4 branch squares instead
  // of cubes. On five 2s this body returns 16, not the original result 20.
  claim [mutated-cube-branch]:
    <k>
      FuncDef(
        "sum_squares",
        Params("lst"),
        Assign(Name("total"), Int(0))
        Assign(Name("index"), Int(0))
        Assign(Name("value"), Int(0))
        For(
          Name("value"),
          Name("lst"),
          If(
            Compare(BinOp("%", Name("index"), Int(3)), CmpOp("==", Int(0))),
            AugAssign(
              Name("total"),
              "+",
              BinOp("*", Name("value"), Name("value"))),
            If(
              Compare(BinOp("%", Name("index"), Int(4)), CmpOp("==", Int(0))),
              AugAssign(
                Name("total"),
                "+",
                BinOp("*", Name("value"), Name("value"))),
              AugAssign(Name("total"), "+", Name("value"))))
          AugAssign(Name("index"), "+", Int(1)))
        Return(Name("total")))
      ~> Call(
           Name("sum_squares"),
           list(valsOf(
             intCons(2,
               intCons(2,
                 intCons(2,
                   intCons(2,
                     intCons(2, .IntList))))))))
      => 20
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope) => ?SC:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
