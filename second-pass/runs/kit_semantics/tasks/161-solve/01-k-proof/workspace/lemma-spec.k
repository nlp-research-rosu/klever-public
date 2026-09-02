requires "lemma-verification.k"

module LEMMA-SPEC
  imports LEMMA-VERIFICATION

  claim [one-char-is-not-empty]:
    <k>
      iCons(C:Int, .IntSeq) ==K .IntSeq
      =>
      false
    </k>
    <env> ENV:Int </env>
    <scopes> SCOPES:Map </scopes>
    <scopeLoc> SCOPELOC:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> RET:RetState </ret>
    <exc> EXC:Exc </exc>
    <exit-code> EXIT:Int </exit-code>
endmodule
