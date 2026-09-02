requires "/tmp/audit-work/anti-shuffle-audit/spec.k"

module AUDIT-VACUITY
  imports SPEC

  // Fresh false mutation of the ground empty-input instance of the real entry
  // claim. The actual result is empty; the mutation demands one exclamation.
  claim [false-empty-result]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "anti_shuffle",
            Params("s"),
            Assign(Name("result"), Str(""))
            Assign(Name("word"), Str(""))
            Assign(Name("character"), Str(""))
            Assign(Name("existing"), Str(""))
            Assign(Name("new_word"), Str(""))
            Assign(Name("inserted"), Bool(false))
            For(
              Name("character"),
              Name("s"),
              If(
                Compare(Name("character"), CmpOp("==", Str(" "))),
                AugAssign(Name("result"), "+", Name("word"))
                AugAssign(Name("result"), "+", Str(" "))
                Assign(Name("word"), Str("")),
                Assign(Name("new_word"), Str(""))
                Assign(Name("inserted"), Bool(false))
                For(
                  Name("existing"),
                  Name("word"),
                  If(
                    Name("inserted"),
                    AugAssign(Name("new_word"), "+", Name("existing")),
                    If(
                      Compare(Name("character"), CmpOp("<", Name("existing"))),
                      AugAssign(Name("new_word"), "+", Name("character"))
                      Assign(Name("inserted"), Bool(true)),
                      .Stmts)
                    AugAssign(Name("new_word"), "+", Name("existing"))))
                If(
                  Name("inserted"),
                  Assign(Name("word"), Name("new_word")),
                  Assign(
                    Name("word"),
                    BinOp("+", Name("new_word"), Name("character"))))))
            AugAssign(Name("result"), "+", Name("word"))
            Return(Name("result")))))
      ~> Call(Name("anti_shuffle"), str(.IntSeq))
      => str(iCons(33, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> (scope(.Map, parent(-1))
             => scope("anti_shuffle" |-> antiClosure, parent(-1)))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
