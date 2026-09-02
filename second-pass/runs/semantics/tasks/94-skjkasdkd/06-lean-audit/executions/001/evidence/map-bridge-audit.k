requires "domains.md"

module MAP-BRIDGE-AUDIT
  imports MAP
  imports INT
  imports K-EQUAL

  syntax Exp ::= "commutativityWitness"

  rule commutativityWitness
    => (((0 |-> 2) (1 |-> 2)) ==K ((1 |-> 2) (0 |-> 2)))
endmodule
