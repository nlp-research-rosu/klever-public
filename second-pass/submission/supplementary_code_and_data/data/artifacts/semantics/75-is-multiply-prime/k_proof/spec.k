requires "verification.k"

// The prompt bounds the integer input by a < 100. SPEC-NEGATIVE proves the
// unbounded negative tail (as well as 0 and 1) symbolically. The remaining
// modules exhaust 2 through 99. Checkpoints can rewrite only when the function
// result agrees with the independently calculated product-of-three-primes set.

module SPEC-NEGATIVE
  imports VERIFICATION

  claim <k> #runIsMultiplyPrime(A:Int) => false </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    requires A <Int 2
endmodule

module SPEC-02-11
  imports VERIFICATION

  claim <k>
    #runIsMultiplyPrime(2) ~> #expect(false) ~>
    #runIsMultiplyPrime(3) ~> #expect(false) ~>
    #runIsMultiplyPrime(4) ~> #expect(false) ~>
    #runIsMultiplyPrime(5) ~> #expect(false) ~>
    #runIsMultiplyPrime(6) ~> #expect(false) ~>
    #runIsMultiplyPrime(7) ~> #expect(false) ~>
    #runIsMultiplyPrime(8) ~> #expect(true) ~>
    #runIsMultiplyPrime(9) ~> #expect(false) ~>
    #runIsMultiplyPrime(10) ~> #expect(false) ~>
    #runIsMultiplyPrime(11) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule

module SPEC-12-21
  imports VERIFICATION

  claim <k>
    #runIsMultiplyPrime(12) ~> #expect(true) ~>
    #runIsMultiplyPrime(13) ~> #expect(false) ~>
    #runIsMultiplyPrime(14) ~> #expect(false) ~>
    #runIsMultiplyPrime(15) ~> #expect(false) ~>
    #runIsMultiplyPrime(16) ~> #expect(false) ~>
    #runIsMultiplyPrime(17) ~> #expect(false) ~>
    #runIsMultiplyPrime(18) ~> #expect(true) ~>
    #runIsMultiplyPrime(19) ~> #expect(false) ~>
    #runIsMultiplyPrime(20) ~> #expect(true) ~>
    #runIsMultiplyPrime(21) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule

module SPEC-22-31
  imports VERIFICATION

  claim <k>
    #runIsMultiplyPrime(22) ~> #expect(false) ~>
    #runIsMultiplyPrime(23) ~> #expect(false) ~>
    #runIsMultiplyPrime(24) ~> #expect(false) ~>
    #runIsMultiplyPrime(25) ~> #expect(false) ~>
    #runIsMultiplyPrime(26) ~> #expect(false) ~>
    #runIsMultiplyPrime(27) ~> #expect(true) ~>
    #runIsMultiplyPrime(28) ~> #expect(true) ~>
    #runIsMultiplyPrime(29) ~> #expect(false) ~>
    #runIsMultiplyPrime(30) ~> #expect(true) ~>
    #runIsMultiplyPrime(31) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule

module SPEC-32-41
  imports VERIFICATION

  claim <k>
    #runIsMultiplyPrime(32) ~> #expect(false) ~>
    #runIsMultiplyPrime(33) ~> #expect(false) ~>
    #runIsMultiplyPrime(34) ~> #expect(false) ~>
    #runIsMultiplyPrime(35) ~> #expect(false) ~>
    #runIsMultiplyPrime(36) ~> #expect(false) ~>
    #runIsMultiplyPrime(37) ~> #expect(false) ~>
    #runIsMultiplyPrime(38) ~> #expect(false) ~>
    #runIsMultiplyPrime(39) ~> #expect(false) ~>
    #runIsMultiplyPrime(40) ~> #expect(false) ~>
    #runIsMultiplyPrime(41) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule

