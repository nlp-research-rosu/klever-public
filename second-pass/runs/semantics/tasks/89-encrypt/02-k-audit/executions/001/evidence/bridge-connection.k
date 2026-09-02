requires "verification.k"

module BRIDGE-CONNECTION-SPEC
  imports VERIFICATION

  // Reviewer-authored universal connection claim for the complete match
  // domain of verification.k:66. It deliberately imports VERIFICATION, not
  // VERIFICATION-WITH-LOOP, so the operational bridge is unavailable.
  claim <k>
          #loop(str(CS:IntSeq), Name("char"), encryptLoopBody)
          => .K
          ...
        </k>
        <env> 1 </env>
        <scopes>
          ...
          (1 |-> scope(
             ("result" |-> str(A:IntSeq))
             ("char" |-> OLD:Str)
             ("s" |-> str(INPUT:IntSeq)),
             parent(0))
           =>
           1 |-> scope(
             ("result" |-> str(encryptAcc(A, CS)))
             ("char" |-> lastChar(CS, OLD))
             ("s" |-> str(INPUT)),
             parent(0)))
          ...
        </scopes>
        <heap> .Map </heap>
endmodule
