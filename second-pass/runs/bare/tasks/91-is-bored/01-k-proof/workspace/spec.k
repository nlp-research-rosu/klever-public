requires "verification.k"

module SPEC
  imports VERIFICATION

  // The two examples in prompt.py.
  claim <k> start => done </k>
        <program> solutionModule </program>
        <input> "Hello world" </input>
        <result> 0 </result>

  claim <k> start => done </k>
        <program> solutionModule </program>
        <input> "The sky is blue. The sun is shining. I love this weather" </input>
        <result> 0 => 1 </result>

  // All three delimiters, repeated matches, and a trailing delimiter.
  claim <k> start => done </k>
        <program> solutionModule </program>
        <input> "I am bored. I am still bored! Are you? I think so." </input>
        <result> 0 => 3 </result>

  // Leading whitespace is ignored independently for every sentence.
  claim <k> start => done </k>
        <program> solutionModule </program>
        <input> " I am here?You are there!  I agree" </input>
        <result> 0 => 2 </result>

  // "I" must be a whole initial word, not merely an initial letter.
  claim <k> start => done </k>
        <program> solutionModule </program>
        <input> "It is cold. Island life! In time? I agree" </input>
        <result> 0 => 1 </result>

  // Empty sentences and whitespace-only sentences contribute nothing.
  claim <k> start => done </k>
        <program> solutionModule </program>
        <input> "... ! ?  . I count!" </input>
        <result> 0 => 1 </result>

  // strip() includes tabs and newlines, not only ordinary spaces.
  claim <k> start => done </k>
        <program> solutionModule </program>
        <input> "\tI tabbed.\nI newline?\rNot me!" </input>
        <result> 0 => 2 </result>

  // Direct agreement with the separately stated contract model.
  claim <k> start => done </k>
        <program> solutionModule </program>
        <input> "I first! No. I second?" </input>
        <result> 0 => boredSpec("I first! No. I second?") </result>
endmodule
