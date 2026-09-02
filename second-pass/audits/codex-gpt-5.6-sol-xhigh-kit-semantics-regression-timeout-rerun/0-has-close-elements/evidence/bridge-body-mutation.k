requires "verification.k"

module AUDIT-BRIDGE-BODY-MUTATION
  imports VERIFICATION-BASE

  // Reachable one-element Float loop. The real body would increment j by one;
  // this mutation increments it by two while retaining the real-body poststate.
  claim [changed-increment]:
    <k> #loop(
          list(vCons(F:Float, .ValSeq)),
          Name("other"),
          If(Compare(Name("i"), CmpOp("<", Name("j"))),
             If(Compare(Call(Name("abs"),
                             BinOp("-", Name("number"), Name("other"))),
                        CmpOp("<", Name("threshold"))),
                Assign(Name("result"), Bool(true)),
                .Stmts),
             .Stmts)
          Assign(Name("j"), BinOp("+", Name("j"), Int(2))))
        => .K </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
             "has_close_elements" |->
               closureVal(("numbers", "threshold"),
                          HC-FUNCTION-BODY, 0),
             parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
             "numbers"   |-> list(vCons(F, .ValSeq))
             "threshold" |-> T:Float
             "result"    |-> false
             "i"         |-> 0
             "number"    |-> F
             "j"         |-> (0 => 1)
             "other"     |-> (0.0 => F),
             parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
