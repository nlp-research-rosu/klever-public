# Exhaustive K source inventory

This is a lexical inventory of every `syntax`, `rule`, `configuration`, `context`, `claim`, and `alias` sentence in the trusted supplied semantics, candidate `verification.k`, and positive `spec.k`.

## Summary

- Files: 26
- Sentences: 975
- Kind counts: `{"claim": 7, "configuration": 1, "context": 5, "rule": 724, "syntax": 238}`
- Attribute counts: `{"concrete": 31, "function": 150, "macro": 2, "macro-rec": 1, "no-evaluators": 23, "owise": 20, "preserves-definedness": 2, "priority(40)": 31, "priority(45)": 2, "simplification": 9, "simplification(10)": 1, "symbol(absF)": 1, "symbol(addF)": 1, "symbol(ceilF)": 1, "symbol(decStrToF)": 1, "symbol(divF)": 1, "symbol(divFloatIntV)": 1, "symbol(divII)": 1, "symbol(eqF)": 1, "symbol(floatLt)": 1, "symbol(floatMod)": 1, "symbol(floorFI)": 1, "symbol(gtF)": 1, "symbol(intFloatDiv)": 1, "symbol(intToF)": 1, "symbol(mulF)": 1, "symbol(powF)": 1, "symbol(projectIntTotal)": 1, "symbol(roundF)": 1, "symbol(roundFN)": 1, "symbol(sortKeyVS)": 1, "symbol(sortVS)": 1, "symbol(sqrtF)": 1, "symbol(subF)": 1, "symbol(toF)": 1, "symbol(truncF)": 1, "symbolic(V)": 1, "total": 117}`

### Special attributes

- `function` (150): /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:20-20, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:36-36, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:54-54, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:97-97, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:102-102, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:114-114, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:117-117, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:126-126, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:134-134, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:158-158, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:188-188, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:194-194, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:196-196, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:199-199, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:203-203, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:214-215, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:226-226, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:230-230, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:238-238, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:244-244, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:247-247, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:250-250, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:255-255, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:265-265, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:269-269, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:272-272, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:293-293, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/call.k:52-52, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/concrete.k:42-42, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/concrete.k:51-51, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/concrete.k:56-56, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:68-68, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:76-76, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:100-100, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:107-107, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:109-109, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:157-157, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:199-199, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:208-208, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:209-209, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:213-213, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:217-217, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:223-223, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:227-227, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:233-233, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k:37-37, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k:43-43, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k:49-49, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k:64-64, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k:70-70, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k:90-90, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k:97-97, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k:101-101, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:24-24, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:30-30, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:37-37, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:50-50, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:54-54, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:73-73, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:86-86, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:93-93, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:103-103, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:107-107, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:111-111, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:115-115, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:119-119, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:125-125, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:142-142, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:160-160, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:165-165, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:167-167, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:173-173, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:179-179, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:190-190, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:195-195, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:209-209, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:217-217, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:223-223, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:230-230, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/int.k:19-19, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/list.k:18-18, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/list.k:33-33, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/list.k:37-38, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:27-27, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:35-35, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:41-41, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:48-48, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:52-52, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:65-65, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:82-82, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:85-85, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:106-106, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:112-112, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:115-115, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:118-118, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:121-121, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:124-124, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:128-128, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:132-132, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:136-136, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:140-140, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:145-145, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:149-149, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:154-154, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:158-158, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:162-162, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:166-166, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/range.k:9-9, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/range.k:12-12, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/set.k:11-11, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/set.k:16-17, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/set.k:25-25, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/set.k:31-31, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/set.k:35-35, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:18-18, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:19-19, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:26-26, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:49-49, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:51-52, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:57-57, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/str.k:13-13, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/str.k:20-20, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/str.k:32-32, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/str.k:37-37, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/str.k:48-48, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:11-11, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:16-16, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:21-21, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:37-37, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:63-63, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:72-72, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:76-76, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:83-83, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:90-90, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:96-96, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:102-102, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:109-109, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:116-116, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/tuple.k:24-24, /tmp/audit-work/108-count-nums-audit/verification.k:9-9, /tmp/audit-work/108-count-nums-audit/verification.k:18-18, /tmp/audit-work/108-count-nums-audit/verification.k:21-22, /tmp/audit-work/108-count-nums-audit/verification.k:50-50, /tmp/audit-work/108-count-nums-audit/verification.k:57-58, /tmp/audit-work/108-count-nums-audit/verification.k:69-69, /tmp/audit-work/108-count-nums-audit/verification.k:80-80, /tmp/audit-work/108-count-nums-audit/verification.k:86-86, /tmp/audit-work/108-count-nums-audit/verification.k:95-95, /tmp/audit-work/108-count-nums-audit/verification.k:99-99, /tmp/audit-work/108-count-nums-audit/verification.k:108-108
- `total` (117): /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:36-36, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:114-114, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:117-117, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:126-126, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:134-134, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:158-158, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:194-194, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:196-196, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:199-199, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:203-203, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:214-215, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:226-226, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:230-230, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:238-238, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:244-244, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:247-247, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:250-250, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:255-255, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:265-265, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:269-269, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:272-272, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/call.k:52-52, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/concrete.k:56-56, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:68-68, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:76-76, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:100-100, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:109-109, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:157-157, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:213-213, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:217-217, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:223-223, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:227-227, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:233-233, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k:37-37, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k:43-43, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k:49-49, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k:90-90, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:24-24, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:30-30, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:37-37, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:50-50, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:54-54, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:73-73, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:86-86, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:93-93, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:103-103, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:107-107, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:111-111, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:115-115, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:119-119, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:125-125, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:142-142, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:160-160, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:167-167, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:173-173, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:179-179, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:190-190, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:195-195, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:209-209, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:217-217, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:223-223, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:230-230, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/list.k:18-18, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/list.k:33-33, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:27-27, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:41-41, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:48-48, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:52-52, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:65-65, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:85-85, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:106-106, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:112-112, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:115-115, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:118-118, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:121-121, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:124-124, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:128-128, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:132-132, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:136-136, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:140-140, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:145-145, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:149-149, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:154-154, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:158-158, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:162-162, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:166-166, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/range.k:9-9, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/set.k:11-11, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/set.k:16-17, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/set.k:25-25, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/set.k:31-31, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/set.k:35-35, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:18-18, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:49-49, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:51-52, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:57-57, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/str.k:20-20, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/str.k:32-32, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/str.k:37-37, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/str.k:48-48, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:11-11, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:21-21, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:72-72, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:90-90, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:96-96, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:102-102, /tmp/audit-work/108-count-nums-audit/verification.k:9-9, /tmp/audit-work/108-count-nums-audit/verification.k:18-18, /tmp/audit-work/108-count-nums-audit/verification.k:21-22, /tmp/audit-work/108-count-nums-audit/verification.k:50-50, /tmp/audit-work/108-count-nums-audit/verification.k:57-58, /tmp/audit-work/108-count-nums-audit/verification.k:69-69, /tmp/audit-work/108-count-nums-audit/verification.k:80-80, /tmp/audit-work/108-count-nums-audit/verification.k:86-86, /tmp/audit-work/108-count-nums-audit/verification.k:95-95, /tmp/audit-work/108-count-nums-audit/verification.k:99-99, /tmp/audit-work/108-count-nums-audit/verification.k:108-108
- `functional` (0): 
- `no-evaluators` (23): /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:24-24, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:30-30, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:37-37, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:50-50, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:54-54, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:103-103, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:107-107, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:111-111, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:115-115, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:119-119, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:125-125, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:142-142, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:160-160, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:190-190, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:195-195, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:209-209, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:217-217, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:223-223, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:230-230, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:18-18, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:49-49, /tmp/audit-work/108-count-nums-audit/verification.k:21-22, /tmp/audit-work/108-count-nums-audit/verification.k:57-58
- `simplification` (10): /tmp/audit-work/108-count-nums-audit/verification.k:24-26, /tmp/audit-work/108-count-nums-audit/verification.k:28-30, /tmp/audit-work/108-count-nums-audit/verification.k:31-33, /tmp/audit-work/108-count-nums-audit/verification.k:34-34, /tmp/audit-work/108-count-nums-audit/verification.k:41-44, /tmp/audit-work/108-count-nums-audit/verification.k:45-48, /tmp/audit-work/108-count-nums-audit/verification.k:59-61, /tmp/audit-work/108-count-nums-audit/verification.k:63-67, /tmp/audit-work/108-count-nums-audit/verification.k:76-78, /tmp/audit-work/108-count-nums-audit/verification.k:90-93
- `concrete` (31): /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:25-25, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:31-31, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:38-38, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:51-51, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:55-55, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:74-74, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:87-87, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:94-94, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:104-104, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:108-108, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:112-112, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:116-116, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:120-120, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:126-126, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:143-143, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:161-161, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:162-164, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:191-191, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:196-196, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:210-210, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:218-222, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:224-226, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:231-231, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:20-20, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:21-21, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:22-22, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:23-23, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:27-27, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:28-28, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k:29-30, /tmp/audit-work/108-count-nums-audit/verification.k:28-30
- `symbolic` (1): /tmp/audit-work/108-count-nums-audit/verification.k:31-33
- `priority` (33): /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/assert.k:13-15, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/bool.k:29-30, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/bool.k:31-34, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/bool.k:35-38, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/bool.k:39-42, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/bool.k:43-46, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:280-281, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/call.k:38-41, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/call.k:42-46, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/call.k:47-50, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/call.k:63-67, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/concrete.k:28-30, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/concrete.k:31-33, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/controls.k:12-18, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/controls.k:95-97, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/controls.k:98-100, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/controls.k:106-108, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k:145-151, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:66-66, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:71-71, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:83-83, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k:233-233, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/list.k:24-25, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:72-74, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:94-96, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/operators.k:25-27, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/operators.k:34-37, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/operators.k:38-42, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/operators.k:44-46, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:31-33, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k:58-60, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/tuple.k:35-41, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/tuple.k:52-54
- `owise` (20): /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:198-198, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:201-201, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:223-223, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:228-228, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:236-236, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:243-243, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:263-264, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:268-268, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:295-295, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k:297-297, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/call.k:20-20, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/call.k:31-31, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/concrete.k:59-59, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/controls.k:36-36, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/controls.k:89-89, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:43-43, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:143-143, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:147-147, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k:152-152, /tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/operators.k:17-17

## Per-file inventory

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/assert.k`

SHA-256: `4258987a261d24b02ab3abfa52b3b2e013ea6323f9d5eb9a59c8f42cbcba030b`. Provenance: trusted supplied semantics.

- Lines 6-7; kind `rule`: `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)`
- Lines 8-11; kind `rule`: `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)`
- Lines 13-15; kind `rule`, attributes: `priority(40)`: `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/bool.k`

SHA-256: `8d6cfa9cd1ed776e51d776e4d358c418960c57715a6f9654ef9af41aea29f4fd`. Provenance: trusted supplied semantics.

- Lines 8-8; kind `rule`: `rule applyUn("not", V:Val) => notBool truthy(V)`
- Lines 10-10; kind `rule`: `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2`
- Lines 11-15; kind `rule`: `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2 // ==== BoolOp: short-circuit, value-returning and / or ===================== // the node is its own accumulator: heat the HEAD element only, then either return it // (short-circuit) or drop it and continue`
- Lines 16-16; kind `context`: `context BoolOp(_, (HOLE:Expr, _:Exprs))`
- Lines 17-17; kind `rule`: `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>`
- Lines 18-19; kind `rule`: `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)`
- Lines 20-21; kind `rule`: `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)`
- Lines 22-23; kind `rule`: `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)`
- Lines 24-28; kind `rule`: `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V) // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the // operand — and/or return the OBJECT itself (Python identity), not its structure`
- Lines 29-30; kind `rule`, attributes: `priority(40)`: `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]`
- Lines 31-34; kind `rule`, attributes: `priority(40)`: `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`
- Lines 35-38; kind `rule`, attributes: `priority(40)`: `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`
- Lines 39-42; kind `rule`, attributes: `priority(40)`: `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`
- Lines 43-46; kind `rule`, attributes: `priority(40)`: `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/builtins.k`

SHA-256: `fa43a855b8a4548f305f3dd210c8f6c6e7aa15b8d1cb0b8296977f061310c2dd`. Provenance: trusted supplied semantics.

