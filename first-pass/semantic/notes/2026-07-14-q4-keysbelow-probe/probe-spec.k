requires "probe.k"

module Q4KB-PROBE-SPEC
  imports Q4KB-PROBE

  claim
    <k>
      #pb(0 <Int HLM +Int 1
          andBool HLM +Int 1 <Int HLM +Int 2
          andBool keysBelow(
            (AN:Int |-> list(_R:ValSeq))
            (HLM:Int |-> list(vCons(absF(subF(projectFloatTotal(V:Val), MEANT:Float)), .ValSeq)))
            HREST:Map,
            HLM +Int 2))
    => .K ... </k>
    requires 0 <Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    [all-path]
endmodule
