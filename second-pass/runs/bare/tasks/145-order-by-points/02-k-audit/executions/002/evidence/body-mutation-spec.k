requires "body-mutation.k"

module BODY-MUTATION-SPEC
  imports BODY-MUTATION

  claim [label(mutated-prompt-result)]:
        <py>
          <k> init => .K </k>
          <program> mutatedProgram </program>
          <input>
            ListExpr(Int(1), Int(11), Int(-1), Int(-11), Int(-12))
          </input>
          <output>
            NoValue =>
            ListVal(IntVal(-1), IntVal(-11), IntVal(1), IntVal(-12), IntVal(11))
          </output>
        </py>
endmodule
