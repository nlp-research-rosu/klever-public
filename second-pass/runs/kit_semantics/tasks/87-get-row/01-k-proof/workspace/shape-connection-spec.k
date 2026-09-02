requires "shape-connection.k"

module SHAPE-CONNECTION-SPEC
  imports SHAPE-CONNECTION

  claim [for-list-shape]:
    <k> For(T:Expr, V:Val, B:Stmts)
        => #loop(list(rowContents(V)), T, B) ... </k>
    requires V ==K list(rowContents(V))
endmodule
