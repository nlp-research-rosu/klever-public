requires "../source/verification.k"

module SPEC-UNICODE-CANDIDATE-RESULT
  imports VERIFICATION

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
        ~> #invoke(
             "is_palindrome",
             PyString("🙂a🙂"))
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
