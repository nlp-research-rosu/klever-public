requires "verification.k"

module SPEC-SUMMARY
  imports VERIFICATION

  claim [prime-181]: <k> isPrime(181) => true </k>
  claim [composite-4]: <k> isPrime(4) => false </k>
  claim [digits-181]: <k> digitSum(181) => 10 </k>
  claim [largest-example]:
    <k>
      largestPrime(
        vCons(3, vCons(181, vCons(32, vCons(7, .ValSeq)))),
        0)
      => 181
    </k>
endmodule
