requires "verification.k"

module CONNECTION-SPEC
  imports VERIFICATION-BASE

  // Datatype value-fidelity theorem for the guarded total projection.
  claim [projection-identity]:
    <k> V:Val => projectStrTotal(V) </k>
    requires isStringVal(V)

  // Universal fixed-semantics connection for the static-sort yield twin.
  claim [yield-connection]:
    <k>
      #iterYield(V:Val, list(VS))
      ~> #loopStep(Name("extension"), OUTER-BODY)
      => #bindTgt(Name("extension"), projectStrTotal(V))
         ~> OUTER-BODY
         ~> #loopLbl(
              #loop(
                list(VS),
                Name("extension"),
                OUTER-BODY
              )
            )
      ...
    </k>
    requires isStringVal(V)

  // Universal fixed-semantics connection for the complete inner-loop bridge.
  claim [inner-loop]:
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
          S:Int => S +Int extensionStrength(codesOf(STRING))
        )
        "character" |-> (
          str(OLDCHAR)
          => str(lastCharacter(codesOf(STRING), OLDCHAR))
        ),
        parent(0)
      )
      ...
    </scopes>
endmodule
