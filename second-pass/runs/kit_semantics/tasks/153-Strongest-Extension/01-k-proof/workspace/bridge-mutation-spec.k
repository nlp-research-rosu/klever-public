requires "verification.k"

module BRIDGE-MUTATION-SPEC
  imports VERIFICATION-BASE

  // Deliberately wrong inner-loop summary (+1).
  claim [inner-wrong-value]:
    <k>
      #loop(STRING:Str, Name("character"), INNER-BODY)
      => .K
      ...
    </k>
    <env> L </env>
    <scopes>
      ...
      L |-> scope(
        "class_name" |-> str(CLASS)
        "extensions" |-> list(ALLEXTS)
        "strongest" |-> str(BEST)
        "best_strength" |-> BESTVAL:Val
        "extension" |-> str(EXT)
        "strength" |-> (
          S:Int
          => S +Int extensionStrength(codesOf(STRING)) +Int 1
        )
        "character" |-> (
          str(OLDCHAR)
          => str(lastCharacter(codesOf(STRING), OLDCHAR))
        ),
        parent(0)
      )
      ...
    </scopes>

  // Deliberately wrong value projection for a concrete "A" yield.
  claim [yield-wrong-value]:
    <k>
      #iterYield(
        str(iCons(65, .IntSeq)),
        list(.ValSeq)
      )
      ~> #loopStep(Name("extension"), OUTER-BODY)
      => #bindTgt(Name("extension"), str(.IntSeq))
         ~> OUTER-BODY
         ~> #loopLbl(
              #loop(
                list(.ValSeq),
                Name("extension"),
                OUTER-BODY
              )
            )
      ...
    </k>
endmodule
