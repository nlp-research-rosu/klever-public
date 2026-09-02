requires "verification.k"

module SPEC-VACUITY-AUDITOR
  imports VERIFICATION

  // Fresh false mutation: the real residual check for [1,2] is true.
  claim
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