- Lines 17-19; kind `syntax`: `syntax Val ::= applyBuiltin(String, Vals) [function] // ==== len(obj) — O(1) per kind ============================================`
- Lines 20-20; kind `syntax`, attributes: `function`: `syntax Int ::= seqLen(Val) [function]`
- Lines 21-21; kind `rule`: `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)`
- Lines 22-22; kind `rule`: `rule seqLen(list(VS:ValSeq)) => vsLen(VS)`
- Lines 23-23; kind `rule`: `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)`
- Lines 24-24; kind `rule`: `rule seqLen(str(IS:IntSeq)) => isLen(IS)`
- Lines 25-25; kind `rule`: `rule seqLen(setV(DS:IntSeq)) => isLen(DS)`
- Lines 26-31; kind `rule`: `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST) // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) == // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order). // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed. // (k-cell — list() constructs a NEW object)`
- Lines 32-32; kind `rule`: `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`
- Lines 33-33; kind `rule`: `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`
- Lines 34-34; kind `rule`: `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>`
- Lines 35-35; kind `rule`: `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>`
- Lines 36-36; kind `syntax`, attributes: `function`, `total`: `syntax ValSeq ::= charsOf(IntSeq) [function, total]`
- Lines 37-37; kind `rule`: `rule charsOf(.IntSeq) => .ValSeq`
- Lines 38-40; kind `rule`: `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R)) // ==== set(str) — distinct character codes =================================`
- Lines 41-43; kind `rule`: `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS)) // ==== abs(int) ============================================================`
- Lines 44-46; kind `rule`: `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I) // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==`
- Lines 47-47; kind `syntax`: `syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)`
- Lines 48-48; kind `rule`: `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>`
- Lines 49-49; kind `rule`: `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>`
- Lines 50-52; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)`
- Lines 54-54; kind `syntax`, attributes: `function`: `syntax Int ::= intOf(Val) [function]`
- Lines 55-55; kind `rule`: `rule intOf(I:Int) => I`
- Lines 56-58; kind `rule`: `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi // ==== all / any (short-circuiting #iterNext folds) ========================`
- Lines 59-59; kind `syntax`: `syntax KItem ::= #allAcc(Iterable) | "#allCont"`
- Lines 60-60; kind `rule`: `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>`
- Lines 61-61; kind `rule`: `rule <k> #iterDone ~> #allCont => true ... </k>`
- Lines 62-63; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)`
- Lines 64-65; kind `rule`: `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)`
- Lines 67-67; kind `syntax`: `syntax KItem ::= #anyAcc(Iterable) | "#anyCont"`
- Lines 68-68; kind `rule`: `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>`
- Lines 69-69; kind `rule`: `rule <k> #iterDone ~> #anyCont => false ... </k>`
- Lines 70-71; kind `rule`: `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)`
- Lines 72-75; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V) // ==== max / min over an iterable (#iterNext folds; first element seeds) ====`
- Lines 76-76; kind `syntax`: `syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)`
- Lines 77-77; kind `rule`: `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>`
- Lines 78-79; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)`
- Lines 80-80; kind `rule`: `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>`
- Lines 81-81; kind `rule`: `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>`
- Lines 82-84; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)`
- Lines 86-86; kind `syntax`: `syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)`
- Lines 87-87; kind `rule`: `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>`
- Lines 88-89; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)`
- Lines 90-90; kind `rule`: `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>`
- Lines 91-91; kind `rule`: `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>`
- Lines 92-96; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V) // ==== variadic max / min (a Vals fold) ====================================`
- Lines 97-97; kind `syntax`, attributes: `function`: `syntax Int ::= maxVals(Int, Vals) [function]`
- Lines 98-98; kind `rule`: `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)`
- Lines 99-99; kind `rule`: `rule maxVals(M:Int, .Vals) => M`
- Lines 100-100; kind `rule`: `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)`
- Lines 102-102; kind `syntax`, attributes: `function`: `syntax Int ::= minVals(Int, Vals) [function]`
- Lines 103-103; kind `rule`: `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)`
- Lines 104-104; kind `rule`: `rule minVals(M:Int, .Vals) => M`
- Lines 105-107; kind `rule`: `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R) // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==`
- Lines 108-110; kind `rule`: `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0 // negative operand: the '-' sign prefixes the magnitude's digits`
- Lines 111-113; kind `rule`: `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0`
- Lines 114-114; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= binCodes(Int) [function, total]`
- Lines 115-115; kind `rule`: `rule binCodes(0) => iCons(48, .IntSeq)`
- Lines 116-116; kind `rule`: `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0`
- Lines 117-117; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]`
- Lines 118-118; kind `rule`: `rule binAcc(0, ACC:IntSeq) => ACC`
- Lines 119-123; kind `rule`: `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0 // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========`
- Lines 124-125; kind `rule`: `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>`
- Lines 126-126; kind `syntax`, attributes: `function`, `total`: `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]`
- Lines 127-127; kind `rule`: `rule enumVS(.ValSeq, _:Int) => .ValSeq`
- Lines 128-131; kind `rule`: `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1)) // ==== map(str, xs) — eager (only the str case is in the subset) =============`
- Lines 132-133; kind `rule`: `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>`
- Lines 134-134; kind `syntax`, attributes: `function`, `total`: `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]`
- Lines 135-135; kind `rule`: `rule mapStrVS(.ValSeq) => .ValSeq`
- Lines 136-136; kind `rule`: `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))`
- Lines 137-139; kind `rule`: `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R)) // ==== int(x) identities (int(round(x)) composes through) ====================`
- Lines 140-142; kind `rule`: `rule applyBuiltin("int", I:Int, .Vals) => I // ==== ord / chr ===========================================================`
- Lines 143-143; kind `rule`: `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C`
- Lines 144-147; kind `rule`: `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128 // ==== str(int) / str(str) =================================================`
- Lines 148-148; kind `rule`: `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))`
- Lines 149-151; kind `rule`: `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS) // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====`
- Lines 152-155; kind `rule`: `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57 // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)`
- Lines 156-157; kind `rule`: `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2`
- Lines 158-158; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]`
- Lines 159-159; kind `rule`: `rule intDigAcc(.IntSeq, ACC:Int) => ACC`
- Lines 160-162; kind `rule`: `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48)) // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====`
- Lines 163-163; kind `rule`: `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)`
- Lines 164-166; kind `rule`: `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B) // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)`
- Lines 167-168; kind `rule`: `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>`
- Lines 169-169; kind `rule`: `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>`
- Lines 170-170; kind `rule`: `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>`
- Lines 171-172; kind `rule`: `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>`
- Lines 173-173; kind `rule`: `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>`
- Lines 174-176; kind `rule`: `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k> // ==== range(stop) / range(start, stop) / range(start, stop, step) =========`
- Lines 177-177; kind `rule`: `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)`
- Lines 178-178; kind `rule`: `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)`
- Lines 179-186; kind `rule`: `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0 // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ======== // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's // trusted pass evaluator, now DEFINED in the reference and driven by a // code-level tokenizer. Reduces on concrete strings (krun); a symbolic // argument leaves the call unevaluated for problem-level folds.`
- Lines 187-187; kind `rule`: `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)`
- Lines 188-188; kind `syntax`, attributes: `function`: `syntax Int ::= evalArith(IntSeq) [function]`
- Lines 189-190; kind `rule`: `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))`
- Lines 192-192; kind `syntax`: `syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)`
- Lines 194-194; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= evDigit(Int) [function, total]`
- Lines 195-195; kind `rule`: `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57`
- Lines 196-196; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= evHead42(IntSeq) [function, total]`
- Lines 197-197; kind `rule`: `rule evHead42(iCons(42, _:IntSeq)) => true`
- Lines 198-198; kind `rule`, attributes: `owise`: `rule evHead42(_:IntSeq) => false [owise]`
- Lines 199-199; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= evHead47(IntSeq) [function, total]`
- Lines 200-200; kind `rule`: `rule evHead47(iCons(47, _:IntSeq)) => true`
- Lines 201-201; kind `rule`, attributes: `owise`: `rule evHead47(_:IntSeq) => false [owise]`
- Lines 203-203; kind `syntax`, attributes: `function`, `total`: `syntax OpSeq ::= tokOps(IntSeq) [function, total]`
- Lines 204-204; kind `rule`: `rule tokOps(.IntSeq) => .OpSeq`
- Lines 205-205; kind `rule`: `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)`
- Lines 206-206; kind `rule`: `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)`
- Lines 207-207; kind `rule`: `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))`
- Lines 208-208; kind `rule`: `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)`
- Lines 209-209; kind `rule`: `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))`
- Lines 210-210; kind `rule`: `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)`
- Lines 211-211; kind `rule`: `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))`
- Lines 212-212; kind `rule`: `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))`
- Lines 214-215; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= tokNds(IntSeq) [function, total] | tokNdAcc(Int, IntSeq) [function, total]`
- Lines 216-216; kind `rule`: `rule tokNds(.IntSeq) => .IntSeq`
- Lines 217-217; kind `rule`: `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)`
- Lines 218-218; kind `rule`: `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)`
- Lines 219-220; kind `rule`: `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32`
- Lines 221-222; kind `rule`: `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)`
- Lines 223-223; kind `rule`, attributes: `owise`: `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]`
- Lines 225-225; kind `syntax`: `syntax EvPair ::= evp(OpSeq, IntSeq)`
- Lines 226-226; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= firstNdE(EvPair) [function, total]`
- Lines 227-227; kind `rule`: `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N`
- Lines 228-228; kind `rule`, attributes: `owise`: `rule firstNdE(_:EvPair) => 0 [owise]`
- Lines 230-230; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= applyOpE(String, Int, Int) [function, total]`
- Lines 231-231; kind `rule`: `rule applyOpE("+", A:Int, B:Int) => A +Int B`
- Lines 232-232; kind `rule`: `rule applyOpE("-", A:Int, B:Int) => A -Int B`
- Lines 233-233; kind `rule`: `rule applyOpE("*", A:Int, B:Int) => A *Int B`
- Lines 234-234; kind `rule`: `rule applyOpE("//", A:Int, B:Int) => A divInt B`
- Lines 235-235; kind `rule`: `rule applyOpE("**", A:Int, B:Int) => A ^Int B`
- Lines 236-236; kind `rule`, attributes: `owise`: `rule applyOpE(_:String, A:Int, _:Int) => A [owise]`
- Lines 238-238; kind `syntax`, attributes: `function`, `total`: `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]`
- Lines 239-239; kind `rule`: `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)`
- Lines 240-240; kind `rule`: `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))`
- Lines 241-242; kind `rule`: `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"`
- Lines 243-243; kind `rule`, attributes: `owise`: `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]`
- Lines 244-244; kind `syntax`, attributes: `function`, `total`: `syntax EvPair ::= powCombE(Int, EvPair) [function, total]`
- Lines 245-245; kind `rule`: `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))`
- Lines 246-246; kind `rule`: `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))`
- Lines 247-247; kind `syntax`, attributes: `function`, `total`: `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]`
- Lines 248-248; kind `rule`: `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))`
- Lines 250-250; kind `syntax`, attributes: `function`, `total`: `syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]`
- Lines 251-251; kind `rule`: `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)`
- Lines 252-252; kind `rule`: `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`
- Lines 253-253; kind `rule`: `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)`
- Lines 254-254; kind `rule`: `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`
- Lines 255-255; kind `syntax`, attributes: `function`, `total`: `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]`
- Lines 256-256; kind `rule`: `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))`
- Lines 257-259; kind `rule`: `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)`
- Lines 260-262; kind `rule`: `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)`
- Lines 263-264; kind `rule`, attributes: `owise`: `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]`
- Lines 265-265; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= inLevelE(String, String) [function, total]`
- Lines 266-266; kind `rule`: `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"`
- Lines 267-267; kind `rule`: `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"`
- Lines 268-268; kind `rule`, attributes: `owise`: `rule inLevelE(_:String, _:String) => false [owise]`
- Lines 269-269; kind `syntax`, attributes: `function`, `total`: `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]`
- Lines 270-270; kind `rule`: `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)`
- Lines 271-271; kind `rule`: `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))`
- Lines 272-272; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]`
- Lines 273-273; kind `rule`: `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)`
- Lines 274-278; kind `rule`: `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N)) // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ================== // The md5 value itself is a named shared trust (sortVS-style, no concrete // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).`
- Lines 279-279; kind `syntax`: `syntax KItem ::= "#md5"`
- Lines 280-281; kind `rule`, attributes: `priority(40)`: `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]`
- Lines 282-282; kind `rule`: `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>`
- Lines 283-283; kind `syntax`: `syntax Val ::= md5Obj(IntSeq)`
- Lines 284-284; kind `rule`: `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))`
- Lines 285-290; kind `syntax`: `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] // ==== isinstance(V, int|str) — an ordinary 2-arg builtin =================== // The type argument (int/str) is an ordinary name that resolves via the builtins frame to // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).`
- Lines 291-291; kind `rule`: `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)`
- Lines 292-292; kind `rule`: `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)`
- Lines 293-293; kind `syntax`, attributes: `function`: `syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]`
- Lines 294-294; kind `rule`: `rule isIntV(_:Int) => true`
- Lines 295-295; kind `rule`, attributes: `owise`: `rule isIntV(_:Val) => false [owise]`
- Lines 296-296; kind `rule`: `rule isStrV(str(_:IntSeq)) => true`
- Lines 297-297; kind `rule`, attributes: `owise`: `rule isStrV(_:Val) => false [owise]`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/call.k`

SHA-256: `7e4d6c7cabe7bb4ccff52f21c5d5f30920ccb48d42864146ce53146509f736e4`. Provenance: trusted supplied semantics.

- Lines 16-18; kind `rule`: `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k> // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)`
- Lines 19-19; kind `syntax`: `syntax KItem ::= #callee(Exprs)`
- Lines 20-20; kind `rule`, attributes: `owise`: `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]`
- Lines 21-23; kind `rule`: `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k> // ==== dispatch on the callee value ========================================`
- Lines 24-24; kind `rule`: `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>`
- Lines 26-26; kind `rule`: `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>`
- Lines 27-27; kind `rule`: `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>`
- Lines 28-28; kind `rule`: `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>`
- Lines 29-29; kind `rule`: `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>`
- Lines 30-30; kind `rule`: `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>`
- Lines 31-31; kind `rule`, attributes: `owise`: `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]`
- Lines 32-37; kind `rule`: `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k> // ==== heap-object arguments/receivers ===================================== // Builtins and type calls READ structure — deref the first two arg positions // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list // methods take the ref itself; every other method receiver is deref'd.`
- Lines 38-41; kind `rule`, attributes: `priority(40)`: `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- Lines 42-46; kind `rule`, attributes: `priority(40)`: `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]`
- Lines 47-50; kind `rule`, attributes: `priority(40)`: `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- Lines 52-52; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= isMutMethod(String) [function, total]`
- Lines 53-55; kind `rule`: `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"`
- Lines 56-62; kind `rule`: `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)] // non-mutating methods READ their heap-object arguments too (join's list); // mutators keep refs (append of a list into a list-of-lists stays aliased)`
- Lines 63-67; kind `rule`, attributes: `priority(40)`: `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]`
- Lines 69-79; kind `rule`: `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> // annotated closure: the frame starts with the captured freevar cells, its // parent is the module scope (all enclosing-local reads go through cells), // and the cellvars' fresh cells allocate before params bind (a cellvar param // then writes through its cell in #bindP).`
- Lines 80-85; kind `rule`: `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`
- Lines 87-87; kind `syntax`: `syntax KItem ::= #allocCells(ParamNames)`
- Lines 88-88; kind `rule`: `rule <k> #allocCells(.ParamNames) => .K ... </k>`
- Lines 89-94; kind `rule`: `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N |-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/comprehension.k`

SHA-256: `cf7c38aad5cff698ebb05ecbadf00cbf210ddb2f54ae86f22b328311c027c6a7`. Provenance: trusted supplied semantics.

- Lines 11-11; kind `rule`: `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`
- Lines 12-12; kind `rule`: `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`
- Lines 14-14; kind `syntax`, attributes: `macro`: `syntax Stmts ::= compBody(CompFors, Expr) [macro]`
- Lines 15-16; kind `rule`: `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))`
- Lines 18-18; kind `syntax`, attributes: `macro-rec`: `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]`
- Lines 19-20; kind `rule`: `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))`
- Lines 21-22; kind `rule`: `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))`
- Lines 24-24; kind `syntax`, attributes: `macro`: `syntax Expr ::= compGuard(Exprs) [macro]`
- Lines 25-25; kind `rule`: `rule compGuard(.Exprs) => Bool(true)`
- Lines 26-26; kind `rule`: `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/concrete.k`

