requires "domain.k"

module VERIFICATION-CORE
  imports STRING-SEQUENCE-DOMAIN

  // Exact AST fragments shared by the entry and loop claims.
  syntax Stmts ::= "filterLoopBody" [macro]
  rule filterLoopBody
    => If(
         Call(Attribute(Name("string"), "startswith"), Name("prefix")),
         Expr(Call(Attribute(Name("result"), "append"), Name("string"))),
         .Stmts)

  syntax Stmts ::= "filterFunctionBody" [macro]
  rule filterFunctionBody
    => Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("string"), Str(""))
       For(Name("string"), Name("strings"), filterLoopBody)
       Return(Name("result"))

  syntax Module ::= "filterByPrefixProgram" [macro]
  rule filterByPrefixProgram
    => Module(
         ImportFrom("typing", "List")
         FuncDef(
           "filter_by_prefix",
           Params("strings", "prefix"),
           filterFunctionBody))

  // Stable prefix filter with an explicit accumulator.  It is totalized by
  // projecting arbitrary off-domain values through stringCodes; on the
  // theorem's allStrings domain that projection is the value's exact codes.
  // The second argument strictly shrinks and the guards are complementary.
  syntax ValSeq ::= filterPrefixAcc(ValSeq, ValSeq, IntSeq)
                    [function, total]
  rule filterPrefixAcc(ACC:ValSeq, .ValSeq, _:IntSeq) => ACC
  rule filterPrefixAcc(
         ACC:ValSeq,
         vCons(V:Val, REST:ValSeq),
         P:IntSeq)
    => filterPrefixAcc(
         valSeqConcat(
           ACC,
           vCons(str(stringCodes(V)), .ValSeq)),
         REST,
         P)
    requires startsWith(P, stringCodes(V))
    [simplification]
  rule filterPrefixAcc(
         ACC:ValSeq,
         vCons(V:Val, REST:ValSeq),
         P:IntSeq)
    => filterPrefixAcc(ACC, REST, P)
    requires notBool startsWith(P, stringCodes(V))
    [simplification]

  // Operational bridge justified by the bridge-free universal claim
  // CONNECTION-SPEC.string-iterator-normalization.  It preserves the
  // arbitrary continuation and touches no state cell.
  rule <k>
         #iterNext(list(vCons(V:Val, REST:ValSeq)))
         => #iterYield(str(stringCodes(V)), list(REST))
         ...
       </k>
    requires isStringVal(V)
    [priority(40)]

  // The function-call semantics has already performed this deletion.  This
  // derived map identity exposes its normal form to the symbolic simplifier.
  rule ((1 |-> _:Scope) SC:Map)[1 <- undef] => SC
    requires notBool (1 in_keys(SC))
    [simplification]
endmodule
