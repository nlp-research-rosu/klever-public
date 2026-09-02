requires "verification.k"

// This ground state lies in the installed bridge's match domain. It binds the
// global name "ord" to a normal source-language closure returning 91. Python
// name resolution therefore treats each ']' as if ord(char) were 91.
module BRIDGE-WITNESS-FIXED-SPEC
  imports IS-NESTED-VERIFICATION

  claim [fixed-shadowed-ord]:
    <k>
      #loop(
        str(bCodes(bClose(bClose(bNil)))),
        Name("char"),
        scanBody)
      ~> (Return(Compare(Name("state"), CmpOp("==", Int(4))))
          .Stmts):Stmts
      ~> #endcall
      => false
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (1 |-> scope(
        "state" |-> 2
        "char" |-> str(.IntSeq)
        "string" |-> str(bCodes(bClose(bClose(bNil)))),
        parent(0)) => .Map)
      0 |-> scope(
        "ord" |-> closureVal(
          ("x", .ParamNames),
          Return(Int(91)) .Stmts,
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module BRIDGE-WITNESS-EXTENDED-SPEC
  imports IS-NESTED-VERIFICATION-WITH-LOOP-LEMMA

  claim [bridge-shadowed-ord]:
    <k>
      #loop(
        str(bCodes(bClose(bClose(bNil)))),
        Name("char"),
        scanBody)
      ~> (Return(Compare(Name("state"), CmpOp("==", Int(4))))
          .Stmts):Stmts
      ~> #endcall
      => true
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (1 |-> scope(
        "state" |-> 2
        "char" |-> str(.IntSeq)
        "string" |-> str(bCodes(bClose(bClose(bNil)))),
        parent(0)) => .Map)
      0 |-> scope(
        "ord" |-> closureVal(
          ("x", .ParamNames),
          Return(Int(91)) .Stmts,
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
