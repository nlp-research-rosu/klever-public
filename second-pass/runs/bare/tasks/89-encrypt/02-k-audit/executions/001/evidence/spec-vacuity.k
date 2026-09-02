requires "semantic.k"

module SPEC-VACUITY
  imports MPY
  imports MPY-VERIFICATION

  // Preserve the recursive helper needed by the end-to-end proof.
  claim [encrypt-call-correct]:
    <k> S:String ~> applyFun("encrypt") ~> K
      => rotate4(S) ~> K </k>
    <function>
      <funName> "encrypt" </funName>
      <parameter> "s" </parameter>
      <body> solutionBody </body>
    </function>
    <env> ENV => ENV </env>
    <stack> STACK => STACK </stack>
    <result> _R </result>

  // Fresh false mutation. For the satisfying input S = "", execution returns
  // "", while this postcondition demands "" +String "x" = "x".
  claim [program-wrong-result]:
    <k> Module(FuncDef("encrypt", Params("s"), solutionBody)) ~> start(S:String)
      => .K </k>
    <function>
      <funName> "" => "encrypt" </funName>
      <parameter> "" => "s" </parameter>
      <body> .Stmts => solutionBody </body>
    </function>
    <env> .Map </env>
    <stack> .List </stack>
    <result> noResult => rotate4(S) +String "x" </result>
endmodule
