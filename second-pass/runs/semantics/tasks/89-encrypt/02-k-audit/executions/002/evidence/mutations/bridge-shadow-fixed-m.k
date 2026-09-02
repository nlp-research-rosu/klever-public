requires "verification.k"

module BRIDGE-SHADOW-FIXED-M
  imports VERIFICATION

  // "ord" resolves to len, so the real body computes
  // chr((1 - 97 + 4) % 26 + 97) == "m".
  claim <k>
          #loop(str(iCons(97, .IntSeq)), Name("char"), encryptLoopBody)
          => .K
        </k>
        <env> 1 </env>
        <scopes>
          0 |-> scope("ord" |-> builtinV("len"), parent(-1))
          -1 |-> builtinsScope
          (1 |-> scope(
             ("result" |-> str(.IntSeq))
             ("char" |-> str(.IntSeq))
             ("s" |-> str(iCons(97, .IntSeq))),
             parent(0))
           =>
           1 |-> scope(
             ("result" |-> str(iCons(109, .IntSeq)))
             ("char" |-> str(iCons(97, .IntSeq)))
             ("s" |-> str(iCons(97, .IntSeq))),
             parent(0)))
        </scopes>
        <heap> .Map </heap>
endmodule
