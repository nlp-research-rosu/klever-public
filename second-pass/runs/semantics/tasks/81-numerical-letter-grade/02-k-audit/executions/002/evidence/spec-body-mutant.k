requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION

  claim [empty]:
    <k> runGrades(.ValSeq) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>

  claim [a-plus]:
    <k> runGrades(vCons(F:Float, .ValSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map
      => 0 |-> list(vCons(letter("A+"), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    requires eqFour(F)

  claim [a]:
    <k> runGrades(vCons(F:Float, .ValSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map
      => 0 |-> list(vCons(letter("A"), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    requires notBool eqFour(F)
     andBool above(F, 3.7)

  claim [function-maps-all-numeric-grades]:
    <k> runGrades(numericValues(GS:NumericGrades))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(mappedAppend(.ValSeq, GS))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>

  claim [loop-maps-all-numeric-grades]:
    <k>
      #loop(
          list(numericValues(GS:NumericGrades)),
          Name("grade"),
          Assign(Name("grade"),
            Call(Name("float"), (Name("grade"), .Exprs)))
          numericalLetterGradeStep)
      ~> CONT:K
      =>
      CONT
    </k>
    <env> 1 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope
       1  |-> scope(
               "grade"  |-> OLD:Float
               "grades" |-> INPUT:Val
               "result" |-> ref(0),
               parent(0)))
      =>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope
       1  |-> scope(
               "grade"  |-> afterGradeValue(OLD, GS)
               "grades" |-> INPUT
               "result" |-> ref(0),
               parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      (0 |-> list(PREFIX:ValSeq) HP:Map)
      =>
      (0 |-> list(mappedAppend(PREFIX, GS)) HP)
    </heap>
    <heapLoc> _N:Int </heapLoc>
    <stack> _STACK:List </stack>
    <ret> noRet </ret>
    requires notBool (0 in_keys(HP))

endmodule
