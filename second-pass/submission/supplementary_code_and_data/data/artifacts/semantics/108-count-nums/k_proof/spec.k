requires "verification.k"

module POSITIVE-LOOP-SPEC
  imports COUNT-NUMS-VERIFICATION-BASE

  claim <k> #while(Compare(Name("n"), CmpOp(">", Int(0))),
                    positiveLoopBody) => .K ... </k>
        <env> L:Int </env>
        <scopes>
          ... L |-> scope(
            ("n" |-> N:Int "total" |-> A:Int)
            => ("n" |-> 0
                "total" |-> positiveFold(N, A)),
            P:Parent)
          ...
        </scopes>
        requires N >=Int 0
endmodule

module NEGATIVE-LOOP-SPEC
  imports COUNT-NUMS-VERIFICATION-BASE

  claim <k> #while(Compare(Name("n"), CmpOp(">=", Int(10))),
                    negativeLoopBody) => .K ... </k>
        <env> L:Int </env>
        <scopes>
          ... L |-> scope(
            ("n" |-> N:Int "total" |-> A:Int)
            => ("n" |-> leadingDigit(N)
                "total" |-> negativeTotal(N, A)),
            P:Parent)
          ...
        </scopes>
        requires N >=Int 0
endmodule

module POSITIVE-FUNCTION-SPEC
  imports DIGIT-LOOP-LEMMAS

  claim
    <k> #applyK(toCall(positiveDigitClosure), (N:Int, .Vals))
      => positiveDigitSum(N) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
endmodule

module NEGATIVE-FUNCTION-SPEC
  imports DIGIT-LOOP-LEMMAS

  claim
    <k> #applyK(toCall(negativeDigitClosure), (N:Int, .Vals))
      => negativeDigitSum(N) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
endmodule

module SIGNED-FUNCTION-SPEC
  imports DIGIT-FUNCTION-LEMMAS

  claim
    <k> #applyK(toCall(signedDigitClosure), (N:Int, .Vals))
      => signedDigitSum(N) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(digitFunctionBindings, parent(-1))
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

module COUNT-LOOP-WITH-N-SPEC
  imports SIGNED-DIGIT-LEMMA

  claim <k> #loop(list(VS:ValSeq), Name("n"), countLoopBody)
          => .K ... </k>
        <env> L:Int </env>
        <scopes>
          ... 0 |-> scope(digitFunctionBindings, parent(-1))
              L |-> scope(
                ("arr" |-> list(ALL:ValSeq)
                 "count" |-> C:Int
                 "n" |-> OLD:Val)
                => ("arr" |-> list(ALL)
                    "count" |-> countFold(VS, C)
                    "n" |-> lastOr(VS, OLD)),
                parent(0))
          ...
        </scopes>
        requires L =/=Int 0 andBool allInts(VS)
endmodule

module COUNT-LOOP-SPEC
  imports COUNT-LOOP-WITH-N-LEMMA

  claim <k> #loop(list(.ValSeq), Name("n"), countLoopBody)
          => .K ... </k>
        <env> L:Int </env>
        <scopes>
          ... 0 |-> scope(digitFunctionBindings, parent(-1))
              L |-> scope(
                ("arr" |-> list(ALL:ValSeq) "count" |-> C:Int),
                parent(0))
          ...
        </scopes>
        requires L =/=Int 0

  claim <k> #loop(list(vCons(H:Val, REST:ValSeq)),
                   Name("n"), countLoopBody)
          => .K ... </k>
        <env> L:Int </env>
        <scopes>
          ... 0 |-> scope(digitFunctionBindings, parent(-1))
              L |-> scope(
                ("arr" |-> list(ALL:ValSeq) "count" |-> C:Int)
                => ("arr" |-> list(ALL)
                    "count" |-> countFold(vCons(H, REST), C)
                    "n" |-> lastOr(REST, H)),
                parent(0))
          ...
        </scopes>
        requires L =/=Int 0
         andBool isInt(H) andBool allInts(REST)
endmodule

module COUNT-NUMS-SPEC
  imports COUNT-NUMS-VERIFICATION

  claim
    <k> #applyK(toCall(countNumsClosure),
                (list(VS:ValSeq), .Vals))
      => countPositive(VS) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(digitFunctionBindings, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
endmodule
