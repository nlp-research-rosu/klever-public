requires "verification.k"

module CIRCULAR-SHIFT-SPEC-VACUITY
  imports CIRCULAR-SHIFT-VERIFICATION

  // Deliberately false: for the normal branch, demand prefix ++ suffix instead
  // of the implementation/specification's suffix ++ prefix.
  // Satisfying counterexample: X = 12345, SHIFT = 2, LEN = 5.
  // Correct result "45123"; mutated result "12345".
  claim [false-normal-result]:
    <k>
      Call(Name("circular_shift"), (X:Int, SHIFT:Int))
      =>
      applyBin(
        "+",
        doSlice(
          str(strToCodes(Int2String(X))),
          noB,
          someB(0 -Int SHIFT),
          noB
        ),
        doSlice(
          str(strToCodes(Int2String(X))),
          someB(0 -Int SHIFT),
          noB,
          noB
        )
      )
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("circular_shift" |-> circularShiftClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires LEN ==Int isLen(strToCodes(Int2String(X)))
     andBool SHIFT >=Int 0
     andBool SHIFT <=Int LEN
endmodule
