requires "verification.k"

module STRONGEST-EXTENSION-SPEC
  imports STRONGEST-EXTENSION-VERIFICATION

  // Induction step for the character loop.  The empty suffix is discharged by
  // the reference semantics; the nonempty suffix reuses this circularity.
  claim
    <k>
      #loop(
        str(iCons(CURRENT:Int, REST:IntSeq)),
        Name("character"),
        characterStrengthBody)
      ~> CONT:K
    =>
      CONT
    </k>
    <env> 2 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (2 |-> scope(
        ("extension" |-> str(ALL:IntSeq))
        ("score" |-> ACC:Int)
        ("character" |-> str(PREV:IntSeq)),
        parent(0)))
    =>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (2 |-> scope(
        ("extension" |-> str(ALL))
        ("score" |->
          strengthAcc(iCons(CURRENT, REST), ACC))
        ("character" |->
          str(lastCharacter(iCons(CURRENT, REST), PREV))),
        parent(0)))
    </scopes>
    <scopeLoc> 3 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(character-loop-correct), circularity]

  // Helper theorem, proved using only the already-discharged character loop.
  claim
    <k>
      Call(Name("_extension_strength"), str(CS:IntSeq))
      ~> CONT:K
    =>
      extensionStrength(CS)
      ~> CONT
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(LOCALS:Map, parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool ("_extension_strength" in_keys(LOCALS))
    [label(extension-strength-correct), depends(character-loop-correct)]

  // Symbolic stable first-maximum loop theorem for three arbitrary names.
  claim
    <k>
      #loop(
        list(vCons(
          str(E1:IntSeq),
          vCons(str(E2:IntSeq),
          vCons(str(E3:IntSeq), .ValSeq)))),
        Name("extension"),
        selectionLoopBody)
      ~> CONT:K
    =>
      CONT
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(
        ("class_name" |-> str(CLASS:IntSeq))
        ("extensions" |-> list(ALL:ValSeq))
        ("strongest" |-> str(BEST:IntSeq))
        ("strongest_strength" |-> BESTS:Int)
        ("extension" |-> str(LAST:IntSeq))
        ("score" |-> extensionStrength(LAST)),
        parent(0)))
    =>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(
        ("class_name" |-> str(CLASS))
        ("extensions" |-> list(ALL))
        ("strongest" |->
          str(bestExtension(
            vCons(str(E1), vCons(str(E2), vCons(str(E3), .ValSeq))),
            BEST,
            BESTS)))
        ("strongest_strength" |->
          bestStrength(
            vCons(str(E1), vCons(str(E2), vCons(str(E3), .ValSeq))),
            BEST,
            BESTS))
        ("extension" |->
          str(lastExtension(
            vCons(str(E1), vCons(str(E2), vCons(str(E3), .ValSeq))),
            LAST)))
        ("score" |->
          extensionStrength(
            lastExtension(
              vCons(str(E1), vCons(str(E2), vCons(str(E3), .ValSeq))),
              LAST))),
        parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(selection-loop-correct),
     depends(extension-strength-correct)]

  // Entry-point theorem for an arbitrary ASCII class and three arbitrary
  // ASCII extension names (the shape used by the prompt's main example).
  claim
    <k>
      Call(
        Name("Strongest_Extension"),
        str(CLASS:IntSeq),
        list(vCons(
          str(E1:IntSeq),
          vCons(str(E2:IntSeq),
          vCons(str(E3:IntSeq), .ValSeq)))))
    =>
      str(seqConcat(
        seqConcat(CLASS, iCons(46, .IntSeq)),
        bestExtension(
          vCons(str(E1), vCons(str(E2), vCons(str(E3), .ValSeq))),
          E1,
          extensionStrength(E1))))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(strongest-extension-correct),
     depends(extension-strength-correct, selection-loop-correct)]
endmodule
