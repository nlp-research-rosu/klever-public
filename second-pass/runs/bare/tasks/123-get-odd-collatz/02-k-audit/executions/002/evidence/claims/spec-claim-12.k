requires "verification.k"

module SPEC-CLAIM-12
  imports VERIFICATION

  claim
    <python>
      <k> checkAllOdd(17 :: 1 :: 7 :: 5 :: 13 :: 11 :: .Ints)
            => true </k>
      <input> 0 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
endmodule
