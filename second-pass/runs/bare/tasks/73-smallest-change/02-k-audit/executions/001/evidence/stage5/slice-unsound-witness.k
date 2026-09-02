requires "semantic.k"

module SLICE-UNSOUND-WITNESS
  imports SEMANTIC

  // The submitted generic slice equation interprets HIGH as a count removed
  // from the back. For HIGH = 0 it therefore proves [0,1,2,3][1:0] is
  // [1,2,3], while Python's slice is empty.
  claim [candidate-slice-result]:
      <k>
        eval(
          Subscript(Name("arr"), Slice(Int(1), Int(0), NoBound)),
          ListItem(0) ListItem(1) ListItem(2) ListItem(3),
          .Stmts)
        => ListItem(1) ListItem(2) ListItem(3)
      </k>
endmodule
