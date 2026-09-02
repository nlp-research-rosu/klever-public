requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // Compile-time abbreviations for the exact translated source blocks.
  // These are macros, so no execution rule for the program is added.
  syntax Stmts ::= "INNER-BODY" [macro]
  rule INNER-BODY
    => If(
         Call(Attribute(Name("character"), "isupper"), .Exprs),
         AugAssign(Name("strength"), "+", Int(1)) .Stmts,
         If(
           Call(Attribute(Name("character"), "islower"), .Exprs),
           AugAssign(Name("strength"), "-", Int(1)) .Stmts,
           .Stmts
         ) .Stmts
       ) .Stmts

  syntax Stmts ::= "OUTER-BODY" [macro]
  rule OUTER-BODY
    => Assign(Name("strength"), Int(0))
       For(Name("character"), Name("extension"), INNER-BODY)
       If(
         BoolOp(
           "or",
           Compare(Name("best_strength"), CmpOp("is", NoneVal)),
           Compare(
             Name("strength"),
             CmpOp(">", Name("best_strength"))
           ),
           .Exprs
         ),
         Assign(Name("strongest"), Name("extension"))
         Assign(Name("best_strength"), Name("strength"))
         .Stmts,
         .Stmts
       )
       .Stmts

  syntax Stmts ::= "STRONGEST-BODY" [macro]
  rule STRONGEST-BODY
    => Assign(Name("strongest"), Str(""))
       Assign(Name("best_strength"), NoneVal)
       Assign(Name("extension"), Str(""))
       Assign(Name("character"), Str(""))
       For(Name("extension"), Name("extensions"), OUTER-BODY)
       Return(
         BinOp(
           "+",
           BinOp("+", Name("class_name"), Str(".")),
           Name("strongest")
         )
       )
       .Stmts

  // The score defined by the prompt, over the reference semantics' code
  // sequence model. The three guarded cases are exhaustive and disjoint.
  syntax Int ::= charStrength(Int) [function, total]
  rule charStrength(C) => 1
    requires isUpperC(C)
  rule charStrength(C) => 0 -Int 1
    requires isLowerC(C)
  rule charStrength(C) => 0
    requires notBool isUpperC(C) andBool notBool isLowerC(C)

  syntax Int ::= extensionStrength(IntSeq) [function, total]
  rule extensionStrength(.IntSeq) => 0
  rule extensionStrength(iCons(C, CS))
    => charStrength(C) +Int extensionStrength(CS)

  // The character variable retains its old value on an empty string and
  // otherwise retains the final one-character string visited by the loop.
  syntax IntSeq ::= lastCharacter(IntSeq, IntSeq) [function, total]
  rule lastCharacter(.IntSeq, OLD) => OLD
  rule lastCharacter(iCons(C, CS), OLD)
    => lastCharacter(CS, iCons(C, .IntSeq))

  syntax Bool ::= isStringVal(Val) [function, total]
  rule isStringVal(_:Str) => true
  rule isStringVal(_:Val) => false [owise]

  syntax Bool ::= allStrings(ValSeq) [function, total]
  rule allStrings(.ValSeq) => true
  rule allStrings(vCons(V, VS))
    => isStringVal(V) andBool allStrings(VS)

  // Guarded total twin of K's partial Val-to-Str subsort projection. It is
  // an identity on Str and has no evaluator that can invent a string value.
  syntax Bool ::= definedProjectStr(Val) [function, total]
  rule definedProjectStr(V) => isStringVal(V)

  syntax Str ::= projectStrTotal(Val)
    [function, total, symbol(projectStrTotal), no-evaluators]

  rule #Ceil({@V:Val}:>Str)
    => (
         { definedProjectStr(@V) #Equals true }
         #And #Ceil(@V)
       )
    [simplification]

  rule projectStrTotal(V:Val) => {V}:>Str
    requires definedProjectStr(V)
    [concrete, simplification(10), preserves-definedness]

  rule {V:Val}:>Str => projectStrTotal(V)
    requires definedProjectStr(V)
    [symbolic(V), simplification, preserves-definedness]

  rule projectStrTotal(S:Str) => S
    [simplification]

  rule projectStrTotal(projectStrTotal(V)) => projectStrTotal(V)
    [simplification]

  // Exact datatype characterization of the identity projection.
  rule { @V:Val #Equals projectStrTotal(@V) }
    => { isStringVal(@V) #Equals true }
    [simplification]

  rule { @V:Val #Equals str(codesProject(@V)) }
    => { isStringVal(@V) #Equals true }
    [simplification]

  syntax IntSeq ::= codesOf(Str) [function, total]
  rule codesOf(str(CS)) => CS

  syntax IntSeq ::= codesProject(Val)
    [function, total, no-evaluators]
  rule codesProject(str(CS)) => CS

  rule projectStrTotal(V:Val) => str(codesProject(V))
    requires isStringVal(V)
    [symbolic(V), simplification(20), preserves-definedness]

  // Exact left-to-right scan summaries. Strict comparison preserves the
  // earlier extension on ties, matching the source program.
  syntax IntSeq ::= bestCodes(ValSeq, IntSeq, Int) [function]
  rule bestCodes(.ValSeq, BEST, _BESTSCORE) => BEST
  rule bestCodes(vCons(V, VS), _BEST, BESTSCORE)
    => bestCodes(
         VS,
         codesProject(V),
         extensionStrength(codesProject(V))
       )
    requires isStringVal(V)
      andBool extensionStrength(codesProject(V)) >Int BESTSCORE
    [simplification]
  rule bestCodes(vCons(V, VS), BEST, BESTSCORE)
    => bestCodes(VS, BEST, BESTSCORE)
    requires isStringVal(V)
      andBool (
        (extensionStrength(codesProject(V)) >Int BESTSCORE)
        ==Bool false
      )
    [simplification]

  syntax Int ::= bestScore(ValSeq, Int) [function]
  rule bestScore(.ValSeq, BESTSCORE) => BESTSCORE
  rule bestScore(vCons(V, VS), BESTSCORE)
    => bestScore(
         VS,
         extensionStrength(codesProject(V))
       )
    requires isStringVal(V)
      andBool extensionStrength(codesProject(V)) >Int BESTSCORE
    [simplification]
  rule bestScore(vCons(V, VS), BESTSCORE)
    => bestScore(VS, BESTSCORE)
    requires isStringVal(V)
      andBool (
        (extensionStrength(codesProject(V)) >Int BESTSCORE)
        ==Bool false
      )
    [simplification]

  // Exact summaries for the loop variables that remain in the Python frame.
  syntax IntSeq ::= lastExtension(ValSeq, IntSeq) [function]
  rule lastExtension(.ValSeq, OLD) => OLD
  rule lastExtension(vCons(V, VS), _OLD)
    => lastExtension(VS, codesProject(V))
    requires isStringVal(V)

  syntax Int ::= lastStrength(ValSeq, Int) [function]
  rule lastStrength(.ValSeq, OLD) => OLD
  rule lastStrength(vCons(V, VS), _OLD)
    => lastStrength(
         VS,
         extensionStrength(codesProject(V))
       )
    requires isStringVal(V)

  syntax IntSeq ::= lastCharacterAcross(ValSeq, IntSeq) [function]
  rule lastCharacterAcross(.ValSeq, OLD) => OLD
  rule lastCharacterAcross(vCons(V, VS), OLD)
    => lastCharacterAcross(
         VS,
         lastCharacter(codesProject(V), OLD)
       )
    requires isStringVal(V)

  // Whole-function mathematical result. The empty-list case is the
  // implementation's explicit, total extension of the prompt.
  syntax Str ::= expectedResult(IntSeq, ValSeq) [function]
  rule expectedResult(CLASS, .ValSeq)
    => str(
         seqConcat(
           seqConcat(CLASS, iCons(46, .IntSeq)),
           .IntSeq
         )
       )
  rule expectedResult(CLASS, vCons(str(CS), VS))
    => str(
         seqConcat(
           seqConcat(CLASS, iCons(46, .IntSeq)),
           bestCodes(VS, CS, extensionStrength(CS))
         )
       )
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // Connection-backed static-sort twin of the fixed
  // #iterYield/#loopStep transition.
  rule <k>
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
    [priority(40)]

  // Exact inner-loop bridge. CONNECTION-SPEC.inner-loop proves this complete
  // transition under VERIFICATION-BASE, which does not import this rule.
  rule <k>
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
             => S +Int extensionStrength(codesOf(STRING))
           )
           "character" |-> (
             str(OLDCHAR)
             => str(lastCharacter(codesOf(STRING), OLDCHAR))
           ),
           parent(0)
         )
         ...
       </scopes>
    [priority(30)]
endmodule

module TARGET-VERIFICATION
  imports VERIFICATION

  // Exact outer-loop bridge. OUTER-CONNECTION-SPEC.outer-loop proves this
  // transition under VERIFICATION, before this rule is imported.
  rule <k>
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
             OLDSTRENGTH:Int
             => lastStrength(VS, OLDSTRENGTH)
           ),
           parent(0)
         )
         ...
       </scopes>
    requires allStrings(VS)
    [priority(20)]
endmodule
