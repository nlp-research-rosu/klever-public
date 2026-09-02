requires "verification.k"

module BRIDGE-SHADOW-FIXED-E
  imports VERIFICATION

  // Deliberately false under fixed semantics for the shadowed binding.
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
             ("result" |-> str(iCons(101, .IntSeq)))
             ("char" |-> str(iCons(97, .IntSeq)))
             ("s" |-> str(iCons(97, .IntSeq))),
             parent(0)))
        </scopes>
        <heap> .Map </heap>
endmodule
