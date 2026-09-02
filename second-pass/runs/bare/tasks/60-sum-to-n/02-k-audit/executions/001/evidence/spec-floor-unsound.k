requires "verification.k"

module SPEC-FLOOR-UNSOUND
  imports VERIFICATION

  // False for Python: def probe(n): return -3 // 2 returns -2, not -1.
  // Input 0 is within the target claim's N >= 0 input domain.
  claim
    <k>
      Module(
        FuncDef("probe", Params("n"),
          Return(BinOp("//", Int(-3), Int(2)))))
      ~> invoke("probe", 0)
      => .K
    </k>
    <result> noResult => -1 </result>
endmodule
