requires "verification.k"

module VERIFICATION-WITH-LOOP
  imports VERIFICATION

  // Auxiliary execution theorem.  prove.sh first proves the identical
  // SPEC.loop claim against VERIFICATION, before this module is compiled.
  rule [loop-lemma]:
    <k>
      #loop(
        str(CS:IntSeq),
        Name("bracket"),
        If(
          Compare(Name("bracket"), CmpOp("==", Str("("))),
          AugAssign(Name("balance"), "+", Int(1)),
          AugAssign(Name("balance"), "-", Int(1)))
        If(
          Compare(Name("balance"), CmpOp("<", Int(0))),
          Assign(Name("valid"), Bool(false)),
          .Stmts))
      ~> (Return(
            BoolOp(
              "and",
              Name("valid"),
              Compare(Name("balance"), CmpOp("==", Int(0)))))
          .Stmts)
      ~> #endcall
      =>
      scanBrackets(CS, B:Int, V:Bool)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> BUILTINS:Scope
         0 |-> scope(MODULE:Map, parent(-1))
         1 |-> scope(
                "bracket" |-> _OLD:Val
                "brackets" |-> str(_INPUT:IntSeq)
                "balance" |-> B
                "valid" |-> V,
                parent(0)) )
      =>
      ( -1 |-> BUILTINS
         0 |-> scope(MODULE, parent(-1)) )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires bracketInput(CS)
    [priority(40)]
endmodule
