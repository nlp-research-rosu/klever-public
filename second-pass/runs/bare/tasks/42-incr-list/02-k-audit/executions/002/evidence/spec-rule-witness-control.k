requires "verification.k"

module SPEC-RULE-WITNESS-CONTROL
  imports VERIFICATION

  // Without the outer shortcut, the same symbolic out-of-bounds access has no
  // result.
  claim
    <k>
      #return(#at(L, size(L)))
      => .K
    </k>
    <env> .Map </env>
    <iter> noIter </iter>
    <result>
      noResult => result(pyInt(999))
    </result>
    requires size(L) >Int 0
endmodule