SHA-256: `1ffea42a32610e9116506d709e9163413aeb5f6deb7824ea554aca8341f2d305`. Provenance: trusted supplied semantics.

- Lines 13-15; kind `rule`: `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)`
- Lines 16-24; kind `rule`: `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) // ==== keyed sort, concrete leg ============================================ // Computes each key by a REAL call through the uniform #callee machinery // (closures, len, type objects all work), stable-inserts on the key, and // allocates the result. priority(40) beats sort.k's opaque rules, so krun // runs this and proofs (which never see MPY-CONCRETE) keep sortKeyVS.`
- Lines 25-25; kind `syntax`: `syntax Val ::= kvP(Val, Val)`
- Lines 26-27; kind `syntax`: `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) | #ksIns(Val, ValSeq, Val, ValSeq, Bool)`
- Lines 28-30; kind `rule`, attributes: `priority(40)`: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]`
- Lines 31-33; kind `rule`, attributes: `priority(40)`: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]`
- Lines 34-35; kind `rule`: `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>`
- Lines 36-37; kind `rule`: `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>`
- Lines 38-40; kind `rule`: `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)`
- Lines 42-42; kind `syntax`, attributes: `function`: `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]`
- Lines 43-43; kind `rule`: `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)`
- Lines 44-46; kind `rule`: `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)`
- Lines 47-49; kind `rule`: `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)`
- Lines 51-51; kind `syntax`, attributes: `function`: `syntax Bool ::= kLt(Val, Val) [function]`
- Lines 52-52; kind `rule`: `rule kLt(I1:Int, I2:Int) => I1 <Int I2`
- Lines 53-53; kind `rule`: `rule kLt(F1:Float, F2:Float) => F1 <Float F2`
- Lines 54-54; kind `rule`: `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`
- Lines 56-56; kind `syntax`, attributes: `function`, `total`: `syntax ValSeq ::= unpairVS(ValSeq) [function, total]`
- Lines 57-57; kind `rule`: `rule unpairVS(.ValSeq) => .ValSeq`
- Lines 58-58; kind `rule`: `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))`
- Lines 59-59; kind `rule`, attributes: `owise`: `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/controls.k`

SHA-256: `325c73757d5a7ccf541b93240accd590a2cee90d84470efa3a4a0a14165aafae`. Provenance: trusted supplied semantics.

- Lines 9-11; kind `rule`: `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`
- Lines 12-18; kind `rule`, attributes: `priority(40)`: `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`
- Lines 20-26; kind `rule`: `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M) // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).`
- Lines 27-34; kind `rule`: `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)] // ==== import trivia: `from math import floor, ceil` binds the supported // names as builtins in the current scope; every other import is a no-op`
- Lines 35-35; kind `rule`: `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>`
- Lines 36-36; kind `rule`, attributes: `owise`: `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]`
- Lines 37-37; kind `syntax`: `syntax KItem ::= #bindImports(ParamNames)`
- Lines 38-38; kind `rule`: `rule <k> #bindImports(.ParamNames) => .K ... </k>`
- Lines 39-42; kind `rule`: `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"`
- Lines 43-47; kind `rule`: `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil") // ==== Expr statement: evaluate for effect, discard the value =============== // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)`
- Lines 48-50; kind `rule`: `rule <k> Expr(_:Val) => .K ... </k> // ==== If (condition evaluated by strictness) ==============================`
- Lines 51-51; kind `syntax`: `syntax KItem ::= #branch(Bool, Stmts, Stmts)`
- Lines 52-52; kind `rule`: `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>`
- Lines 53-53; kind `rule`: `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>`
- Lines 54-56; kind `rule`: `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k> // ==== IfExp: ternary T if C else E ========================================`
- Lines 57-58; kind `rule`: `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)`
- Lines 59-64; kind `rule`: `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V) // ==== For: one loop, in-cell continuation, over #iterNext ================= // (the iterable is evaluated once, by strictness; the protocol stays rewrites — // circularities anchor on #loop and narrowing substitutes the structure)`
- Lines 65-67; kind `syntax`: `syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts) | #while(Expr, Stmts) | #whileCond(Expr, Stmts) | #loopLbl(K) | "#cont" | "#brk"`
- Lines 69-69; kind `rule`: `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>`
- Lines 71-71; kind `rule`: `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>`
- Lines 72-72; kind `rule`: `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>`
- Lines 73-76; kind `rule`: `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k> // ==== While ==============================================================`
- Lines 77-77; kind `rule`: `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>`
- Lines 78-78; kind `rule`: `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>`
- Lines 79-80; kind `rule`: `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)`
- Lines 81-84; kind `rule`: `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V) // ==== loop control (break / continue) =====================================`
- Lines 85-85; kind `rule`: `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>`
- Lines 86-86; kind `rule`: `rule <k> Continue => #cont ... </k>`
- Lines 87-87; kind `rule`: `rule <k> Break => #brk ... </k>`
- Lines 88-88; kind `rule`: `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>`
- Lines 89-89; kind `rule`, attributes: `owise`: `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]`
- Lines 90-90; kind `rule`: `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>`
- Lines 91-94; kind `rule`: `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise] // ==== heap-object deref at the truthiness/iteration consumers ============== // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)`
- Lines 95-97; kind `rule`, attributes: `priority(40)`: `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- Lines 98-100; kind `rule`, attributes: `priority(40)`: `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- Lines 101-105; kind `rule`: `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)] // For derefs its iterable ONCE at loop start (iteration is over the snapshot; // mutating the iterated list inside its own loop is outside the subset)`
- Lines 106-108; kind `rule`, attributes: `priority(40)`: `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/core.k`

SHA-256: `e0fdc11dc2b9cd0acb18fe7c832c1ea1ac0c9e79cadf40c63f34276aca513d7e`. Provenance: trusted supplied semantics.

- Lines 13-13; kind `syntax`: `syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)`
- Lines 14-14; kind `syntax`: `syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)`
- Lines 15-17; kind `syntax`: `syntax Str ::= str(IntSeq) // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)`
- Lines 18-23; kind `syntax`: `syntax Iterable ::= list(ValSeq) | tuple(ValSeq) | Str | rangeObj(Int, Int, Int) | zipObj(ValSeq, ValSeq) | zipObjS(IntSeq, IntSeq)`
- Lines 25-34; kind `syntax`: `syntax Val ::= Int | Bool | "noneV" | Iterable | ref(Int) // a heap object: <heap> holds its list(VS) | cellRef(Int) // a closure cell: <heap> holds cellV(V) | closureVal(ParamNames, Stmts, Int) | typeV(String) // a type object (int/str), resolved from the builtins frame | builtinV(String) // a builtin function, resolved like any name (LEGB fallthrough) | boundMethodV(Val, String) // a cooled Attribute: obj.method`
- Lines 36-36; kind `syntax`: `syntax Parent ::= "root" | parent(Int)`
- Lines 37-37; kind `syntax`: `syntax Scope ::= scope(Map, Parent)`
- Lines 38-38; kind `syntax`: `syntax KResult ::= Val`
- Lines 39-39; kind `syntax`: `syntax Expr ::= Val // cooling puts results back into expression holes`
- Lines 40-40; kind `syntax`: `syntax Vals ::= List{Val, ","}`
- Lines 41-41; kind `syntax`: `syntax Exc ::= "NoExc" | "AssertionError"`
- Lines 42-48; kind `syntax`: `syntax RetState ::= "noRet" | retV(Val) // ==== configuration ======================================================= // The builtins namespace is a real scope at reserved location -1 (the bottom of every // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0) // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str` // resolve to their type objects; any local/global binding shadows them via normal lookup.`
- Lines 49-67; kind `configuration`: `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code> // ==== heap allocation (constructed lists become objects) ================== // Cons-form emission with a freshness guard (the heap-list-probe discipline: // an update-form H[N <- _] never re-normalizes symbolically). heapLoc is // monotonic — it does NOT wind back at #pop: returned lists escape by ref. // A bare list(VS) Val stays legal (read-only inputs in claims flow unboxed); // only CONSTRUCTORS in program syntax allocate.`
- Lines 68-68; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= isRefV(Val) [function, total]`
- Lines 69-69; kind `rule`: `rule isRefV(ref(_:Int)) => true`
- Lines 70-74; kind `rule`: `rule isRefV(_:Val) => false [owise] // closure cells (Python-faithful capture): the heap holds cellV(V); a // cellRef surfacing as the k-redex reads through (lookup is the only use — // cellRefs never escape to user-visible values)`
- Lines 75-75; kind `syntax`: `syntax HeapVal ::= cellV(Val)`
- Lines 76-76; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= isCellRef(Val) [function, total]`
- Lines 77-77; kind `rule`: `rule isCellRef(cellRef(_:Int)) => true`
- Lines 78-84; kind `rule`: `rule isCellRef(_:Val) => false [owise] // k-top deref for cell-bound reads surfacing INSIDE the annotated frame // (AugAssign's in-place read and friends). The "$cells" guard keeps this // DECIDABLY inapplicable in plain frames — an unguarded rule lets the // prover narrow abstract k-top values into cellRef junk (probed on // 26-remove-duplicates). Cross-frame reads (a comprehension closure // reading the enclosing function's cellvar) deref inside #look instead.`
- Lines 85-94; kind `rule`: `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)] // write through a cell (Assign / #bindP / #bindTgt dispatch here on // cell-bound names) // a keyword argument cools to a TAGGED value (consumed by kw-aware builtins)`
- Lines 95-95; kind `syntax`: `syntax Val ::= kwV(String, Val)`
- Lines 96-96; kind `syntax`: `syntax KItem ::= #kwTag(String)`
- Lines 97-97; kind `rule`: `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>`
- Lines 98-99; kind `rule`: `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)`
- Lines 100-100; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= isKwV(Val) [function, total]`
- Lines 101-101; kind `rule`: `rule isKwV(kwV(_:String, _:Val)) => true`
- Lines 102-105; kind `rule`: `rule isKwV(_:Val) => false [owise] // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch // decides by pnMember even over an abstract frame rest (no prover branching)`
- Lines 106-106; kind `syntax`: `syntax Val ::= cellsMark(ParamNames)`
- Lines 107-107; kind `syntax`, attributes: `function`: `syntax ParamNames ::= cellsOf(Val) [function]`
- Lines 108-108; kind `rule`: `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS`
- Lines 109-109; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= pnMember(String, ParamNames) [function, total]`
- Lines 110-110; kind `rule`: `rule pnMember(_:String, .ParamNames) => false`
- Lines 111-111; kind `rule`: `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)`
- Lines 113-113; kind `syntax`: `syntax KItem ::= #cellW(Val, Val)`
- Lines 114-115; kind `rule`: `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H |-> cellV(_:Val => V) ... </heap>`
- Lines 117-117; kind `syntax`: `syntax KItem ::= #alloc(Val)`
- Lines 118-123; kind `rule`: `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N |-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) // ==== module load + statement sequencing ==================================`
- Lines 124-124; kind `syntax`: `syntax KItem ::= #loadAll(Module)`
- Lines 125-125; kind `rule`: `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>`
- Lines 126-126; kind `rule`: `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>`
- Lines 127-129; kind `rule`: `rule <k> .Stmts => .K ... </k> // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====`
- Lines 130-130; kind `syntax`: `syntax KItem ::= #look(String, Int)`
- Lines 131-131; kind `rule`: `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>`
- Lines 132-144; kind `rule`: `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M) // a SYNTACTICALLY cell-bound name reads through the heap cell AT THE // LOOKUP (higher priority beats the plain return above on concrete cell // bindings; abstract claim values take the plain rule unchanged) — this // covers cross-frame cell reads (a comprehension closure reading the // enclosing function's cellvar) without a narrowing-prone k-top redex // guarded on the FOUND frame's DECLARED cellvars (pnMember over the // cellsMark): decidable for every concrete frame pin — plain frames and // non-cell names prune outright, so an abstract looked-up value never // drags a narrowing cellV heap match along (probed on 5-intersperse and // Q4's abstract `numbers` in the annotated frame)`
- Lines 145-151; kind `rule`, attributes: `priority(40)`: `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]`
- Lines 152-156; kind `rule`: `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M)) // the ONE predefined builtins scope (the -1 frame; claims write `-1 |-> builtinsScope`)`
- Lines 157-157; kind `syntax`, attributes: `function`, `total`: `syntax Scope ::= "builtinsScope" [function, total]`
- Lines 158-184; kind `rule`: `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list" <- builtinV("list") ] [ "round" <- builtinV("round") ] [ "bin" <- builtinV("bin") ] [ "enumerate" <- builtinV("enumerate") ] [ "map" <- builtinV("map") ] [ "eval" <- builtinV("eval") ] [ "int" <- typeV("int") ] [ "str" <- typeV("str") ] [ "float" <- typeV("float") ], root) // ==== argument/element evaluation: ONE left-to-right loop, tagged by destination == // (list/tuple literals and calls all use it; modules extend ApplyK with their tags)`
- Lines 185-185; kind `syntax`: `syntax ApplyK ::= toCall(Val)`
- Lines 186-188; kind `syntax`: `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) | #evalArgCont(Exprs, Vals, ApplyK) | #applyK(ApplyK, Vals)`
- Lines 189-189; kind `rule`: `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>`
- Lines 190-190; kind `rule`: `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>`
- Lines 191-193; kind `rule`: `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k> // ==== Int / Bool / None literals ==========================================`
- Lines 194-194; kind `rule`: `rule <k> Int(I:Int) => I ... </k>`
- Lines 195-195; kind `rule`: `rule <k> Bool(B:Bool) => B ... </k>`
- Lines 196-198; kind `rule`: `rule <k> NoneVal => noneV ... </k> // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================`
- Lines 199-199; kind `syntax`, attributes: `function`: `syntax Bool ::= truthy(Val) [function]`
- Lines 200-200; kind `rule`: `rule truthy(B:Bool) => B`
- Lines 201-201; kind `rule`: `rule truthy(noneV) => false`
- Lines 202-202; kind `rule`: `rule truthy(I:Int) => I =/=Int 0`
- Lines 203-203; kind `rule`: `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)`
- Lines 204-204; kind `rule`: `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)`
- Lines 205-207; kind `rule`: `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq) // ==== extensible operator dispatch (cases added by the construct modules) ==`
- Lines 208-208; kind `syntax`, attributes: `function`: `syntax Val ::= applyUn(String, Val) [function]`
- Lines 209-209; kind `syntax`, attributes: `function`: `syntax Val ::= applyBin(String, Val, Val) [function]`
- Lines 210-212; kind `syntax`: `syntax Bool ::= applyCmp(String, Val, Val) [function] // ==== shared list helpers =================================================`
- Lines 213-213; kind `syntax`, attributes: `function`, `total`: `syntax Vals ::= appendVal(Vals, Val) [function, total]`
- Lines 214-214; kind `rule`: `rule appendVal(.Vals, V:Val) => V , .Vals`
- Lines 215-215; kind `rule`: `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)`
- Lines 217-217; kind `syntax`, attributes: `function`, `total`: `syntax ValSeq ::= vals2valSeq(Vals) [function, total]`
- Lines 218-218; kind `rule`: `rule vals2valSeq(.Vals) => .ValSeq`
- Lines 219-222; kind `rule`: `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS)) // ==== shared sequence length (len / summaries across many modules) ======== // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)`
- Lines 223-223; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= vsLen(ValSeq) [function, total]`
- Lines 224-224; kind `rule`: `rule vsLen(.ValSeq) => 0`
- Lines 225-225; kind `rule`: `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)`
- Lines 227-227; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= isLen(IntSeq) [function, total]`
- Lines 228-228; kind `rule`: `rule isLen(.IntSeq) => 0`
- Lines 229-232; kind `rule`: `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S) // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)`
- Lines 233-233; kind `syntax`, attributes: `function`, `total`: `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]`
- Lines 234-234; kind `rule`: `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq`
- Lines 235-235; kind `rule`: `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)`
- Lines 236-237; kind `rule`: `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0`
- Lines 238-239; kind `rule`: `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/dict.k`

