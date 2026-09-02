requires "verification.k"

module SPEC
  imports VERIFICATION

  // The two examples from prompt.py, represented as exact decimal rationals.
  claim <k> verify(
                  VList(VRat(10, 10), VRat(20, 10), VRat(30, 10)),
                  VRat(5, 10)) => VBool(false) </k>

  claim <k> verify(
                  VList(VRat(10, 10), VRat(28, 10), VRat(30, 10),
                        VRat(40, 10), VRat(50, 10), VRat(20, 10)),
                  VRat(3, 10)) => VBool(true) </k>

  // Boundary behavior: no pair in lists of size zero or one.
  claim <k> verify(VList(.PValues), VInt(_T)) => VBool(false) </k>

  claim <k> verify(VList(VInt(_X)), VInt(_T)) => VBool(false) </k>

  // A symbolic pair establishes strictness: equality with the threshold is
  // false, and the result for arbitrary integers is exactly |x-y| < t.
  claim <k> verify(VList(VInt(X), VInt(Y)), VInt(T))
             => VBool(absInt(X -Int Y) <Int T) </k>

  // For arbitrary values, the interpreter agrees with the independently
  // recursive existential-pair specification.  Length four exercises all six
  // pair positions as well as both source-level recursive functions.
  claim <k> verify(VList(VInt(X), VInt(Y), VInt(Z)), VInt(T))
             => VBool(hasCloseRef(
                  VList(VInt(X), VInt(Y), VInt(Z)), VInt(T)))
        </k>

  claim <k> verify(VList(VInt(W), VInt(X), VInt(Y), VInt(Z)), VInt(T))
             => VBool(hasCloseRef(
                  VList(VInt(W), VInt(X), VInt(Y), VInt(Z)), VInt(T)))
        </k>

  // Concrete strict-boundary checks.
  claim <k> verify(VList(VRat(10, 10), VRat(15, 10)),
                  VRat(5, 10)) => VBool(false) </k>

  claim <k> verify(VList(VRat(10, 10), VRat(15, 10)),
                  VRat(5000001, 10000000)) => VBool(true) </k>
endmodule
