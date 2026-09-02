requires "verification.k"

module ADD-ELEMENTS-SPEC
  imports ADD-ELEMENTS-VERIFICATION

  // Loop invariant: starting from ACC, iteration over any non-empty integer
  // sequence adds precisely its qualifying elements and leaves the loop
  // variable equal to the final element.
  claim
    <k>
      #loop(
        list(vCons(V:Val, VS:ValSeq)),
        Name("element"),
        If(
          Compare(
            Call(Name("abs"), Name("element")),
            CmpOp("<", Int(100))
          ),
          AugAssign(Name("total"), "+", Name("element")),
          .Stmts
        )
      ) => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(GLOBALS:Map, parent(-1))
      1 |-> scope(
        "arr" |-> ARR:Val
        "k" |-> KARG:Int
        "total" |-> ACC:Int
        "element" |-> OLD:Val,
        parent(0)
      )
      =>
      -1 |-> builtinsScope
      0 |-> scope(GLOBALS, parent(-1))
      1 |-> scope(
        "arr" |-> ARR
        "k" |-> KARG
        "total" |-> qualifyingSumAcc(ACC, vCons(V, VS))
        "element" |-> ?FINAL:Val,
        parent(0)
      )
    </scopes>
    requires notBool "abs" in_keys(GLOBALS)
     andBool isInt(V)
     andBool intsOnly(VS)

  // End-to-end call of the exact translated function body.  PREFIX is
  // non-empty, k = len(PREFIX), and ARRAY = PREFIX ++ SUFFIX; this is a
  // decomposition of every input satisfying 1 <= k <= len(arr).
  claim
    <k>
      Call(
        closureVal(
          ("arr", "k", .ParamNames),
          Assign(Name("total"), Int(0))
          For(
            Name("element"),
            Subscript(
              Name("arr"),
              Slice(NoBound, Name("k"), NoBound)
            ),
            If(
              Compare(
                Call(Name("abs"), Name("element")),
                CmpOp("<", Int(100))
              ),
              AugAssign(Name("total"), "+", Name("element")),
              .Stmts
            )
          )
          Return(Name("total"))
          .Stmts,
          0
        ),
        list(
          valSeqConcat(
            vCons(HEAD:Val, PREFIX:ValSeq),
            SUFFIX:ValSeq
          )
        ),
        vsLen(vCons(HEAD, PREFIX))
      )
      =>
      qualifyingSumAcc(0, vCons(HEAD, PREFIX))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isInt(HEAD)
     andBool intsOnly(PREFIX)
     andBool intsOnly(SUFFIX)
     andBool (
       vsLen(vCons(HEAD, PREFIX)) +Int vsLen(SUFFIX)
       <=Int 100
     )
endmodule
