requires "verification.k"

module WITNESS-VALUES
  imports VERIFICATION

  claim [empty]:
    <k> dtd(.ValSeq) => 0 </k>

  claim [examples-and-boundaries]:
    <k>
      dtd(vCons(-3,
          vCons(-2,
          vCons(-1,
          vCons(0,
          vCons(1,
          vCons(2,
          vCons(3, .ValSeq))))))))
      => 10
    </k>

  claim [mixed-numeric]:
    <k>
      dtd(vCons(1.5,
          vCons(3,
          vCons(-5,
          vCons(7.0,
          vCons(5, .ValSeq))))))
      => 34
    </k>
endmodule
