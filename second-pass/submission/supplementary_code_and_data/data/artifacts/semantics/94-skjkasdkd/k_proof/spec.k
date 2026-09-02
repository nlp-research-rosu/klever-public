requires "verification.k"

module SPEC
  imports VERIFICATION

  // Trial-division loop invariant.
  claim [prime-loop]:
    <k> #while(#primeCond, #primeBody) ~> K:K
      => K
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        ("number" |-> N:Int)
        ("divisor" |-> D:Int)
        ("prime" |-> B:Bool)
        REST:Map,
        P:Parent)
      =>
      SC
      L |-> scope(
        ("number" |-> N)
        ("divisor" |-> trialDivisor(N, D, B))
        ("prime" |-> trialPrime(N, D, B))
        REST,
        P)
    </scopes>
    requires D >=Int 2
      andBool (notBool B orBool N >=Int 2)
      andBool notBool ("number" in_keys(REST))
      andBool notBool ("divisor" in_keys(REST))
      andBool notBool ("prime" in_keys(REST))
      andBool notBool ("$cells" in_keys(REST))
      andBool notBool ("$cells" in_keys(
        ("number" |-> N)
        ("divisor" |-> D)
        ("prime" |-> B)
        REST))

  // Decimal digit accumulation loop invariant.
  claim [digit-loop]:
    <k> #while(#digitCond, #digitBody) ~> K:K
      => K
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        ("largest" |-> N:Int)
        ("digit_total" |-> A:Int)
        REST:Map,
        P:Parent)
      =>
      SC
      L |-> scope(
        ("largest" |-> 0)
        ("digit_total" |-> digitAcc(N, A))
        REST,
        P)
    </scopes>
    requires N >=Int 0
      andBool notBool ("largest" in_keys(REST))
      andBool notBool ("digit_total" in_keys(REST))
      andBool notBool ("$cells" in_keys(REST))
      andBool notBool ("$cells" in_keys(
        ("largest" |-> N)
        ("digit_total" |-> A)
        REST))

  // The list-loop invariant includes the fixed suffix of the function.  On
  // completion it returns to the caller, so temporary locals are unobservable.
  claim [scan-loop]:
    <k>
      #loop(list(asVals(IS:IntList)), Name("number"), #scanBody)
      ~> While(#digitCond, #digitBody)
      ~> Return(Name("digit_total"))
      ~> #endcall
      => digitSum(largestPrime(IS, CUR)) ~> CONT:K
    </k>
    <env> S:Int => CALLER:Int </env>
    <scopes>
      BASE:Map
      S |-> scope(
        ("largest" |-> CUR:Int)
        ("number" |-> OLDN:Int)
        ("divisor" |-> OLDD:Int)
        ("prime" |-> OLDB:Bool)
        ("digit_total" |-> 0)
        REST:Map,
        parent(0))
      => BASE
    </scopes>
    <scopeLoc> S +Int 1 => S </scopeLoc>
    <stack>
      ListItem(frame(CONT, CALLER, S)) STACK:List
      => STACK
    </stack>
    <ret> noRet </ret>
    requires CUR >=Int 0
      andBool notBool ("largest" in_keys(REST))
      andBool notBool ("number" in_keys(REST))
      andBool notBool ("divisor" in_keys(REST))
      andBool notBool ("prime" in_keys(REST))
      andBool notBool ("digit_total" in_keys(REST))
      andBool notBool ("$cells" in_keys(REST))
      andBool notBool ("$cells" in_keys(
        ("largest" |-> CUR)
        ("number" |-> OLDN)
        ("divisor" |-> OLDD)
        ("prime" |-> OLDB)
        ("digit_total" |-> 0)
        REST))
      andBool notBool (S in_keys(BASE))

  // Function-call theorem.  The bounded entry prefix reaches scan-loop; the
  // proven scan-loop invariant then discharges the unbounded computation.
  claim [entry-prefix]:
    <k>
      #applyK(
        toCall(closureVal(
          ("lst", .ParamNames),
          #functionBody,
          0)),
        (list(asVals(IS:IntList)), .Vals))
      => digitSum(largestPrime(IS, 0))
    </k>
    <env> 0 </env>
    <scopes> MOD:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    requires notBool (1 in_keys(MOD))

  // End-to-end theorem: the translated function, loaded into the supplied
  // Python semantics, returns the digit sum of the largest prime in any
  // integer list (or zero when no prime exists).
  claim [main-correct]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("skjkasdkd"), (list(asVals(IS:IntList)), .Exprs))
      => digitSum(largestPrime(IS, 0))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "skjkasdkd" |-> closureVal(
          ("lst", .ParamNames),
          #functionBody,
          0),
        parent(-1))
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
