requires "verification-no-bridges.k"

module SPEC-NO-BRIDGES
  imports MPY-VERIFICATION

  // Full contract: for arbitrary strings over the promised alphabet, return
  // Yes exactly when at least one concatenation is balanced.
  claim
    <k> solutionProgram => .K </k>
    <input> ListExpr(PStr(A), PStr(B)) </input>
    <env> .Map </env>
    <functions> .Map => ?_M1:Map </functions>
    <result> noResult => strVal(contractAnswer(A, B)) </result>

  // The two examples from prompt.py are also included as closed claims.
  claim
    <k> solutionProgram => .K </k>
    <input> ListExpr(Str("()(") , Str(")")) </input>
    <env> .Map </env>
    <functions> .Map => ?_M2:Map </functions>
    <result> noResult => strVal(yesString) </result>

  claim
    <k> solutionProgram => .K </k>
    <input> ListExpr(Str(")"), Str(")")) </input>
    <env> .Map </env>
    <functions> .Map => ?_M3:Map </functions>
    <result> noResult => strVal(noString) </result>
endmodule
