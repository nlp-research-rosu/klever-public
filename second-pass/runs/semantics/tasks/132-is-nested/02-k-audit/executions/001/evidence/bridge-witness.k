requires "verification.k"

// The candidate's proved loop claim fixes module scope 0 to contain only
// is_nested and therefore resolves ord from builtins scope -1.  This module
// deliberately exercises a state admitted only by the installed rule's broader
// _REST:Map: module scope 0 soundly shadows ord with len.  On valid input "[[]]",
// fixed execution calls len(char), never increments state, and returns false.
module BASE-BRIDGE-WITNESS
  imports IS-NESTED-VERIFICATION

  claim [shadowed-ord-fixed-semantics]:
    <k>
      #loop(
        str(bCodes(bOpen(bOpen(bClose(bClose(bNil)))))),
        Name("char"),
        scanBody)
      ~> (Return(Compare(Name("state"), CmpOp("==", Int(4)))) .Stmts):Stmts
      ~> #endcall
      => true
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (1 |-> scope(
        "state" |-> 0
        "char" |-> str(.IntSeq)
        "string" |-> str(bCodes(bOpen(bOpen(bClose(bClose(bNil)))))),
        parent(0)) => .Map)
      0 |-> scope("ord" |-> builtinV("len"), parent(-1))
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

// Same state under the candidate's installed proved-scan-loop operational rule.
module EXTENDED-BRIDGE-WITNESS
  imports IS-NESTED-VERIFICATION-WITH-LOOP-LEMMA

  claim [shadowed-ord-candidate-bridge]:
    <k>
      #loop(
        str(bCodes(bOpen(bOpen(bClose(bClose(bNil)))))),
        Name("char"),
        scanBody)
      ~> (Return(Compare(Name("state"), CmpOp("==", Int(4)))) .Stmts):Stmts
      ~> #endcall
      => true
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (1 |-> scope(
        "state" |-> 0
        "char" |-> str(.IntSeq)
        "string" |-> str(bCodes(bOpen(bOpen(bClose(bClose(bNil)))))),
        parent(0)) => .Map)
      0 |-> scope("ord" |-> builtinV("len"), parent(-1))
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
