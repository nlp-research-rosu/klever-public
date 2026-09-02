requires "verification.k"

module SPEC-AUDIT
  imports VERIFICATION

  claim [loop-audit]:
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

  claim [entry-audit]:
    <py>
      <k> solutionProgram => .K </k>
      <input> pyList(VS) </input>
      <lst> noValue </lst>
      <total> pyInt(0) </total>
      <value> pyInt(0) </value>
      <function> noFunction </function>
      <result> noResult => pyInt(oddSquareFold(VS, 0)) </result>
    </py>
endmodule
