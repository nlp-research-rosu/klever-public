requires "verification.k"

module SPEC-PREFIX-STEPS
  imports VERIFICATION

  claim
    <k>
      #bindP(("strings", .ParamNames), (ARG:Val, .Vals)) ~> REST:K
      => REST
    </k>
    <env> 1 </env>
    <scopes>
      (1 |-> scope(.Map, parent(0))
       => 1 |-> scope("strings" |-> ARG, parent(0)))
      OTHER:Map
    </scopes>
    [label(bind-input-step)]

  claim
    <k>
      Assign(Name("result"), NoneVal) ~> REST:K
      => REST
    </k>
    <env> 1 </env>
    <scopes>
      (1 |-> scope("strings" |-> ARG:Val, parent(0))
       => 1 |-> scope(
            "strings" |-> ARG
            "result" |-> noneV,
            parent(0)))
      OTHER:Map
    </scopes>
    [label(init-result-step)]

  claim
    <k>
      Assign(Name("string"), NoneVal) ~> REST:K
      => REST
    </k>
    <env> 1 </env>
    <scopes>
      (1 |-> scope(
            "strings" |-> ARG:Val
            "result" |-> noneV,
            parent(0))
       => 1 |-> scope(
            "strings" |-> ARG
            "result" |-> noneV
            "string" |-> noneV,
            parent(0)))
      OTHER:Map
    </scopes>
    [label(init-string-step)]

  claim
    <k>
      For(Name("string"), Name("strings"), BODY:Stmts) ~> REST:K
      => #loop(list(stringVals(SEQ:StringSeq)), Name("string"), BODY) ~> REST
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "strings" |-> list(stringVals(SEQ))
        "result" |-> noneV
        "string" |-> noneV,
        parent(0))
      OTHER:Map
    </scopes>
    [label(for-lowering-step)]
endmodule
