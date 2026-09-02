requires "verification.k"

module SPEC
  imports VERIFICATION

  // Prompt example: 1 + 2x.
  claim
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

  // Prompt example: -6 + 11x - 6x^2 + x^3.
  claim
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

  // The root is the initial midpoint; this exercises the zero-product branch.
  claim
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

  // x^3 - 8: both initial endpoint values are negative, so the bracket grows.
  claim
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

  // x^3 + 8: symmetric expansion to a negative root.
  claim
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
