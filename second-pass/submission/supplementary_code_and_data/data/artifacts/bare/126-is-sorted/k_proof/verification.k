requires "list-domain.k"

module VERIFICATION
  imports PY-LIST-DOMAIN

  // For integer lists, equality with the ascending sort is equivalent to
  // nondecreasing order.  The second conjunct is the prompt's duplicate bound:
  // every value occurring in the list has multiplicity at most two.
  syntax Bool ::= ascending(IntList) [function]
  rule ascending(IS) => eqIntLists(IS, sortInts(IS))

  syntax Bool ::= duplicateBound(IntList) [function]
  rule duplicateBound(IS) => countsAtMostTwo(IS, IS)

  syntax Bool ::= isSortedContract(IntList) [function]
  rule isSortedContract(IS) => ascending(IS) andBool duplicateBound(IS)
endmodule
