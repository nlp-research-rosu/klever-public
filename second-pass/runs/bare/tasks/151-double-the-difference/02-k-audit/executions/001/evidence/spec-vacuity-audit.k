requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Keep the genuine loop helper so the entry reaches its result obligation.
  claim [loop-helper]:
    <py>
      <k>
        loop("value", pyList(VS), loopBody)
        ~> Return(Name("total")) .Stmts
        => .K
      </k>
      <input> _INPUT:Val </input>
      <lst> _L:Val => noValue </lst>
      <total> pyInt(ACC) => pyInt(0) </total>
      <value> _OLD:Val => pyInt(0) </value>
      <function> _FUN:Function => noFunction </function>
      <result> noResult => pyInt(oddSquareFold(VS, ACC)) </result>
    </py>

  // Fresh false mutation: require one more than the real returned result.
  // The precondition is satisfiable, for example VS = nil, where 0 != 1.
  claim [false-entry-result]:
    <py>
      <k> solutionProgram => .K </k>
      <input> pyList(VS) </input>
      <lst> noValue </lst>
      <total> pyInt(0) </total>
      <value> pyInt(0) </value>
      <function> noFunction </function>
      <result>
        noResult => pyInt(oddSquareFold(VS, 0) +Int 1)
      </result>
    </py>
endmodule
