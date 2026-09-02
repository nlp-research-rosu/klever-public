requires "/tmp/audit-work/anti-shuffle-audit/verification.k"

module AUDIT-BRIDGE-SYMBOLIC
  imports VERIFICATION

  claim [true-with-continuation]:
    <k>
      #branch(
        B:Bool,
        Assign(Name("x"), Int(1)),
        Assign(Name("x"), Int(2)))
      ~> Assign(Name("y"), Int(3))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> (scope("x" |-> 0 "y" |-> 0, parent(-1))
             => scope("x" |-> 1 "y" |-> 3, parent(-1)))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires B

  claim [false-with-continuation]:
    <k>
      #branch(
        B:Bool,
        Assign(Name("x"), Int(4)),
        Assign(Name("x"), Int(5)))
      ~> Assign(Name("y"), Int(6))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> (scope("x" |-> 0 "y" |-> 0, parent(-1))
             => scope("x" |-> 5 "y" |-> 6, parent(-1)))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool B
endmodule
