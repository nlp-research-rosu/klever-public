requires "verification.k"

module SPEC-HELPER-ONLY
  imports VERIFICATION

  claim [helper]:
    <k> decodeBody ~> #endcall => #pop </k>
    <env> L </env>
    <scopes>
      0 |-> scope("decode_cyclic" |-> decodeClosure, parent(-1))
      L |-> scope("s" |-> str(CS), parent(0))
      -1 |-> builtinsScope
      SC:Map
    </scopes>
    <scopeLoc> NEXT </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HNEXT </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet => retV(str(decodeCodes(CS))) </ret>
    <exc> NoExc </exc>
    <exit-code> CODE </exit-code>
    requires L =/=Int 0
     andBool L =/=Int -1
     andBool L <Int NEXT
     andBool 0 <Int NEXT
     andBool keysBelow(SC, NEXT)
endmodule
