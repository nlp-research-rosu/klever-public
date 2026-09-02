requires "connection.k"

module CONNECTION-SPEC
  imports CONNECTION

  // These universal constructor-domain claims are the fixed equations that
  // the guarded dynamic dispatch twins restate through the total projection.
  claim [set-str-connection]:
    <k>
      applyBuiltin("set", str(CS), .Vals)
      => setV(dedupCodes(CS))
    </k>

  claim [str-lt-connection]:
    <k>
      applyCmp("<", str(A), str(B))
      => strLt(A, B)
    </k>
endmodule
