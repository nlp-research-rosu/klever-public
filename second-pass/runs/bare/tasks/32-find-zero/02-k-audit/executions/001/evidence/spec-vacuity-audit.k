requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: for [1, 2], the actual returned point has residual
  // at most 1/100000000, so VerifyRoot evaluates to true, not false.
  claim [false-linear-result]:
    <k>
      solution ;;
      VerifyRoot(
        ListItem(rat(1, 1)) ListItem(rat(2, 1)),
        Invoke("find_zero", list(
          ListItem(rat(1, 1)) ListItem(rat(2, 1)))),
        rat(1, 100000000))
      => bool(false)
    </k>
    <env> .Map </env>
    <functions> .Map </functions>
    <stack> .List </stack>
endmodule
