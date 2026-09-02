requires "semantic.k"

module BRIDGE-WITNESS-BASE-MATCH
  imports MPY-SEMANTICS

  // Fixed semantics calls the binding supplied in <functions>, so this
  // intentionally adversarial binding makes match_parens return "Yes".
  claim
    <k>
      invoke(closure("match_parens", Params("lst"),
        If(Call(
          Name("is_balanced"),
          BinOp(
            "+",
            Subscript(Name("lst"), Int(0)),
            Subscript(Name("lst"), Int(1))),
          Int(0)),
          Return(Str("Yes")),
          .Stmts)
        If(Call(
          Name("is_balanced"),
          BinOp(
            "+",
            Subscript(Name("lst"), Int(1)),
            Subscript(Name("lst"), Int(0))),
          Int(0)),
          Return(Str("Yes")),
          .Stmts)
        Return(Str("No"))),
        listVal(
          strVal(parens(rp .PString)),
          strVal(parens(rp .PString)),
          .Values))
      => .K
    </k>
    <input> ListExpr(PStr(rp .PString), PStr(rp .PString)) </input>
    <env> .Map </env>
    <functions>
      "is_balanced" |->
        closure("evil", Params("s", "depth"), Return(Bool(true)))
    </functions>
    <result> noResult => strVal(yesString) </result>
endmodule

module BRIDGE-WITNESS-EXTENDED-MATCH
  imports MPY-SEMANTICS

  // The candidate priority bridge omits <functions> and instead fabricates
  // contractAnswer(")", ")") = "No" from this identical start state.
  claim
    <k>
      invoke(closure("match_parens", Params("lst"),
        If(Call(
          Name("is_balanced"),
          BinOp(
            "+",
            Subscript(Name("lst"), Int(0)),
            Subscript(Name("lst"), Int(1))),
          Int(0)),
          Return(Str("Yes")),
          .Stmts)
        If(Call(
          Name("is_balanced"),
          BinOp(
            "+",
            Subscript(Name("lst"), Int(1)),
            Subscript(Name("lst"), Int(0))),
          Int(0)),
          Return(Str("Yes")),
          .Stmts)
        Return(Str("No"))),
        listVal(
          strVal(parens(rp .PString)),
          strVal(parens(rp .PString)),
          .Values))
      => .K
    </k>
    <input> ListExpr(PStr(rp .PString), PStr(rp .PString)) </input>
    <env> .Map </env>
    <functions>
      "is_balanced" |->
        closure("evil", Params("s", "depth"), Return(Bool(true)))
    </functions>
    <result> noResult => strVal(noString) </result>
endmodule

module BRIDGE-WITNESS-BASE-HELPER
  imports MPY-SEMANTICS

  // After consuming the first ")", fixed execution recursively resolves
  // Name("is_balanced") to the supplied true-returning binding.
  claim
    <k>
      invoke(closure("is_balanced", Params("s", "depth"),
        If(Compare(Name("depth"), CmpOp("<", Int(0))),
          Return(Bool(false)),
          .Stmts)
        If(Compare(Name("s"), CmpOp("==", Str(""))),
          Return(Compare(Name("depth"), CmpOp("==", Int(0)))),
          .Stmts)
        If(Compare(Subscript(Name("s"), Int(0)), CmpOp("==", Str("("))),
          Return(
            Call(
              Name("is_balanced"),
              Subscript(Name("s"), Slice(Int(1), NoBound, NoBound)),
              BinOp("+", Name("depth"), Int(1)))),
          .Stmts)
        Return(
          Call(
            Name("is_balanced"),
            Subscript(Name("s"), Slice(Int(1), NoBound, NoBound)),
            BinOp("-", Name("depth"), Int(1))))),
        strVal(parens(rp .PString)),
        intVal(0))
      => .K
    </k>
    <input> PStr(rp .PString) </input>
    <env> .Map </env>
    <functions>
      "is_balanced" |->
        closure("evil", Params("s", "depth"), Return(Bool(true)))
    </functions>
    <result> noResult => boolVal(true) </result>
endmodule

module BRIDGE-WITNESS-EXTENDED-HELPER
  imports MPY-SEMANTICS

  // The candidate helper bridge also omits <functions> and produces the
  // mathematical summary balanced(")", 0) = false.
  claim
    <k>
      invoke(closure("is_balanced", Params("s", "depth"),
        If(Compare(Name("depth"), CmpOp("<", Int(0))),
          Return(Bool(false)),
          .Stmts)
        If(Compare(Name("s"), CmpOp("==", Str(""))),
          Return(Compare(Name("depth"), CmpOp("==", Int(0)))),
          .Stmts)
        If(Compare(Subscript(Name("s"), Int(0)), CmpOp("==", Str("("))),
          Return(
            Call(
              Name("is_balanced"),
              Subscript(Name("s"), Slice(Int(1), NoBound, NoBound)),
              BinOp("+", Name("depth"), Int(1)))),
          .Stmts)
        Return(
          Call(
            Name("is_balanced"),
            Subscript(Name("s"), Slice(Int(1), NoBound, NoBound)),
            BinOp("-", Name("depth"), Int(1))))),
        strVal(parens(rp .PString)),
        intVal(0))
      => .K
    </k>
    <input> PStr(rp .PString) </input>
    <env> .Map </env>
    <functions>
      "is_balanced" |->
        closure("evil", Params("s", "depth"), Return(Bool(true)))
    </functions>
    <result> noResult => boolVal(false) </result>
endmodule
