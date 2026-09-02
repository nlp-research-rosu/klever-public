requires "bridge-audit-base.k"

module BRIDGE-FIXED-REF-SPEC
  imports BRIDGE-AUDIT-BASE

  // Under the fixed semantics, builtin arguments that are heap references are
  // dereferenced before isinstance dispatch.
  claim [fixed-ref-to-string]:
    <k> #applyK(toCall(builtinV("isinstance")),
                (ref(7), typeV("str"), .Vals))
      =>
         true
    </k>
    <heap> 7 |-> str(iCons(97, .IntSeq)) </heap>
endmodule
