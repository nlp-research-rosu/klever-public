module MEDIAN-VERIFICATION
  imports MEDIAN-SEMANTICS

  // Independent reference function extracted from the supplied examples.
  // For odd sizes it selects n//2.  For even sizes it averages n//2 and
  // n//2+1, which is the only interpretation that yields the prompt's 15.0.
  syntax Val ::= promptMedian(Ints) [function]
               | promptMedianSorted(Ints) [function]

  rule promptMedian(IS) => promptMedianSorted(sortInts(IS))
  rule promptMedianSorted(ORDERED)
    => ifVal(
         intVal(lenInts(ORDERED) %Int 2),
         intVal(nthInt(ORDERED, lenInts(ORDERED) /Int 2)),
         floatVal(
           nthInt(ORDERED, lenInts(ORDERED) /Int 2)
             +Int nthInt(ORDERED, (lenInts(ORDERED) /Int 2) +Int 1),
           2))
endmodule
