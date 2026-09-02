requires "semantic.k"

module SPEC-VACUITY-AUDIT
  imports MPY

  // Satisfiable initial configuration: submitted program with input "a".
  // The program returns "e"; the deliberately false obligation requires "f".
  claim [program-wrong-ground-result]:
    <k>
      Module(FuncDef("encrypt", Params("s"), solutionBody)) ~> start("a")
      => .K
    </k>
    <function>
      <funName> "" => "encrypt" </funName>
      <parameter> "" => "s" </parameter>
      <body> .Stmts => solutionBody </body>
    </function>
    <env> .Map </env>
    <stack> .List </stack>
    <result> noResult => "f" </result>
endmodule
