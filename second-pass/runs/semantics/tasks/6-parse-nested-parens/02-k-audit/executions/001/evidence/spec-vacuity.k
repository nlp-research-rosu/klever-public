requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [parse-loop]:
    <k> #loop(str(S:IntSeq), Name("char"), parseLoopBody) => .K ... </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        ("paren_string" |-> INPUT:Val)
        ("result" |-> ref(0))
        ("depth" |-> (D:Int => scanDepth(scanParens(S, D, M, VS))))
        ("maximum" |-> (M:Int => scanMaximum(scanParens(S, D, M, VS))))
        ("char" |-> (OLD:Val => finalChar(S, OLD))),
        parent(0))
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> 0 |-> list(VS:ValSeq => scanValues(scanParens(S, D, M, VS))) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ST:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires parenInput(S)

  // Deliberately false: prepend 999 to the actual result sequence.
  // S = .IntSeq satisfies the precondition; the real copied body yields [0],
  // whereas this destination requires [999, 0].
  claim [false-result-prefix]:
    <k> Call(parseNestedParensClosure, str(S:IntSeq)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(999, parsedParens(S))) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires parenInput(S)
endmodule
