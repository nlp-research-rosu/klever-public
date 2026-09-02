requires "reference-semantics/semantics.k"

module STRONGEST-EXTENSION-VERIFICATION
  imports MPY

  // Mathematical strength: +1 per ASCII uppercase code and -1 per ASCII
  // lowercase code.  The supplied semantics models strings as ASCII IntSeqs.
  syntax Int ::= charContribution(Int) [function, total]
               | strengthAcc(IntSeq, Int) [function, total]
               | extensionStrength(IntSeq) [function, total]

  rule charContribution(C:Int)
    => (#if isUpperC(C) andBool notBool isLowerC(C)
        #then 1 #else 0 #fi)
       -Int
       (#if isLowerC(C) andBool notBool isUpperC(C)
        #then 1 #else 0 #fi)
  rule strengthAcc(.IntSeq, ACC:Int) => ACC
  rule strengthAcc(iCons(C:Int, REST:IntSeq), ACC:Int)
    => strengthAcc(REST, ACC +Int charContribution(C))
  rule extensionStrength(CS:IntSeq) => strengthAcc(CS, 0)

  syntax IntSeq ::= lastCharacter(IntSeq, IntSeq) [function, total]
  rule lastCharacter(.IntSeq, PREV:IntSeq) => PREV
  rule lastCharacter(iCons(C:Int, REST:IntSeq), _:IntSeq)
    => lastCharacter(REST, iCons(C, .IntSeq))

  // Stable first-maximum fold over extension names.
  syntax IntSeq ::= bestExtension(ValSeq, IntSeq, Int) [function, total]
                  | lastExtension(ValSeq, IntSeq) [function, total]
  syntax Int ::= bestStrength(ValSeq, IntSeq, Int) [function, total]

  rule bestExtension(.ValSeq, BEST:IntSeq, _:Int) => BEST
  rule bestExtension(vCons(str(CS:IntSeq), REST:ValSeq), _:IntSeq, BS:Int)
    => bestExtension(REST, CS, extensionStrength(CS))
    requires extensionStrength(CS) >Int BS
  rule bestExtension(vCons(str(CS:IntSeq), REST:ValSeq), BEST:IntSeq, BS:Int)
    => bestExtension(REST, BEST, BS)
    requires extensionStrength(CS) <=Int BS

  rule bestStrength(.ValSeq, _:IntSeq, BS:Int) => BS
  rule bestStrength(vCons(str(CS:IntSeq), REST:ValSeq), _:IntSeq, BS:Int)
    => bestStrength(REST, CS, extensionStrength(CS))
    requires extensionStrength(CS) >Int BS
  rule bestStrength(vCons(str(CS:IntSeq), REST:ValSeq), BEST:IntSeq, BS:Int)
    => bestStrength(REST, BEST, BS)
    requires extensionStrength(CS) <=Int BS

  rule lastExtension(.ValSeq, PREV:IntSeq) => PREV
  rule lastExtension(vCons(str(CS:IntSeq), REST:ValSeq), _:IntSeq)
    => lastExtension(REST, CS)

  // Exact AST bodies emitted from solution.py.
  syntax Stmts ::= "characterStrengthBody" [function]
                 | "extensionStrengthBody" [function]
                 | "selectionLoopBody" [function]
                 | "strongestExtensionBody" [function]

  rule characterStrengthBody =>
    If(Call(Attribute(Name("character"), "isupper"), .Exprs),
      AugAssign(Name("score"), "+", Int(1)),
      .Stmts)
    If(Call(Attribute(Name("character"), "islower"), .Exprs),
      AugAssign(Name("score"), "-", Int(1)),
      .Stmts)

  rule extensionStrengthBody =>
    Assign(Name("score"), Int(0))
    Assign(Name("character"), Str(""))
    For(Name("character"), Name("extension"), characterStrengthBody)
    Return(Name("score"))

  rule selectionLoopBody =>
    Assign(Name("score"), Call(Name("_extension_strength"), Name("extension")))
    If(Compare(Name("score"), CmpOp(">", Name("strongest_strength"))),
      Assign(Name("strongest"), Name("extension"))
      Assign(Name("strongest_strength"), Name("score")),
      .Stmts)

  rule strongestExtensionBody =>
    Assign(Name("strongest"), Subscript(Name("extensions"), Int(0)))
    Assign(Name("strongest_strength"),
      Call(Name("_extension_strength"), Name("strongest")))
    Assign(Name("extension"), Name("strongest"))
    Assign(Name("score"), Name("strongest_strength"))
    For(Name("extension"), Name("extensions"), selectionLoopBody)
    Return(BinOp("+",
      BinOp("+", Name("class_name"), Str(".")),
      Name("strongest")))

  syntax Scope ::= "solutionScope" [function]
  rule solutionScope =>
    scope(
      .Map
        [ "_extension_strength" <-
          closureVal(("extension", .ParamNames), extensionStrengthBody, 0) ]
        [ "Strongest_Extension" <-
          closureVal(("class_name", "extensions", .ParamNames),
                     strongestExtensionBody, 0) ],
      parent(-1))
endmodule

// Stage 1: use the character-loop theorem after proving it in the base module.
module STRONGEST-EXTENSION-WITH-CHAR-LOOP-LEMMA
  imports STRONGEST-EXTENSION-VERIFICATION

  rule
    <k>
      #loop(
        str(iCons(CURRENT:Int, REST:IntSeq)),
        Name("character"),
        BODY:Stmts)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      SCOPES:Map
      L |-> scope(
        ("extension" |-> str(ALL:IntSeq))
        ("score" |-> ACC:Int)
        ("character" |-> str(PREV:IntSeq)),
        PARENT:Parent)
    =>
      SCOPES
      L |-> scope(
        ("extension" |-> str(ALL))
        ("score" |->
          strengthAcc(iCons(CURRENT, REST), ACC))
        ("character" |->
          str(lastCharacter(iCons(CURRENT, REST), PREV))),
        PARENT)
    </scopes>
    requires BODY ==K characterStrengthBody
    [priority(40)]
endmodule

// Stage 2: use the proved helper theorem while verifying the outer loop.
module STRONGEST-EXTENSION-WITH-STRENGTH-LEMMA
  imports STRONGEST-EXTENSION-WITH-CHAR-LOOP-LEMMA

  rule
    <k>
      Call(Name("_extension_strength"), Name(X:String))
      => extensionStrength(CS)
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope((X |-> str(CS:IntSeq)) _REST:Map, _P:Parent)
      ...
    </scopes>
    [priority(40)]

  rule <k>
    #applyK(
      toCall(closureVal(("extension", .ParamNames), BODY:Stmts, 0)),
      (str(CS:IntSeq), .Vals))
    => extensionStrength(CS)
    ...
  </k>
  requires BODY ==K extensionStrengthBody
  [priority(40)]
