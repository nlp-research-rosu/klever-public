requires "semantic.k"

module SPEC
  imports SEMANTIC
  imports DIGIT-SUM-VERIFICATION

  // End-to-end functional correctness for every K String S.  The left side
  // is the exact constructor tree emitted in solution.mpy; the right side is
  // the independent recursive contract from verification.k.
  claim <k>
      Module(
        FuncDef("digitSum", Params("s"),
          Assign(Name("total"), Int(0))
          For(Name("char"), Name("s"),
            If(Compare(Str("A"),
                 CmpOp("<=", Name("char")), CmpOp("<=", Str("Z"))),
               Assign(Name("total"),
                 BinOp("+", Name("total"),
                   Call(Name("ord"), Name("char")))),
               .Stmts))
          Return(Name("total"))))
        => .K
        </k>
        <input> S:String => S:String </input>
        <env> .Map => .Map </env>
        <result> noResult => intVal(upperAsciiSum(S)) </result>

  // Loop invariant: with accumulator A and unprocessed suffix S, execution
  // returns A plus the contract value of S. FRAME holds unrelated locals.
  claim <k>
          loopString("char", S:String,
            If(Compare(Str("A"),
                 CmpOp("<=", Name("char")), CmpOp("<=", Str("Z"))),
               Assign(Name("total"),
                 BinOp("+", Name("total"),
                   Call(Name("ord"), Name("char")))),
               .Stmts)
            .Stmts)
          ~> execute(Return(Name("total")) .Stmts)
          ~> .K
          => .K
        </k>
        <input> INPUT:String => INPUT:String </input>
        <env>
          ("total" |-> intVal(A:Int)) FRAME:Map
          => .Map
        </env>
        <result>
          noResult => intVal(A +Int upperAsciiSum(S))
        </result>
    requires notBool ("total" in_keys(FRAME))
endmodule
