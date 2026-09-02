requires "verification.k"

module GROUND-SUMMARY-SPEC
  imports VERIFICATION

  claim <k> digitSum(largestPrime(.IntList, 0)) => 0 </k>
  claim <k> digitSum(largestPrime(intCons(1, .IntList), 0)) => 0 </k>
  claim <k> digitSum(largestPrime(intCons(2, .IntList), 0)) => 2 </k>
  claim <k> digitSum(largestPrime(intCons(4, .IntList), 0)) => 0 </k>
  claim <k> digitSum(largestPrime(intCons(5, .IntList), 0)) => 5 </k>
  claim <k> digitSum(largestPrime(intCons(49, .IntList), 0)) => 0 </k>
  claim <k> digitSum(largestPrime(
    intCons(2, intCons(4, intCons(11, .IntList))), 0)) => 2 </k>
  claim <k> digitSum(largestPrime(
    intCons(97, intCons(101, intCons(99, .IntList))), 0)) => 2 </k>
  claim <k> digitSum(largestPrime(
    intCons(0, intCons(3, intCons(2, intCons(181, .IntList)))), 0)) => 10 </k>

  claim <k> trialPrime(5, 2, true) => true </k>
  claim <k> trialPrime(4, 2, true) => false </k>
  claim <k> trialDivisor(5, 2, true) => 3 </k>
  claim <k> trialDivisor(4, 2, true) => 3 </k>
  claim <k> digitAcc(101, 0) => 2 </k>
endmodule
