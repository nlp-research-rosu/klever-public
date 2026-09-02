requires "verification.k"

module VERIFICATION-MUTANT-SYNTAX
  imports VERIFICATION-SYNTAX

  syntax Stmts ::= "mutantMakePalindromeBody" [macro]
  syntax Val ::= "mutantMakePalindromeClosure" [macro]
  syntax Module ::= "mutantSolutionModule" [macro]
endmodule

module VERIFICATION-MUTANT
  imports VERIFICATION
  imports VERIFICATION-MUTANT-SYNTAX

  rule mutantMakePalindromeBody
    => Return(Str(""))

  rule mutantMakePalindromeClosure
    => closureVal(
         ("string", .ParamNames),
         mutantMakePalindromeBody,
         0)

  rule mutantSolutionModule
    => Module(
         FuncDef(
           "is_palindrome",
           Params("string", .ParamNames),
           isPalindromeBody)
         FuncDef(
           "make_palindrome",
           Params("string", .ParamNames),
           mutantMakePalindromeBody))
endmodule
