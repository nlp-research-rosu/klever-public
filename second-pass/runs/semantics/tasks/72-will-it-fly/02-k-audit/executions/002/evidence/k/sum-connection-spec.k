requires "bridge-base.k"

module SUM-CONNECTION-SPEC
  imports BRIDGE-BASE

  claim
    <k>
      #sumAcc(list(VS:ValSeq), 0) ~> CONT:K
      => auditSumIntVS(VS) ~> CONT
    </k>
    <env> E:Int </env>
    <scopes> SC:Map </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> HP:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> ST:List </stack>
    <ret> RT:RetState </ret>
    <exc> EX:Exc </exc>
    <exit-code> EC:Int </exit-code>
    requires auditAllInts(VS)
endmodule
