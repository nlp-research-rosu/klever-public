requires "verification.k"

module STAGE5-TOTALITY-PROBE
  imports VERIFICATION

  // The declared [total] domain is Value x Value, but no equation covers this.
  claim <py>
          <k>
            strlenPost(Str("x"), Str("y"))
            => strlenPost(Str("x"), Int(1))
          </k>
          <functions> .Map </functions>
          <locals> .Map </locals>
          <result> noResult </result>
        </py>
endmodule
