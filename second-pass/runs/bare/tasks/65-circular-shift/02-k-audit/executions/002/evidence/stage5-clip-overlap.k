requires "verification.k"

module AUDIT-CLIP-OVERLAP
  imports VERIFICATION

  // Outside every actual program call (whose L is a string length), L = -1
  // makes the first and fourth clipIndex guards overlap with different RHSs.
  claim <mpy>
          <k> .K </k>
          <entry> "" </entry>
          <args> .Vals </args>
          <result> VInt(clipIndex(0, 0 -Int 1)) => VInt(0) </result>
        </mpy>
  claim <mpy>
          <k> .K </k>
          <entry> "" </entry>
          <args> .Vals </args>
          <result>
            VInt(clipIndex(0, 0 -Int 1)) => VInt(0 -Int 1)
          </result>
        </mpy>
endmodule
