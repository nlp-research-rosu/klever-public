requires "verification.k"

module SPEC-AUDIT-LABELED
  imports MPY-VERIFICATION

  claim [universal]:
    <k> solutionProgram => .K </k>
    <input> ListExpr(PStr(A), PStr(B)) </input>
    <env> .Map </env>
    <functions> .Map => ?_M1:Map </functions>
    <result> noResult => strVal(contractAnswer(A, B)) </result>

  claim [prompt-yes]:
    <k> solutionProgram => .K </k>
    <input> ListExpr(Str("()(") , Str(")")) </input>
    <env> .Map </env>
    <functions> .Map => ?_M2:Map </functions>
    <result> noResult => strVal(yesString) </result>

  claim [prompt-no]:
    <k> solutionProgram => .K </k>
    <input> ListExpr(Str(")"), Str(")")) </input>
    <env> .Map </env>
    <functions> .Map => ?_M3:Map </functions>
    <result> noResult => strVal(noString) </result>
endmodule
