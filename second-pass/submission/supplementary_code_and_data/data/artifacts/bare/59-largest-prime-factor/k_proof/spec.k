requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop invariant/refinement: at any positive residual N and candidate F,
  // executing the translated loop and return computes the pure lpfSpec value.
  claim [loop-refines-lpf]:
    <py>
      <k> execStmt(factorLoop) ~> exec(Return(Name("n")) .Stmts)
        => .K </k>
      <input> _INPUT </input>
      <env> "factor" |-> F "n" |-> N
        => "factor" |-> ?_:Int "n" |-> lpfSpec(N, F) </env>
      <result> noResult => result(lpfSpec(N, F)) </result>
    </py>
    requires N >Int 1 andBool F >=Int 2

  // Universal end-to-end theorem.  This is stronger than the prompt's domain:
  // it holds for every N > 1, including prime inputs.
  claim [largest-prime-factor-correct]:
    <py>
      <k> solutionModule => .K </k>
      <input> N </input>
      <env> .Map
        => "factor" |-> ?_:Int "n" |-> lpfSpec(N, 2) </env>
      <result> noResult => result(lpfSpec(N, 2)) </result>
    </py>
    requires N >Int 1

  claim [prompt-example-13195]:
    <py>
      <k> solutionModule => .K </k>
      <input> 13195 </input>
      <env> .Map => ?_:Map </env>
      <result> noResult => result(29) </result>
    </py>

  claim [prompt-example-2048]:
    <py>
      <k> solutionModule => .K </k>
      <input> 2048 </input>
      <env> .Map => ?_:Map </env>
      <result> noResult => result(2) </result>
    </py>
endmodule
