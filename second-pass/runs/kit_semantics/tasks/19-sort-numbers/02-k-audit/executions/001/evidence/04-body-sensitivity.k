requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-SENSITIVITY
  imports MPY

  // Material mutation: zero and one are swapped in the tuple actually
  // executed by the claim.
  syntax Val ::= "mutatedNumberKeyClosure" [macro]
  rule mutatedNumberKeyClosure
    => closureVal(
         ("number", .ParamNames),
         (Return(
            Call(
              Attribute(
                TupleExpr(
                  Str("one"),
                  Str("zero"),
                  Str("two"),
                  Str("three"),
                  Str("four"),
                  Str("five"),
                  Str("six"),
                  Str("seven"),
                  Str("eight"),
                  Str("nine")),
                "index"),
              Name("number"))) .Stmts),
         0)
endmodule

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION-BODY-SENSITIVITY

  claim [mutated-key-zero]:
    <k> Call(Name("_number_key"), Str("zero")) => 0 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("_number_key" |-> mutatedNumberKeyClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
