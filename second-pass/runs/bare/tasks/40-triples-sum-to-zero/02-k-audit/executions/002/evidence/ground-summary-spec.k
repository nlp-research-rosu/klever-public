requires "verification.k"

module GROUND-SUMMARY-SPEC
  imports VERIFICATION

  claim
    <mpy>
      <k> VBool(hasZeroTriple(.Ints)) => VBool(false) </k>
      <funs> _FUNS </funs>
      <env> _ENV </env>
      <input> _INPUT </input>
      <result> _RESULT </result>
    </mpy>

  claim
    <mpy>
      <k> VBool(hasZeroTriple(1 ; 3 ; -2 ; 1 ; .Ints))
        => VBool(true) </k>
      <funs> _FUNS </funs>
      <env> _ENV </env>
      <input> _INPUT </input>
      <result> _RESULT </result>
    </mpy>

  claim
    <mpy>
      <k> VBool(hasZeroTriple(1 ; 2 ; 3 ; 7 ; .Ints))
        => VBool(false) </k>
      <funs> _FUNS </funs>
      <env> _ENV </env>
      <input> _INPUT </input>
      <result> _RESULT </result>
    </mpy>
endmodule
