requires "semantic-generic.k"

module LOOP-CONNECTION-SPEC
  imports HUMAN-EVAL

  // Built-in Map update exposed as a simplification over a fresh key.
  rule (REST:Map [ KEY:String <- V:KItem ])
    => (KEY |-> V REST)
    requires notBool (KEY in_keys(REST))
    [simplification]

  rule ((KEY:String |-> _OLD:KItem REST:Map) [ KEY <- V:KItem ])
    => (KEY |-> V REST)
    requires notBool (KEY in_keys(REST))
    [simplification]

  // Independent reviewer theorems: the generic small-step loop has exactly
  // the state transition asserted by the candidate's accelerated loop rule.
  // The split exposes whether the loop-variable binding exists before entry.
  claim [loop-summary-no-value]:
        <k> loop("value", I :: IS,
          If(Compare(Name("previous"), CmpOp(">", Name("value"))),
            Assign(Name("drops"), BinOp("+", Name("drops"), Int(1))) .Stmts,
            .Stmts)
          Assign(Name("previous"), Name("value")) .Stmts)
          => .K ...
        </k>
        <env> ("drops" |-> iVal(D)
               "previous" |-> iVal(P)
               REST)
          => ("drops" |-> iVal(D +Int dropsFrom(P, I :: IS))
               "previous" |-> iVal(last(I :: IS))
               (REST [ "value" <- iVal(last(I :: IS)) ]))
        </env>
    requires notBool ("value" in_keys(REST))

  claim [loop-summary-with-value]:
        <k> loop("value", I :: IS,
          If(Compare(Name("previous"), CmpOp(">", Name("value"))),
            Assign(Name("drops"), BinOp("+", Name("drops"), Int(1))) .Stmts,
            .Stmts)
          Assign(Name("previous"), Name("value")) .Stmts)
          => .K ...
        </k>
        <env> ("drops" |-> iVal(D)
               "previous" |-> iVal(P)
               "value" |-> OLD
               REST)
          => ("drops" |-> iVal(D +Int dropsFrom(P, I :: IS))
               "previous" |-> iVal(last(I :: IS))
               "value" |-> iVal(last(I :: IS))
               REST)
        </env>
endmodule