SHA-256: `779b06e18162464c8422bbd6ac35fa0b9e34ef82807d5c707c6f4552d63c0580`. Provenance: trusted supplied semantics.

- Lines 20-22; kind `syntax`: `syntax Val ::= dictV(ValSeq, ValSeq) // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.`
- Lines 23-25; kind `syntax`: `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) | #dictKey(Expr, Entries, ValSeq, ValSeq) | #dictVal(Val, Entries, ValSeq, ValSeq)`
- Lines 26-26; kind `rule`: `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>`
- Lines 27-27; kind `rule`: `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>`
- Lines 28-29; kind `rule`: `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>`
- Lines 30-31; kind `rule`: `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>`
- Lines 32-36; kind `rule`: `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k> // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.`
- Lines 37-37; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]`
- Lines 38-38; kind `rule`: `rule dHasKey(.ValSeq, _:Val) => false`
- Lines 39-39; kind `rule`: `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K`
- Lines 40-42; kind `rule`: `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K) // dPutK: KS unchanged if K already present, else append K (keep-first-position).`
- Lines 43-43; kind `syntax`, attributes: `function`, `total`: `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]`
- Lines 44-44; kind `rule`: `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)`
- Lines 45-48; kind `rule`: `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K) // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).`
- Lines 49-49; kind `syntax`, attributes: `function`, `total`: `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]`
- Lines 50-51; kind `rule`: `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K`
- Lines 52-53; kind `rule`: `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)`
- Lines 54-57; kind `rule`: `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise] // ==== dict methods ======================================================== // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).`
- Lines 58-62; kind `rule`: `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)] // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==`
- Lines 63-63; kind `rule`: `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)`
- Lines 64-64; kind `syntax`, attributes: `function`: `syntax Val ::= applyIndexD(Val, Val) [function]`
- Lines 65-69; kind `rule`: `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)] // ==== dict subscript-assign: d[k] = v (insert/update in place) ============= // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.`
- Lines 70-70; kind `syntax`, attributes: `function`: `syntax Val ::= dictSet(Val, Val, Val) [function]`
- Lines 71-75; kind `rule`: `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V)) // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope // value: a bare dict updates in the scope (dicts stay values); a ref (a heap // list — or a heap dict later) writes the heap in place.`
- Lines 76-76; kind `syntax`: `syntax KItem ::= #dsetK(String, Val)`
- Lines 77-77; kind `rule`: `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>`
- Lines 78-81; kind `rule`: `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)`
- Lines 82-85; kind `rule`: `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)`
- Lines 86-86; kind `syntax`: `syntax KItem ::= #dsetV(Val, Val, Val)`
- Lines 87-89; kind `rule`: `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap> // negative-index normalization local to the write (subscript.k's is not imported here)`
- Lines 90-90; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= normIdxD(Int, Int) [function, total]`
- Lines 91-91; kind `rule`: `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0`
- Lines 92-94; kind `rule`: `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0 // ==== dict == (order-insensitive: same size + same key->value pairs) =======`
- Lines 95-96; kind `rule`: `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)`
- Lines 97-97; kind `syntax`, attributes: `function`: `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]`
- Lines 98-98; kind `rule`: `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true`
- Lines 99-100; kind `rule`: `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)`
- Lines 101-101; kind `syntax`, attributes: `function`: `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]`
- Lines 102-102; kind `rule`: `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K`
- Lines 103-103; kind `rule`: `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/float.k`

SHA-256: `5dfeee8700c90c3aa6dc515b15b74283882845fb6cdcc3627d97ef650124b70f`. Provenance: trusted supplied semantics.

- Lines 20-20; kind `syntax`: `syntax Val ::= Float`
- Lines 21-23; kind `rule`: `rule <k> Float(F:Float) => F ... </k> // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.`
- Lines 24-24; kind `syntax`, attributes: `function`, `total`, `symbol(intFloatDiv)`, `no-evaluators`: `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`
- Lines 25-25; kind `rule`, attributes: `concrete`: `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]`
- Lines 27-29; kind `rule`: `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F) // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.`
- Lines 30-30; kind `syntax`, attributes: `function`, `total`, `symbol(divII)`, `no-evaluators`: `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`
- Lines 31-31; kind `rule`, attributes: `concrete`: `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]`
- Lines 32-36; kind `rule`: `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2) // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).`
- Lines 37-37; kind `syntax`, attributes: `function`, `total`, `symbol(floatMod)`, `no-evaluators`: `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`
- Lines 38-38; kind `rule`, attributes: `concrete`: `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]`
- Lines 39-42; kind `rule`: `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2) // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on // concrete floats. kprove proofs return floats structurally and do not compare them.`
- Lines 43-43; kind `rule`: `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2`
- Lines 44-49; kind `rule`: `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2) // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade), // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise // `abs(a-b) < t` proximity test.)`
- Lines 50-50; kind `syntax`, attributes: `function`, `total`, `symbol(floatLt)`, `no-evaluators`: `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`
- Lines 51-51; kind `rule`, attributes: `concrete`: `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]`
- Lines 52-52; kind `rule`: `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)`
- Lines 54-54; kind `syntax`, attributes: `function`, `total`, `symbol(absF)`, `no-evaluators`: `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`
- Lines 55-55; kind `rule`, attributes: `concrete`: `rule absF(F:Float) => absFloat(F) [concrete]`
- Lines 56-60; kind `rule`: `rule applyBuiltin("abs", F:Float, .Vals) => absF(F) // ==== math.ceil =========================================================== // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is // never bound as a value).`
- Lines 61-64; kind `rule`: `rule <k> Import(_:String) => .K ... </k> // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher // priority than the generic Attribute/method dispatch in call.k).`
- Lines 65-65; kind `syntax`: `syntax KItem ::= "#mathCeil"`
- Lines 66-66; kind `rule`, attributes: `priority(40)`: `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]`
- Lines 67-69; kind `rule`: `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k> // math.floor(x) — same interception shape as math.ceil`
- Lines 70-70; kind `syntax`: `syntax KItem ::= "#mathFloor"`
- Lines 71-71; kind `rule`, attributes: `priority(40)`: `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]`
- Lines 72-72; kind `rule`: `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>`
- Lines 73-73; kind `syntax`, attributes: `function`, `total`, `symbol(floorFI)`: `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]`
- Lines 74-74; kind `rule`, attributes: `concrete`: `rule floorFI(I:Int) => I [concrete]`
- Lines 75-77; kind `rule`: `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete] // bare floor/ceil (bound by `from math import floor, ceil`)`
- Lines 78-78; kind `rule`: `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)`
- Lines 79-81; kind `rule`: `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V) // math.pow(x, y) — a two-arg interception onto powF (ints promote)`
- Lines 82-82; kind `syntax`: `syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)`
- Lines 83-83; kind `rule`, attributes: `priority(40)`: `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]`
- Lines 84-84; kind `rule`: `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>`
- Lines 85-85; kind `rule`: `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>`
- Lines 86-86; kind `syntax`, attributes: `function`, `total`, `symbol(toF)`: `syntax Float ::= toF(Val) [function, total, symbol(toF)]`
- Lines 87-87; kind `rule`, attributes: `concrete`: `rule toF(F:Float) => F [concrete]`
- Lines 88-92; kind `rule`: `rule toF(I:Int) => intToF(I) [concrete] // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm). // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).`
- Lines 93-93; kind `syntax`, attributes: `function`, `total`, `symbol(ceilF)`: `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]`
- Lines 94-94; kind `rule`, attributes: `concrete`: `rule ceilF(I:Int) => I [concrete]`
- Lines 95-98; kind `rule`: `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete] // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun; // proofs use symbolic elements, never a float literal.`
- Lines 99-102; kind `rule`: `rule applyUn("-", F:Float) => 0.0 -Float F // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.`
- Lines 103-103; kind `syntax`, attributes: `function`, `total`, `symbol(subF)`, `no-evaluators`: `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`
- Lines 104-104; kind `rule`, attributes: `concrete`: `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]`
- Lines 105-105; kind `rule`: `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)`
- Lines 107-107; kind `syntax`, attributes: `function`, `total`, `symbol(divF)`, `no-evaluators`: `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`
- Lines 108-108; kind `rule`, attributes: `concrete`: `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]`
- Lines 109-109; kind `rule`: `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)`
- Lines 111-111; kind `syntax`, attributes: `function`, `total`, `symbol(addF)`, `no-evaluators`: `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`
- Lines 112-112; kind `rule`, attributes: `concrete`: `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]`
- Lines 113-113; kind `rule`: `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)`
- Lines 115-115; kind `syntax`, attributes: `function`, `total`, `symbol(mulF)`, `no-evaluators`: `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`
- Lines 116-116; kind `rule`, attributes: `concrete`: `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]`
- Lines 117-117; kind `rule`: `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)`
- Lines 119-119; kind `syntax`, attributes: `function`, `total`, `symbol(powF)`, `no-evaluators`: `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`
- Lines 120-120; kind `rule`, attributes: `concrete`: `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]`
- Lines 121-124; kind `rule`: `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2) // ---- the remaining comparisons (gtF promoted from find_zero — its summaries // case-split on the atom; >= / <= derive from the two opaque compares) ----`
- Lines 125-125; kind `syntax`, attributes: `function`, `total`, `symbol(gtF)`, `no-evaluators`: `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`
- Lines 126-126; kind `rule`, attributes: `concrete`: `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]`
- Lines 127-127; kind `rule`: `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)`
- Lines 128-128; kind `rule`: `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)`
- Lines 129-131; kind `rule`: `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2) // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----`
- Lines 132-132; kind `rule`: `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)`
- Lines 133-133; kind `rule`: `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))`
- Lines 134-134; kind `rule`: `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`
- Lines 135-135; kind `rule`: `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`
- Lines 136-136; kind `rule`: `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`
- Lines 137-137; kind `rule`: `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`
- Lines 138-138; kind `rule`: `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`
- Lines 139-141; kind `rule`: `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I)) // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----`
- Lines 142-142; kind `syntax`, attributes: `function`, `total`, `symbol(eqF)`, `no-evaluators`: `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`
- Lines 143-143; kind `rule`, attributes: `concrete`: `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]`
- Lines 144-144; kind `rule`: `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)`
- Lines 145-145; kind `rule`: `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))`
- Lines 146-146; kind `rule`: `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)`
- Lines 147-147; kind `rule`: `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))`
- Lines 148-148; kind `rule`: `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`
- Lines 149-149; kind `rule`: `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`
- Lines 150-150; kind `rule`: `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`
- Lines 151-153; kind `rule`: `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- x == None (promoted from 137; `is` cases live in operators.k) ----`
- Lines 154-154; kind `rule`: `rule applyCmp("==", V:Val, noneV) => V ==K noneV`
- Lines 155-159; kind `rule`: `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV) // ---- float(str): decimal parse (promoted from 137's defined chain) ---- // digits '.' digits, optional leading '-'; concrete evaluation only (the // symbolic side stays an opaque decStrToF term a proof case-splits on).`
- Lines 160-160; kind `syntax`, attributes: `function`, `total`, `symbol(decStrToF)`, `no-evaluators`: `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`
- Lines 161-161; kind `rule`, attributes: `concrete`: `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]`
- Lines 162-164; kind `rule`, attributes: `concrete`: `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]`
- Lines 165-165; kind `syntax`, attributes: `function`: `syntax Int ::= headIS(IntSeq) [function]`
- Lines 166-166; kind `rule`: `rule headIS(iCons(C:Int, _:IntSeq)) => C`
- Lines 167-167; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]`
- Lines 168-168; kind `rule`: `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)`
- Lines 169-169; kind `rule`: `rule intPartAcc(.IntSeq, A:Int) => A`
- Lines 170-170; kind `rule`: `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A`
- Lines 171-172; kind `rule`: `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46`
- Lines 173-173; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]`
- Lines 174-174; kind `rule`: `rule fracPart(.IntSeq) => 0`
- Lines 175-175; kind `rule`: `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)`
- Lines 176-176; kind `rule`: `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46`
- Lines 177-177; kind `rule`: `rule fracAcc(.IntSeq, A:Int) => A`
- Lines 178-178; kind `rule`: `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))`
- Lines 179-179; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]`
- Lines 180-180; kind `rule`: `rule fracScale(.IntSeq) => 1`
- Lines 181-181; kind `rule`: `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)`
- Lines 182-182; kind `rule`: `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46`
- Lines 183-183; kind `rule`: `rule fscAcc(.IntSeq, A:Int) => A`
- Lines 184-184; kind `rule`: `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)`
- Lines 185-185; kind `rule`: `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)`
- Lines 186-186; kind `rule`: `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)`
- Lines 187-189; kind `rule`: `rule applyBuiltin("float", F:Float, .Vals) => F // ---- float / int division (promoted from mean_absolute_deviation) ----`
- Lines 190-190; kind `syntax`, attributes: `function`, `total`, `symbol(divFloatIntV)`, `no-evaluators`: `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`
- Lines 191-191; kind `rule`, attributes: `concrete`: `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]`
- Lines 192-194; kind `rule`: `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I) // ---- int -> float promotion for the remaining mixed arithmetic/compares ----`
- Lines 195-195; kind `syntax`, attributes: `function`, `total`, `symbol(intToF)`, `no-evaluators`: `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`
- Lines 196-196; kind `rule`, attributes: `concrete`: `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]`
- Lines 197-197; kind `rule`: `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`
- Lines 198-198; kind `rule`: `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`
- Lines 199-199; kind `rule`: `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`
- Lines 200-200; kind `rule`: `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`
- Lines 201-201; kind `rule`: `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`
- Lines 202-202; kind `rule`: `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`
- Lines 203-203; kind `rule`: `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`
- Lines 204-204; kind `rule`: `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`
- Lines 205-205; kind `rule`: `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`
- Lines 206-208; kind `rule`: `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----`
- Lines 209-209; kind `syntax`, attributes: `function`, `total`, `symbol(truncF)`, `no-evaluators`: `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`
- Lines 210-210; kind `rule`, attributes: `concrete`: `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]`
- Lines 211-211; kind `rule`: `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)`
- Lines 213-213; kind `rule`: `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)`
- Lines 214-216; kind `rule`: `rule applyBuiltin("float", F:Float, .Vals) => F // round: Python half-even (banker's); round(F, N) scales by 10^N`
- Lines 217-217; kind `syntax`, attributes: `function`, `total`, `symbol(roundF)`, `no-evaluators`: `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`
- Lines 218-222; kind `rule`, attributes: `concrete`: `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]`
- Lines 223-223; kind `syntax`, attributes: `function`, `total`, `symbol(roundFN)`, `no-evaluators`: `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`
- Lines 224-226; kind `rule`, attributes: `concrete`: `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]`
- Lines 227-227; kind `rule`: `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)`
- Lines 228-228; kind `rule`: `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)`
- Lines 230-230; kind `syntax`, attributes: `function`, `total`, `symbol(sqrtF)`, `no-evaluators`: `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`
- Lines 231-231; kind `rule`, attributes: `concrete`: `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]`
- Lines 232-232; kind `syntax`: `syntax KItem ::= "#mathSqrt"`
- Lines 233-233; kind `rule`, attributes: `priority(40)`: `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]`
- Lines 234-234; kind `rule`: `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>`
- Lines 235-242; kind `rule`: `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k> // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive: // the isFloat guard is disjoint from the existing isInt one.`
- Lines 243-243; kind `syntax`: `syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)`
- Lines 244-244; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)`
- Lines 245-245; kind `rule`: `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>`
- Lines 246-246; kind `rule`: `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>`
- Lines 247-248; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)`
- Lines 250-250; kind `syntax`: `syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)`
- Lines 251-251; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)`
- Lines 252-252; kind `rule`: `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>`
- Lines 253-253; kind `rule`: `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>`
- Lines 254-260; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V) // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin). // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof // with isInt(V) in its path condition refutes this branch without sort reasoning.`
- Lines 261-261; kind `syntax`: `syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)`
- Lines 262-264; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))`
- Lines 265-265; kind `rule`: `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>`
- Lines 266-266; kind `rule`: `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>`
- Lines 267-269; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)`
- Lines 270-272; kind `rule`: `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/functions.k`

