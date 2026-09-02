requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Unchanged helper claim, retained so the entry claim has the same
  // recursive proof support as the positive proof.
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

  // Deliberately false: append code point 33 ('!') to the required output.
  // Satisfying witness CS=.IntSeq: the program returns "", not "!".
  claim [false-entry]:
    <k>
      Call(Name("decode_cyclic"), (str(CS), .Exprs))
      =>
      str(seqConcat(decodeCodes(CS), iCons(33, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("decode_cyclic" |-> decodeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
