requires "semantic.k"

module SPEC
  imports MPY
  imports MPY-VERIFICATION

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

  claim [program-correct]:
    <k> Module(FuncDef("encrypt", Params("s"), solutionBody)) ~> start(S:String)
      => .K </k>
    <function>
      <funName> "" => "encrypt" </funName>
      <parameter> "" => "s" </parameter>
      <body> .Stmts => solutionBody </body>
    </function>
    <env> .Map </env>
    <stack> .List </stack>
    <result> noResult => rotate4(S) </result>
endmodule
