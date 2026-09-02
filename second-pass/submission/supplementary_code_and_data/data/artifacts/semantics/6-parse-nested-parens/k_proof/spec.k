requires "verification.k"

module SPEC
  imports VERIFICATION

  // Inductive loop invariant.  S is the unconsumed suffix, D/M are the
  // current group's depth/maximum, and VS contains completed group maxima.
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

  // Universal target theorem: execute the exact solution closure on any
  // semantic string and return precisely the mathematical scan result.
  claim [parse-nested-parens]:
    <k> Call(parseNestedParensClosure, str(S:IntSeq)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(parsedParens(S)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires parenInput(S)
endmodule
