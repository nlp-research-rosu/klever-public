requires "verification.k"

module SPEC-RULE-WITNESS-POSITIVE
  imports VERIFICATION

  // For every nonempty intended-domain list, size(L) is out of bounds. The
  // special #add simplification bypasses that #at and fabricates a successor.
  claim
    <k>
      #return(
        #add(
          #incPrefix(L, size(L)),
          pyList(
            ListItem(
              #add(
                #at(L, size(L)),
                pyInt(1))))))
      => .K
    </k>
    <env> .Map </env>
    <iter> noIter </iter>
    <result>
      noResult => result(#incPrefix(L, size(L) +Int 1))
    </result>
    requires size(L) >Int 0
endmodule
