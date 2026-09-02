requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [c1]:
        <k> start => done </k>
        <program> solutionModule </program>
        <input> "Hello world" </input>
        <result> 0 </result>

  claim [c2]:
        <k> start => done </k>
        <program> solutionModule </program>
        <input> "The sky is blue. The sun is shining. I love this weather" </input>
        <result> 0 => 1 </result>

  claim [c3]:
        <k> start => done </k>
        <program> solutionModule </program>
        <input> "I am bored. I am still bored! Are you? I think so." </input>
        <result> 0 => 3 </result>

  claim [c4]:
        <k> start => done </k>
        <program> solutionModule </program>
        <input> " I am here?You are there!  I agree" </input>
        <result> 0 => 2 </result>

  claim [c5]:
        <k> start => done </k>
        <program> solutionModule </program>
        <input> "It is cold. Island life! In time? I agree" </input>
        <result> 0 => 1 </result>

  claim [c6]:
        <k> start => done </k>
        <program> solutionModule </program>
        <input> "... ! ?  . I count!" </input>
        <result> 0 => 1 </result>

  claim [c7]:
        <k> start => done </k>
        <program> solutionModule </program>
        <input> "\tI tabbed.\nI newline?\rNot me!" </input>
        <result> 0 => 2 </result>

  claim [c8]:
        <k> start => done </k>
        <program> solutionModule </program>
        <input> "I first! No. I second?" </input>
        <result> 0 => boredSpec("I first! No. I second?") </result>
endmodule
