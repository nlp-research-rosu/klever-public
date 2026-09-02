requires "verification.k"

module GROUND-SUBSTITUTION
  imports VERIFICATION

  claim <k> palindrome(.IntSeq) => true </k>

  claim <k> palindrome(iCons(97, .IntSeq)) => true </k>

  claim <k> palindrome(iCons(97, iCons(98, iCons(97, .IntSeq)))) => true </k>

  claim
    <k>
      palindrome(iCons(122, iCons(98, iCons(99, iCons(100, .IntSeq)))))
      => false
    </k>

  claim
    <k>
      palindrome(iCons(233, iCons(97, iCons(233, .IntSeq)))) => true
    </k>

  claim
    <k>
      palindrome(iCons(233, iCons(97, iCons(232, .IntSeq)))) => false
    </k>
endmodule
