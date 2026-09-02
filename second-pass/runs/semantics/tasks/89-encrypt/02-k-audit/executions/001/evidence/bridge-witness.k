requires "verification.k"

// Ground witness: the loop input is the intended lowercase string "a", but
// module scope 0 shadows chr with ord. Fixed execution therefore reaches
// applyBuiltin("ord", 101, .Vals) and cannot produce the claimed "e".
// verification.k:66 ignores that binding and fabricates the loop summary.

module BRIDGE-WITNESS-BASE
  imports VERIFICATION

  claim <k>
          #loop(
            str(iCons(97, .IntSeq)),
            Name("char"),
            encryptLoopBody)
          => .K
        </k>
        <env> 1 </env>
        <scopes>
          0 |-> scope(
            ("encrypt" |-> encryptClosure)
            ("chr" |-> builtinV("ord")),
            parent(-1))
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

module BRIDGE-WITNESS-EXTENDED
  imports VERIFICATION-WITH-LOOP

  claim <k>
          #loop(
            str(iCons(97, .IntSeq)),
            Name("char"),
            encryptLoopBody)
          => .K
        </k>
        <env> 1 </env>
        <scopes>
          0 |-> scope(
            ("encrypt" |-> encryptClosure)
            ("chr" |-> builtinV("ord")),
            parent(-1))
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
