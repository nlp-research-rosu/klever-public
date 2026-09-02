requires "body-identity-verification.k"

module AUDIT-BODY-IDENTITY
  imports AUDIT-BODY-IDENTITY-VERIFICATION

  claim [body-identity]:
    <k> getRowBody => expectedGetRowBody </k>
    <env> E:Int </env>
    <scopes> SC:Map </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> H:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> ST:List </stack>
    <ret> RS:RetState </ret>
    <exc> EX:Exc </exc>
    <exit-code> EC:Int </exit-code>

  claim [closure-identity]:
    <k> getRowClosure => expectedGetRowClosure </k>
    <env> E:Int </env>
    <scopes> SC:Map </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> H:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> ST:List </stack>
    <ret> RS:RetState </ret>
    <exc> EX:Exc </exc>
    <exit-code> EC:Int </exit-code>
endmodule
