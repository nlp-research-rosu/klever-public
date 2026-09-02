requires "verification.k"

module SPEC-SURROGATE-WITNESS
  imports VERIFICATION

  // The K semantics fabricates UTF-8 bytes for a lone surrogate, whereas
  // Python's default strict UTF-8 encoder raises UnicodeEncodeError.
  claim [label(surrogate-fabrication)]:
    <py>
      <k> #load(solutionProgram) => .K </k>
      <input> "\ud800" </input>
      <functions>
        .Map => "string_to_md5" |-> fn("text", solutionBody)
      </functions>
      <env> .Map => "text" |-> pyString("\ud800") </env>
      <result>
        noResult => pyString("546d3dc8de10fbf8b448f678a47901e4")
      </result>
    </py>
endmodule
