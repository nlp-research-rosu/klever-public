requires "semantic.k"

module SPEC
  imports MPY

  // Every claim describes a complete function call: it preserves the caller's
  // continuation, environment, and stack.  The cases are exhaustive for the
  // recursive Chars datatype (vowels and consonants partition Char).

  claim <T>
          <k> invoke("get_closest_vowel", pyStr(.Chars)) ~> KREST:K
            => callResult(pyStr(.Chars)) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim <T>
          <k> invoke("get_closest_vowel", pyStr(snoc(.Chars, A:Char))) ~> KREST:K
            => callResult(pyStr(.Chars)) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(.Chars, A:Char), B:Char))) ~> KREST:K
            => callResult(pyStr(.Chars)) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  // The rightmost triple is consonant-vowel-consonant.
  claim <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(P:Chars, con(A:String)), vow(V:Vowel)),
                                con(C:String)))) ~> KREST:K
            => callResult(pyStr(snoc(.Chars, vow(V)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  // Last-window failure 1: its middle character is a consonant.  The base
  // case and three predecessor-window shapes form structural induction cases.
  claim <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(.Chars, A:Char), con(B:String)),
                                C:Char))) ~> KREST:K
            => callResult(pyStr(.Chars)) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(snoc(P:Chars, D:Char), con(A:String)),
                                     con(B:String)), C:Char))) ~> KREST:K
            => callResult(closestSpec(snoc(snoc(snoc(P, D), con(A)), con(B)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(snoc(P:Chars, vow(D:Vowel)), vow(A:Vowel)),
                                     con(B:String)), C:Char))) ~> KREST:K
            => callResult(closestSpec(snoc(snoc(snoc(P, vow(D)), vow(A)), con(B)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(snoc(P:Chars, con(D:String)), vow(A:Vowel)),
                                     con(B:String)), C:Char))) ~> KREST:K
            => callResult(closestSpec(snoc(snoc(snoc(P, con(D)), vow(A)), con(B)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  // Last-window failure 2: its left and middle characters are vowels.
  claim <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(.Chars, vow(V1:Vowel)), vow(V2:Vowel)),
                                C:Char))) ~> KREST:K
            => callResult(pyStr(.Chars)) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(snoc(P:Chars, vow(D:Vowel)), vow(V1:Vowel)),
                                     vow(V2:Vowel)), C:Char))) ~> KREST:K
            => callResult(closestSpec(snoc(snoc(snoc(P, vow(D)), vow(V1)), vow(V2)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(snoc(P:Chars, con(D:String)), vow(V1:Vowel)),
                                     vow(V2:Vowel)), C:Char))) ~> KREST:K
            => callResult(closestSpec(snoc(snoc(snoc(P, con(D)), vow(V1)), vow(V2)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  // Last-window failure 3: its left character is a consonant and both
  // following characters are vowels.
  claim <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(.Chars, con(A:String)), vow(V:Vowel)),
                                vow(V2:Vowel)))) ~> KREST:K
            => callResult(pyStr(.Chars)) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(snoc(P:Chars, D:Char), con(A:String)),
                                     vow(V:Vowel)), vow(V2:Vowel)))) ~> KREST:K
            => callResult(closestSpec(snoc(snoc(snoc(P, D), con(A)), vow(V)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>
endmodule
