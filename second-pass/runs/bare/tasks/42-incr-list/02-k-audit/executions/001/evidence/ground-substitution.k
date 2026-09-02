requires "verification.k"

module GROUND-SUBSTITUTION
  imports VERIFICATION

  claim [empty]:
    <k>
      #init(
        Module(
          FuncDef("incr_list", Params("l"),
            Assign(Name("result"), ListExpr(.Exps))
            For(Name("value"), Name("l"),
              Assign(
                Name("result"),
                BinOp(
                  "+",
                  Name("result"),
                  ListExpr(BinOp("+", Name("value"), Int(1))))))
            Return(Name("result")))),
        pyList(.List))
      => .K
    </k>
    <env> .Map => ?_ </env>
    <iter> noIter => ?_ </iter>
    <result> noResult => result(pyList(.List)) </result>

  claim [three-elements]:
    <k>
      #init(
        Module(
          FuncDef("incr_list", Params("l"),
            Assign(Name("result"), ListExpr(.Exps))
            For(Name("value"), Name("l"),
              Assign(
                Name("result"),
                BinOp(
                  "+",
                  Name("result"),
                  ListExpr(BinOp("+", Name("value"), Int(1))))))
            Return(Name("result")))),
        pyList(
          ListItem(pyInt(1))
          ListItem(pyInt(2))
          ListItem(pyInt(3))))
      => .K
    </k>
    <env> .Map => ?_ </env>
    <iter> noIter => ?_ </iter>
    <result>
      noResult
      => result(
           pyList(
             ListItem(pyInt(2))
             ListItem(pyInt(3))
             ListItem(pyInt(4))))
    </result>
endmodule
