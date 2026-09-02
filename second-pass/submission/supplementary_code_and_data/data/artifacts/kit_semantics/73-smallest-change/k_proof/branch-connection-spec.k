requires "branch-connection.k"

module BRANCH-CONNECTION-SPEC
  imports BRANCH-CONNECTION

  claim [branch-true]:
    <k> #branch(B:Bool, T:Stmts, _E:Stmts) => T ... </k>
    requires B

  claim [branch-false]:
    <k> #branch(B:Bool, _T:Stmts, E:Stmts) => E ... </k>
    requires notBool B

  claim [count-branch-true]:
    <k>
      #branch(
        B:Bool,
        AugAssign(Name("changes"), "+", Int(1)),
        .Stmts)
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
             "arr" |-> list(VS:ValSeq)
             "changes" |-> (C:Int => C +Int 1)
             "i" |-> I:Int,
             parent(0))
      REST:Map
    </scopes>
    requires B

  claim [count-branch-false]:
    <k>
      #branch(
        B:Bool,
        AugAssign(Name("changes"), "+", Int(1)),
        .Stmts)
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
             "arr" |-> list(VS:ValSeq)
             "changes" |-> C:Int
             "i" |-> I:Int,
             parent(0))
      REST:Map
    </scopes>
    requires notBool B
endmodule
