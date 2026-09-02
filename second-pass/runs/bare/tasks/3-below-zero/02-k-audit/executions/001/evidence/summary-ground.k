requires "verification.k"

module SUMMARY-GROUND
  imports VERIFICATION

  claim [empty]:
    <mpy>
      <k> .K </k>
      <input> .IntList </input>
      <balance> 0 </balance>
      <current> 0 </current>
      <result>
        BoolV(belowZeroFrom(0, .IntList)) => BoolV(false)
      </result>
    </mpy>

  claim [zero-boundary]:
    <mpy>
      <k> .K </k>
      <input> cons(1, cons(-1, .IntList)) </input>
      <balance> 0 </balance>
      <current> 0 </current>
      <result>
        BoolV(belowZeroFrom(0, cons(1, cons(-1, .IntList))))
        => BoolV(false)
      </result>
    </mpy>

  claim [crossing]:
    <mpy>
      <k> .K </k>
      <input> cons(1, cons(-2, .IntList)) </input>
      <balance> 0 </balance>
      <current> 0 </current>
      <result>
        BoolV(belowZeroFrom(0, cons(1, cons(-2, .IntList))))
        => BoolV(true)
      </result>
    </mpy>
endmodule
