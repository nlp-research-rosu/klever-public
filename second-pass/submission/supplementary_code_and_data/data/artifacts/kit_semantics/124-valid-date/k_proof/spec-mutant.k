requires "verification-mutant.k"

module SPEC-MUTANT
  imports VERIFICATION

  // Validation scope:
  // - boundary: load the exact translated module, look up valid_date, execute
  //   its closure body, and return to the module continuation;
  // - domain: every MPY string value str(CS);
  // - observable final state: the returned Bool plus clean call-control cells;
  // - property: validDateResult is true exactly for mm-dd-yyyy strings whose
  //   month/day pair obeys the limits in prompt.py.
  claim [valid-date-10]:
    <k>
      #loadAll(validDateProgram)
        ~> Call(Name("valid_date"),
             str(iCons(C0:Int,
                 iCons(C1:Int,
                 iCons(C2:Int,
                 iCons(C3:Int,
                 iCons(C4:Int,
                 iCons(C5:Int,
                 iCons(C6:Int,
                 iCons(C7:Int,
                 iCons(C8:Int,
                 iCons(C9:Int, .IntSeq))))))))))))
      => ?R:Bool
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool
      validDateResult(
        iCons(C0,
        iCons(C1,
        iCons(C2,
        iCons(C3,
        iCons(C4,
        iCons(C5,
        iCons(C6,
        iCons(C7,
        iCons(C8,
        iCons(C9, .IntSeq)))))))))))

  claim [valid-date-non10]:
    <k>
      #loadAll(validDateProgram)
        ~> Call(Name("valid_date"), str(CS:IntSeq))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isLen(CS) =/=Int 10
endmodule
