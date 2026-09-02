requires "fixed-verification.k"

module BRIDGE-CONNECTIONS-REACHABLE
  imports FIXED-VERIFICATION

  claim [compare-gt]:
    <k>
      Compare(Name("n"), CmpOp(">", Name("factor")))
      => N >Int F
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        ("n" |-> N:Int) ("factor" |-> F:Int),
        parent(0))
      ...
    </scopes>

  claim [compare-mod-zero]:
    <k>
      Compare(
        BinOp("%", Name("n"), Name("factor")),
        CmpOp("==", Int(0)))
      => pyMod(N, F) ==Int 0
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        ("n" |-> N:Int) ("factor" |-> F:Int),
        parent(0))
      ...
    </scopes>
    requires F >Int 1

  claim [assign-floor]:
    <k>
      Assign(Name("n"), BinOp("//", Name("n"), Name("factor")))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        ("n" |-> N:Int) ("factor" |-> F:Int)
        => ("n" |-> ((N -Int pyMod(N, F)) /Int F))
           ("factor" |-> F),
        parent(0))
      ...
    </scopes>
    requires F >Int 1

  claim [augassign-one]:
    <k>
      AugAssign(Name("factor"), "+", Int(1))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        ("n" |-> N:Int) ("factor" |-> F:Int)
        => ("n" |-> N) ("factor" |-> (F +Int 1)),
        parent(0))
      ...
    </scopes>

  claim [return-factor]:
    <k> Return(Name("factor")) ~> RESTK:K => #pop </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        ("n" |-> N:Int) ("factor" |-> F:Int),
        parent(0))
      ...
    </scopes>
    <ret> noRet => retV(F) </ret>

endmodule
