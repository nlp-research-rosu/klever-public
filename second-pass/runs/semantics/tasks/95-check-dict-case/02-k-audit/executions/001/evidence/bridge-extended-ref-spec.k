requires "verification.k"

module BRIDGE-EXTENDED-REF-SPEC
  imports CHECK-DICT-CASE-VERIFICATION

  // The candidate priority-30 splitter preempts the fixed priority-40 heap
  // dereference and classifies the reference itself as non-string.
  claim [extended-ref-to-string]:
    <k> #applyK(toCall(builtinV("isinstance")),
                (ref(7), typeV("str"), .Vals))
      =>
         false
    </k>
    <heap> 7 |-> str(iCons(97, .IntSeq)) </heap>
endmodule