SHA-256: `e4c8f67741117b29703c3c61d48a5b0f92cf7bd531e78e25c03e794a910ac193`. Provenance: trusted supplied semantics.

- Lines 8-13; kind `syntax`: `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) | #bindP(ParamNames, Vals) | "#pop" | "#endcall" // ==== def / anonymous closure =============================================`
- Lines 14-16; kind `rule`: `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>`
- Lines 18-18; kind `syntax`: `syntax Expr ::= closureExpr(ParamNames, Stmts)`
- Lines 19-26; kind `rule`: `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env> // ==== annotated def/lambda (closure cells; spec 2.3) ====================== // closureValC(params, cellvars, body, captured-cells). No frame anchor: all // enclosing-local reads are freevars (symtable-complete) and go through the // captured cells; everything else is global/builtin, so the callee frame's // parent is the module scope (0) — sound after the defining frame dies.`
- Lines 27-30; kind `syntax`: `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map) // capture: resolve each freevar to the enclosing frame's cellRef, then bind // (FuncDef) or yield (Lambda) the closure value.`
- Lines 31-32; kind `syntax`: `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)`
- Lines 33-35; kind `rule`: `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>`
- Lines 36-41; kind `rule`: `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`
- Lines 42-45; kind `rule`: `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>`
- Lines 47-49; kind `rule`: `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>`
- Lines 50-52; kind `rule`: `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>`
- Lines 53-58; kind `rule`: `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`
- Lines 59-62; kind `rule`: `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k> // ==== bind params ========================================================`
- Lines 63-63; kind `rule`: `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>`
- Lines 64-67; kind `rule`: `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes> // a param that is a cellvar was pre-bound to its cell at frame entry`
- Lines 68-77; kind `rule`: `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)] // ==== return / pop the frame (the returned expr evaluates by strictness) ==`
- Lines 78-79; kind `rule`: `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>`
- Lines 80-84; kind `rule`: `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret> // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).`
- Lines 85-90; kind `rule`: `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/int.k`

SHA-256: `dc2da7d81578370651ecb6905b69cb44443cdd8db3869441242b81420382abe5`. Provenance: trusted supplied semantics.

- Lines 7-7; kind `rule`: `rule applyUn("-", I:Int) => 0 -Int I`
- Lines 9-10; kind `rule`: `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2 // Bool participates in int arithmetic (x += (a == b))`
- Lines 11-11; kind `rule`: `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi`
- Lines 12-12; kind `rule`: `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I`
- Lines 13-13; kind `rule`: `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2`
- Lines 14-14; kind `rule`: `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2`
- Lines 15-15; kind `rule`: `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)`
- Lines 16-16; kind `rule`: `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2`
- Lines 17-17; kind `rule`: `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0`
- Lines 19-19; kind `syntax`, attributes: `function`: `syntax Int ::= pyMod(Int, Int) [function]`
- Lines 20-20; kind `rule`: `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2`
- Lines 22-22; kind `rule`: `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2`
- Lines 23-23; kind `rule`: `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2`
- Lines 24-24; kind `rule`: `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2`
- Lines 25-25; kind `rule`: `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2`
- Lines 26-26; kind `rule`: `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2`
- Lines 27-27; kind `rule`: `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/iter.k`

SHA-256: `5085db2fed67b7bbd39f6289ec275905aaee742690895d7b3f843f73bd62f77f`. Provenance: trusted supplied semantics.

- Lines 8-8; kind `syntax`: `syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/list.k`

SHA-256: `870c72341c25e2c16283726191a71bf5b571ed2995c8ae12e3e2923cdce5a9aa`. Provenance: trusted supplied semantics.

- Lines 9-9; kind `rule`: `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>`
- Lines 10-12; kind `rule`: `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k> // ==== ListExpr: [...] literal -> a fresh heap object =======================`
- Lines 13-13; kind `syntax`: `syntax ApplyK ::= "toList"`
- Lines 14-14; kind `rule`: `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>`
- Lines 15-17; kind `rule`: `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k> // ==== list ops: + / == / != ===============================================`
- Lines 18-18; kind `syntax`, attributes: `function`, `total`: `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]`
- Lines 19-19; kind `rule`: `rule valSeqConcat(.ValSeq, T:ValSeq) => T`
- Lines 20-23; kind `rule`: `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T)) // list + list constructs a NEW object (k-cell — it allocates; operands land here // already deref'd). priority(45) beats the generic BinOp dispatch.`
- Lines 24-25; kind `rule`, attributes: `priority(45)`: `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]`
- Lines 27-27; kind `rule`: `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B`
- Lines 28-32; kind `rule`: `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B) // ==== deep equality when elements are heap objects (list-of-lists) ======== // Python == is structural at every depth. Fires ONLY when a ref is present // (the guard decides on concrete seqs); the plain ==K path above is unchanged.`
- Lines 33-33; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= hasRefVS(ValSeq) [function, total]`
- Lines 34-34; kind `rule`: `rule hasRefVS(.ValSeq) => false`
- Lines 35-35; kind `rule`: `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)`
- Lines 37-38; kind `syntax`, attributes: `function`: `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] | deepEqV(Val, Val, Map) [function]`
- Lines 39-39; kind `rule`: `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true`
- Lines 40-40; kind `rule`: `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false`
- Lines 41-41; kind `rule`: `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false`
- Lines 42-43; kind `rule`: `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)`
- Lines 45-46; kind `rule`: `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)`
- Lines 47-48; kind `rule`: `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)`
- Lines 49-49; kind `rule`: `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)`
- Lines 50-52; kind `rule`: `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise] // ==== mutator: xs.append(v) — an in-place heap write ======================`
- Lines 53-57; kind `rule`: `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)] // ==== `x in list` — a <k>-cell fold over #iterNext ========================`
- Lines 58-58; kind `syntax`: `syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"`
- Lines 59-59; kind `rule`: `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>`
- Lines 60-60; kind `rule`: `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>`
- Lines 61-61; kind `rule`: `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>`
- Lines 62-62; kind `rule`: `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>`
- Lines 63-64; kind `rule`: `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V`
- Lines 65-66; kind `rule`: `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)`
- Lines 67-67; kind `rule`: `rule <k> B:Bool ~> #notB => notBool B ... </k>`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/methods.k`

SHA-256: `ff9acc6dab2d1cc99ec4f2d234f27ae4526d752aae62bcfd7f9fd2a0399f7743`. Provenance: trusted supplied semantics.

- Lines 10-12; kind `syntax`: `syntax Val ::= applyMethod(Val, String, Vals) [function] // ==== string predicates (Python semantics) =================================`
- Lines 13-13; kind `rule`: `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)`
- Lines 14-14; kind `rule`: `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)`
- Lines 15-15; kind `rule`: `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)`
- Lines 16-18; kind `rule`: `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS) // ==== case maps ============================================================`
- Lines 19-19; kind `rule`: `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))`
- Lines 20-20; kind `rule`: `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))`
- Lines 21-25; kind `rule`: `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS)) // ==== join / count / strip / encode ======================================== // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by // the call layer; the result str is a value)`
- Lines 26-26; kind `rule`: `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))`
- Lines 27-27; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]`
- Lines 28-28; kind `rule`: `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq`
- Lines 29-29; kind `rule`: `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS`
- Lines 30-33; kind `rule`: `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R)))) // S.count(sub): non-overlapping window scan (Python str.count)`
- Lines 34-34; kind `rule`: `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)`
- Lines 35-35; kind `syntax`, attributes: `function`: `syntax Int ::= cntSub(IntSeq, IntSeq) [function]`
- Lines 36-36; kind `rule`: `rule cntSub(.IntSeq, _:IntSeq) => 0`
- Lines 37-38; kind `rule`: `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0`
- Lines 39-40; kind `rule`: `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0`
- Lines 41-41; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]`
- Lines 42-42; kind `rule`: `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0`
- Lines 43-43; kind `rule`, attributes: `owise`: `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]`
- Lines 44-46; kind `rule`: `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0 // S.strip(): trim whitespace runs from both ends`
- Lines 47-47; kind `rule`: `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))`
- Lines 48-48; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= trimWS(IntSeq) [function, total]`
- Lines 49-49; kind `rule`: `rule trimWS(.IntSeq) => .IntSeq`
- Lines 50-50; kind `rule`: `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)`
- Lines 51-51; kind `rule`: `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)`
- Lines 52-52; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]`
- Lines 53-53; kind `rule`: `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)`
- Lines 54-54; kind `rule`: `rule revISAcc(.IntSeq, A:IntSeq) => A`
- Lines 55-57; kind `rule`: `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A)) // S.encode('ascii'): identity on the code-sequence model (bytes == codes)`
- Lines 58-60; kind `rule`: `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS) // ==== prefix ===============================================================`
- Lines 61-63; kind `rule`: `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC) // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========`
- Lines 64-64; kind `rule`: `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)`
- Lines 65-65; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]`
- Lines 66-66; kind `rule`: `rule cntOccVS(.ValSeq, _:Val) => 0`
- Lines 67-67; kind `rule`: `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V`
- Lines 68-71; kind `rule`: `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V) // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ========== // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.`
- Lines 72-74; kind `rule`, attributes: `priority(40)`: `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]`
- Lines 75-75; kind `syntax`: `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] // remaining, current token, result`
- Lines 76-76; kind `rule`: `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)`
- Lines 77-78; kind `rule`: `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)`
- Lines 79-81; kind `rule`: `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C) // flush the current token to the result list iff non-empty.`
- Lines 82-82; kind `syntax`, attributes: `function`: `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]`
- Lines 83-83; kind `rule`: `rule flushTok(ACC:ValSeq, .IntSeq) => ACC`
- Lines 84-84; kind `rule`: `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))`
- Lines 85-85; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= isWSC(Int) [function, total]`
- Lines 86-88; kind `rule`: `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13 // split(sep='x') keyword form delegates to the positional k-cell rule`
- Lines 89-93; kind `rule`: `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)] // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).`
- Lines 94-96; kind `rule`, attributes: `priority(40)`: `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]`
- Lines 97-97; kind `syntax`: `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] // remaining, sep code, current token`
- Lines 98-98; kind `rule`: `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)`
- Lines 99-100; kind `rule`: `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP`
- Lines 101-102; kind `rule`: `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)`
- Lines 104-105; kind `rule`: `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))`
- Lines 106-106; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]`
- Lines 107-107; kind `rule`: `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq`
- Lines 108-108; kind `rule`: `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A`
- Lines 109-111; kind `rule`: `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A) // ==== char helpers =========================================================`
- Lines 112-112; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= isUpperC(Int) [function, total]`
- Lines 113-113; kind `rule`: `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90`
- Lines 115-115; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= isLowerC(Int) [function, total]`
- Lines 116-116; kind `rule`: `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122`
- Lines 118-118; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= isAlphaC(Int) [function, total]`
- Lines 119-119; kind `rule`: `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)`
- Lines 121-121; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= isDigitC(Int) [function, total]`
- Lines 122-122; kind `rule`: `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57`
- Lines 124-124; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= hasUpper(IntSeq) [function, total]`
- Lines 125-125; kind `rule`: `rule hasUpper(.IntSeq) => false`
- Lines 126-126; kind `rule`: `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)`
- Lines 128-128; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= hasLower(IntSeq) [function, total]`
- Lines 129-129; kind `rule`: `rule hasLower(.IntSeq) => false`
- Lines 130-130; kind `rule`: `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)`
- Lines 132-132; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= allAlpha(IntSeq) [function, total]`
- Lines 133-133; kind `rule`: `rule allAlpha(.IntSeq) => true`
- Lines 134-134; kind `rule`: `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)`
- Lines 136-136; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= allDigit(IntSeq) [function, total]`
- Lines 137-137; kind `rule`: `rule allDigit(.IntSeq) => true`
- Lines 138-138; kind `rule`: `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)`
- Lines 140-140; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= lowerC(Int) [function, total]`
- Lines 142-142; kind `rule`: `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)`
- Lines 143-143; kind `rule`, attributes: `owise`: `rule lowerC(C:Int) => C [owise]`
- Lines 145-145; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= upperC(Int) [function, total]`
- Lines 146-146; kind `rule`: `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)`
- Lines 147-147; kind `rule`, attributes: `owise`: `rule upperC(C:Int) => C [owise]`
- Lines 149-149; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= swapC(Int) [function, total]`
- Lines 150-150; kind `rule`: `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)`
- Lines 151-151; kind `rule`: `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)`
- Lines 152-152; kind `rule`, attributes: `owise`: `rule swapC(C:Int) => C [owise]`
- Lines 154-154; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= mapLower(IntSeq) [function, total]`
- Lines 155-155; kind `rule`: `rule mapLower(.IntSeq) => .IntSeq`
- Lines 156-156; kind `rule`: `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))`
- Lines 158-158; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= mapUpper(IntSeq) [function, total]`
- Lines 159-159; kind `rule`: `rule mapUpper(.IntSeq) => .IntSeq`
- Lines 160-160; kind `rule`: `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))`
- Lines 162-162; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= mapSwap(IntSeq) [function, total]`
- Lines 163-163; kind `rule`: `rule mapSwap(.IntSeq) => .IntSeq`
- Lines 164-164; kind `rule`: `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))`
- Lines 166-166; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]`
- Lines 167-167; kind `rule`: `rule startsWith(.IntSeq, _:IntSeq) => true`
- Lines 168-168; kind `rule`: `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false`
- Lines 169-169; kind `rule`: `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/operators.k`

SHA-256: `f3d1fd85734f5e1757307e606cbfb8d6d4bf0893ee85ce20ec99606ade910e8b`. Provenance: trusted supplied semantics.

- Lines 10-10; kind `rule`: `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>`
- Lines 12-14; kind `rule`: `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k> // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes`
- Lines 15-15; kind `context`: `context Compare(HOLE, _)`
- Lines 16-16; kind `context`: `context Compare(_:Val, CmpOp(_, HOLE))`
- Lines 17-17; kind `rule`, attributes: `owise`: `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]`
- Lines 19-19; kind `rule`: `rule applyCmp("is", V:Val, noneV) => V ==K noneV`
- Lines 20-24; kind `rule`: `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV) // ==== operand deref: heap objects combine/compare by STRUCTURE ============ // (Python: list == is structural; identity only via `is`.) priority(40) // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.`
- Lines 25-27; kind `rule`, attributes: `priority(40)`: `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- Lines 28-33; kind `rule`: `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)] // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd`
- Lines 34-37; kind `rule`, attributes: `priority(40)`: `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H |-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]`
- Lines 38-42; kind `rule`, attributes: `priority(40)`: `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]`
- Lines 44-46; kind `rule`, attributes: `priority(40)`: `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/range.k`

