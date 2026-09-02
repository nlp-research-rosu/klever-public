requires "fixed-verification.k"

module BRIDGE-CONNECTIONS
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
        ("n" |-> N:Int) ("factor" |-> F:Int) REST:Map,
        P:Parent)
      ...
    </scopes>
    requires notBool ("$cells" in_keys(REST))

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
        ("n" |-> N:Int) ("factor" |-> F:Int) REST:Map,
        P:Parent)
      ...
    </scopes>
    requires F >Int 1
     andBool notBool ("$cells" in_keys(REST))

  claim [assign-floor]:
    <k>
      Assign(Name("n"), BinOp("//", Name("n"), Name("factor")))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        ("n" |-> N:Int) ("factor" |-> F:Int) REST:Map
        => ("n" |-> ((N -Int pyMod(N, F)) /Int F))
           ("factor" |-> F) REST,
        P:Parent)
      ...
    </scopes>
    requires F >Int 1
     andBool notBool ("$cells" in_keys(REST))

  claim [augassign-one]:
    <k>
      AugAssign(Name("factor"), "+", Int(1))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        ("n" |-> N:Int) ("factor" |-> F:Int) REST:Map
        => ("n" |-> N) ("factor" |-> (F +Int 1)) REST,
        P:Parent)
      ...
    </scopes>
    requires notBool ("$cells" in_keys(REST))

  claim [return-factor]:
    <k> Return(Name("factor")) ~> RESTK:K => #pop </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        ("factor" |-> F:Int) REST:Map,
        P:Parent)
      ...
    </scopes>
    <ret> noRet => retV(F) </ret>
    requires notBool ("$cells" in_keys(REST))

endmodule
