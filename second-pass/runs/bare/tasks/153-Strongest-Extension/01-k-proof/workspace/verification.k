requires "semantic.k"

// Verification-only name for the exact constructor tree in solution.mpy.
// Keeping it as a macro makes claims readable; macro expansion removes the
// name before proving, so all execution uses MPY-SEMANTIC's source rules.
module VERIFICATION
  imports MPY-SEMANTIC

  syntax Program ::= "StrongestProgram" [macro]

  rule StrongestProgram =>
    Module(
      FuncDef("Strongest_Extension", Params("class_name", "extensions"),
        Assign(Name("strongest"), Subscript(Name("extensions"), Int(0)))
        Assign(Name("strongest_strength"), Int(0))
        For(Name("character"), Name("strongest"),
          If(Call(Attribute(Name("character"), "isupper"), .Exprs),
            AugAssign(Name("strongest_strength"), "+", Int(1)),
            .Stmts)
          If(Call(Attribute(Name("character"), "islower"), .Exprs),
            AugAssign(Name("strongest_strength"), "-", Int(1)),
            .Stmts))
        For(Name("extension"),
            Subscript(Name("extensions"), Slice(Int(1), NoBound, NoBound)),
          Assign(Name("extension_strength"), Int(0))
          For(Name("character"), Name("extension"),
            If(Call(Attribute(Name("character"), "isupper"), .Exprs),
              AugAssign(Name("extension_strength"), "+", Int(1)),
              .Stmts)
            If(Call(Attribute(Name("character"), "islower"), .Exprs),
              AugAssign(Name("extension_strength"), "-", Int(1)),
              .Stmts))
          If(Compare(Name("extension_strength"),
                     CmpOp(">", Name("strongest_strength"))),
            Assign(Name("strongest"), Name("extension"))
            Assign(Name("strongest_strength"), Name("extension_strength")),
            .Stmts))
        Return(BinOp("+",
          BinOp("+", Name("class_name"), Str(".")),
          Name("strongest")))))

  // A verification-only mathematical rendering of the contract.  It is
  // independent of statement execution: refStrength counts character classes,
  // and refSelect performs a left fold whose strict comparison preserves the
  // first candidate on ties.
  syntax Int ::= "refDelta" "(" String ")" [function]
               | "refStrength" "(" String ")" [function]
               | "refStrengthAt" "(" String "," Int ")" [function]
  syntax String ::= "refStrongest" "(" Values ")" [function]
                  | "refSelect" "(" String "," Int "," Values ")" [function]

  rule refDelta(S) => 1
       requires isUpperChar(S)
  rule refDelta(S) => -1
       requires notBool isUpperChar(S) andBool isLowerChar(S)
  rule refDelta(S) => 0
       requires notBool isUpperChar(S) andBool notBool isLowerChar(S)

  rule refStrength(S) => refStrengthAt(S, 0)
  rule refStrengthAt(S, I) => 0
       requires I >=Int lengthString(S)
  rule refStrengthAt(S, I)
    => refDelta(substrString(S, I, I +Int 1))
       +Int refStrengthAt(S, I +Int 1)
       requires I <Int lengthString(S)

  rule refStrongest(strVal(S) ; REST)
    => refSelect(S, refStrength(S), REST)
  rule refSelect(BEST, _, .Values) => BEST
  rule refSelect(_, BESTSCORE, strVal(S) ; REST)
    => refSelect(S, refStrength(S), REST)
       requires refStrength(S) >Int BESTSCORE
  rule refSelect(BEST, BESTSCORE, strVal(S) ; REST)
    => refSelect(BEST, BESTSCORE, REST)
       requires refStrength(S) <=Int BESTSCORE
endmodule
