requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh result mutation: the real program is required to return false for
  // every string. This is false for the satisfying witness S = "".
  claim
    <py>
      <k>
        Module(
          FuncDef("is_palindrome", Params("text"),
            Return(
              Compare(
                Name("text"),
                CmpOp(
                  "==",
                  Subscript(
                    Name("text"),
                    Slice(NoBound, NoBound, UnaryOp("-", Int(1)))))))))
        ~> #invoke("is_palindrome", PyString(S:String))
      => PyBool(false)
      </k>
      <functions>
        .Map
      => "is_palindrome" |-> #function(
           "text",
           Return(
             Compare(
               Name("text"),
               CmpOp(
                 "==",
                 Subscript(
                   Name("text"),
                   Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))))
      </functions>
      <env> .Map </env>
    </py>
endmodule
