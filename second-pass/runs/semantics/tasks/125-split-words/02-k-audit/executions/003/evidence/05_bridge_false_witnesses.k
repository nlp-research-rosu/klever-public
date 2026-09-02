requires "verification.k"

module BRIDGE-FALSE-WITNESSES
  imports SPLIT-WORDS-VERIFICATION

  // Each claim is a false fixed-semantics conclusion enabled by exactly one
  // candidate rule.  The Boolean is deliberately opposite to the branch that
  // the corresponding $proofPath rule forces.
  claim [rule-1-false-boolean]:
    <k>
      #branch(
        false,
        Return(Call(Attribute(Name("txt"), "split"), .Exprs)) .Stmts,
        .Stmts)
      => Return(Call(Attribute(Name("txt"), "split"), .Exprs))
    </k>
    <scopes> 0 |-> scope("$proofPath" |-> 1, parent(-1)) </scopes>

  claim [rule-2-true-boolean-discarded]:
    <k>
      #branch(
        true,
        Return(Call(Attribute(Name("txt"), "split"), .Exprs)) .Stmts,
        .Stmts)
      => .K
    </k>
    <scopes> 0 |-> scope("$proofPath" |-> 2, parent(-1)) </scopes>

  claim [rule-3-true-boolean-discarded]:
    <k>
      #branch(
        true,
        Return(Call(Attribute(Name("txt"), "split"), .Exprs)) .Stmts,
        .Stmts)
      => .K
    </k>
    <scopes> 0 |-> scope("$proofPath" |-> 3, parent(-1)) </scopes>

  claim [rule-4-false-boolean]:
    <k>
      #branch(
        false,
        Return(Call(Attribute(Name("txt"), "split"), Str(","))) .Stmts,
        .Stmts)
      => Return(Call(Attribute(Name("txt"), "split"), Str(",")))
    </k>
    <scopes> 0 |-> scope("$proofPath" |-> 2, parent(-1)) </scopes>

  claim [rule-5-true-boolean-discarded]:
    <k>
      #branch(
        true,
        Return(Call(Attribute(Name("txt"), "split"), Str(","))) .Stmts,
        .Stmts)
      => .K
    </k>
    <scopes> 0 |-> scope("$proofPath" |-> 3, parent(-1)) </scopes>
endmodule
