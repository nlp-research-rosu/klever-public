requires "verification.k"

module OUTER-CONNECTION-SPEC
  imports VERIFICATION

  // Universal connection theorem for the final outer-loop bridge.
  claim [outer-loop]:
    <k>
      #loop(list(VS), Name("extension"), OUTER-BODY)
      => .K
      ...
    </k>
    <env> L </env>
    <scopes>
      ...
      L |-> scope(
        "class_name" |-> str(CLASS)
        "extensions" |-> list(ALLEXTS)
        "strongest" |-> (
          str(BEST) => str(bestCodes(VS, BEST, BESTSCORE))
        )
        "best_strength" |-> (
          BESTSCORE:Int => bestScore(VS, BESTSCORE)
        )
        "extension" |-> (
          str(OLDEXT) => str(lastExtension(VS, OLDEXT))
        )
        "character" |-> (
          str(OLDCHAR)
          => str(lastCharacterAcross(VS, OLDCHAR))
        )
        "strength" |-> (
          OLDSTRENGTH:Int => lastStrength(VS, OLDSTRENGTH)
        ),
        parent(0)
      )
      ...
    </scopes>
    requires allStrings(VS)
endmodule
