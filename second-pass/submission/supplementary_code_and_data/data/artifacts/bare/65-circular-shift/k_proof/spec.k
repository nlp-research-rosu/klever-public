requires "verification.k"

module SPEC
  imports VERIFICATION

  // Every integer x and every nonnegative shift in the ordinary branch.
  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(X), VInt(SHIFT)) </args>
          <result> VNone => VString(normalCircularShift(Int2String(X), SHIFT)) </result>
        </mpy>
    requires 0 <=Int SHIFT
     andBool SHIFT <=Int lengthString(Int2String(X))

  // Every integer x and every shift in the contract's oversized branch.
  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(X), VInt(SHIFT)) </args>
          <result> VNone => VString(reverseString(Int2String(X))) </result>
        </mpy>
    requires lengthString(Int2String(X)) <Int SHIFT

  // The two examples are retained as concrete regression proofs.
  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(12), VInt(1)) </args>
          <result> VNone => VString("21") </result>
        </mpy>
  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(12), VInt(2)) </args>
          <result> VNone => VString("12") </result>
        </mpy>
  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(1234), VInt(2)) </args>
          <result> VNone => VString("3412") </result>
        </mpy>
  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(1234), VInt(5)) </args>
          <result> VNone => VString("4321") </result>
        </mpy>
endmodule
