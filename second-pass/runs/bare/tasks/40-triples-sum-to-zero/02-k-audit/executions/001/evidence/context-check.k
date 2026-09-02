requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CONTEXT-CHECK
  imports VERIFICATION

  claim [pair-observable-continuation]:
    <mpy>
      <k>
        invoke2(
          "_has_pair_sum",
          VInt(1),
          VList(1 ; -2 ; .Ints))
        ~> finish
        => .K
      </k>
      <funs> solutionFunctions </funs>
      <env> .Map </env>
      <input> VList(.Ints) </input>
      <result>
        noResult => result(VBool(true))
      </result>
    </mpy>

  claim [entry-observable-continuation]:
    <mpy>
      <k>
        invoke1(
          "triples_sum_to_zero",
          VList(1 ; 1 ; -2 ; .Ints))
        ~> finish
        => .K
      </k>
      <funs> solutionFunctions </funs>
      <env> .Map </env>
      <input> VList(.Ints) </input>
      <result>
        noResult => result(VBool(true))
      </result>
    </mpy>
endmodule
