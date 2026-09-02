requires "semantic.k"

module SPEC-LABELED
  imports MPY

  claim [case-01]:
        <T>
          <k> invoke("get_closest_vowel", pyStr(.Chars)) ~> KREST:K
            => callResult(pyStr(.Chars)) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim [case-02]:
        <T>
          <k> invoke("get_closest_vowel", pyStr(snoc(.Chars, A:Char))) ~> KREST:K
            => callResult(pyStr(.Chars)) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim [case-03]:
        <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(.Chars, A:Char), B:Char))) ~> KREST:K
            => callResult(pyStr(.Chars)) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim [case-04]:
        <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(P:Chars, con(A:String)), vow(V:Vowel)),
                                con(C:String)))) ~> KREST:K
            => callResult(pyStr(snoc(.Chars, vow(V)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim [case-05]:
        <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(.Chars, A:Char), con(B:String)),
                                C:Char))) ~> KREST:K
            => callResult(pyStr(.Chars)) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim [case-06]:
        <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(snoc(P:Chars, D:Char), con(A:String)),
                                     con(B:String)), C:Char))) ~> KREST:K
            => callResult(closestSpec(snoc(snoc(snoc(P, D), con(A)), con(B)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim [case-07]:
        <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(snoc(P:Chars, vow(D:Vowel)), vow(A:Vowel)),
                                     con(B:String)), C:Char))) ~> KREST:K
            => callResult(closestSpec(snoc(snoc(snoc(P, vow(D)), vow(A)), con(B)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim [case-08]:
        <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(snoc(P:Chars, con(D:String)), vow(A:Vowel)),
                                     con(B:String)), C:Char))) ~> KREST:K
            => callResult(closestSpec(snoc(snoc(snoc(P, con(D)), vow(A)), con(B)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim [case-09]:
        <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(.Chars, vow(V1:Vowel)), vow(V2:Vowel)),
                                C:Char))) ~> KREST:K
            => callResult(pyStr(.Chars)) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim [case-10]:
        <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(snoc(P:Chars, vow(D:Vowel)), vow(V1:Vowel)),
                                     vow(V2:Vowel)), C:Char))) ~> KREST:K
            => callResult(closestSpec(snoc(snoc(snoc(P, vow(D)), vow(V1)), vow(V2)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim [case-11]:
        <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(snoc(P:Chars, con(D:String)), vow(V1:Vowel)),
                                     vow(V2:Vowel)), C:Char))) ~> KREST:K
            => callResult(closestSpec(snoc(snoc(snoc(P, con(D)), vow(V1)), vow(V2)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim [case-12]:
        <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(.Chars, con(A:String)), vow(V:Vowel)),
                                vow(V2:Vowel)))) ~> KREST:K
            => callResult(pyStr(.Chars)) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>

  claim [case-13]:
        <T>
          <k> invoke("get_closest_vowel",
                     pyStr(snoc(snoc(snoc(snoc(P:Chars, D:Char), con(A:String)),
                                     vow(V:Vowel)), vow(V2:Vowel)))) ~> KREST:K
            => callResult(closestSpec(snoc(snoc(snoc(P, D), con(A)), vow(V)))) ~> KREST </k>
          <program> solutionProgram </program>
          <env> ENV:Map </env> <stack> STACK:Frames </stack>
        </T>
endmodule
