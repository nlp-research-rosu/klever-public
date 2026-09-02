requires "verification.k"

module SPEC-UNICODE-WITNESS
  imports VERIFICATION

  // Auditor witness for the generated semantics' non-ASCII mismatch:
  // the K model computes false, whereas CPython "é".islower() is true.
  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("é")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(false) </result>
    </task>
endmodule
