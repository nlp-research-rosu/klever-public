requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [c1]:
    <k>
      solution ;;
      VerifyRoot(
        ListItem(rat(1, 1)) ListItem(rat(2, 1)),
        Invoke("find_zero", list(
          ListItem(rat(1, 1)) ListItem(rat(2, 1)))),
        rat(1, 100000000))
      => bool(true)
    </k>
    <env> .Map </env>
    <functions> .Map </functions>
    <stack> .List </stack>

  claim [c2]:
    <k>
      solution ;;
      VerifyRoot(
        ListItem(rat(-6, 1)) ListItem(rat(11, 1))
          ListItem(rat(-6, 1)) ListItem(rat(1, 1)),
        Invoke("find_zero", list(
          ListItem(rat(-6, 1)) ListItem(rat(11, 1))
            ListItem(rat(-6, 1)) ListItem(rat(1, 1)))),
        rat(1, 100000000))
      => bool(true)
    </k>
    <env> .Map </env>
    <functions> .Map </functions>
    <stack> .List </stack>

  claim [c3]:
    <k>
      solution ;;
      VerifyRoot(
        ListItem(rat(0, 1)) ListItem(rat(1, 1)),
        Invoke("find_zero", list(
          ListItem(rat(0, 1)) ListItem(rat(1, 1)))),
        rat(1, 100000000))
      => bool(true)
    </k>
    <env> .Map </env>
    <functions> .Map </functions>
    <stack> .List </stack>

  claim [c4]:
    <k>
      solution ;;
      VerifyRoot(
        ListItem(rat(-8, 1)) ListItem(rat(0, 1))
          ListItem(rat(0, 1)) ListItem(rat(1, 1)),
        Invoke("find_zero", list(
          ListItem(rat(-8, 1)) ListItem(rat(0, 1))
            ListItem(rat(0, 1)) ListItem(rat(1, 1)))),
        rat(1, 100000000))
      => bool(true)
    </k>
    <env> .Map </env>
    <functions> .Map </functions>
    <stack> .List </stack>

  claim [c5]:
    <k>
      solution ;;
      VerifyRoot(
        ListItem(rat(8, 1)) ListItem(rat(0, 1))
          ListItem(rat(0, 1)) ListItem(rat(1, 1)),
        Invoke("find_zero", list(
          ListItem(rat(8, 1)) ListItem(rat(0, 1))
            ListItem(rat(0, 1)) ListItem(rat(1, 1)))),
        rat(1, 100000000))
      => bool(true)
    </k>
    <env> .Map </env>
    <functions> .Map </functions>
    <stack> .List </stack>
endmodule
