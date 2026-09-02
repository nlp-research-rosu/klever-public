requires "/tmp/audit-work/154-cycpattern-check/candidate/verification.k"

module GROUND-WITNESSES
  imports VERIFICATION

  // Documented true case.
  claim <k>
    rotationsLoop(
      strToCodes("hello"),
      strToCodes("ell"),
      strToCodes("ell"))
    => true
  </k>

  // Documented false case.
  claim <k>
    rotationsLoop(
      strToCodes("abcd"),
      strToCodes("abd"),
      strToCodes("abd"))
    => false
  </k>

  // A later rotation ("baa" -> "aab" -> "aba") is found.
  claim <k>
    rotationsLoop(
      strToCodes("abab"),
      strToCodes("baa"),
      strToCodes("baa"))
    => true
  </k>

  // The candidate's empty-pattern result, which disagrees with canonical.py.
  claim <k>
    rotationsLoop(
      strToCodes(""),
      strToCodes(""),
      strToCodes(""))
    => false
  </k>
endmodule
