requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [label(example-abcd-abd)]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("abcd") pyStr("abd") </args>
          <env> .Map => ?_RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("abcd", "abd"))) </out>
        </mpy>

  claim [label(example-hello-ell)]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("hello") pyStr("ell") </args>
          <env> .Map => ?_RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("hello", "ell"))) </out>
        </mpy>

  claim [label(example-whassup-psus)]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("whassup") pyStr("psus") </args>
          <env> .Map => ?_RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("whassup", "psus"))) </out>
        </mpy>

  claim [label(example-abab-baa)]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("abab") pyStr("baa") </args>
          <env> .Map => ?_RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("abab", "baa"))) </out>
        </mpy>

  claim [label(example-efef-eeff)]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("efef") pyStr("eeff") </args>
          <env> .Map => ?_RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("efef", "eeff"))) </out>
        </mpy>

  claim [label(example-himenss-simen)]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("himenss") pyStr("simen") </args>
          <env> .Map => ?_RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("himenss", "simen"))) </out>
        </mpy>

  claim [label(boundary-unrotated)]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("abc") pyStr("abc") </args>
          <env> .Map => ?_RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("abc", "abc"))) </out>
        </mpy>

  claim [label(boundary-one-character)]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("x") pyStr("x") </args>
          <env> .Map => ?_RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("x", "x"))) </out>
        </mpy>

  claim [label(boundary-empty-ground)]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("anything") pyStr("") </args>
          <env> .Map => ?_RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("anything", ""))) </out>
        </mpy>

  claim [label(boundary-empty-symbolic)]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr(A) pyStr("") </args>
          <env> .Map => ?_RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains(A, ""))) </out>
        </mpy>

  claim [label(loop-invariant)]:
        <mpy>
          <k> solutionLoop() ~> exec(Return(Bool(false))) => .K </k>
          <args> pyStr(A) pyStr(B) </args>
          <env> ("a" |-> pyStr(A)) ("b" |-> pyStr(B)) ("i" |-> pyInt(I))
                => ?_RHO </env>
          <out> NoResult => Result(pyBool(cyclicContainsFrom(A, B, I))) </out>
        </mpy>
    requires 0 <=Int I andBool I <=Int lengthString(B)

  claim [label(whole-program)]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr(A) pyStr(B) </args>
          <env> .Map => ?_RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains(A, B))) </out>
        </mpy>
endmodule
