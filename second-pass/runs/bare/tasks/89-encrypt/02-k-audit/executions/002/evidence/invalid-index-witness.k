requires "semantic.k"

module INVALID-INDEX-WITNESS
  imports MPY

  // The candidate semantics concludes that Python ""[0] has value "".
  claim [empty-index-fabricates-empty-string]:
    <k> eval(Subscript(Str(""), Int(0))) => "" </k>
    <function>
      <funName> "" </funName>
      <parameter> "" </parameter>
      <body> .Stmts </body>
    </function>
    <env> .Map </env>
    <stack> .List </stack>
    <result> noResult </result>
endmodule
