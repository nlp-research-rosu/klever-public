requires "verification.k"

module SPEC
  imports VERIFICATION

  // All six examples from the original prompt.
  claim <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("abcd") pyStr("abd") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("abcd", "abd"))) </out>
        </mpy>

  claim <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("hello") pyStr("ell") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("hello", "ell"))) </out>
        </mpy>

  claim <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("whassup") pyStr("psus") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("whassup", "psus"))) </out>
        </mpy>

  claim <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("abab") pyStr("baa") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("abab", "baa"))) </out>
        </mpy>

  claim <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("efef") pyStr("eeff") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("efef", "eeff"))) </out>
        </mpy>

  claim <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("himenss") pyStr("simen") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("himenss", "simen"))) </out>
        </mpy>

  // Boundary cases: the unrotated match, a one-character word, and the empty
  // set of rotations.
  claim <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("abc") pyStr("abc") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("abc", "abc"))) </out>
        </mpy>

  claim <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("x") pyStr("x") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("x", "x"))) </out>
        </mpy>

  claim <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("anything") pyStr("") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("anything", ""))) </out>
        </mpy>

  // Symbolic boundary theorem: for every first string, an empty second string
  // has no rotations and the implementation agrees with the contract model.
  claim <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr(A) pyStr("") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains(A, ""))) </out>
        </mpy>

  // Loop invariant for arbitrary strings: at index I, the remaining program
  // computes exactly the remaining rotations in cyclicContainsFrom.
  claim <mpy>
          <k> solutionLoop() ~> exec(Return(Bool(false))) => .K </k>
          <args> pyStr(A) pyStr(B) </args>
          <env> ("a" |-> pyStr(A)) ("b" |-> pyStr(B)) ("i" |-> pyInt(I))
                => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContainsFrom(A, B, I))) </out>
        </mpy>
    requires 0 <=Int I andBool I <=Int lengthString(B)

  // Whole-program correctness for arbitrary strings.
  claim <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr(A) pyStr(B) </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains(A, B))) </out>
        </mpy>
endmodule
