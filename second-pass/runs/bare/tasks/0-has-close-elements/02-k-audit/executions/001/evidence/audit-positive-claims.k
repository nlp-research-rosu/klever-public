requires "verification.k"

module AUDIT-CLAIM-1
  imports VERIFICATION
  claim <k> verify(
                  VList(VRat(10, 10), VRat(20, 10), VRat(30, 10)),
                  VRat(5, 10)) => VBool(false) </k>
endmodule

module AUDIT-CLAIM-2
  imports VERIFICATION
  claim <k> verify(
                  VList(VRat(10, 10), VRat(28, 10), VRat(30, 10),
                        VRat(40, 10), VRat(50, 10), VRat(20, 10)),
                  VRat(3, 10)) => VBool(true) </k>
endmodule

module AUDIT-CLAIM-3
  imports VERIFICATION
  claim <k> verify(VList(.PValues), VInt(_T)) => VBool(false) </k>
endmodule

module AUDIT-CLAIM-4
  imports VERIFICATION
  claim <k> verify(VList(VInt(_X)), VInt(_T)) => VBool(false) </k>
endmodule

module AUDIT-CLAIM-5
  imports VERIFICATION
  claim <k> verify(VList(VInt(X), VInt(Y)), VInt(T))
             => VBool(absInt(X -Int Y) <Int T) </k>
endmodule

module AUDIT-CLAIM-6
  imports VERIFICATION
  claim <k> verify(VList(VInt(X), VInt(Y), VInt(Z)), VInt(T))
             => VBool(hasCloseRef(
                  VList(VInt(X), VInt(Y), VInt(Z)), VInt(T)))
        </k>
endmodule

module AUDIT-CLAIM-7
  imports VERIFICATION
  claim <k> verify(VList(VInt(W), VInt(X), VInt(Y), VInt(Z)), VInt(T))
             => VBool(hasCloseRef(
                  VList(VInt(W), VInt(X), VInt(Y), VInt(Z)), VInt(T)))
        </k>
endmodule

module AUDIT-CLAIM-8
  imports VERIFICATION
  claim <k> verify(VList(VRat(10, 10), VRat(15, 10)),
                  VRat(5, 10)) => VBool(false) </k>
endmodule

module AUDIT-CLAIM-9
  imports VERIFICATION
  claim <k> verify(VList(VRat(10, 10), VRat(15, 10)),
                  VRat(5000001, 10000000)) => VBool(true) </k>
endmodule
