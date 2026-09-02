requires "verification.k"

module SPEC-VACUITY
  imports MPY-VERIFICATION

  // Deliberately false: two arbitrary parenthesis strings do not always
  // admit a balanced concatenation.  Witness A = rp .PString,
  // B = rp .PString must produce noString, not yesString.
  claim
    <k> solutionProgram => .K </k>
    <input> ListExpr(PStr(A), PStr(B)) </input>
    <env> .Map </env>
    <functions> .Map => ?_M:Map </functions>
    <result> noResult => strVal(yesString) </result>
endmodule
