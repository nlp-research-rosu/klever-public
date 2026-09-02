#!/usr/bin/env python3
import json
import re
from pathlib import Path

from tools import klean_export

candidate_path = Path('/candidate/Proof.lean')
candidate = candidate_path.read_text()
manifest = json.loads(Path('/reference/klean-generation/generator-manifest.json').read_text())
audit = json.loads(Path('/audit-input.json').read_text())['resolution']
target = manifest['target']

base_target = klean_export.target_statement(
    Path('/tmp/audit-work/35-max-element-proof-audit/Base')
)

forbidden = {
    token: [match.start() for match in re.finditer(rf'\b{token}\b', candidate)]
    for token in ('sorry', 'admit', 'unsafe', 'axiom', 'opaque')
}
trust_declarations = klean_export.lean_trust_declarations(candidate_path)
shadow_declarations = re.findall(
    r'(?m)^\s*(?:def|theorem|axiom|opaque)\s+targetStatement\b', candidate
)

final_match = re.search(
    r'(?ms)^theorem\s+final\s*:\s*(.*?)\s*:=\s*by\s*$',
    candidate,
)
if final_match is None:
    raise SystemExit('cannot locate theorem final statement')
final_statement = ' '.join(final_match.group(1).split())

parameter_rows = []
for parameter in target['parameters']:
    name = parameter['name']
    pattern = re.compile(
        rf'(?m)^(?P<prefix>noncomputable\s+)?def\s+{re.escape(name)}\s*:\s*'
        rf'(?P<type>.*?)\s*:=\s*(?P<body>.*)$'
    )
    matches = list(pattern.finditer(candidate))
    parameter_rows.append({
        'name': name,
        'kore_symbol': parameter['kore_symbol'],
        'source_rule_ids': parameter['source_rule_ids'],
        'manifest_type': parameter['type'],
        'definition_count': len(matches),
        'line': None if not matches else candidate.count('\n', 0, matches[0].start()) + 1,
        'candidate_type': None if not matches else ' '.join(matches[0].group('type').split()),
        'candidate_body': None if not matches else matches[0].group('body').strip(),
        'type_matches': bool(matches) and ' '.join(matches[0].group('type').split()) == parameter['type'],
    })

checks = {
    'base_target_equals_generator_manifest': base_target == target,
    'base_target_equals_audit_input': base_target == audit['target'],
    'candidate_forbidden_tokens': forbidden,
    'candidate_new_axiom_or_opaque_declarations': trust_declarations,
    'candidate_target_shadow_declarations': shadow_declarations,
    'parameter_count': len(parameter_rows),
    'all_parameters_defined_once': all(row['definition_count'] == 1 for row in parameter_rows),
    'all_parameter_types_match': all(row['type_matches'] for row in parameter_rows),
    'proof_final_statement': final_statement,
    'proof_final_is_exact_manifest_target_application': final_statement == target['statement'],
}

print('CANDIDATE STRUCTURE CHECKS')
print(json.dumps(checks, indent=2, sort_keys=True))
print('TARGET PARAMETER DEFINITIONS')
print(json.dumps(parameter_rows, indent=2, sort_keys=True))

if not all([
    checks['base_target_equals_generator_manifest'],
    checks['base_target_equals_audit_input'],
    not any(forbidden.values()),
    not trust_declarations,
    not shadow_declarations,
    checks['all_parameters_defined_once'],
    checks['all_parameter_types_match'],
    checks['proof_final_is_exact_manifest_target_application'],
]):
    raise SystemExit('candidate structure check failed')