endmodule

// Stage 3: use both proved loop summaries for the symbolic three-name theorem.
module STRONGEST-EXTENSION-WITH-LOOP-LEMMAS
  imports STRONGEST-EXTENSION-WITH-STRENGTH-LEMMA

  rule
    <k>
      #loop(
        list(vCons(
          str(E1:IntSeq),
          vCons(str(E2:IntSeq),
          vCons(str(E3:IntSeq), .ValSeq)))),
        Name("extension"),
        BODY:Stmts)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> MODULESCOPE:Scope)
      (-1 |-> BUILTINSSCOPE:Scope)
      (1 |-> scope(
        ("class_name" |-> str(CLASS:IntSeq))
        ("extensions" |-> list(ALL:ValSeq))
        ("strongest" |-> str(BEST:IntSeq))
        ("strongest_strength" |-> BESTS:Int)
        ("extension" |-> str(LAST:IntSeq))
        ("score" |-> SCORE:Int),
        parent(0)))
    =>
      (0 |-> MODULESCOPE)
      (-1 |-> BUILTINSSCOPE)
      (1 |-> scope(
        ("class_name" |-> str(CLASS))
        ("extensions" |-> list(ALL))
        ("strongest" |->
          str(bestExtension(
            vCons(str(E1), vCons(str(E2), vCons(str(E3), .ValSeq))),
            BEST,
            BESTS)))
        ("strongest_strength" |->
          bestStrength(
            vCons(str(E1), vCons(str(E2), vCons(str(E3), .ValSeq))),
            BEST,
            BESTS))
        ("extension" |->
          str(lastExtension(
            vCons(str(E1), vCons(str(E2), vCons(str(E3), .ValSeq))),
            LAST)))
        ("score" |->
          extensionStrength(
            lastExtension(
              vCons(str(E1), vCons(str(E2), vCons(str(E3), .ValSeq))),
              LAST))),
        parent(0)))
    </scopes>
    requires BODY ==K selectionLoopBody
     andBool MODULESCOPE ==K solutionScope
     andBool BUILTINSSCOPE ==K builtinsScope
     andBool SCORE ==Int extensionStrength(LAST)
    [priority(40)]
endmodule
