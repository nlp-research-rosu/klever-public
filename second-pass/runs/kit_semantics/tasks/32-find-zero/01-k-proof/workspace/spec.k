requires "verification.k"

module SPEC-CONNECTION
  imports VERIFICATION-BASE

  // Constructor-split circularities for the unbounded coefficient fold in
  // poly.  They preserve an arbitrary continuation and all framed state.
  claim [poly-loop-empty]:
    <k>
      #loop(list(numVals(.NumSeq)), Name("coeff"), polyStep)
      => .K ...
    </k>
    <env> L </env>
    <scopes>
      BASE:Map
      (L |-> scope(
        .Map
          [ "xs" <- XSV:Val ]
          [ "value" <- (A:Float => polyAcc(.NumSeq, X, A, P)) ]
          [ "power" <- (P:Float => polyPower(.NumSeq, X, P)) ]
          [ "x" <- X:Float ]
          [ "coeff" <- (C:Val => polyLast(.NumSeq, C)) ],
        PAR:Parent))
    </scopes>
    <scopeLoc> SL </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HL </heapLoc>
    <stack> REST:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool L in_keys(BASE)

  claim [poly-loop-int]:
    <k>
      #loop(list(numVals(nInt(I:Int, NS:NumSeq))), Name("coeff"), polyStep)
      => .K ...
    </k>
    <env> L </env>
    <scopes>
      BASE:Map
      (L |-> scope(
        .Map
          [ "xs" <- XSV:Val ]
          [ "value" <- (A:Float => polyAcc(nInt(I, NS), X, A, P)) ]
          [ "power" <- (P:Float => polyPower(nInt(I, NS), X, P)) ]
          [ "x" <- X:Float ]
          [ "coeff" <- (C:Val => polyLast(nInt(I, NS), C)) ],
        PAR:Parent))
    </scopes>
    <scopeLoc> SL </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HL </heapLoc>
    <stack> REST:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool L in_keys(BASE)

  claim [poly-loop-float]:
    <k>
      #loop(list(numVals(nFloat(F:Float, NS:NumSeq))), Name("coeff"), polyStep)
      => .K ...
    </k>
    <env> L </env>
    <scopes>
      BASE:Map
      (L |-> scope(
        .Map
          [ "xs" <- XSV:Val ]
          [ "value" <- (A:Float => polyAcc(nFloat(F, NS), X, A, P)) ]
          [ "power" <- (P:Float => polyPower(nFloat(F, NS), X, P)) ]
          [ "x" <- X:Float ]
          [ "coeff" <- (C:Val => polyLast(nFloat(F, NS), C)) ],
        PAR:Parent))
    </scopes>
    <scopeLoc> SL </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HL </heapLoc>
    <stack> REST:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool L in_keys(BASE)

  // Circularity for the root-bracketing loop.  It stops at the exact
  // fixed-semantics head of the following bisection loop.
  claim [expand-loop]:
    <k>
      #while(expandCond, expandBody)
      ~> (While(bisectCond, bisectBody)
          Return(Name("begin")) .Stmts)
      ~> #endcall
      =>
      (While(bisectCond, bisectBody)
       Return(Name("begin")) .Stmts)
      ~> #endcall
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> scope(
        .Map
          [ "poly" <- closureVal(("xs", "x"), polyBody, 0) ]
          [ "find_zero" <- closureVal("xs", findZeroBody, 0) ],
        parent(-1)))
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map
          [ "xs" <- list(numVals(NS:NumSeq)) ]
          [ "begin" <- B:Float ]
          [ "end" <- E:Float ]
          [ "center" <- C:Float ],
        parent(0)))
      =>
      (0 |-> scope(
        .Map
          [ "poly" <- closureVal(("xs", "x"), polyBody, 0) ]
          [ "find_zero" <- closureVal("xs", findZeroBody, 0) ],
        parent(-1)))
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map
          [ "xs" <- list(numVals(NS)) ]
          [ "begin" <- bracketBegin(NS, B, E) ]
          [ "end" <- bracketEnd(NS, B, E) ]
          [ "center" <- C ],
        parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HL </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validCoeffs(NS)

  // The fixed semantics exposes a statement-list tail one statement at a
  // time.  This generic connection contains no program summary.
  claim [bisect-head]:
    <k>
      (While(bisectCond, bisectBody)
       Return(Name("begin")) .Stmts)
      ~> #endcall
      =>
      #while(bisectCond, bisectBody)
      ~> (Return(Name("begin")) .Stmts)
      ~> #endcall
    </k>
    <env> ENV </env>
    <scopes> SCOPES </scopes>
    <scopeLoc> SL </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HL </heapLoc>
    <stack> STACK </stack>
    <ret> RET </ret>
    <exc> EXC </exc>
    <exit-code> 0 </exit-code>

  // Circularity for the unbounded bisection loop and its exact return suffix.
  claim [bisect-loop]:
    <k>
      #while(bisectCond, bisectBody)
      ~> (Return(Name("begin")) .Stmts)
      ~> #endcall
      => bisectFrom(NS, B, E)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(
        .Map
          [ "poly" <- closureVal(("xs", "x"), polyBody, 0) ]
          [ "find_zero" <- closureVal("xs", findZeroBody, 0) ],
        parent(-1)))
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map
          [ "xs" <- list(numVals(NS:NumSeq)) ]
          [ "begin" <- B:Float ]
          [ "end" <- E:Float ]
          [ "center" <- C:Float ],
        parent(0)))
      =>
         (0 |-> scope(
           .Map
             [ "poly" <- closureVal(("xs", "x"), polyBody, 0) ]
             [ "find_zero" <- closureVal("xs", findZeroBody, 0) ],
           parent(-1)))
         (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HL </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validCoeffs(NS)

endmodule

module SPEC
  imports VERIFICATION-BASE

  // Prefix 1: exact module loading, name resolution, and argument evaluation.
  claim [find-load]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("find_zero"), (list(numVals(NS:NumSeq)), .Exprs))
      => #applyK(
           toCall(closureVal("xs", findZeroBody, 0)),
           (list(numVals(NS)), .Vals))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |-> scope(
        .Map
          [ "poly" <- closureVal(("xs", "x"), polyBody, 0) ]
          [ "find_zero" <- closureVal("xs", findZeroBody, 0) ],
        parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validCoeffs(NS)

  // Prefix 2: exact closure application, parameter binding, and initialization
  // through the loop head used by SPEC-CONNECTION.expand-loop.
  claim [find-init]:
    <k>
      #applyK(
        toCall(closureVal("xs", findZeroBody, 0)),
        (list(numVals(NS:NumSeq)), .Vals))
      =>
      #while(expandCond, expandBody)
      ~> (While(bisectCond, bisectBody)
          Return(Name("begin")) .Stmts)
      ~> #endcall
    </k>
    <env> 0 => 1 </env>
    <scopes>
      (0 |-> scope(
        .Map
          [ "poly" <- closureVal(("xs", "x"), polyBody, 0) ]
          [ "find_zero" <- closureVal("xs", findZeroBody, 0) ],
        parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |-> scope(
        .Map
          [ "poly" <- closureVal(("xs", "x"), polyBody, 0) ]
          [ "find_zero" <- closureVal("xs", findZeroBody, 0) ],
        parent(-1)))
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map
          [ "xs" <- list(numVals(NS)) ]
          [ "begin" <-
              divII(vsLen(numVals(NS)), 0 -Int vsLen(numVals(NS))) ]
          [ "end" <- divII(vsLen(numVals(NS)), vsLen(numVals(NS))) ]
          [ "center" <- 0.0 ],
        parent(0)))
    </scopes>
    <scopeLoc> 1 => 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      .List
      => ListItem(frame(.K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validCoeffs(NS)
endmodule
