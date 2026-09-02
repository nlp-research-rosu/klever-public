requires "verification-no-bridges.k"

module BRIDGE-CONTEXT-FIXED
  imports XOR-VERIFICATION-NO-BRIDGES

  syntax Module ::= "bridgeInput" "(" Int "," Int "," Stream "," Stream ")"
  syntax Sem ::= "observe"
  syntax ExecResult ::= "observed" "(" Value ")"

  rule <k> bridgeInput(N, M, S1, S2)
        => exec(solutionBody,
                env(str(segment(N, S1)), str(segment(M, S2))),
                solutionBody)
           ~> observe ... </k>

  rule <k> returned(V) ~> observe => observed(V) ... </k>
endmodule
