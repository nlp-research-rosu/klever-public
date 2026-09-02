requires "verification.k"

module SPEC-AUDIT-LABELED
  imports VERIFICATION

  claim [entry-normal]:
        <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(X), VInt(SHIFT)) </args>
          <result> VNone => VString(normalCircularShift(Int2String(X), SHIFT)) </result>
        </mpy>
    requires 0 <=Int SHIFT
     andBool SHIFT <=Int lengthString(Int2String(X))

  claim [entry-oversized]:
        <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(X), VInt(SHIFT)) </args>
          <result> VNone => VString(reverseString(Int2String(X))) </result>
        </mpy>
    requires lengthString(Int2String(X)) <Int SHIFT

  claim [example-12-1]:
        <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(12), VInt(1)) </args>
          <result> VNone => VString("21") </result>
        </mpy>

  claim [example-12-2]:
        <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(12), VInt(2)) </args>
          <result> VNone => VString("12") </result>
        </mpy>

  claim [example-1234-2]:
        <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(1234), VInt(2)) </args>
          <result> VNone => VString("3412") </result>
        </mpy>

  claim [example-1234-5]:
        <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(1234), VInt(5)) </args>
          <result> VNone => VString("4321") </result>
        </mpy>
endmodule
