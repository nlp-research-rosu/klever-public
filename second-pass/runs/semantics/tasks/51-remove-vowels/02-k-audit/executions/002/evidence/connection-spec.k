requires "connection-verification.k"

module CONNECTION-SPEC
  imports CONNECTION

  claim [below-65]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 0), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C <Int 65

  claim [point-65]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 1), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C ==Int 65

  claim [between-65-69]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 0), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C >Int 65 andBool C <Int 69

  claim [point-69]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 1), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C ==Int 69

  claim [between-69-73]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 0), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C >Int 69 andBool C <Int 73

  claim [point-73]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 1), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C ==Int 73

  claim [between-73-79]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 0), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C >Int 73 andBool C <Int 79

  claim [point-79]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 1), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C ==Int 79

  claim [between-79-85]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 0), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C >Int 79 andBool C <Int 85

  claim [point-85]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 1), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C ==Int 85

  claim [between-85-97]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 0), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C >Int 85 andBool C <Int 97

  claim [point-97]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 1), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C ==Int 97

  claim [between-97-101]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 0), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C >Int 97 andBool C <Int 101

  claim [point-101]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 1), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C ==Int 101

  claim [between-101-105]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 0), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C >Int 101 andBool C <Int 105

  claim [point-105]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 1), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C ==Int 105

  claim [between-105-111]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 0), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C >Int 105 andBool C <Int 111

  claim [point-111]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 1), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C ==Int 111

  claim [between-111-117]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 0), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C >Int 111 andBool C <Int 117

  claim [point-117]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 1), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C ==Int 117

  claim [above-117]:
    <k> auditCheck(C:Int) => .K </k>
    <env> 0 </env>
    <scopes> 0 |-> scope("$audit" |-> (9 => 0), parent(-1)) -1 |-> builtinsScope </scopes>
    requires C >Int 117
endmodule
