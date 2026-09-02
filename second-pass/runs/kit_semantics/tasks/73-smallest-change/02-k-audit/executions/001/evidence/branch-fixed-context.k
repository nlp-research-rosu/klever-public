requires "/tmp/audit-work/candidate-src/branch-connection.k"

module BRANCH-FIXED-CONTEXT
  imports BRANCH-CONNECTION

  claim [true-observable-suffix]:
    <k>
      #branch(
        true,
        AugAssign(Name("changes"), "+", Int(1)),
        .Stmts)
      ~> Assign(Name("i"), Int(99))
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
             "arr" |-> list(vCons(1, vCons(2, .ValSeq)))
             "changes" |-> (7 => 8)
             "i" |-> (0 => 99),
             parent(0))
    </scopes>

  claim [false-observable-suffix]:
    <k>
      #branch(
        false,
        AugAssign(Name("changes"), "+", Int(1)),
        .Stmts)
      ~> Assign(Name("i"), Int(99))
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
             "arr" |-> list(vCons(1, vCons(2, .ValSeq)))
             "changes" |-> 7
             "i" |-> (0 => 99),
             parent(0))
    </scopes>
endmodule
