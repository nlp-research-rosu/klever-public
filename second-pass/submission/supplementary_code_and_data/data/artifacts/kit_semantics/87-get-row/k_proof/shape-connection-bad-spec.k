requires "shape-connection.k"

module SHAPE-CONNECTION-BAD-SPEC
  imports SHAPE-CONNECTION

  // False mutation of the proved bridge: it drops the sole list element.
  claim [wrong-for-shape]:
    <k> For(T:Expr, list(vCons(7, .ValSeq)), B:Stmts)
        => #loop(list(.ValSeq), T, B) ... </k>
endmodule
