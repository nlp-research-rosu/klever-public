requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Reviewer mutation: the last hex digit is changed from 2 to 3.
  // "Hello world" is a satisfying initial input and the alternative is false.
  claim [label(false-prompt-result)]:
    <py>
      <k> #load(solutionProgram) => .K </k>
      <input> "Hello world" </input>
      <functions>
        .Map => "string_to_md5" |-> fn("text", solutionBody)
      </functions>
      <env> .Map => "text" |-> pyString("Hello world") </env>
      <result>
        noResult => pyString("3e25960a79dbc69b674cd4ec67a72c63")
      </result>
    </py>
endmodule
