requires "verification.k"

module AUDIT-PINNING
  imports VERIFICATION

  // A ground instance of loop-correct's precondition.
  claim [ground-loop-witness]:
    <mpy>
      <k> loop(
             "word",
             cons("ba", cons("ab", nil)),
             solutionLoopBody)
           ~> exec(Return(Name("best")) .Stmts)
        => .K </k>
      <words> cons("ba", cons("ab", nil)) </words>
      <best> "" => ?FINALBEST:String </best>
      <bestCount> -1 => ?FINALCOUNT:Int </bestCount>
      <word> "" => ?FINALWORD:String </word>
      <count> 0 => ?LASTCOUNT:Int </count>
      <result> noResult => result(strVal("ab")) </result>
    </mpy>

  // A ground instance of program-initializes using the literal submitted AST.
  claim [ground-initialization-witness]:
    <mpy>
      <k>
        Module(
          FuncDef("find_max", Params("words"),
            Assign(Name("best"), Str(""))
            Assign(Name("best_count"), UnaryOp("-", Int(1)))
            For(Name("word"), Name("words"),
              Assign(
                Name("count"),
                Call(Name("len"), Call(Name("set"), Name("word"))))
              If(Compare(Name("count"), CmpOp(">", Name("best_count"))),
                Assign(Name("best"), Name("word"))
                Assign(Name("best_count"), Name("count")),
                .Stmts)
              If(Compare(Name("count"), CmpOp("==", Name("best_count"))),
                If(Compare(Name("word"), CmpOp("<", Name("best"))),
                  Assign(Name("best"), Name("word")),
                  .Stmts),
                .Stmts))
            Return(Name("best"))))
        =>
        loop(
          "word",
          cons("name", cons("enam", cons("game", nil))),
          solutionLoopBody)
        ~> exec(Return(Name("best")) .Stmts)
      </k>
      <words> cons("name", cons("enam", cons("game", nil))) </words>
      <best> "" </best>
      <bestCount> -1 </bestCount>
      <word> "" </word>
      <count> 0 </count>
      <result> noResult </result>
    </mpy>

  // The same literal AST executes to a concrete, result-constrained value.
  claim [ground-end-to-end-witness]:
    <mpy>
      <k>
        Module(
          FuncDef("find_max", Params("words"),
            Assign(Name("best"), Str(""))
            Assign(Name("best_count"), UnaryOp("-", Int(1)))
            For(Name("word"), Name("words"),
              Assign(
                Name("count"),
                Call(Name("len"), Call(Name("set"), Name("word"))))
              If(Compare(Name("count"), CmpOp(">", Name("best_count"))),
                Assign(Name("best"), Name("word"))
                Assign(Name("best_count"), Name("count")),
                .Stmts)
              If(Compare(Name("count"), CmpOp("==", Name("best_count"))),
                If(Compare(Name("word"), CmpOp("<", Name("best"))),
                  Assign(Name("best"), Name("word")),
                  .Stmts),
                .Stmts))
            Return(Name("best"))))
        => .K
      </k>
      <words> cons("name", cons("enam", cons("game", nil))) </words>
      <best> "" => ?FINALBEST:String </best>
      <bestCount> -1 => ?FINALCOUNT:Int </bestCount>
      <word> "" => ?FINALWORD:String </word>
      <count> 0 => ?LASTCOUNT:Int </count>
      <result> noResult => result(strVal("enam")) </result>
    </mpy>
endmodule
