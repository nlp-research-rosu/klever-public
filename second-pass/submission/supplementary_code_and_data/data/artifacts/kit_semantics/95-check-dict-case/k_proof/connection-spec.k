requires "connection.k"

module CONNECTION-SPEC
  imports CONNECTION

  // Complete fixed-semantics result of the exact isinstance call site for an
  // arbitrary value and arbitrary following computation.
  claim [isinstance]:
    <k>
      #applyK(
        toCall(builtinV("isinstance")),
        (V:Val, typeV("str"), .Vals))
      ~> CONT:K
      =>
      isStringKey(V) ~> CONT
    </k>
    requires notBool isRefV(V)

  // Direct evidence that, after the discriminator narrows the true case to
  // the Str constructor, both frozen method rules retain arbitrary suffixes.
  claim [islower]:
    <k>
      #applyK(
        toCall(boundMethodV(str(CS:IntSeq), "islower")),
        .Vals)
      ~> CONT:K
      =>
      (hasLower(CS) andBool notBool hasUpper(CS)) ~> CONT
    </k>

  claim [isupper]:
    <k>
      #applyK(
        toCall(boundMethodV(str(CS:IntSeq), "isupper")),
        .Vals)
      ~> CONT:K
      =>
      (hasUpper(CS) andBool notBool hasLower(CS)) ~> CONT
    </k>
endmodule
