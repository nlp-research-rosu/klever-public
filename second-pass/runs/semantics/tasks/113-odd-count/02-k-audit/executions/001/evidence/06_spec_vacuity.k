requires "verification.k"

module ODD-COUNT-SPEC-VACUITY
  imports ODD-COUNT-VERIFICATION

  claim
    <k>
      #loop(str(CS:IntSeq), Name("digit"), ODD-INNER-BODY) ~> CONT:K
      =>
      CONT
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
              "odd_count" |-> closureVal("lst", ODD-COUNT-BODY, 0),
              parent(-1))
      1  |-> scope(
              ("lst" |-> list(INPUT:ValSeq))
              ("result" |-> ref(OUT:Int))
              ("digits" |-> str(WHOLE:IntSeq))
              ("count" |-> N:Int)
              ("digit" |-> D:Val)
              ("text" |-> TXT:Val),
              parent(0))
      =>
      -1 |-> builtinsScope
      0  |-> scope(
              "odd_count" |-> closureVal("lst", ODD-COUNT-BODY, 0),
              parent(-1))
      1  |-> scope(
              ("lst" |-> list(INPUT))
              ("result" |-> ref(OUT))
              ("digits" |-> str(WHOLE))
              ("count" |-> oddDigitsFrom(N, CS))
              ("digit" |-> lastDigit(CS, D))
              ("text" |-> TXT),
              parent(0))
    </scopes>
    requires allDigit(CS)
    [label(digit-loop)]

  claim
    <k>
      #loop(list(.ValSeq), Name("digits"), ODD-OUTER-BODY) ~> CONT:K
      =>
      CONT
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
              "odd_count" |-> closureVal("lst", ODD-COUNT-BODY, 0),
              parent(-1))
      1  |-> scope(
              ("lst" |-> list(WHOLE:ValSeq))
              ("result" |-> ref(OUT:Int))
              ("digits" |-> str(.IntSeq))
              ("count" |-> 0)
              ("digit" |-> str(.IntSeq))
              ("text" |-> str(.IntSeq)),
              parent(0))
      =>
      -1 |-> builtinsScope
      0  |-> scope(
              "odd_count" |-> closureVal("lst", ODD-COUNT-BODY, 0),
              parent(-1))
      1  |-> scope(
              ("lst" |-> list(WHOLE))
              ("result" |-> ref(OUT))
              ("digits" |-> str(.IntSeq))
              ("count" |-> 0)
              ("digit" |-> str(.IntSeq))
              ("text" |-> str(.IntSeq)),
              parent(0))
    </scopes>
    <heap>
      OUT |-> list(ACC:ValSeq)
      =>
      OUT |-> list(ACC)
    </heap>
    [label(outer-empty)]

  claim
    <k>
      #loop(
        list(vCons(str(CS:IntSeq), REST:ValSeq)),
        Name("digits"),
        ODD-OUTER-BODY) ~> CONT:K
      =>
      CONT
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
              "odd_count" |-> closureVal("lst", ODD-COUNT-BODY, 0),
              parent(-1))
      1  |-> scope(
              ("lst" |-> list(WHOLE:ValSeq))
              ("result" |-> ref(OUT:Int))
              ("digits" |-> str(.IntSeq))
              ("count" |-> 0)
              ("digit" |-> str(.IntSeq))
              ("text" |-> str(.IntSeq)),
              parent(0))
      =>
      -1 |-> builtinsScope
      0  |-> scope(
              "odd_count" |-> closureVal("lst", ODD-COUNT-BODY, 0),
              parent(-1))
      1  |-> scope(
              ("lst" |-> list(WHOLE))
              ("result" |-> ref(OUT))
              ("digits" |-> str(.IntSeq))
              ("count" |-> 0)
              ("digit" |-> str(.IntSeq))
              ("text" |-> str(.IntSeq)),
              parent(0))
    </scopes>
    <heap>
      OUT |-> list(ACC:ValSeq)
      =>
      OUT |-> list(
               oddCountFrom(
                 ACC,
                 vCons(str(CS), REST)))
    </heap>
    requires allDigit(CS)
     andBool validDigitStrings(REST)
    [label(outer-loop)]

  claim
    <k>
      #loadAll(ODD-COUNT-PROGRAM)
      ~> Call(Name("odd_count"), list(INPUT:ValSeq))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(.Map, parent(-1))
      =>
      -1 |-> builtinsScope
      0  |-> scope(
              "odd_count" |-> closureVal("lst", ODD-COUNT-BODY, 0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
             vCons(
               str(strToCodes("WRONG")),
               oddCountSpec(INPUT)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validDigitStrings(INPUT)
    [label(target)]
endmodule
