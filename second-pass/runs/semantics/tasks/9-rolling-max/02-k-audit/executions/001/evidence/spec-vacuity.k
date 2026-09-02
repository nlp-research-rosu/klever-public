requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation of ground-entry-witness: the actual last rolling
  // maximum for [3, 1, 4] is 4, not 5.
  claim [false-last-maximum]:
    <k> #loadAll(rollingMaxModule)
         ~> Call(
              Name("rolling_max"),
              (list(intsVS(iCons(3, iCons(1, iCons(4, .IntSeq))))), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0  |-> scope(("rolling_max" |->
                       closureVal(("numbers", .ParamNames), rollingMaxBody, 0)),
                    parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map =>
      (0 |-> list(vCons(3, vCons(3, vCons(5, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
