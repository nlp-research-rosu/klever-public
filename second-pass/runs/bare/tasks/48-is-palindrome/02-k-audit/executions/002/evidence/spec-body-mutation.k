requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Operational-sensitivity probe: execute a materially different body
  // (text == text, always true) while keeping the original palindrome result.
  claim
    <py>
      <k>
        Module(
          FuncDef("is_palindrome", Params("text"),
            Return(
              Compare(
                Name("text"),
                CmpOp("==", Name("text"))))))
        ~> #invoke("is_palindrome", PyString(S:String))
      => PyBool(isPalindrome(S))
      </k>
      <functions>
        .Map
      => "is_palindrome" |-> #function(
           "text",
           Return(
             Compare(
               Name("text"),
               CmpOp("==", Name("text")))))
      </functions>
      <env> .Map </env>
    </py>
endmodule
