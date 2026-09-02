requires "verification.k"

module SPEC-WITNESS
  imports VERIFICATION

  // Ground witness for the universal entry precondition N > 1.
  claim [entry-n4]:
    <py>
      <k> solutionModule => .K </k>
      <input> 4 </input>
      <env> .Map => "factor" |-> 2 "n" |-> 2 </env>
      <result> noResult => result(2) </result>
    </py>

  // Ground witness for the loop precondition N > 1 and F >= 2.
  claim [loop-n4-f2]:
    <py>
      <k> execStmt(factorLoop) ~> exec(Return(Name("n")) .Stmts)
        => .K </k>
      <input> 4 </input>
      <env> "factor" |-> 2 "n" |-> 4
        => "factor" |-> 2 "n" |-> 2 </env>
      <result> noResult => result(2) </result>
    </py>
endmodule