SHA-256: `810e4c04b757445c03592aef25c97d6b2cc7c6fffa646288bc6cd15a3cae643d`. Provenance: trusted supplied semantics.

- Lines 9-9; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= inRange(Int, Int, Int) [function, total]`
- Lines 10-10; kind `rule`: `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)`
- Lines 12-12; kind `syntax`, attributes: `function`: `syntax Int ::= rangeLen(Int, Int, Int) [function]`
- Lines 13-14; kind `rule`: `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO`
- Lines 15-16; kind `rule`: `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO`
- Lines 17-18; kind `rule`: `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)`
- Lines 20-22; kind `rule`: `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)`
- Lines 23-24; kind `rule`: `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/set.k`

SHA-256: `b822c3c6944f9940a4477fa6b7a42490c407663f2a314394e9c146e8951f1ac7`. Provenance: trusted supplied semantics.

- Lines 8-10; kind `syntax`: `syntax Val ::= setV(IntSeq) // membership of a code in the accumulated distinct-code sequence`
- Lines 11-11; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= codeIn(Int, IntSeq) [function, total]`
- Lines 12-12; kind `rule`: `rule codeIn(_:Int, .IntSeq) => false`
- Lines 13-15; kind `rule`: `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T) // the distinct codes of CS (insert-if-absent fold, first-seen order)`
- Lines 16-17; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] | dedupFrom(IntSeq, IntSeq) [function, total]`
- Lines 18-18; kind `rule`: `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)`
- Lines 19-19; kind `rule`: `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC`
- Lines 20-21; kind `rule`: `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)`
- Lines 22-23; kind `rule`: `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)`
- Lines 25-25; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]`
- Lines 26-26; kind `rule`: `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)`
- Lines 27-30; kind `rule`: `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C)) // ==== set equality: two sets are equal iff mutually subsuming ============== // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).`
- Lines 31-31; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]`
- Lines 32-32; kind `rule`: `rule subsetCodes(.IntSeq, _:IntSeq) => true`
- Lines 33-33; kind `rule`: `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)`
- Lines 35-35; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]`
- Lines 36-38; kind `rule`: `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A) // set == set (the only comparison sets support here)`
- Lines 39-39; kind `rule`: `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/sort.k`

SHA-256: `df79670e4794a92e96ffc824857fbc34d3a65b6b6a3026d1dcf322128fbaba5a`. Provenance: trusted supplied semantics.

- Lines 18-18; kind `syntax`, attributes: `function`, `total`, `symbol(sortVS)`, `no-evaluators`: `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`
- Lines 19-19; kind `syntax`, attributes: `function`: `syntax ValSeq ::= insVS(Int, ValSeq) [function]`
- Lines 20-20; kind `rule`, attributes: `concrete`: `rule sortVS(.ValSeq) => .ValSeq [concrete]`
- Lines 21-21; kind `rule`, attributes: `concrete`: `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]`
- Lines 22-22; kind `rule`, attributes: `concrete`: `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]`
- Lines 23-23; kind `rule`, attributes: `concrete`: `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]`
- Lines 24-25; kind `rule`: `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete] // str elements insert by the shared lexicographic strLt (methods.k)`
- Lines 26-26; kind `syntax`, attributes: `function`: `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]`
- Lines 27-27; kind `rule`, attributes: `concrete`: `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]`
- Lines 28-28; kind `rule`, attributes: `concrete`: `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]`
- Lines 29-30; kind `rule`, attributes: `concrete`: `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]`
- Lines 31-35; kind `rule`: `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete] // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise] // applyBuiltin routing in call.k) so the result allocates.`
- Lines 36-39; kind `rule`: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k> // mutator: xs.sort() — the in-place heap write over the same trusted sortVS`
- Lines 40-48; kind `rule`: `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)] // ==== keyed / reversed sorted() (WP2) ===================================== // sortKeyVS(VS, KV): the stable ascending sort of VS by the key value KV // (a closure/builtin/type — anything callable). OPAQUE here; the concrete // leg (MPY-CONCRETE, llvm only) computes keys by REAL calls and stable- // inserts, at priority(40) over these.`
- Lines 49-49; kind `syntax`, attributes: `function`, `total`, `symbol(sortKeyVS)`, `no-evaluators`: `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`
- Lines 51-52; kind `syntax`, attributes: `function`, `total`: `syntax ValSeq ::= revVS(ValSeq) [function, total] | revVSAcc(ValSeq, ValSeq) [function, total]`
- Lines 53-53; kind `rule`: `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)`
- Lines 54-54; kind `rule`: `rule revVSAcc(.ValSeq, A:ValSeq) => A`
- Lines 55-55; kind `rule`: `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))`
- Lines 57-57; kind `syntax`, attributes: `function`, `total`: `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]`
- Lines 58-58; kind `rule`: `rule condRev(S:ValSeq, false) => S`
- Lines 59-59; kind `rule`: `rule condRev(S:ValSeq, true) => revVS(S)`
- Lines 61-62; kind `rule`: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>`
- Lines 63-64; kind `rule`: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>`
- Lines 65-71; kind `rule`: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k> // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write // their postcondition directly as valSeqAt(sortVS(VS), …).`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/str.k`

SHA-256: `1bf0abf61d7c5df6301433a89c79d2ef4259d47a68d98385ff74618c4c310e0f`. Provenance: trusted supplied semantics.

- Lines 8-8; kind `rule`: `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>`
- Lines 9-12; kind `rule`: `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k> // ==== str literal (ASCII-only) ============================================`
- Lines 13-13; kind `syntax`, attributes: `function`: `syntax IntSeq ::= strToCodes(String) [function]`
- Lines 14-14; kind `rule`: `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>`
- Lines 15-15; kind `rule`: `rule strToCodes("") => .IntSeq`
- Lines 16-19; kind `rule`: `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128 // ==== operators: + / == / != / in =========================================`
- Lines 20-20; kind `syntax`, attributes: `function`, `total`: `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]`
- Lines 21-21; kind `rule`: `rule seqConcat(.IntSeq, T:IntSeq) => T`
- Lines 22-22; kind `rule`: `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))`
- Lines 24-24; kind `rule`: `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))`
- Lines 25-25; kind `rule`: `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B`
- Lines 26-28; kind `rule`: `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B) // substring membership: `P in X` iff the code-seq P occurs contiguously in X`
- Lines 29-29; kind `rule`: `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)`
- Lines 30-30; kind `rule`: `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)`
- Lines 32-32; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]`
- Lines 33-33; kind `rule`: `rule strPrefix(.IntSeq, _:IntSeq) => true`
- Lines 34-34; kind `rule`: `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false`
- Lines 35-35; kind `rule`: `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)`
- Lines 37-37; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]`
- Lines 38-38; kind `rule`: `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)`
- Lines 39-39; kind `rule`: `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)`
- Lines 40-47; kind `rule`: `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs)) // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on // str </<=/>/>= comparisons.`
- Lines 48-48; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]`
- Lines 49-49; kind `rule`: `rule strLt(.IntSeq, .IntSeq) => false`
- Lines 50-50; kind `rule`: `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true`
- Lines 51-51; kind `rule`: `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false`
- Lines 52-52; kind `rule`: `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B`
- Lines 53-53; kind `rule`: `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B`
- Lines 54-54; kind `rule`: `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B`
- Lines 56-56; kind `rule`: `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`
- Lines 57-57; kind `rule`: `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)`
- Lines 58-58; kind `rule`: `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)`
- Lines 59-59; kind `rule`: `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/subscript.k`

SHA-256: `dba04c0acf213bef4f9f7b11243ca00a2b3ca5fa8666c544ede7d382d27d36a7`. Provenance: trusted supplied semantics.

- Lines 11-11; kind `syntax`, attributes: `function`, `total`: `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]`
- Lines 12-12; kind `rule`: `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V`
- Lines 13-14; kind `rule`: `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0`
- Lines 16-16; kind `syntax`, attributes: `function`: `syntax Int ::= intSeqAt(IntSeq, Int) [function]`
- Lines 17-17; kind `rule`: `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C`
- Lines 18-19; kind `rule`: `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0`
- Lines 21-21; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= normIdx(Int, Int) [function, total]`
- Lines 22-22; kind `rule`: `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0`
- Lines 23-26; kind `rule`: `rule normIdx(I:Int, _:Int) => I requires I >=Int 0 // ==== Subscript: indexing obj[i] (list / tuple / str) ===================== // contexts (not strict attrs): the Index slot's Slice alternative must never heat`
- Lines 27-27; kind `context`: `context Subscript(HOLE, _)`
- Lines 28-30; kind `context`: `context Subscript(_:Val, HOLE:Expr) // heap-object deref (covers both the index and slice forms via the Index slot)`
- Lines 31-33; kind `rule`, attributes: `priority(40)`: `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- Lines 35-35; kind `rule`: `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>`
- Lines 37-37; kind `syntax`, attributes: `function`: `syntax Val ::= applyIndex(Val, Int) [function]`
- Lines 38-38; kind `rule`: `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`
- Lines 39-39; kind `rule`: `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`
- Lines 40-43; kind `rule`: `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq)) // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========`
- Lines 44-47; kind `syntax`: `syntax KItem ::= #evalB(Bound) | "#toSome" | #slLo(Val, Bound, Bound) | #slHi(Val, OptInt, Bound) | #slStep(Val, OptInt, OptInt)`
- Lines 49-49; kind `syntax`: `syntax OptInt ::= "noB" | someB(Int)`
- Lines 50-50; kind `rule`: `rule <k> #evalB(NoBound) => noB ... </k>`
- Lines 51-51; kind `rule`: `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>`
- Lines 52-52; kind `rule`: `rule <k> I:Int ~> #toSome => someB(I) ... </k>`
- Lines 54-54; kind `rule`: `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>`
- Lines 55-55; kind `rule`: `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>`
- Lines 56-57; kind `rule`: `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k> // a list slice constructs a NEW object; a str slice stays a value`
- Lines 58-60; kind `rule`, attributes: `priority(45)`: `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]`
- Lines 61-61; kind `rule`: `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>`
- Lines 63-63; kind `syntax`, attributes: `function`: `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]`
- Lines 64-65; kind `rule`: `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`
- Lines 66-67; kind `rule`: `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`
- Lines 68-71; kind `rule`: `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST))) // ==== slice.indices: step / start / stop / clamp ==========================`
- Lines 72-72; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= slStep(OptInt) [function, total]`
- Lines 73-73; kind `rule`: `rule slStep(noB) => 1`
- Lines 74-74; kind `rule`: `rule slStep(someB(S:Int)) => S`
- Lines 76-76; kind `syntax`, attributes: `function`: `syntax Int ::= slStart(OptInt, OptInt, Int) [function]`
- Lines 77-78; kind `rule`: `rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0`
- Lines 79-80; kind `rule`: `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0`
- Lines 81-81; kind `rule`: `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))`
- Lines 83-83; kind `syntax`, attributes: `function`: `syntax Int ::= slStop(OptInt, OptInt, Int) [function]`
- Lines 84-85; kind `rule`: `rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0`
- Lines 86-87; kind `rule`: `rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0`
- Lines 88-88; kind `rule`: `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))`
- Lines 90-90; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= slAdjust(Int, Int, Int) [function, total]`
- Lines 91-92; kind `rule`: `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0`
- Lines 93-94; kind `rule`: `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0`
- Lines 96-96; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= clampLo(Int, Int) [function, total]`
- Lines 97-98; kind `rule`: `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0`
- Lines 99-100; kind `rule`: `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0`
- Lines 102-102; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= clampHi(Int, Int, Int) [function, total]`
- Lines 103-104; kind `rule`: `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN`
- Lines 105-108; kind `rule`: `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN // ==== build the strided sub-sequence (indices in range by construction) ====`
- Lines 109-109; kind `syntax`, attributes: `function`: `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]`
- Lines 110-112; kind `rule`: `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`
- Lines 113-114; kind `rule`: `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`
- Lines 116-116; kind `syntax`, attributes: `function`: `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]`
- Lines 117-119; kind `rule`: `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`
- Lines 120-121; kind `rule`: `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/syntax.k`

