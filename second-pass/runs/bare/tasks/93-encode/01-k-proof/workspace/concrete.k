requires "semantic.k"

module CONCRETE
  imports SEMANTIC

  // Ground implementation of the three total string primitives abstracted by
  // SEMANTIC.  Universal control-flow proofs can keep them opaque, while krun
  // and the concrete contract claims evaluate these equations.
  rule swapCaseChar(C) =>
    #if ordChar(C) >=Int 65 andBool ordChar(C) <=Int 90
    #then chrChar(ordChar(C) +Int 32)
    #else
      #if ordChar(C) >=Int 97 andBool ordChar(C) <=Int 122
      #then chrChar(ordChar(C) -Int 32)
      #else C
      #fi
    #fi

  rule advancedVowel(C) =>
    #if C ==String "a" orBool C ==String "e"
      orBool C ==String "i" orBool C ==String "o"
      orBool C ==String "u" orBool C ==String "A"
      orBool C ==String "E" orBool C ==String "I"
      orBool C ==String "O" orBool C ==String "U"
    #then chrChar(ordChar(C) +Int 2)
    #else C
    #fi

  rule encodedChar(C) => swapCaseChar(advancedVowel(C))
endmodule
