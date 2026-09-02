requires "bridge-base.k"

module SLICE-CONNECTION-SPEC
  imports BRIDGE-BASE

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
endmodule
