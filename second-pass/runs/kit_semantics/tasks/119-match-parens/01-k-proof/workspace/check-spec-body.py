import re
from pathlib import Path


solution_term = re.sub(r'\s+', '', Path('solution.mpy').read_text())
solution_prefix = 'Module(FuncDef("match_parens",Params("lst"),'
assert solution_term.startswith(solution_prefix)
assert solution_term.endswith('))')
solution_body = solution_term[len(solution_prefix):-2]

spec_text = re.sub(r'\s+', '', Path('spec.k').read_text())
# The K inner parser requires explicit empty statement-list units; the external
# .mpy parser accepts the translator's empty list position.  They denote the
# same constructor, so remove only those explicit units before comparison.
spec_text = spec_text.replace('.Stmts', '')
closure_prefix = 'closureVal("lst",'
before, separator, after = spec_text.partition(closure_prefix)
assert separator and 'closureVal("lst",' not in before
spec_body, separator, _rest = after.partition(',0),parent(-1))')
assert separator

assert spec_body == solution_body
print('spec-body-identity: PASS')
