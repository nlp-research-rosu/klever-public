requires "verification.k"

module SPEC
  imports VERIFICATION

  // Exhaustive symbolic proof of the recurrence defining the minimum.  These
  // claims cover every finite list: the length test is true or false, and in
  // the latter case the two endpoints are equal or unequal.
  claim <k>
          run(#smallestChangeBody, L, #smallestChangeBody) ~> KONT
          => finish(0) ~> KONT
        </k>
    requires size(L) <=Int 1

  claim <k>
          run(#smallestChangeBody, L, #smallestChangeBody) ~> KONT
          => recur(#smallestChangeBody, range(L, 1, 1),
                   #smallestChangeBody) ~> KONT
        </k>
    requires size(L) >Int 1
     andBool {L[0]}:>Int ==Int {L[-1]}:>Int

  claim <k>
          run(#smallestChangeBody, L, #smallestChangeBody) ~> KONT
          => recur(#smallestChangeBody, range(L, 1, 1),
                   #smallestChangeBody) ~> addResult(1) ~> KONT
        </k>
    requires size(L) >Int 1
     andBool notBool ({L[0]}:>Int ==Int {L[-1]}:>Int)

  // The independent mathematical specification has the same exhaustive
  // recurrence, establishing the correspondence used by the three program
  // claims above.
  claim <k> minimumPalindromeChanges(L) => 0 </k>
    requires size(L) <=Int 1

  claim <k>
          minimumPalindromeChanges(L)
          => minimumPalindromeChanges(range(L, 1, 1))
        </k>
    requires size(L) >Int 1
     andBool {L[0]}:>Int ==Int {L[-1]}:>Int

  claim <k>
          minimumPalindromeChanges(L)
          => 1 +Int minimumPalindromeChanges(range(L, 1, 1))
        </k>
    requires size(L) >Int 1
     andBool notBool ({L[0]}:>Int ==Int {L[-1]}:>Int)

  // The three examples from prompt.py additionally prove concrete executions
  // of the evaluator.  Full Module/FuncDef linkage is exercised by krun.
  claim <k>
          run(#smallestChangeBody,
               ListItem(1) ListItem(2) ListItem(3) ListItem(5)
               ListItem(4) ListItem(7) ListItem(9) ListItem(6),
               #smallestChangeBody)
          => finish(4)
        </k>

  claim <k>
          run(#smallestChangeBody,
               ListItem(1) ListItem(2) ListItem(3) ListItem(4)
               ListItem(3) ListItem(2) ListItem(2),
               #smallestChangeBody)
          => finish(1)
        </k>

  claim <k>
          run(#smallestChangeBody,
               ListItem(1) ListItem(2) ListItem(3)
               ListItem(2) ListItem(1),
               #smallestChangeBody)
          => finish(0)
        </k>
endmodule
