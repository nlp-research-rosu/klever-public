requires "verification.k"

module SPEC
  imports TARGET-VERIFICATION

  // Inner structural induction: every finite code sequence is scanned.
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

  // Outer structural induction after a best score has been established.
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

  // Full entry theorem for an empty extension list.
  claim [entry-empty]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "Strongest_Extension",
            Params("class_name", "extensions"),
            STRONGEST-BODY
          )
          .Stmts
        )
      )
      ~> Call(
           Name("Strongest_Extension"),
           str(CLASS),
           list(.ValSeq),
           .Exprs
         )
      => expectedResult(CLASS, .ValSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "Strongest_Extension" |->
             closureVal(
               "class_name", "extensions", .ParamNames,
               STRONGEST-BODY,
               0
             ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Full entry theorem for every nonempty finite list of finite strings.
  claim [entry-nonempty]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "Strongest_Extension",
            Params("class_name", "extensions"),
            STRONGEST-BODY
          )
          .Stmts
        )
      )
      ~> Call(
           Name("Strongest_Extension"),
           str(CLASS),
           list(vCons(str(FIRST), RESTEXTS)),
           .Exprs
         )
      => expectedResult(
           CLASS,
           vCons(str(FIRST), RESTEXTS)
         )
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "Strongest_Extension" |->
             closureVal(
               "class_name", "extensions", .ParamNames,
               STRONGEST-BODY,
               0
             ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStrings(RESTEXTS)
endmodule
