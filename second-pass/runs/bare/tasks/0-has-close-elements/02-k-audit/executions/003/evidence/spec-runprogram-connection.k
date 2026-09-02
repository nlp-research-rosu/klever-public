requires "/tmp/audit-work/candidate-src/semantic.k"

module SPEC-RUNPROGRAM-CONNECTION
  imports MPY

  // Fixed-semantics, bridge-free connection for any module body, arguments,
  // and framed continuation. Program pinning separately establishes that the
  // submitted constructor term is the Module term used by `verify`.
  claim [runprogram-to-call]:
    <k> runProgram(Module(SS), ARGS)
         => call("has_close_elements", ARGS, collect(SS)) ... </k>
endmodule
