module SPEC
  imports VERIFICATION

  claim
      <k> solutionProgram ~> start => .K </k>
      <args> pyArgs(promptInput, pyInt(1)) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => returned(pyList(matrixCoords(promptMatrix, 1, 0))) </result>

  claim
      <k> solutionProgram ~> start => .K </k>
      <args> pyArgs(pyList(vnil), pyInt(1)) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => returned(pyList(matrixCoords(mnil, 1, 0))) </result>

  claim
      <k> solutionProgram ~> start => .K </k>
      <args> pyArgs(thirdInput, pyInt(3)) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => returned(pyList(matrixCoords(thirdMatrix, 3, 0))) </result>

  claim [symbolic-000]:
      <k> solutionProgram ~> start => .K </k>
      <args>
        pyArgs(pyList(encodeMatrix(
          mcons(icons(A:Int, icons(B:Int, inil)),
            mcons(icons(C:Int, inil), mnil)))), pyInt(X:Int))
      </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result>
        noResult => returned(pyList(expectedFlags(false, false, false)))
      </result>
    requires A =/=Int X andBool B =/=Int X andBool C =/=Int X

  claim [symbolic-001]:
      <k> solutionProgram ~> start => .K </k>
      <args> pyArgs(pyList(encodeMatrix(mcons(icons(A:Int, icons(B:Int, inil)), mcons(icons(C:Int, inil), mnil)))), pyInt(X:Int)) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => returned(pyList(expectedFlags(false, false, true))) </result>
    requires A =/=Int X andBool B =/=Int X andBool C ==Int X

  claim [symbolic-010]:
      <k> solutionProgram ~> start => .K </k>
      <args> pyArgs(pyList(encodeMatrix(mcons(icons(A:Int, icons(B:Int, inil)), mcons(icons(C:Int, inil), mnil)))), pyInt(X:Int)) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => returned(pyList(expectedFlags(false, true, false))) </result>
    requires A =/=Int X andBool B ==Int X andBool C =/=Int X

  claim [symbolic-011]:
      <k> solutionProgram ~> start => .K </k>
      <args> pyArgs(pyList(encodeMatrix(mcons(icons(A:Int, icons(B:Int, inil)), mcons(icons(C:Int, inil), mnil)))), pyInt(X:Int)) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => returned(pyList(expectedFlags(false, true, true))) </result>
    requires A =/=Int X andBool B ==Int X andBool C ==Int X

  claim [symbolic-100]:
      <k> solutionProgram ~> start => .K </k>
      <args> pyArgs(pyList(encodeMatrix(mcons(icons(A:Int, icons(B:Int, inil)), mcons(icons(C:Int, inil), mnil)))), pyInt(X:Int)) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => returned(pyList(expectedFlags(true, false, false))) </result>
    requires A ==Int X andBool B =/=Int X andBool C =/=Int X

  claim [symbolic-101]:
      <k> solutionProgram ~> start => .K </k>
      <args> pyArgs(pyList(encodeMatrix(mcons(icons(A:Int, icons(B:Int, inil)), mcons(icons(C:Int, inil), mnil)))), pyInt(X:Int)) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => returned(pyList(expectedFlags(true, false, true))) </result>
    requires A ==Int X andBool B =/=Int X andBool C ==Int X

  claim [symbolic-110]:
      <k> solutionProgram ~> start => .K </k>
      <args> pyArgs(pyList(encodeMatrix(mcons(icons(A:Int, icons(B:Int, inil)), mcons(icons(C:Int, inil), mnil)))), pyInt(X:Int)) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => returned(pyList(expectedFlags(true, true, false))) </result>
    requires A ==Int X andBool B ==Int X andBool C =/=Int X

  claim [symbolic-111]:
      <k> solutionProgram ~> start => .K </k>
      <args> pyArgs(pyList(encodeMatrix(mcons(icons(A:Int, icons(B:Int, inil)), mcons(icons(C:Int, inil), mnil)))), pyInt(X:Int)) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => returned(pyList(expectedFlags(true, true, true))) </result>
    requires A ==Int X andBool B ==Int X andBool C ==Int X
endmodule
