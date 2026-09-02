requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  claim [label(body-sensitivity)]:
    <py>
      <k> #load(solutionProgramMutant) => .K </k>
      <input> "Hello world" </input>
      <functions>
        .Map => "string_to_md5" |-> fn("text", solutionBodyMutant)
      </functions>
      <env> .Map => "text" |-> pyString("Hello world") </env>
      <result>
        noResult => pyString("3e25960a79dbc69b674cd4ec67a72c62")
      </result>
    </py>
endmodule
