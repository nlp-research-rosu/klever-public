requires "verification.k"

module AUDIT-ADEQUACY-GROUND
  imports STRING-XOR-VERIFICATION

  // "010" and "110" satisfy the binary-domain predicate.
  claim
    <k>
      binaryCodes(iCons(48, iCons(49, iCons(48, .IntSeq))))
      =>
      true
    </k>
  claim
    <k>
      binaryCodes(iCons(49, iCons(49, iCons(48, .IntSeq))))
      =>
      true
    </k>

  // Substituting the documented example into the mathematical postcondition
  // yields the code sequence for "100".
  claim
    <k>
      xorAcc(
        .IntSeq,
        iCons(48, iCons(49, iCons(48, .IntSeq))),
        iCons(49, iCons(49, iCons(48, .IntSeq))))
      =>
      iCons(49, iCons(48, iCons(48, .IntSeq)))
    </k>

  // Concrete satisfying witness for the loop claim's entry state.  The
  // explicit execution is finite and does not import the symbolic spec claim.
  claim
    <k>
      #loop(
        zipObjS(
          iCons(48, iCons(49, iCons(48, .IntSeq))),
          iCons(49, iCons(49, iCons(48, .IntSeq)))),
        stringXorTarget,
        stringXorLoopBody)
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        ("a" |-> str(iCons(48, iCons(49, iCons(48, .IntSeq)))))
        ("b" |-> str(iCons(49, iCons(49, iCons(48, .IntSeq)))))
        ("result" |-> str(.IntSeq))
        ("x" |-> str(.IntSeq))
        ("y" |-> str(.IntSeq)),
        root)
      =>
      1 |-> scope(
        ("a" |-> str(iCons(48, iCons(49, iCons(48, .IntSeq)))))
        ("b" |-> str(iCons(49, iCons(49, iCons(48, .IntSeq)))))
        ("result" |-> str(iCons(49, iCons(48, iCons(48, .IntSeq)))))
        ("x" |-> str(iCons(48, .IntSeq)))
        ("y" |-> str(iCons(48, .IntSeq))),
        root)
    </scopes>

  // Concrete satisfying witness for the end-to-end entry precondition.
  claim
    <k>
      #loadAll(stringXorModule)
      ~> Call(
        Name("string_xor"),
        str(iCons(48, iCons(49, iCons(48, .IntSeq)))),
        str(iCons(49, iCons(49, iCons(48, .IntSeq)))))
      =>
      str(iCons(49, iCons(48, iCons(48, .IntSeq))))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))) (-1 |-> builtinsScope)
      =>
      (0 |-> scope(("string_xor" |-> stringXorClosure), parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
