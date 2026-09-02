requires "verification.k"

// Concrete digit "1" with a module-level shadowing of ord. The fixed
// semantics calls this closure and therefore classifies the digit as even.
module BRIDGE-BASE-WITNESS
  imports EVEN-ODD-VERIFICATION

  claim
    <k>
      #loop(
        str(iCons(49, .IntSeq)),
        Name("digit"),
        #digitLoopBody)
    =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "ord" |-> closureVal(
          ("x", .ParamNames),
          Return(Int(0)) .Stmts,
          0),
        parent(-1))
      1  |-> scope(
        "num"        |-> 1
        "even_count" |-> 0
        "odd_count"  |-> 0
        "digit"      |-> 0,
        parent(0))
    =>
      -1 |-> builtinsScope
      0  |-> scope(
        "ord" |-> closureVal(
          ("x", .ParamNames),
          Return(Int(0)) .Stmts,
          0),
        parent(-1))
      1  |-> scope(
        "num"        |-> 1
        "even_count" |-> 1
        "odd_count"  |-> 0
        "digit"      |-> str(iCons(49, .IntSeq)),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

// This is the opposite result. It is false under fixed semantics, but the
// proof-local priority summary can establish it because its ellipses admit
// the shadowed module scope and it never performs the ord lookup.
module BRIDGE-SUMMARY-FALSE-WITNESS
  imports EVEN-ODD-VERIFICATION-SUMMARY

  claim
    <k>
      #loop(
        str(iCons(49, .IntSeq)),
        Name("digit"),
        #digitLoopBody)
    =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "ord" |-> closureVal(
          ("x", .ParamNames),
          Return(Int(0)) .Stmts,
          0),
        parent(-1))
      1  |-> scope(
        "num"        |-> 1
        "even_count" |-> 0
        "odd_count"  |-> 0
        "digit"      |-> 0,
        parent(0))
    =>
      -1 |-> builtinsScope
      0  |-> scope(
        "ord" |-> closureVal(
          ("x", .ParamNames),
          Return(Int(0)) .Stmts,
          0),
        parent(-1))
      1  |-> scope(
        "num"        |-> 1
        "even_count" |-> 0
        "odd_count"  |-> 1
        "digit"      |-> str(iCons(49, .IntSeq)),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
