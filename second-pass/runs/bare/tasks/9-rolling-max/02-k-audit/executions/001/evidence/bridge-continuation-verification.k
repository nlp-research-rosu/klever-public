requires "/tmp/audit-work/9-rolling-max/build/verification.k"

module BRIDGE-CONTINUATION-VERIFICATION
  imports VERIFICATION

  // The bridge's ellipsis admits this observable continuation. Fixed loop
  // execution leaves first=false, so Name("first") must evaluate to false.
  claim <py>
          <k> For(Name("number"), Name("numbers"), ROLLING-LOOP)
                ~> Name("first")
            => BoolVal(false) </k>
          <functions> .Map </functions>
          <env>
            "first"   |-> BoolVal(true)
            "maximum" |-> IntVal(0)
            "numbers" |-> ListVal(ListItem(2) ListItem(1))
            "result"  |-> ListVal(.List)
            =>
            "first"   |-> BoolVal(false)
            "maximum" |-> IntVal(2)
            "number"  |-> IntVal(1)
            "numbers" |-> ListVal(ListItem(2) ListItem(1))
            "result"  |-> ListVal(ListItem(2) ListItem(2))
          </env>
          <stack> .List </stack>
        </py>
endmodule
