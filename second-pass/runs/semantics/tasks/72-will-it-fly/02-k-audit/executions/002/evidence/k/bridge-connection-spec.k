requires "bridge-base.k"

module BRIDGE-CONNECTION-SPEC
  imports BRIDGE-BASE

  // No candidate doSlice override is imported.
  claim
    <k>
      doSlice(list(VS:ValSeq), noB, noB, someB(-1)) ~> CONT:K
      => list(auditReverseVS(VS)) ~> CONT
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

  // No candidate #sumAcc override is imported.
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
