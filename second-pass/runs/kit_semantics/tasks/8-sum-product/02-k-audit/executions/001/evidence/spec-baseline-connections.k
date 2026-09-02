requires "reference-semantics/semantics.k"

module SPEC-BASELINE-CONNECTIONS
  imports MPY

  // Bridge-free fixed-semantics equations underlying the guarded dispatch twins.
  claim [fixed-add-int]:
    <k>
      applyBin("+", I:Int, J:Int) => I +Int J
      ...
    </k>

  claim [fixed-multiply-int]:
    <k>
      applyBin("*", I:Int, J:Int) => I *Int J
      ...
    </k>

  // Universal read-only input representation connection: an actual heap-backed
  // list is dereferenced exactly once at For entry to the same bare list value
  // used by the candidate's entry theorem.
  claim [fixed-for-list-dereference]:
    <k>
      For(T:Expr, ref(H:Int), B:Stmts)
      =>
      For(T, list(VS:ValSeq), B)
      ...
    </k>
    <heap>
      ...
      H |-> list(VS)
      ...
    </heap>
endmodule
