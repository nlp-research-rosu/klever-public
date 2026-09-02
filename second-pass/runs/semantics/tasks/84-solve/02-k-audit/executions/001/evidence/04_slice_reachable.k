requires "/tmp/audit-work/candidate-src/reference-semantics/semantics.k"

module SLICE-REACHABLE
  imports MPY

  // digit_sum=0, bin payload=0
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(48, .IntSeq)))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(48, .IntSeq)) ~> CONT
    </k>

  // digit_sum=1, bin payload=1
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, .IntSeq)))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, .IntSeq)) ~> CONT
    </k>

  // digit_sum=2, bin payload=10
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, .IntSeq))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, .IntSeq))) ~> CONT
    </k>

  // digit_sum=3, bin payload=11
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, .IntSeq))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, .IntSeq))) ~> CONT
    </k>

  // digit_sum=4, bin payload=100
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(48, .IntSeq)))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(48, .IntSeq)))) ~> CONT
    </k>

  // digit_sum=5, bin payload=101
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(49, .IntSeq)))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(49, .IntSeq)))) ~> CONT
    </k>

  // digit_sum=6, bin payload=110
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(48, .IntSeq)))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(48, .IntSeq)))) ~> CONT
    </k>

  // digit_sum=7, bin payload=111
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(49, .IntSeq)))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(49, .IntSeq)))) ~> CONT
    </k>

  // digit_sum=8, bin payload=1000
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(48, iCons(48, .IntSeq))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(48, iCons(48, .IntSeq))))) ~> CONT
    </k>

  // digit_sum=9, bin payload=1001
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(48, iCons(49, .IntSeq))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(48, iCons(49, .IntSeq))))) ~> CONT
    </k>

  // digit_sum=10, bin payload=1010
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(49, iCons(48, .IntSeq))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(49, iCons(48, .IntSeq))))) ~> CONT
    </k>

  // digit_sum=11, bin payload=1011
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(49, iCons(49, .IntSeq))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(49, iCons(49, .IntSeq))))) ~> CONT
    </k>

  // digit_sum=12, bin payload=1100
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(48, iCons(48, .IntSeq))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(48, iCons(48, .IntSeq))))) ~> CONT
    </k>

  // digit_sum=13, bin payload=1101
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(48, iCons(49, .IntSeq))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(48, iCons(49, .IntSeq))))) ~> CONT
    </k>

  // digit_sum=14, bin payload=1110
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(49, iCons(48, .IntSeq))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(49, iCons(48, .IntSeq))))) ~> CONT
    </k>

  // digit_sum=15, bin payload=1111
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(49, iCons(49, .IntSeq))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(49, iCons(49, .IntSeq))))) ~> CONT
    </k>

  // digit_sum=16, bin payload=10000
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(48, iCons(48, iCons(48, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(48, iCons(48, iCons(48, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=17, bin payload=10001
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(48, iCons(48, iCons(49, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(48, iCons(48, iCons(49, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=18, bin payload=10010
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(48, iCons(49, iCons(48, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(48, iCons(49, iCons(48, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=19, bin payload=10011
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(48, iCons(49, iCons(49, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(48, iCons(49, iCons(49, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=20, bin payload=10100
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(49, iCons(48, iCons(48, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(49, iCons(48, iCons(48, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=21, bin payload=10101
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(49, iCons(48, iCons(49, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(49, iCons(48, iCons(49, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=22, bin payload=10110
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(49, iCons(49, iCons(48, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(49, iCons(49, iCons(48, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=23, bin payload=10111
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(49, iCons(49, iCons(49, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(49, iCons(49, iCons(49, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=24, bin payload=11000
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(48, iCons(48, iCons(48, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(48, iCons(48, iCons(48, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=25, bin payload=11001
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(48, iCons(48, iCons(49, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(48, iCons(48, iCons(49, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=26, bin payload=11010
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(48, iCons(49, iCons(48, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(48, iCons(49, iCons(48, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=27, bin payload=11011
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(48, iCons(49, iCons(49, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(48, iCons(49, iCons(49, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=28, bin payload=11100
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(49, iCons(48, iCons(48, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(49, iCons(48, iCons(48, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=29, bin payload=11101
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(49, iCons(48, iCons(49, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(49, iCons(48, iCons(49, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=30, bin payload=11110
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(49, iCons(49, iCons(48, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(49, iCons(49, iCons(48, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=31, bin payload=11111
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(49, iCons(49, iCons(49, iCons(49, .IntSeq)))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(49, iCons(49, iCons(49, iCons(49, .IntSeq)))))) ~> CONT
    </k>

  // digit_sum=32, bin payload=100000
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(48, iCons(48, iCons(48, iCons(48, .IntSeq))))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(48, iCons(48, iCons(48, iCons(48, .IntSeq))))))) ~> CONT
    </k>

  // digit_sum=33, bin payload=100001
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(48, iCons(48, iCons(48, iCons(49, .IntSeq))))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(48, iCons(48, iCons(48, iCons(49, .IntSeq))))))) ~> CONT
    </k>

  // digit_sum=34, bin payload=100010
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(48, iCons(48, iCons(49, iCons(48, .IntSeq))))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(48, iCons(48, iCons(49, iCons(48, .IntSeq))))))) ~> CONT
    </k>

  // digit_sum=35, bin payload=100011
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(48, iCons(48, iCons(49, iCons(49, .IntSeq))))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(48, iCons(48, iCons(49, iCons(49, .IntSeq))))))) ~> CONT
    </k>

  // digit_sum=36, bin payload=100100
  claim
    <k>
      Subscript(str(iCons(48, iCons(98, iCons(49, iCons(48, iCons(48, iCons(49, iCons(48, iCons(48, .IntSeq))))))))), Slice(Int(2), NoBound, NoBound)) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(48, iCons(49, iCons(48, iCons(48, .IntSeq))))))) ~> CONT
    </k>
endmodule
