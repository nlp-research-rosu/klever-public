requires "reference-semantics/semantics.k"

module VOWELS-BASE
  imports MPY

  // A Boolean contributes one to Python's integer result exactly when true.
  syntax Int ::= boolToInt(Bool) [function, total]
  rule boolToInt(B:Bool) => #if B #then 1 #else 0 #fi

  // Count ordinary vowels in the already lower-cased loop input.
  syntax Int ::= ordinaryVowels(IntSeq) [function, total]
  rule ordinaryVowels(.IntSeq) => 0
  rule ordinaryVowels(iCons(C:Int, REST:IntSeq))
    => boolToInt(
         strContains(
           iCons(C, .IntSeq),
           iCons(97, iCons(101, iCons(105, iCons(111, iCons(117, .IntSeq)))))
         )
       ) +Int ordinaryVowels(REST)

  // The accumulator is overwritten on every character, so at loop exit it
  // says whether the lower-cased word's final character is y.
  syntax Bool ::= finalIsY(IntSeq, Bool) [function, total]
  rule finalIsY(.IntSeq, PREVIOUS:Bool) => PREVIOUS
  rule finalIsY(iCons(C:Int, REST:IntSeq), _PREVIOUS:Bool)
    => finalIsY(
         REST,
         strContains(iCons(C, .IntSeq), iCons(121, .IntSeq))
       )

  // Exact final value of the Python loop target.  It is semantically dead
  // after the loop, but retaining it makes the loop theorem frame-exact.
  syntax IntSeq ::= finalLowerChar(IntSeq, IntSeq) [function, total]
  rule finalLowerChar(.IntSeq, PREVIOUS:IntSeq) => PREVIOUS
  rule finalLowerChar(iCons(C:Int, REST:IntSeq), _PREVIOUS:IntSeq)
    => finalLowerChar(REST, iCons(C, .IntSeq))

  syntax Int ::= specifiedVowels(IntSeq) [function, total]
  rule specifiedVowels(S:IntSeq)
    => ordinaryVowels(mapLower(S))
       +Int boolToInt(finalIsY(mapLower(S), false))

  // These macros are the literal constructors emitted in solution.mpy.
  syntax Stmts ::= "vowelLoopBody" [macro]
  rule vowelLoopBody
    => If(
         Compare(Name("char"), CmpOp("in", Str("aeiou"))),
         AugAssign(Name("count"), "+", Int(1)) .Stmts,
         .Stmts
       )
       Assign(
         Name("last_y"),
         Compare(Name("char"), CmpOp("in", Str("y")))
       )
       .Stmts

  syntax Stmts ::= "vowelsBody" [macro]
  rule vowelsBody
    => Assign(Name("s"), Call(Attribute(Name("s"), "lower"), .Exprs))
       Assign(Name("count"), Int(0))
       Assign(Name("char"), Str(""))
       Assign(Name("last_y"), Bool(false))
       For(Name("char"), Name("s"), vowelLoopBody)
       Return(BinOp("+", Name("count"), Name("last_y")))
       .Stmts

  syntax Module ::= "vowelsModule" [macro]
  rule vowelsModule
    => Module(FuncDef("vowels_count", Params("s"), vowelsBody) .Stmts)
endmodule

// This module contains only the proved loop theorem as a reusable rewrite.
// LOOP-SPEC proves the same sentence against VOWELS-BASE, where this rule is
// absent. MAIN-SPEC then uses it to compose the whole-function proof.
module VOWELS-VERIFICATION
  imports VOWELS-BASE

  rule <k>
         #loop(str(S:IntSeq), Name("char"), vowelLoopBody)
         => .K
         ...
       </k>
       <scopes>
         SC:Map
         1 |-> scope(
           "s"      |-> ORIGINALS:Str
           "count"  |-> COUNT:Int
           "char"   |-> str(PREVIOUS:IntSeq)
           "last_y" |-> PREVIOUSY:Bool,
           parent(0)
         )
         =>
         SC
         1 |-> scope(
           "s"      |-> ORIGINALS
           "count"  |-> COUNT +Int ordinaryVowels(S)
           "char"   |-> str(finalLowerChar(S, PREVIOUS))
           "last_y" |-> finalIsY(S, PREVIOUSY),
           parent(0)
         )
       </scopes>
       requires notBool (1 in_keys(SC))
       [priority(40)]
endmodule
