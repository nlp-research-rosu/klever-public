requires "solution-ast.k"

module VERIFICATION
  imports SOLUTION-AST

  // The symbolic harness differs from OpRunList only in name, making it clear
  // which claims intentionally use the verified loop summary below.
  syntax Program ::= VerifyRunList(Module, List)
  rule <k> VerifyRunList(M, XS)
        => M ~> Invoke("rolling_max", ListVal(XS)) ~> Cleanup ... </k>

  // Loop invariant summarized as a verification rule.  The three preceding
  // assignments establish this exact environment.  For an arbitrary integer
  // list XS, the first iteration initializes the maximum from its head; every
  // remaining iteration appends max(current, previous), exactly #rollingMax.
  // Matching ROLLING-LOOP makes the summary implementation-sensitive.
  rule <k> For(Name("number"), Name("numbers"), ROLLING-LOOP)
        => .K ... </k>
       <env>
         "first" |-> BoolVal(true)
         "maximum" |-> IntVal(0)
         "numbers" |-> ListVal(XS)
         "result" |-> ListVal(.List)
       =>
         "numbers" |-> ListVal(XS)
         "result" |-> ListVal(#rollingMax(XS))
       </env>
       [priority(40)]
endmodule
