requires "verification.k"

module ISCube-SPEC
  imports ISCube-VERIFICATION

  // End-to-end implementation refinement for an arbitrary Python integer.
  claim [implementation]:
    <k>
      Call(Name("iscube"), (Int(A), .Exprs))
      =>
      (roundedCubeRoot(absInt(A)) ^Int 3)
        ==Int absInt(A)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("iscube" |-> iscubeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Every integer is, after abs, either N^3 or uniquely N^3 + D with
  // 0 < D < (N+1)^3 - N^3.  The following four claims therefore cover both
  // signs and both outcomes of the contract.
  claim [positive-cubes]:
    <k>
      Call(Name("iscube"),
        (Int(N *Int N *Int N), .Exprs))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("iscube" |-> iscubeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0

  claim [negative-cubes]:
    <k>
      Call(Name("iscube"),
        (Int(0 -Int (N *Int N *Int N)), .Exprs))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("iscube" |-> iscubeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 0

  claim [positive-noncubes]:
    <k>
      Call(Name("iscube"),
        (Int(N *Int N *Int N +Int D), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("iscube" |-> iscubeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
     andBool D >Int 0
     andBool D <Int (3 *Int N *Int N +Int 3 *Int N +Int 1)

  claim [negative-noncubes]:
    <k>
      Call(Name("iscube"),
        (Int(0 -Int (N *Int N *Int N +Int D)), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("iscube" |-> iscubeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
     andBool D >Int 0
     andBool D <Int (3 *Int N *Int N +Int 3 *Int N +Int 1)
endmodule
