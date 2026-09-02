requires "verification.k"

module SPEC-PI-CONCRETE-RESULT
  imports VERIFICATION

  // Result observed by direct Haskell concrete execution from a full KORE
  // configuration containing the actual Unicode K String U+03C0.
  claim [label(pi-double-encoded)]:
    <py>
      <k> #load(solutionProgram) => .K </k>
      <input> "π" </input>
      <functions>
        .Map => "string_to_md5" |-> fn("text", solutionBody)
      </functions>
      <env> .Map => "text" |-> pyString("π") </env>
      <result>
        noResult => pyString("2a5f10f35166380a06f52a5b53ccc849")
      </result>
    </py>
endmodule
