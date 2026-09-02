requires "verification.k"

module SPEC-RULE-WITNESS-GROUND
  imports VERIFICATION

  // Ground instance L = [1] of the symbolic claim in
  // SPEC-RULE-WITNESS-POSITIVE. It exposes the competing inner #at reduction.
  claim
    <k>
      #return(
        #add(
          #incPrefix(ListItem(pyInt(1)), 1),
          pyList(
            ListItem(
              #add(
                #at(ListItem(pyInt(1)), 1),
                pyInt(1))))))
      => .K
    </k>
    <env> .Map </env>
    <iter> noIter </iter>
    <result>
      noResult => result(#incPrefix(ListItem(pyInt(1)), 2))
    </result>
endmodule
