requires "verification.k"

module SPEC-UNIVERSAL-AUDIT
  imports VERIFICATION

  // Auditor scope probe corresponding to the theorem the ground examples
  // would need to generalize to for arbitrary nonempty modeled key sequences.
  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(KEYS:Values) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(KEYS))) </result>
    </task>
endmodule
