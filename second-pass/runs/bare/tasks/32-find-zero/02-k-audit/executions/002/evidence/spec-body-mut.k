requires "verification-body-mut.k"

module SPEC-BODY-MUT
  imports VERIFICATION-BODY-MUT

  claim
    <k>
      solutionBodyMut ;;
      VerifyRootMut(
        ListItem(rat(1, 1)) ListItem(rat(2, 1)),
        Invoke("find_zero", list(
          ListItem(rat(1, 1)) ListItem(rat(2, 1)))),
        rat(1, 100000000))
      => bool(true)
    </k>
    <env> .Map </env>
    <functions> .Map </functions>
    <stack> .List </stack>
endmodule
