requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop circularity.  The exact return and #endcall continuation remains in
  // place, so the claim covers the loop, Return, and the fixed frame pop.
  claim [loop-invariant]:
    <k>
      #loop(list(VS:ValSeq), Name("value"), sumSquaresLoopBody)
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
      =>
      sumSquaresAcc(VS, INDEX, ACC)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (SC:Map
       1 |-> scope(
         "lst" |-> INPUT:Val
         "result" |-> ACC:Int
         "index" |-> INDEX:Int
         "value" |-> CURRENT:Val,
         parent(0)))
      =>
      ?FINALSC:Map
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
      andBool INDEX >=Int 0
      andBool notBool (1 in_keys(SC))

  // Primary whole-program entry for a Python list object in the supplied heap
  // model.  The heap cell is unchanged, proving that the input is not mutated.
  claim [sum-squares]:
    <k>
      #loadAll(Module(sumSquaresDef))
      ~> Call(Name("sum_squares"), ref(H))
      =>
      sumSquaresAcc(VS, 0, 0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?GLOBALS:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> H:Int |-> list(VS) HEAP:Map </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
      andBool notBool (H in_keys(HEAP))

  // Equivalent read-only claim-input representation explicitly supported by
  // MPY-CORE for proofs.
  claim [sum-squares-bare]:
    <k>
      #loadAll(Module(sumSquaresDef))
      ~> Call(Name("sum_squares"), list(VS:ValSeq))
      =>
      sumSquaresAcc(VS, 0, 0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?GLOBALS:Map
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
