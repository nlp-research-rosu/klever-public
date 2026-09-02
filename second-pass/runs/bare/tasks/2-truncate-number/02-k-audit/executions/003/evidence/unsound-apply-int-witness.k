requires "verification.k"

module UNSOUND-APPLY-INT-WITNESS
  imports VERIFICATION

  // semantic.k declares num(I,F,S) to denote I + F/S.  Thus num(0,2,1)
  // denotes the positive source-domain value 2.0.  This claim records the
  // generated semantics' false result for the exact submitted body: it returns
  // num(0,2,1), denoting 2.0, rather than the real program's decimal part 0.0.
  claim
    <k>
      Module(FuncDef("truncate_number", Params("number"),
        Return(BinOp("-", Name("number"),
          Call(Name("int"), Name("number"))))))
      ~> invoke("truncate_number", num(0, 2, 1))
      => .K
    </k>
    <env> .Map => "number" |-> num(0, 2, 1) </env>
    <result> noResult => num(0, 2, 1) </result>
endmodule
