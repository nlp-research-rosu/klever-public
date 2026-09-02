requires "verification.k"

module SPEC-VACUITY-AUDITOR
  imports VERIFICATION

  // Fresh false result mutation. The initial state is satisfiable and the
  // actual/canonical result for ("C", ["Zz"]) is "C.Zz", not "C.WRONG".
  claim [wrong-singleton-result]:
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> "C" </inputClass>
      <inputExtensions> strVal("Zz") </inputExtensions>
      <result> noResult => returned(strVal("C.WRONG")) </result>
    </py>
endmodule
