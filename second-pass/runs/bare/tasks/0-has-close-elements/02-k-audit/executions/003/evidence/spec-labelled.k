requires "/tmp/audit-work/candidate-src/verification.k"

module SPEC-LABELLED
  imports VERIFICATION

  claim [audit-claim-01]:
    <k> verify(
          VList(VRat(10, 10), VRat(20, 10), VRat(30, 10)),
          VRat(5, 10)) => VBool(false) </k>

  claim [audit-claim-02]:
    <k> verify(
          VList(VRat(10, 10), VRat(28, 10), VRat(30, 10),
                VRat(40, 10), VRat(50, 10), VRat(20, 10)),
          VRat(3, 10)) => VBool(true) </k>

  claim [audit-claim-03]:
    <k> verify(VList(.PValues), VInt(_T)) => VBool(false) </k>

  claim [audit-claim-04]:
    <k> verify(VList(VInt(_X)), VInt(_T)) => VBool(false) </k>

  claim [audit-claim-05]:
    <k> verify(VList(VInt(X), VInt(Y)), VInt(T))
         => VBool(absInt(X -Int Y) <Int T) </k>

  claim [audit-claim-06]:
    <k> verify(VList(VInt(X), VInt(Y), VInt(Z)), VInt(T))
         => VBool(hasCloseRef(
              VList(VInt(X), VInt(Y), VInt(Z)), VInt(T)))
    </k>

  claim [audit-claim-07]:
    <k> verify(VList(VInt(W), VInt(X), VInt(Y), VInt(Z)), VInt(T))
         => VBool(hasCloseRef(
              VList(VInt(W), VInt(X), VInt(Y), VInt(Z)), VInt(T)))
    </k>

  claim [audit-claim-08]:
    <k> verify(VList(VRat(10, 10), VRat(15, 10)),
              VRat(5, 10)) => VBool(false) </k>

  claim [audit-claim-09]:
    <k> verify(VList(VRat(10, 10), VRat(15, 10)),
              VRat(5000001, 10000000)) => VBool(true) </k>
endmodule