module SPEC-42-51
  imports VERIFICATION

  claim <k>
    #runIsMultiplyPrime(42) ~> #expect(true) ~>
    #runIsMultiplyPrime(43) ~> #expect(false) ~>
    #runIsMultiplyPrime(44) ~> #expect(true) ~>
    #runIsMultiplyPrime(45) ~> #expect(true) ~>
    #runIsMultiplyPrime(46) ~> #expect(false) ~>
    #runIsMultiplyPrime(47) ~> #expect(false) ~>
    #runIsMultiplyPrime(48) ~> #expect(false) ~>
    #runIsMultiplyPrime(49) ~> #expect(false) ~>
    #runIsMultiplyPrime(50) ~> #expect(true) ~>
    #runIsMultiplyPrime(51) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule

module SPEC-52-61
  imports VERIFICATION

  claim <k>
    #runIsMultiplyPrime(52) ~> #expect(true) ~>
    #runIsMultiplyPrime(53) ~> #expect(false) ~>
    #runIsMultiplyPrime(54) ~> #expect(false) ~>
    #runIsMultiplyPrime(55) ~> #expect(false) ~>
    #runIsMultiplyPrime(56) ~> #expect(false) ~>
    #runIsMultiplyPrime(57) ~> #expect(false) ~>
    #runIsMultiplyPrime(58) ~> #expect(false) ~>
    #runIsMultiplyPrime(59) ~> #expect(false) ~>
    #runIsMultiplyPrime(60) ~> #expect(false) ~>
    #runIsMultiplyPrime(61) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule

module SPEC-62-71
  imports VERIFICATION

  claim <k>
    #runIsMultiplyPrime(62) ~> #expect(false) ~>
    #runIsMultiplyPrime(63) ~> #expect(true) ~>
    #runIsMultiplyPrime(64) ~> #expect(false) ~>
    #runIsMultiplyPrime(65) ~> #expect(false) ~>
    #runIsMultiplyPrime(66) ~> #expect(true) ~>
    #runIsMultiplyPrime(67) ~> #expect(false) ~>
    #runIsMultiplyPrime(68) ~> #expect(true) ~>
    #runIsMultiplyPrime(69) ~> #expect(false) ~>
    #runIsMultiplyPrime(70) ~> #expect(true) ~>
    #runIsMultiplyPrime(71) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule

module SPEC-72-81
  imports VERIFICATION

  claim <k>
    #runIsMultiplyPrime(72) ~> #expect(false) ~>
    #runIsMultiplyPrime(73) ~> #expect(false) ~>
    #runIsMultiplyPrime(74) ~> #expect(false) ~>
    #runIsMultiplyPrime(75) ~> #expect(true) ~>
    #runIsMultiplyPrime(76) ~> #expect(true) ~>
    #runIsMultiplyPrime(77) ~> #expect(false) ~>
    #runIsMultiplyPrime(78) ~> #expect(true) ~>
    #runIsMultiplyPrime(79) ~> #expect(false) ~>
    #runIsMultiplyPrime(80) ~> #expect(false) ~>
    #runIsMultiplyPrime(81) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule

module SPEC-82-91
  imports VERIFICATION

  claim <k>
    #runIsMultiplyPrime(82) ~> #expect(false) ~>
    #runIsMultiplyPrime(83) ~> #expect(false) ~>
    #runIsMultiplyPrime(84) ~> #expect(false) ~>
    #runIsMultiplyPrime(85) ~> #expect(false) ~>
    #runIsMultiplyPrime(86) ~> #expect(false) ~>
    #runIsMultiplyPrime(87) ~> #expect(false) ~>
    #runIsMultiplyPrime(88) ~> #expect(false) ~>
    #runIsMultiplyPrime(89) ~> #expect(false) ~>
    #runIsMultiplyPrime(90) ~> #expect(false) ~>
    #runIsMultiplyPrime(91) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule

module SPEC-92-99
  imports VERIFICATION

  claim <k>
    #runIsMultiplyPrime(92) ~> #expect(true) ~>
    #runIsMultiplyPrime(93) ~> #expect(false) ~>
    #runIsMultiplyPrime(94) ~> #expect(false) ~>
    #runIsMultiplyPrime(95) ~> #expect(false) ~>
    #runIsMultiplyPrime(96) ~> #expect(false) ~>
    #runIsMultiplyPrime(97) ~> #expect(false) ~>
    #runIsMultiplyPrime(98) ~> #expect(true) ~>
    #runIsMultiplyPrime(99) ~> #expect(true)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule
