requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [claim-1]:
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

  claim [claim-2]:
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

  claim [claim-3]:
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

  claim [claim-4]:
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

  claim [claim-5]:
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
