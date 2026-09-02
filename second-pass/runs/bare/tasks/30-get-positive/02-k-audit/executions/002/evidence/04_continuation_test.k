requires "semantic.k"

module CONTINUATION-TEST
  imports SEMANTIC

  syntax KItem ::= "observe"
                 | "observed" "(" PyList ")"

  rule <k> L:PyList ~> observe => observed(L) ... </k>
endmodule
