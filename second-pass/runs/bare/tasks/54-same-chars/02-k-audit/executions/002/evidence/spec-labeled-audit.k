requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [universal]:
    <k> solutionProgram => .K </k>
    <s0> S0:String </s0>
    <s1> S1:String </s1>
    <env>
      .Map
      => ("s0" |-> stringValue(S0)) ("s1" |-> stringValue(S1))
    </env>
    <result>
      noResult => result(boolValue(sameCharsSpec(S0, S1)))
    </result>

  claim [example-1]:
    <k> solutionProgram => .K </k>
    <s0> "eabcdzzzz" </s0>
    <s1> "dddzzzzzzzddeddabc" </s1>
    <env> .Map => ("s0" |-> stringValue("eabcdzzzz"))
                 ("s1" |-> stringValue("dddzzzzzzzddeddabc")) </env>
    <result> noResult => result(boolValue(true)) </result>

  claim [example-2]:
    <k> solutionProgram => .K </k>
    <s0> "abcd" </s0>
    <s1> "dddddddabc" </s1>
    <env> .Map => ("s0" |-> stringValue("abcd"))
                 ("s1" |-> stringValue("dddddddabc")) </env>
    <result> noResult => result(boolValue(true)) </result>

  claim [example-3]:
    <k> solutionProgram => .K </k>
    <s0> "dddddddabc" </s0>
    <s1> "abcd" </s1>
    <env> .Map => ("s0" |-> stringValue("dddddddabc"))
                 ("s1" |-> stringValue("abcd")) </env>
    <result> noResult => result(boolValue(true)) </result>

  claim [example-4]:
    <k> solutionProgram => .K </k>
    <s0> "eabcd" </s0>
    <s1> "dddddddabc" </s1>
    <env> .Map => ("s0" |-> stringValue("eabcd"))
                 ("s1" |-> stringValue("dddddddabc")) </env>
    <result> noResult => result(boolValue(false)) </result>

  claim [example-5]:
    <k> solutionProgram => .K </k>
    <s0> "abcd" </s0>
    <s1> "dddddddabce" </s1>
    <env> .Map => ("s0" |-> stringValue("abcd"))
                 ("s1" |-> stringValue("dddddddabce")) </env>
    <result> noResult => result(boolValue(false)) </result>

  claim [example-6]:
    <k> solutionProgram => .K </k>
    <s0> "eabcdzzzz" </s0>
    <s1> "dddzzzzzzzddddabc" </s1>
    <env> .Map => ("s0" |-> stringValue("eabcdzzzz"))
                 ("s1" |-> stringValue("dddzzzzzzzddddabc")) </env>
    <result> noResult => result(boolValue(false)) </result>
endmodule
