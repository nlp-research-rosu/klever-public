requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports MPY-VERIFICATION

  // Deliberately false: both trusted Python implementations return "Yes" for
  // ["()(", ")"], while this claim requires the result to be "No".
  claim
    <k> solutionProgram => .K </k>
    <input> ListExpr(Str("()("), Str(")")) </input>
    <env> .Map </env>
    <functions> .Map => ?_M:Map </functions>
    <result> noResult => strVal(noString) </result>
endmodule
