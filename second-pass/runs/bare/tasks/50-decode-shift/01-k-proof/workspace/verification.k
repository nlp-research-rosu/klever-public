module VERIFICATION
  imports INT
  imports BOOL

  // Inductive character sequences make the string traversal explicit.
  syntax Chars ::= "nil" [constructor]
                 | "cons" "(" Int "," Chars ")" [constructor]

  // The contract-level decoder is independent of the AST evaluator.
  syntax Int ::= decodeCode(Int) [function, total]
  rule decodeCode(C) => ((C -Int 5 -Int 97) modInt 26) +Int 97

  syntax Chars ::= decodeSpec(Chars) [function, total]
  rule decodeSpec(nil) => nil
  rule decodeSpec(cons(C, CS)) => cons(decodeCode(C), decodeSpec(CS))

  syntax Int ::= encodeCode(Int) [function, total]
  rule encodeCode(C) => ((C +Int 5 -Int 97) modInt 26) +Int 97

  syntax Chars ::= encodeSpec(Chars) [function, total]
  rule encodeSpec(nil) => nil
  rule encodeSpec(cons(C, CS)) => cons(encodeCode(C), encodeSpec(CS))

  syntax Bool ::= isLowerCode(Int) [function, total]
  rule isLowerCode(C) => 97 <=Int C andBool C <=Int 122

  syntax Bool ::= allLower(Chars) [function, total]
  rule allLower(nil) => true
  rule allLower(cons(C, CS)) => isLowerCode(C) andBool allLower(CS)
endmodule
