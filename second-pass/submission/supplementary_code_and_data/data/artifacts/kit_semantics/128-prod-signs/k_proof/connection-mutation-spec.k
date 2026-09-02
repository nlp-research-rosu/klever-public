requires "connection.k"

module CONNECTION-MUTATION-SPEC
  imports CONNECTION

  // Deliberately false opposite interpretation of the first represented
  // element: fixed iteration must yield 4, not 5.
  claim [typed-iterator-wrong-value]:
    <k>
      #iterNext(list(intVals(iCons(4, .IntSeq))))
      ~> #loopStep(TARGET:Expr, BODY:Stmts)
      ~> CONT:K
      =>
      #iterYield(5, list(intVals(.IntSeq)))
      ~> #loopStep(TARGET, BODY)
      ~> CONT
    </k>
endmodule