SHA-256: `1e9e629e5e6e14bdd7f4d530375e8655a89366b5ecd0c24a3c57ad3b5708f2a6`. Provenance: trusted supplied semantics.

- Lines 9-30; kind `syntax`: `syntax Expr ::= "Int" "(" Int ")" | "Float" "(" Float ")" | "Bool" "(" Bool ")" | "Name" "(" String ")" | "Str" "(" String ")" | "UnaryOp" "(" String "," Expr ")" [strict(2)] | "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] | "BoolOp" "(" String "," Exprs ")" | "ListExpr" "(" Exprs ")" | "DictExpr" "(" Entries ")" | "ListComp" "(" Expr "," CompFors ")" [macro] | "GenExp" "(" Expr "," CompFors ")" [macro] | "TupleExpr" "(" Exprs ")" | "Subscript" "(" Expr "," Index ")" | "IfExp" "(" Expr "," Expr "," Expr ")" [strict(1)] | "Lambda" "(" Params "," Expr ")" | "KwArg" "(" String "," Expr ")" | "Lambda" "(" Params "," CellVars "," FreeVars "," Expr ")" | "NoneVal" | "Call" "(" Expr "," Exprs ")" | "Attribute" "(" Expr "," String ")" [strict(1)] | "Compare" "(" Expr "," CmpOp ")"`
- Lines 32-32; kind `syntax`: `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"`
- Lines 33-33; kind `syntax`: `syntax Entry ::= "Entry" "(" Expr "," Expr ")"`
- Lines 34-34; kind `syntax`: `syntax Entries ::= List{Entry, ","}`
- Lines 35-35; kind `syntax`: `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"`
- Lines 36-36; kind `syntax`: `syntax CompFors ::= List{CompFor, ""}`
- Lines 37-37; kind `syntax`: `syntax Exprs ::= List{Expr, ","}`
- Lines 38-38; kind `syntax`: `syntax Index ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"`
- Lines 39-39; kind `syntax`: `syntax Bound ::= Expr | "NoBound"`
- Lines 41-54; kind `syntax`: `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] | "Import" "(" String ")" | "ImportFrom" "(" String "," ParamNames ")" | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] | "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] | "While" "(" Expr "," Stmts ")" | "Break" | "Continue" | "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] | "Return" "(" Expr ")" [strict] | "Assert" "(" Expr ")" [strict] | "Expr" "(" Expr ")" [strict] | "FuncDef" "(" String "," Params "," Stmts ")" | "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"`
- Lines 56-56; kind `syntax`: `syntax Stmts ::= List{Stmt, ""}`
- Lines 57-57; kind `syntax`: `syntax Params ::= "Params" "(" ParamNames ")"`
- Lines 58-58; kind `syntax`: `syntax CellVars ::= "CellVars" "(" ParamNames ")"`
- Lines 59-59; kind `syntax`: `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"`
- Lines 60-60; kind `syntax`: `syntax ParamNames ::= List{String, ","}`
- Lines 61-61; kind `syntax`: `syntax Module ::= "Module" "(" Stmts ")"`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics/tuple.k`

SHA-256: `41395a1ec6a58129c78facb15b44206907c54d79e86ea363ae68cb37bfc64abb`. Provenance: trusted supplied semantics.

- Lines 10-10; kind `rule`: `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>`
- Lines 11-13; kind `rule`: `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k> // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================`
- Lines 14-14; kind `syntax`: `syntax ApplyK ::= "toTuple"`
- Lines 15-15; kind `rule`: `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>`
- Lines 16-16; kind `rule`: `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>`
- Lines 18-19; kind `rule`: `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B // membership routes through the same k-cell fold as lists (list.k)`
- Lines 20-20; kind `rule`: `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>`
- Lines 21-22; kind `rule`: `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k> // t.index(v): first index of v (ValueError out of subset)`
- Lines 23-23; kind `rule`: `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)`
- Lines 24-24; kind `syntax`, attributes: `function`: `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]`
- Lines 25-25; kind `rule`: `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V`
- Lines 26-27; kind `rule`: `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)`
- Lines 28-30; kind `rule`: `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B) // ==== target binding: bind a Name or a TupleExpr target to a value ========`
- Lines 31-31; kind `syntax`: `syntax KItem ::= #bindTgt(Expr, Val)`
- Lines 32-34; kind `rule`: `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`
- Lines 35-41; kind `rule`, attributes: `priority(40)`: `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`
- Lines 42-42; kind `rule`: `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
- Lines 43-43; kind `rule`: `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
- Lines 44-48; kind `rule`: `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)] // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========`
- Lines 49-49; kind `syntax`: `syntax KItem ::= #unpackSeq(Exprs, ValSeq)`
- Lines 50-50; kind `rule`: `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
- Lines 51-51; kind `rule`: `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
- Lines 52-54; kind `rule`, attributes: `priority(40)`: `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- Lines 55-56; kind `rule`: `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>`
- Lines 57-57; kind `rule`: `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>`

### `/tmp/audit-work/108-count-nums-audit/reference-semantics/semantics.k`

SHA-256: `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97`. Provenance: trusted supplied semantics.

No inventoried sentence.

### `/tmp/audit-work/108-count-nums-audit/verification.k`

SHA-256: `a6a57397f1b7f6b856df6012dcde84159e0506d8875f11edbc0f76579f1f57c0`. Provenance: candidate proof extension/claim.

- Lines 9-9; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= allInts(ValSeq) [function, total]`
- Lines 10-10; kind `rule`: `rule allInts(.ValSeq) => true`
- Lines 11-17; kind `rule`: `rule allInts(vCons(V:Val, R:ValSeq)) => isInt(V) andBool allInts(R) // The Haskell backend does not refine V:Val to Int from an isInt(V) path // condition. This guarded total projection is the standard K cast-boundary // idiom; it creates no integer value unless the fixed subsort cast is // defined.`
- Lines 18-18; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= definedProjectInt(Val) [function, total]`
- Lines 19-19; kind `rule`: `rule definedProjectInt(V:Val) => isInt(V)`
- Lines 21-22; kind `syntax`, attributes: `function`, `total`, `symbol(projectIntTotal)`, `no-evaluators`: `syntax Int ::= projectIntTotal(Val) [function, total, symbol(projectIntTotal), no-evaluators]`
- Lines 24-26; kind `rule`, attributes: `simplification`: `rule #Ceil({@V:Val}:>Int) => ({ definedProjectInt(@V) #Equals true } #And #Ceil(@V)) [simplification]`
- Lines 28-30; kind `rule`, attributes: `concrete`, `simplification(10)`, `preserves-definedness`: `rule projectIntTotal(V:Val) => {V}:>Int requires definedProjectInt(V) [concrete, simplification(10), preserves-definedness]`
- Lines 31-33; kind `rule`, attributes: `symbolic(V)`, `simplification`, `preserves-definedness`: `rule {V:Val}:>Int => projectIntTotal(V) requires definedProjectInt(V) [symbolic(V), simplification, preserves-definedness]`
- Lines 34-34; kind `rule`, attributes: `simplification`: `rule projectIntTotal(I:Int) => I [simplification]`
- Lines 35-40; kind `rule`: `rule projectIntTotal(projectIntTotal(V:Val)) => projectIntTotal(V) [simplification] // Guarded dispatch twins of the supplied Int equations used after list // iteration yields a dynamically sorted Val.`
- Lines 41-44; kind `rule`, attributes: `simplification`: `rule applyCmp("<", V:Val, J:Int) => projectIntTotal(V) <Int J requires isInt(V) [simplification]`
- Lines 45-48; kind `rule`, attributes: `simplification`: `rule applyUn("-", V:Val) => 0 -Int projectIntTotal(V) requires isInt(V) [simplification]`
- Lines 50-50; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= magnitude(Int) [function, total]`
- Lines 51-51; kind `rule`: `rule magnitude(I:Int) => 0 -Int I requires I <Int 0`
- Lines 52-56; kind `rule`: `rule magnitude(I:Int) => I requires I >=Int 0 // A proof-side name for the code sequence returned by the supplied // Int2String/strToCodes primitive. The concrete rule remains in the fixed // semantics; this simplification names its already-produced result.`
- Lines 57-58; kind `syntax`, attributes: `function`, `total`, `no-evaluators`: `syntax IntSeq ::= decimalCodes(Int) [function, total, no-evaluators]`
- Lines 59-61; kind `rule`, attributes: `simplification`: `rule strToCodes(Int2String(N:Int)) => decimalCodes(N) requires N >=Int 0 [simplification]`
- Lines 63-67; kind `rule`, attributes: `simplification`: `rule applyBuiltin("str", V:Val, .Vals) => str(decimalCodes(projectIntTotal(V))) requires isInt(V) andBool projectIntTotal(V) >=Int 0 [simplification]`
- Lines 69-69; kind `syntax`, attributes: `function`, `total`: `syntax Bool ::= allDigitCodes(IntSeq) [function, total]`
- Lines 70-70; kind `rule`: `rule allDigitCodes(.IntSeq) => true`
- Lines 71-75; kind `rule`: `rule allDigitCodes(iCons(C:Int, R:IntSeq)) => (48 <=Int C andBool C <=Int 57) andBool allDigitCodes(R) // Contract of the fixed Int2String primitive on non-negative integers. // This is the only value-level trust boundary in the proof.`
- Lines 76-78; kind `rule`, attributes: `simplification`: `rule allDigitCodes(decimalCodes(N:Int)) => true requires N >=Int 0 [simplification]`
- Lines 80-80; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= codeDigitSum(IntSeq) [function, total]`
- Lines 81-81; kind `rule`: `rule codeDigitSum(.IntSeq) => 0`
- Lines 82-85; kind `rule`: `rule codeDigitSum(iCons(C:Int, R:IntSeq)) => (C -Int 48) +Int codeDigitSum(R) // Result of the source loop's "first nonzero digit seen" accumulator.`
- Lines 86-86; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= chooseFirst(Int, IntSeq) [function, total]`
- Lines 87-87; kind `rule`: `rule chooseFirst(F:Int, .IntSeq) => F`
- Lines 88-89; kind `rule`: `rule chooseFirst(0, iCons(C:Int, R:IntSeq)) => chooseFirst(C -Int 48, R)`
- Lines 90-93; kind `rule`, attributes: `simplification`: `rule chooseFirst(F:Int, iCons(_:Int, R:IntSeq)) => chooseFirst(F, R) requires F =/=Int 0 [simplification]`
- Lines 95-95; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= lastCode(Int, IntSeq) [function, total]`
- Lines 96-96; kind `rule`: `rule lastCode(C:Int, .IntSeq) => C`
- Lines 97-97; kind `rule`: `rule lastCode(_:Int, iCons(C:Int, R:IntSeq)) => lastCode(C, R)`
- Lines 99-99; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= signedDigitSum(Int) [function, total]`
- Lines 100-103; kind `rule`: `rule signedDigitSum(I:Int) => codeDigitSum(decimalCodes(magnitude(I))) -Int (2 *Int chooseFirst(0, decimalCodes(magnitude(I)))) requires I <Int 0`
- Lines 104-106; kind `rule`: `rule signedDigitSum(I:Int) => codeDigitSum(decimalCodes(magnitude(I))) requires I >=Int 0`
- Lines 108-108; kind `syntax`, attributes: `function`, `total`: `syntax Int ::= countNumsSpec(ValSeq) [function, total]`
- Lines 109-109; kind `rule`: `rule countNumsSpec(.ValSeq) => 0`
- Lines 110-114; kind `rule`: `rule countNumsSpec(vCons(V:Val, R:ValSeq)) => (#if signedDigitSum(projectIntTotal(V)) >Int 0 #then 1 #else 0 #fi) +Int countNumsSpec(R) requires isInt(V)`
- Lines 115-117; kind `rule`: `rule countNumsSpec(vCons(V:Val, R:ValSeq)) => countNumsSpec(R) requires notBool isInt(V)`

### `/tmp/audit-work/108-count-nums-audit/spec.k`

SHA-256: `2f3f8182ea2e11d9a8a9572f9bccfcee0f675db831eb6a29bc1bf97cbd47fecf`. Provenance: candidate proof extension/claim.

- Lines 8-53; kind `claim`: `claim [digit-loop]: <k> #loop( str(CS:IntSeq), Name("char"), Assign(Name("digit"), Call(Name("int"), Name("char"))) If(Compare(Name("first_digit"), CmpOp("==", Int(0))), Assign(Name("first_digit"), Name("digit")) .Stmts, .Stmts) AugAssign(Name("digit_sum"), "+", Name("digit")) .Stmts) => .K ... </k> <env> 1 </env> <scopes> 0 |-> scope("count_nums" |-> FN:Val, parent(-1)) -1 |-> builtinsScope 1 |-> scope( "arr" |-> list(ARR:ValSeq) "count" |-> COUNT:Int "num" |-> NUM:Val "n" |-> NN:Val "digit_sum" |-> (SUM:Int => SUM +Int codeDigitSum(CS)) "first_digit" |-> (FIRST:Int => chooseFirst(FIRST, CS)) "char" |-> (str(iCons(PREV:Int, .IntSeq)) => str(iCons(lastCode(PREV, CS), .IntSeq))) "digit" |-> (PREV -Int 48 => lastCode(PREV, CS) -Int 48), parent(0)) </scopes> <scopeLoc> 2 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> STACK:List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires allDigitCodes(CS) andBool 48 <=Int PREV andBool PREV <=Int 57 // Recurrent outer-loop base case. The source return and fixed frame-pop // behavior are part of this claim.`
- Lines 54-119; kind `claim`: `claim [outer-loop-empty]: <k> #loop( list(.ValSeq), Name("num"), If(Compare(Name("num"), CmpOp("<", Int(0))), Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts, Assign(Name("n"), Name("num")) .Stmts) Assign(Name("digit_sum"), Int(0)) Assign(Name("first_digit"), Int(0)) Assign(Name("char"), Str("0")) Assign(Name("digit"), Int(0)) For( Name("char"), Call(Name("str"), Name("n")), Assign(Name("digit"), Call(Name("int"), Name("char"))) If(Compare(Name("first_digit"), CmpOp("==", Int(0))), Assign(Name("first_digit"), Name("digit")) .Stmts, .Stmts) AugAssign(Name("digit_sum"), "+", Name("digit")) .Stmts) If(Compare(Name("num"), CmpOp("<", Int(0))), AugAssign( Name("digit_sum"), "-", BinOp("*", Int(2), Name("first_digit"))) .Stmts, .Stmts) If(Compare(Name("digit_sum"), CmpOp(">", Int(0))), AugAssign(Name("count"), "+", Int(1)) .Stmts, .Stmts) .Stmts) ~> (Return(Name("count")) .Stmts):Stmts ~> #endcall => C:Int </k> <env> 1 => 0 </env> <scopes> 0 |-> scope("count_nums" |-> FN:Val, parent(-1)) -1 |-> builtinsScope 1 |-> scope( "arr" |-> list(ORIGINAL:ValSeq) "count" |-> C:Int "num" |-> OLDNUM:Val "n" |-> OLDN:Val "digit_sum" |-> OLDSUM:Int "first_digit" |-> OLDFIRST:Int "char" |-> str(iCons(OLDCODE:Int, .IntSeq)) "digit" |-> OLDCODE -Int 48, parent(0)) => 0 |-> scope("count_nums" |-> FN, parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 2 => 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> ListItem(frame(.K, 0, 1)) => .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> // Recurrent outer-loop inductive case over one integer head and an // arbitrary all-integer tail.`
- Lines 120-186; kind `claim`: `claim [outer-loop-step]: <k> #loop( list(vCons(I:Val, R:ValSeq)), Name("num"), If(Compare(Name("num"), CmpOp("<", Int(0))), Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts, Assign(Name("n"), Name("num")) .Stmts) Assign(Name("digit_sum"), Int(0)) Assign(Name("first_digit"), Int(0)) Assign(Name("char"), Str("0")) Assign(Name("digit"), Int(0)) For( Name("char"), Call(Name("str"), Name("n")), Assign(Name("digit"), Call(Name("int"), Name("char"))) If(Compare(Name("first_digit"), CmpOp("==", Int(0))), Assign(Name("first_digit"), Name("digit")) .Stmts, .Stmts) AugAssign(Name("digit_sum"), "+", Name("digit")) .Stmts) If(Compare(Name("num"), CmpOp("<", Int(0))), AugAssign( Name("digit_sum"), "-", BinOp("*", Int(2), Name("first_digit"))) .Stmts, .Stmts) If(Compare(Name("digit_sum"), CmpOp(">", Int(0))), AugAssign(Name("count"), "+", Int(1)) .Stmts, .Stmts) .Stmts) ~> (Return(Name("count")) .Stmts):Stmts ~> #endcall => C:Int +Int countNumsSpec(vCons(I, R)) </k> <env> 1 => 0 </env> <scopes> 0 |-> scope("count_nums" |-> FN:Val, parent(-1)) -1 |-> builtinsScope 1 |-> scope( "arr" |-> list(ORIGINAL:ValSeq) "count" |-> C:Int "num" |-> OLDNUM:Val "n" |-> OLDN:Val "digit_sum" |-> OLDSUM:Int "first_digit" |-> OLDFIRST:Int "char" |-> str(iCons(OLDCODE:Int, .IntSeq)) "digit" |-> OLDCODE -Int 48, parent(0)) => 0 |-> scope("count_nums" |-> FN, parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 2 => 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> ListItem(frame(.K, 0, 1)) => .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires isInt(I) andBool allInts(R) // Exact call setup through parameter binding, count initialization, and // evaluation of the outer iterable. No program result is summarized here.`
- Lines 187-324; kind `claim`: `claim [call-setup-nonempty]: <k> Call(Name("count_nums"), list(vCons(I:Int, R:ValSeq))) => #loop( list(vCons(I, R)), Name("num"), If(Compare(Name("num"), CmpOp("<", Int(0))), Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts, Assign(Name("n"), Name("num")) .Stmts) Assign(Name("digit_sum"), Int(0)) Assign(Name("first_digit"), Int(0)) Assign(Name("char"), Str("0")) Assign(Name("digit"), Int(0)) For( Name("char"), Call(Name("str"), Name("n")), Assign(Name("digit"), Call(Name("int"), Name("char"))) If(Compare(Name("first_digit"), CmpOp("==", Int(0))), Assign(Name("first_digit"), Name("digit")) .Stmts, .Stmts) AugAssign(Name("digit_sum"), "+", Name("digit")) .Stmts) If(Compare(Name("num"), CmpOp("<", Int(0))), AugAssign( Name("digit_sum"), "-", BinOp("*", Int(2), Name("first_digit"))) .Stmts, .Stmts) If(Compare(Name("digit_sum"), CmpOp(">", Int(0))), AugAssign(Name("count"), "+", Int(1)) .Stmts, .Stmts) .Stmts) ~> (Return(Name("count")) .Stmts):Stmts ~> #endcall </k> <env> 0 => 1 </env> <scopes> 0 |-> scope( "count_nums" |-> closureVal( "arr" , .ParamNames, Assign(Name("count"), Int(0)) For( Name("num"), Name("arr"), If(Compare(Name("num"), CmpOp("<", Int(0))), Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts, Assign(Name("n"), Name("num")) .Stmts) Assign(Name("digit_sum"), Int(0)) Assign(Name("first_digit"), Int(0)) Assign(Name("char"), Str("0")) Assign(Name("digit"), Int(0)) For( Name("char"), Call(Name("str"), Name("n")), Assign(Name("digit"), Call(Name("int"), Name("char"))) If(Compare(Name("first_digit"), CmpOp("==", Int(0))), Assign(Name("first_digit"), Name("digit")) .Stmts, .Stmts) AugAssign(Name("digit_sum"), "+", Name("digit")) .Stmts) If(Compare(Name("num"), CmpOp("<", Int(0))), AugAssign( Name("digit_sum"), "-", BinOp("*", Int(2), Name("first_digit"))) .Stmts, .Stmts) If(Compare(Name("digit_sum"), CmpOp(">", Int(0))), AugAssign(Name("count"), "+", Int(1)) .Stmts, .Stmts) .Stmts) Return(Name("count")) .Stmts, 0), parent(-1)) -1 |-> builtinsScope => 0 |-> scope( "count_nums" |-> closureVal( "arr" , .ParamNames, Assign(Name("count"), Int(0)) For( Name("num"), Name("arr"), If(Compare(Name("num"), CmpOp("<", Int(0))), Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts, Assign(Name("n"), Name("num")) .Stmts) Assign(Name("digit_sum"), Int(0)) Assign(Name("first_digit"), Int(0)) Assign(Name("char"), Str("0")) Assign(Name("digit"), Int(0)) For( Name("char"), Call(Name("str"), Name("n")), Assign(Name("digit"), Call(Name("int"), Name("char"))) If(Compare(Name("first_digit"), CmpOp("==", Int(0))), Assign(Name("first_digit"), Name("digit")) .Stmts, .Stmts) AugAssign(Name("digit_sum"), "+", Name("digit")) .Stmts) If(Compare(Name("num"), CmpOp("<", Int(0))), AugAssign( Name("digit_sum"), "-", BinOp("*", Int(2), Name("first_digit"))) .Stmts, .Stmts) If(Compare(Name("digit_sum"), CmpOp(">", Int(0))), AugAssign(Name("count"), "+", Int(1)) .Stmts, .Stmts) .Stmts) Return(Name("count")) .Stmts, 0), parent(-1)) -1 |-> builtinsScope 1 |-> scope( "arr" |-> list(vCons(I, R)) "count" |-> 0, parent(0)) </scopes> <scopeLoc> 1 => 2 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List => ListItem(frame(.K, 0, 1)) </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires allInts(R) // First outer iteration, before the loop body has created its temporary // locals. This connects function entry to the recurrent loop claims.`
- Lines 325-384; kind `claim`: `claim [outer-loop-initial]: <k> #loop( list(vCons(I:Int, R:ValSeq)), Name("num"), If(Compare(Name("num"), CmpOp("<", Int(0))), Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts, Assign(Name("n"), Name("num")) .Stmts) Assign(Name("digit_sum"), Int(0)) Assign(Name("first_digit"), Int(0)) Assign(Name("char"), Str("0")) Assign(Name("digit"), Int(0)) For( Name("char"), Call(Name("str"), Name("n")), Assign(Name("digit"), Call(Name("int"), Name("char"))) If(Compare(Name("first_digit"), CmpOp("==", Int(0))), Assign(Name("first_digit"), Name("digit")) .Stmts, .Stmts) AugAssign(Name("digit_sum"), "+", Name("digit")) .Stmts) If(Compare(Name("num"), CmpOp("<", Int(0))), AugAssign( Name("digit_sum"), "-", BinOp("*", Int(2), Name("first_digit"))) .Stmts, .Stmts) If(Compare(Name("digit_sum"), CmpOp(">", Int(0))), AugAssign(Name("count"), "+", Int(1)) .Stmts, .Stmts) .Stmts) ~> (Return(Name("count")) .Stmts):Stmts ~> #endcall => C:Int +Int countNumsSpec(vCons(I, R)) </k> <env> 1 => 0 </env> <scopes> 0 |-> scope("count_nums" |-> FN:Val, parent(-1)) -1 |-> builtinsScope 1 |-> scope( "arr" |-> list(vCons(I, R)) "count" |-> C:Int, parent(0)) => 0 |-> scope("count_nums" |-> FN, parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 2 => 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> ListItem(frame(.K, 0, 1)) => .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires allInts(R) // Exact translated function call on the empty list.`
- Lines 385-441; kind `claim`: `claim [count-nums-empty]: <k> Call(Name("count_nums"), list(.ValSeq)) => 0 </k> <env> 0 </env> <scopes> 0 |-> scope( "count_nums" |-> closureVal( "arr" , .ParamNames, Assign(Name("count"), Int(0)) For( Name("num"), Name("arr"), If(Compare(Name("num"), CmpOp("<", Int(0))), Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts, Assign(Name("n"), Name("num")) .Stmts) Assign(Name("digit_sum"), Int(0)) Assign(Name("first_digit"), Int(0)) Assign(Name("char"), Str("0")) Assign(Name("digit"), Int(0)) For( Name("char"), Call(Name("str"), Name("n")), Assign(Name("digit"), Call(Name("int"), Name("char"))) If(Compare(Name("first_digit"), CmpOp("==", Int(0))), Assign(Name("first_digit"), Name("digit")) .Stmts, .Stmts) AugAssign(Name("digit_sum"), "+", Name("digit")) .Stmts) If(Compare(Name("num"), CmpOp("<", Int(0))), AugAssign( Name("digit_sum"), "-", BinOp("*", Int(2), Name("first_digit"))) .Stmts, .Stmts) If(Compare(Name("digit_sum"), CmpOp(">", Int(0))), AugAssign(Name("count"), "+", Int(1)) .Stmts, .Stmts) .Stmts) Return(Name("count")) .Stmts, 0), parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> // Exact translated function call on every nonempty finite integer list.`
- Lines 442-498; kind `claim`: `claim [count-nums-nonempty]: <k> Call(Name("count_nums"), list(vCons(I:Int, R:ValSeq))) => ?RESULT:Int </k> <env> 0 </env> <scopes> 0 |-> scope( "count_nums" |-> closureVal( "arr" , .ParamNames, Assign(Name("count"), Int(0)) For( Name("num"), Name("arr"), If(Compare(Name("num"), CmpOp("<", Int(0))), Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts, Assign(Name("n"), Name("num")) .Stmts) Assign(Name("digit_sum"), Int(0)) Assign(Name("first_digit"), Int(0)) Assign(Name("char"), Str("0")) Assign(Name("digit"), Int(0)) For( Name("char"), Call(Name("str"), Name("n")), Assign(Name("digit"), Call(Name("int"), Name("char"))) If(Compare(Name("first_digit"), CmpOp("==", Int(0))), Assign(Name("first_digit"), Name("digit")) .Stmts, .Stmts) AugAssign(Name("digit_sum"), "+", Name("digit")) .Stmts) If(Compare(Name("num"), CmpOp("<", Int(0))), AugAssign( Name("digit_sum"), "-", BinOp("*", Int(2), Name("first_digit"))) .Stmts, .Stmts) If(Compare(Name("digit_sum"), CmpOp(">", Int(0))), AugAssign(Name("count"), "+", Int(1)) .Stmts, .Stmts) .Stmts) Return(Name("count")) .Stmts, 0), parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires allInts(R) ensures ?RESULT ==Int countNumsSpec(vCons(I, R))`
