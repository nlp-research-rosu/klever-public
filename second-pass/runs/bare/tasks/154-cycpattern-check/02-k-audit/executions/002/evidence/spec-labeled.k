requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [example-abcd]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("abcd") pyStr("abd") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("abcd", "abd"))) </out>
        </mpy>

  claim [example-hello]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("hello") pyStr("ell") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("hello", "ell"))) </out>
        </mpy>

  claim [example-whassup]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("whassup") pyStr("psus") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("whassup", "psus"))) </out>
        </mpy>

  claim [example-abab]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("abab") pyStr("baa") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("abab", "baa"))) </out>
        </mpy>

  claim [example-efef]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("efef") pyStr("eeff") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("efef", "eeff"))) </out>
        </mpy>

  claim [example-himenss]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("himenss") pyStr("simen") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("himenss", "simen"))) </out>
        </mpy>

  claim [boundary-unrotated]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("abc") pyStr("abc") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("abc", "abc"))) </out>
        </mpy>

  claim [boundary-single]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("x") pyStr("x") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("x", "x"))) </out>
        </mpy>

  claim [boundary-empty-ground]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("anything") pyStr("") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("anything", ""))) </out>
        </mpy>

  claim [boundary-empty-symbolic]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr(A) pyStr("") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains(A, ""))) </out>
        </mpy>

  claim [loop-invariant]:
        <mpy>
          <k> solutionLoop() ~> exec(Return(Bool(false))) => .K </k>
          <args> pyStr(A) pyStr(B) </args>
          <env> ("a" |-> pyStr(A)) ("b" |-> pyStr(B)) ("i" |-> pyInt(I))
                => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContainsFrom(A, B, I))) </out>
        </mpy>
    requires 0 <=Int I andBool I <=Int lengthString(B)

  claim [whole-program]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr(A) pyStr(B) </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains(A, B))) </out>
        </mpy>
endmodule
