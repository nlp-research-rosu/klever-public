# Exhaustive K declaration and rule inventory

Source set:
- `reference-semantics/semantics/assert.k`
- `reference-semantics/semantics/bool.k`
- `reference-semantics/semantics/builtins.k`
- `reference-semantics/semantics/call.k`
- `reference-semantics/semantics/comprehension.k`
- `reference-semantics/semantics/concrete.k`
- `reference-semantics/semantics/controls.k`
- `reference-semantics/semantics/core.k`
- `reference-semantics/semantics/dict.k`
- `reference-semantics/semantics/float.k`
- `reference-semantics/semantics/functions.k`
- `reference-semantics/semantics/int.k`
- `reference-semantics/semantics/iter.k`
- `reference-semantics/semantics/list.k`
- `reference-semantics/semantics/methods.k`
- `reference-semantics/semantics/operators.k`
- `reference-semantics/semantics/range.k`
- `reference-semantics/semantics/set.k`
- `reference-semantics/semantics/sort.k`
- `reference-semantics/semantics/str.k`
- `reference-semantics/semantics/subscript.k`
- `reference-semantics/semantics/syntax.k`
- `reference-semantics/semantics/tuple.k`
- `reference-semantics/semantics.k`
- `verification.k`

Mechanical counts:
- `attr:concrete`: 35
- `attr:function`: 148
- `attr:macro`: 4
- `attr:no-evaluators`: 22
- `attr:owise`: 26
- `attr:priority`: 45
- `attr:seqstrict`: 1
- `attr:strict`: 2
- `attr:symbol`: 25
- `attr:total`: 110
- `configuration`: 1
- `context`: 5
- `rule`: 701
- `syntax`: 230

Every attribute occurrence by containing declaration block:
- `priority` — `reference-semantics/semantics/assert.k:13`
- `priority` — `reference-semantics/semantics/bool.k:29`
- `priority` — `reference-semantics/semantics/bool.k:31`
- `priority` — `reference-semantics/semantics/bool.k:35`
- `priority` — `reference-semantics/semantics/bool.k:39`
- `priority` — `reference-semantics/semantics/bool.k:43`
- `function` — `reference-semantics/semantics/builtins.k:17`
- `function` — `reference-semantics/semantics/builtins.k:20`
- `function` — `reference-semantics/semantics/builtins.k:36`
- `total` — `reference-semantics/semantics/builtins.k:36`
- `function` — `reference-semantics/semantics/builtins.k:54`
- `function` — `reference-semantics/semantics/builtins.k:97`
- `function` — `reference-semantics/semantics/builtins.k:102`
- `function` — `reference-semantics/semantics/builtins.k:114`
- `total` — `reference-semantics/semantics/builtins.k:114`
- `function` — `reference-semantics/semantics/builtins.k:117`
- `total` — `reference-semantics/semantics/builtins.k:117`
- `function` — `reference-semantics/semantics/builtins.k:126`
- `total` — `reference-semantics/semantics/builtins.k:126`
- `function` — `reference-semantics/semantics/builtins.k:134`
- `total` — `reference-semantics/semantics/builtins.k:134`
- `function` — `reference-semantics/semantics/builtins.k:158`
- `total` — `reference-semantics/semantics/builtins.k:158`
- `function` — `reference-semantics/semantics/builtins.k:188`
- `function` — `reference-semantics/semantics/builtins.k:194`
- `total` — `reference-semantics/semantics/builtins.k:194`
- `function` — `reference-semantics/semantics/builtins.k:196`
- `total` — `reference-semantics/semantics/builtins.k:196`
- `owise` — `reference-semantics/semantics/builtins.k:198`
- `function` — `reference-semantics/semantics/builtins.k:199`
- `total` — `reference-semantics/semantics/builtins.k:199`
- `owise` — `reference-semantics/semantics/builtins.k:201`
- `function` — `reference-semantics/semantics/builtins.k:203`
- `total` — `reference-semantics/semantics/builtins.k:203`
- `function` — `reference-semantics/semantics/builtins.k:214`
- `total` — `reference-semantics/semantics/builtins.k:214`
- `owise` — `reference-semantics/semantics/builtins.k:223`
- `function` — `reference-semantics/semantics/builtins.k:226`
- `total` — `reference-semantics/semantics/builtins.k:226`
- `owise` — `reference-semantics/semantics/builtins.k:228`
- `function` — `reference-semantics/semantics/builtins.k:230`
- `total` — `reference-semantics/semantics/builtins.k:230`
- `owise` — `reference-semantics/semantics/builtins.k:236`
- `function` — `reference-semantics/semantics/builtins.k:238`
- `total` — `reference-semantics/semantics/builtins.k:238`
- `owise` — `reference-semantics/semantics/builtins.k:243`
- `function` — `reference-semantics/semantics/builtins.k:244`
- `total` — `reference-semantics/semantics/builtins.k:244`
- `function` — `reference-semantics/semantics/builtins.k:247`
- `total` — `reference-semantics/semantics/builtins.k:247`
- `function` — `reference-semantics/semantics/builtins.k:250`
- `total` — `reference-semantics/semantics/builtins.k:250`
- `function` — `reference-semantics/semantics/builtins.k:255`
- `total` — `reference-semantics/semantics/builtins.k:255`
- `owise` — `reference-semantics/semantics/builtins.k:263`
- `function` — `reference-semantics/semantics/builtins.k:265`
- `total` — `reference-semantics/semantics/builtins.k:265`
- `owise` — `reference-semantics/semantics/builtins.k:268`
- `function` — `reference-semantics/semantics/builtins.k:269`
- `total` — `reference-semantics/semantics/builtins.k:269`
- `function` — `reference-semantics/semantics/builtins.k:272`
- `total` — `reference-semantics/semantics/builtins.k:272`
- `priority` — `reference-semantics/semantics/builtins.k:280`
- `function` — `reference-semantics/semantics/builtins.k:285`
- `total` — `reference-semantics/semantics/builtins.k:285`
- `symbol` — `reference-semantics/semantics/builtins.k:285`
- `no-evaluators` — `reference-semantics/semantics/builtins.k:285`
- `function` — `reference-semantics/semantics/builtins.k:293`
- `owise` — `reference-semantics/semantics/builtins.k:295`
- `owise` — `reference-semantics/semantics/builtins.k:297`
- `owise` — `reference-semantics/semantics/call.k:20`
- `owise` — `reference-semantics/semantics/call.k:31`
- `priority` — `reference-semantics/semantics/call.k:38`
- `priority` — `reference-semantics/semantics/call.k:42`
- `priority` — `reference-semantics/semantics/call.k:47`
- `function` — `reference-semantics/semantics/call.k:52`
- `total` — `reference-semantics/semantics/call.k:52`
- `priority` — `reference-semantics/semantics/call.k:56`
- `priority` — `reference-semantics/semantics/call.k:63`
- `macro` — `reference-semantics/semantics/comprehension.k:14`
- `macro` — `reference-semantics/semantics/comprehension.k:18`
- `macro` — `reference-semantics/semantics/comprehension.k:24`
- `priority` — `reference-semantics/semantics/concrete.k:28`
- `priority` — `reference-semantics/semantics/concrete.k:31`
- `function` — `reference-semantics/semantics/concrete.k:42`
- `function` — `reference-semantics/semantics/concrete.k:51`
- `function` — `reference-semantics/semantics/concrete.k:56`
- `total` — `reference-semantics/semantics/concrete.k:56`
- `owise` — `reference-semantics/semantics/concrete.k:59`
- `priority` — `reference-semantics/semantics/controls.k:12`
- `priority` — `reference-semantics/semantics/controls.k:27`
- `owise` — `reference-semantics/semantics/controls.k:36`
- `owise` — `reference-semantics/semantics/controls.k:89`
- `owise` — `reference-semantics/semantics/controls.k:91`
- `priority` — `reference-semantics/semantics/controls.k:95`
- `priority` — `reference-semantics/semantics/controls.k:98`
- `priority` — `reference-semantics/semantics/controls.k:101`
- `priority` — `reference-semantics/semantics/controls.k:106`
- `function` — `reference-semantics/semantics/core.k:68`
- `total` — `reference-semantics/semantics/core.k:68`
- `owise` — `reference-semantics/semantics/core.k:70`
- `function` — `reference-semantics/semantics/core.k:76`
- `total` — `reference-semantics/semantics/core.k:76`
- `owise` — `reference-semantics/semantics/core.k:78`
- `priority` — `reference-semantics/semantics/core.k:85`
- `function` — `reference-semantics/semantics/core.k:100`
- `total` — `reference-semantics/semantics/core.k:100`
- `owise` — `reference-semantics/semantics/core.k:102`
- `function` — `reference-semantics/semantics/core.k:107`
- `function` — `reference-semantics/semantics/core.k:109`
- `total` — `reference-semantics/semantics/core.k:109`
- `priority` — `reference-semantics/semantics/core.k:145`
- `function` — `reference-semantics/semantics/core.k:157`
- `total` — `reference-semantics/semantics/core.k:157`
- `function` — `reference-semantics/semantics/core.k:199`
- `function` — `reference-semantics/semantics/core.k:208`
- `function` — `reference-semantics/semantics/core.k:209`
- `function` — `reference-semantics/semantics/core.k:210`
- `function` — `reference-semantics/semantics/core.k:213`
- `total` — `reference-semantics/semantics/core.k:213`
- `function` — `reference-semantics/semantics/core.k:217`
- `total` — `reference-semantics/semantics/core.k:217`
- `function` — `reference-semantics/semantics/core.k:223`
- `total` — `reference-semantics/semantics/core.k:223`
- `function` — `reference-semantics/semantics/core.k:227`
- `total` — `reference-semantics/semantics/core.k:227`
- `function` — `reference-semantics/semantics/core.k:233`
- `total` — `reference-semantics/semantics/core.k:233`
- `function` — `reference-semantics/semantics/dict.k:37`
- `total` — `reference-semantics/semantics/dict.k:37`
- `function` — `reference-semantics/semantics/dict.k:43`
- `total` — `reference-semantics/semantics/dict.k:43`
- `function` — `reference-semantics/semantics/dict.k:49`
- `total` — `reference-semantics/semantics/dict.k:49`
- `owise` — `reference-semantics/semantics/dict.k:54`
- `priority` — `reference-semantics/semantics/dict.k:58`
- `function` — `reference-semantics/semantics/dict.k:64`
- `priority` — `reference-semantics/semantics/dict.k:65`
- `function` — `reference-semantics/semantics/dict.k:70`
- `function` — `reference-semantics/semantics/dict.k:90`
- `total` — `reference-semantics/semantics/dict.k:90`
- `function` — `reference-semantics/semantics/dict.k:97`
- `function` — `reference-semantics/semantics/dict.k:101`
- `function` — `reference-semantics/semantics/float.k:24`
- `total` — `reference-semantics/semantics/float.k:24`
- `symbol` — `reference-semantics/semantics/float.k:24`
- `no-evaluators` — `reference-semantics/semantics/float.k:24`
- `concrete` — `reference-semantics/semantics/float.k:25`
- `function` — `reference-semantics/semantics/float.k:30`
- `total` — `reference-semantics/semantics/float.k:30`
- `symbol` — `reference-semantics/semantics/float.k:30`
- `no-evaluators` — `reference-semantics/semantics/float.k:30`
- `concrete` — `reference-semantics/semantics/float.k:31`
- `function` — `reference-semantics/semantics/float.k:37`
- `total` — `reference-semantics/semantics/float.k:37`
- `symbol` — `reference-semantics/semantics/float.k:37`
- `no-evaluators` — `reference-semantics/semantics/float.k:37`
- `concrete` — `reference-semantics/semantics/float.k:38`
- `function` — `reference-semantics/semantics/float.k:50`
- `total` — `reference-semantics/semantics/float.k:50`
- `symbol` — `reference-semantics/semantics/float.k:50`
- `no-evaluators` — `reference-semantics/semantics/float.k:50`
- `concrete` — `reference-semantics/semantics/float.k:51`
- `function` — `reference-semantics/semantics/float.k:54`
- `total` — `reference-semantics/semantics/float.k:54`
- `symbol` — `reference-semantics/semantics/float.k:54`
- `no-evaluators` — `reference-semantics/semantics/float.k:54`
- `concrete` — `reference-semantics/semantics/float.k:55`
- `priority` — `reference-semantics/semantics/float.k:66`
- `priority` — `reference-semantics/semantics/float.k:71`
- `function` — `reference-semantics/semantics/float.k:73`
- `total` — `reference-semantics/semantics/float.k:73`
- `symbol` — `reference-semantics/semantics/float.k:73`
- `concrete` — `reference-semantics/semantics/float.k:74`
- `concrete` — `reference-semantics/semantics/float.k:75`
- `priority` — `reference-semantics/semantics/float.k:83`
- `function` — `reference-semantics/semantics/float.k:86`
- `total` — `reference-semantics/semantics/float.k:86`
- `symbol` — `reference-semantics/semantics/float.k:86`
- `concrete` — `reference-semantics/semantics/float.k:87`
- `concrete` — `reference-semantics/semantics/float.k:88`
- `function` — `reference-semantics/semantics/float.k:93`
- `total` — `reference-semantics/semantics/float.k:93`
- `symbol` — `reference-semantics/semantics/float.k:93`
- `concrete` — `reference-semantics/semantics/float.k:94`
- `concrete` — `reference-semantics/semantics/float.k:95`
- `function` — `reference-semantics/semantics/float.k:103`
- `total` — `reference-semantics/semantics/float.k:103`
- `symbol` — `reference-semantics/semantics/float.k:103`
- `no-evaluators` — `reference-semantics/semantics/float.k:103`
- `concrete` — `reference-semantics/semantics/float.k:104`
- `function` — `reference-semantics/semantics/float.k:107`
- `total` — `reference-semantics/semantics/float.k:107`
- `symbol` — `reference-semantics/semantics/float.k:107`
- `no-evaluators` — `reference-semantics/semantics/float.k:107`
- `concrete` — `reference-semantics/semantics/float.k:108`
- `function` — `reference-semantics/semantics/float.k:111`
- `total` — `reference-semantics/semantics/float.k:111`
- `symbol` — `reference-semantics/semantics/float.k:111`
- `no-evaluators` — `reference-semantics/semantics/float.k:111`
- `concrete` — `reference-semantics/semantics/float.k:112`
- `function` — `reference-semantics/semantics/float.k:115`
- `total` — `reference-semantics/semantics/float.k:115`
- `symbol` — `reference-semantics/semantics/float.k:115`
- `no-evaluators` — `reference-semantics/semantics/float.k:115`
- `concrete` — `reference-semantics/semantics/float.k:116`
- `function` — `reference-semantics/semantics/float.k:119`
- `total` — `reference-semantics/semantics/float.k:119`
- `symbol` — `reference-semantics/semantics/float.k:119`
- `no-evaluators` — `reference-semantics/semantics/float.k:119`
- `concrete` — `reference-semantics/semantics/float.k:120`
- `function` — `reference-semantics/semantics/float.k:125`
- `total` — `reference-semantics/semantics/float.k:125`
- `symbol` — `reference-semantics/semantics/float.k:125`
- `no-evaluators` — `reference-semantics/semantics/float.k:125`
- `concrete` — `reference-semantics/semantics/float.k:126`
- `function` — `reference-semantics/semantics/float.k:142`
- `total` — `reference-semantics/semantics/float.k:142`
- `symbol` — `reference-semantics/semantics/float.k:142`
- `no-evaluators` — `reference-semantics/semantics/float.k:142`
- `concrete` — `reference-semantics/semantics/float.k:143`
- `function` — `reference-semantics/semantics/float.k:160`
- `total` — `reference-semantics/semantics/float.k:160`
- `symbol` — `reference-semantics/semantics/float.k:160`
- `no-evaluators` — `reference-semantics/semantics/float.k:160`
- `concrete` — `reference-semantics/semantics/float.k:161`
- `concrete` — `reference-semantics/semantics/float.k:162`
- `function` — `reference-semantics/semantics/float.k:165`
- `function` — `reference-semantics/semantics/float.k:167`
- `total` — `reference-semantics/semantics/float.k:167`
- `function` — `reference-semantics/semantics/float.k:173`
- `total` — `reference-semantics/semantics/float.k:173`
- `function` — `reference-semantics/semantics/float.k:179`
- `total` — `reference-semantics/semantics/float.k:179`
- `function` — `reference-semantics/semantics/float.k:190`
- `total` — `reference-semantics/semantics/float.k:190`
- `symbol` — `reference-semantics/semantics/float.k:190`
- `no-evaluators` — `reference-semantics/semantics/float.k:190`
- `concrete` — `reference-semantics/semantics/float.k:191`
- `function` — `reference-semantics/semantics/float.k:195`
- `total` — `reference-semantics/semantics/float.k:195`
- `symbol` — `reference-semantics/semantics/float.k:195`
- `no-evaluators` — `reference-semantics/semantics/float.k:195`
- `concrete` — `reference-semantics/semantics/float.k:196`
- `function` — `reference-semantics/semantics/float.k:209`
- `total` — `reference-semantics/semantics/float.k:209`
- `symbol` — `reference-semantics/semantics/float.k:209`
- `no-evaluators` — `reference-semantics/semantics/float.k:209`
- `concrete` — `reference-semantics/semantics/float.k:210`
- `function` — `reference-semantics/semantics/float.k:217`
- `total` — `reference-semantics/semantics/float.k:217`
- `symbol` — `reference-semantics/semantics/float.k:217`
- `no-evaluators` — `reference-semantics/semantics/float.k:217`
- `concrete` — `reference-semantics/semantics/float.k:218`
- `function` — `reference-semantics/semantics/float.k:223`
- `total` — `reference-semantics/semantics/float.k:223`
- `symbol` — `reference-semantics/semantics/float.k:223`
- `no-evaluators` — `reference-semantics/semantics/float.k:223`
- `concrete` — `reference-semantics/semantics/float.k:224`
- `function` — `reference-semantics/semantics/float.k:230`
- `total` — `reference-semantics/semantics/float.k:230`
- `symbol` — `reference-semantics/semantics/float.k:230`
- `no-evaluators` — `reference-semantics/semantics/float.k:230`
- `concrete` — `reference-semantics/semantics/float.k:231`
- `priority` — `reference-semantics/semantics/float.k:233`
- `priority` — `reference-semantics/semantics/functions.k:68`
- `function` — `reference-semantics/semantics/int.k:19`
- `function` — `reference-semantics/semantics/list.k:18`
- `total` — `reference-semantics/semantics/list.k:18`
- `priority` — `reference-semantics/semantics/list.k:24`
- `function` — `reference-semantics/semantics/list.k:33`
- `total` — `reference-semantics/semantics/list.k:33`
- `function` — `reference-semantics/semantics/list.k:37`
- `owise` — `reference-semantics/semantics/list.k:50`
- `priority` — `reference-semantics/semantics/list.k:53`
- `function` — `reference-semantics/semantics/methods.k:10`
- `function` — `reference-semantics/semantics/methods.k:27`
- `total` — `reference-semantics/semantics/methods.k:27`
- `function` — `reference-semantics/semantics/methods.k:35`
- `function` — `reference-semantics/semantics/methods.k:41`
- `total` — `reference-semantics/semantics/methods.k:41`
- `owise` — `reference-semantics/semantics/methods.k:43`
- `function` — `reference-semantics/semantics/methods.k:48`
- `total` — `reference-semantics/semantics/methods.k:48`
- `function` — `reference-semantics/semantics/methods.k:52`
- `total` — `reference-semantics/semantics/methods.k:52`
- `function` — `reference-semantics/semantics/methods.k:65`
- `total` — `reference-semantics/semantics/methods.k:65`
- `priority` — `reference-semantics/semantics/methods.k:72`
- `function` — `reference-semantics/semantics/methods.k:75`
- `function` — `reference-semantics/semantics/methods.k:82`
- `function` — `reference-semantics/semantics/methods.k:85`
- `total` — `reference-semantics/semantics/methods.k:85`
- `priority` — `reference-semantics/semantics/methods.k:89`
- `priority` — `reference-semantics/semantics/methods.k:94`
- `function` — `reference-semantics/semantics/methods.k:97`
- `function` — `reference-semantics/semantics/methods.k:106`
- `total` — `reference-semantics/semantics/methods.k:106`
- `function` — `reference-semantics/semantics/methods.k:112`
- `total` — `reference-semantics/semantics/methods.k:112`
- `function` — `reference-semantics/semantics/methods.k:115`
- `total` — `reference-semantics/semantics/methods.k:115`
- `function` — `reference-semantics/semantics/methods.k:118`
- `total` — `reference-semantics/semantics/methods.k:118`
- `function` — `reference-semantics/semantics/methods.k:121`
- `total` — `reference-semantics/semantics/methods.k:121`
- `function` — `reference-semantics/semantics/methods.k:124`
- `total` — `reference-semantics/semantics/methods.k:124`
- `function` — `reference-semantics/semantics/methods.k:128`
- `total` — `reference-semantics/semantics/methods.k:128`
- `function` — `reference-semantics/semantics/methods.k:132`
- `total` — `reference-semantics/semantics/methods.k:132`
- `function` — `reference-semantics/semantics/methods.k:136`
- `total` — `reference-semantics/semantics/methods.k:136`
- `function` — `reference-semantics/semantics/methods.k:140`
- `total` — `reference-semantics/semantics/methods.k:140`
- `owise` — `reference-semantics/semantics/methods.k:143`
- `function` — `reference-semantics/semantics/methods.k:145`
- `total` — `reference-semantics/semantics/methods.k:145`
- `owise` — `reference-semantics/semantics/methods.k:147`
- `function` — `reference-semantics/semantics/methods.k:149`
- `total` — `reference-semantics/semantics/methods.k:149`
- `owise` — `reference-semantics/semantics/methods.k:152`
- `function` — `reference-semantics/semantics/methods.k:154`
- `total` — `reference-semantics/semantics/methods.k:154`
- `function` — `reference-semantics/semantics/methods.k:158`
- `total` — `reference-semantics/semantics/methods.k:158`
- `function` — `reference-semantics/semantics/methods.k:162`
- `total` — `reference-semantics/semantics/methods.k:162`
- `function` — `reference-semantics/semantics/methods.k:166`
- `total` — `reference-semantics/semantics/methods.k:166`
- `owise` — `reference-semantics/semantics/operators.k:17`
- `priority` — `reference-semantics/semantics/operators.k:25`
- `priority` — `reference-semantics/semantics/operators.k:28`
- `priority` — `reference-semantics/semantics/operators.k:34`
- `priority` — `reference-semantics/semantics/operators.k:38`
- `priority` — `reference-semantics/semantics/operators.k:44`
- `function` — `reference-semantics/semantics/range.k:9`
- `total` — `reference-semantics/semantics/range.k:9`
- `function` — `reference-semantics/semantics/range.k:12`
- `function` — `reference-semantics/semantics/set.k:11`
- `total` — `reference-semantics/semantics/set.k:11`
- `function` — `reference-semantics/semantics/set.k:16`
- `total` — `reference-semantics/semantics/set.k:16`
- `function` — `reference-semantics/semantics/set.k:25`
- `total` — `reference-semantics/semantics/set.k:25`
- `function` — `reference-semantics/semantics/set.k:31`
- `total` — `reference-semantics/semantics/set.k:31`
- `function` — `reference-semantics/semantics/set.k:35`
- `total` — `reference-semantics/semantics/set.k:35`
- `function` — `reference-semantics/semantics/sort.k:18`
- `total` — `reference-semantics/semantics/sort.k:18`
- `symbol` — `reference-semantics/semantics/sort.k:18`
- `no-evaluators` — `reference-semantics/semantics/sort.k:18`
- `function` — `reference-semantics/semantics/sort.k:19`
- `concrete` — `reference-semantics/semantics/sort.k:20`
- `concrete` — `reference-semantics/semantics/sort.k:21`
- `concrete` — `reference-semantics/semantics/sort.k:22`
- `concrete` — `reference-semantics/semantics/sort.k:23`
- `concrete` — `reference-semantics/semantics/sort.k:24`
- `function` — `reference-semantics/semantics/sort.k:26`
- `concrete` — `reference-semantics/semantics/sort.k:27`
- `concrete` — `reference-semantics/semantics/sort.k:28`
- `concrete` — `reference-semantics/semantics/sort.k:29`
- `concrete` — `reference-semantics/semantics/sort.k:31`
- `priority` — `reference-semantics/semantics/sort.k:40`
- `function` — `reference-semantics/semantics/sort.k:49`
- `total` — `reference-semantics/semantics/sort.k:49`
- `symbol` — `reference-semantics/semantics/sort.k:49`
- `no-evaluators` — `reference-semantics/semantics/sort.k:49`
- `function` — `reference-semantics/semantics/sort.k:51`
- `total` — `reference-semantics/semantics/sort.k:51`
- `function` — `reference-semantics/semantics/sort.k:57`
- `total` — `reference-semantics/semantics/sort.k:57`
- `function` — `reference-semantics/semantics/str.k:13`
- `function` — `reference-semantics/semantics/str.k:20`
- `total` — `reference-semantics/semantics/str.k:20`
- `function` — `reference-semantics/semantics/str.k:32`
- `total` — `reference-semantics/semantics/str.k:32`
- `function` — `reference-semantics/semantics/str.k:37`
- `total` — `reference-semantics/semantics/str.k:37`
- `function` — `reference-semantics/semantics/str.k:48`
- `total` — `reference-semantics/semantics/str.k:48`
- `function` — `reference-semantics/semantics/subscript.k:11`
- `total` — `reference-semantics/semantics/subscript.k:11`
- `function` — `reference-semantics/semantics/subscript.k:16`
- `function` — `reference-semantics/semantics/subscript.k:21`
- `total` — `reference-semantics/semantics/subscript.k:21`
- `priority` — `reference-semantics/semantics/subscript.k:31`
- `function` — `reference-semantics/semantics/subscript.k:37`
- `priority` — `reference-semantics/semantics/subscript.k:58`
- `function` — `reference-semantics/semantics/subscript.k:63`
- `function` — `reference-semantics/semantics/subscript.k:72`
- `total` — `reference-semantics/semantics/subscript.k:72`
- `function` — `reference-semantics/semantics/subscript.k:76`
- `function` — `reference-semantics/semantics/subscript.k:83`
- `function` — `reference-semantics/semantics/subscript.k:90`
- `total` — `reference-semantics/semantics/subscript.k:90`
- `function` — `reference-semantics/semantics/subscript.k:96`
- `total` — `reference-semantics/semantics/subscript.k:96`
- `function` — `reference-semantics/semantics/subscript.k:102`
- `total` — `reference-semantics/semantics/subscript.k:102`
- `function` — `reference-semantics/semantics/subscript.k:109`
- `function` — `reference-semantics/semantics/subscript.k:116`
- `strict` — `reference-semantics/semantics/syntax.k:9`
- `seqstrict` — `reference-semantics/semantics/syntax.k:9`
- `macro` — `reference-semantics/semantics/syntax.k:9`
- `strict` — `reference-semantics/semantics/syntax.k:41`
- `function` — `reference-semantics/semantics/tuple.k:24`
- `priority` — `reference-semantics/semantics/tuple.k:35`
- `priority` — `reference-semantics/semantics/tuple.k:44`
- `priority` — `reference-semantics/semantics/tuple.k:52`
- `function` — `verification.k:6`
- `total` — `verification.k:6`
- `function` — `verification.k:19`
- `total` — `verification.k:19`
- `function` — `verification.k:23`
- `total` — `verification.k:23`

Opaque/symbolic/concrete-only declaration candidates:
- `reference-semantics/semantics/builtins.k:285` — `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]`
- `reference-semantics/semantics/float.k:24` — `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`
- `reference-semantics/semantics/float.k:30` — `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`
- `reference-semantics/semantics/float.k:37` — `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`
- `reference-semantics/semantics/float.k:50` — `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`
- `reference-semantics/semantics/float.k:54` — `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`
- `reference-semantics/semantics/float.k:73` — `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]`
- `reference-semantics/semantics/float.k:86` — `syntax Float ::= toF(Val) [function, total, symbol(toF)]`
- `reference-semantics/semantics/float.k:93` — `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]`
- `reference-semantics/semantics/float.k:103` — `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`
- `reference-semantics/semantics/float.k:107` — `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`
- `reference-semantics/semantics/float.k:111` — `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`
- `reference-semantics/semantics/float.k:115` — `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`
- `reference-semantics/semantics/float.k:119` — `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`
- `reference-semantics/semantics/float.k:125` — `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`
- `reference-semantics/semantics/float.k:142` — `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`
- `reference-semantics/semantics/float.k:160` — `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`
- `reference-semantics/semantics/float.k:190` — `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`
- `reference-semantics/semantics/float.k:195` — `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`
- `reference-semantics/semantics/float.k:209` — `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`
- `reference-semantics/semantics/float.k:217` — `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`
- `reference-semantics/semantics/float.k:223` — `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`
- `reference-semantics/semantics/float.k:230` — `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`
- `reference-semantics/semantics/sort.k:18` — `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`
- `reference-semantics/semantics/sort.k:49` — `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`

## reference-semantics/semantics/assert.k
Declaration anchors: 3

### RULE reference-semantics/semantics/assert.k:6

```k
    6   rule <k> Assert(V:Val) => .K ... </k>
    7        requires truthy(V)
```

### RULE reference-semantics/semantics/assert.k:8

```k
    8   rule <k> Assert(V:Val) ~> _ => .K </k>
    9        <exc> NoExc => AssertionError </exc>
   10        <exit-code> _ => 1 </exit-code>
   11        requires notBool truthy(V)
```

### RULE reference-semantics/semantics/assert.k:13 attrs=priority

```k
   13   rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
   14        <heap> ... H |-> V:Val ... </heap>
   15        [priority(40)]
   16 endmodule
```

## reference-semantics/semantics/bool.k
Declaration anchors: 14

### RULE reference-semantics/semantics/bool.k:8

```k
    8   rule applyUn("not", V:Val) => notBool truthy(V)
```

### RULE reference-semantics/semantics/bool.k:10

```k
   10   rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### RULE reference-semantics/semantics/bool.k:11

```k
   11   rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

### CONTEXT reference-semantics/semantics/bool.k:16

```k
   16   context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### RULE reference-semantics/semantics/bool.k:17

```k
   17   rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### RULE reference-semantics/semantics/bool.k:18

```k
   18   rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
   19        requires truthy(V)
```

### RULE reference-semantics/semantics/bool.k:20

```k
   20   rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
   21        requires notBool truthy(V)
```

### RULE reference-semantics/semantics/bool.k:22

```k
   22   rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
   23        requires truthy(V)
```

### RULE reference-semantics/semantics/bool.k:24

```k
   24   rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
   25        requires notBool truthy(V)
```

### RULE reference-semantics/semantics/bool.k:29 attrs=priority

```k
   29   rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
   30        [priority(40)]
```

### RULE reference-semantics/semantics/bool.k:31 attrs=priority

```k
   31   rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
   32        <heap> ... H |-> V:Val ... </heap>
   33        requires truthy(V)
   34        [priority(40)]
```

### RULE reference-semantics/semantics/bool.k:35 attrs=priority

```k
   35   rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
   36        <heap> ... H |-> V:Val ... </heap>
   37        requires notBool truthy(V)
   38        [priority(40)]
```

### RULE reference-semantics/semantics/bool.k:39 attrs=priority

```k
   39   rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
   40        <heap> ... H |-> V:Val ... </heap>
   41        requires truthy(V)
   42        [priority(40)]
```

### RULE reference-semantics/semantics/bool.k:43 attrs=priority

```k
   43   rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
   44        <heap> ... H |-> V:Val ... </heap>
   45        requires notBool truthy(V)
   46        [priority(40)]
   47 endmodule
```

## reference-semantics/semantics/builtins.k
Declaration anchors: 175

### SYNTAX reference-semantics/semantics/builtins.k:17 attrs=function

```k
   17   syntax Val ::= applyBuiltin(String, Vals) [function]
```

### SYNTAX reference-semantics/semantics/builtins.k:20 attrs=function

```k
   20   syntax Int ::= seqLen(Val) [function]
```

### RULE reference-semantics/semantics/builtins.k:21

```k
   21   rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### RULE reference-semantics/semantics/builtins.k:22

```k
   22   rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### RULE reference-semantics/semantics/builtins.k:23

```k
   23   rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### RULE reference-semantics/semantics/builtins.k:24

```k
   24   rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### RULE reference-semantics/semantics/builtins.k:25

```k
   25   rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### RULE reference-semantics/semantics/builtins.k:26

```k
   26   rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

### RULE reference-semantics/semantics/builtins.k:32

```k
   32   rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### RULE reference-semantics/semantics/builtins.k:33

```k
   33   rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### RULE reference-semantics/semantics/builtins.k:34

```k
   34   rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### RULE reference-semantics/semantics/builtins.k:35

```k
   35   rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### SYNTAX reference-semantics/semantics/builtins.k:36 attrs=function,total

```k
   36   syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:37

```k
   37   rule charsOf(.IntSeq)                => .ValSeq
```

### RULE reference-semantics/semantics/builtins.k:38

```k
   38   rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

### RULE reference-semantics/semantics/builtins.k:41

```k
   41   rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

### RULE reference-semantics/semantics/builtins.k:44

```k
   44   rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

### SYNTAX reference-semantics/semantics/builtins.k:47

```k
   47   syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### RULE reference-semantics/semantics/builtins.k:48

```k
   48   rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### RULE reference-semantics/semantics/builtins.k:49

```k
   49   rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### RULE reference-semantics/semantics/builtins.k:50

```k
   50   rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
   51         => #sumAcc(R, ACC +Int intOf(V)) ... </k>
   52        requires isInt(V) orBool isBool(V)
```

### SYNTAX reference-semantics/semantics/builtins.k:54 attrs=function

```k
   54   syntax Int ::= intOf(Val) [function]
```

### RULE reference-semantics/semantics/builtins.k:55

```k
   55   rule intOf(I:Int)  => I
```

### RULE reference-semantics/semantics/builtins.k:56

```k
   56   rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

### SYNTAX reference-semantics/semantics/builtins.k:59

```k
   59   syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### RULE reference-semantics/semantics/builtins.k:60

```k
   60   rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### RULE reference-semantics/semantics/builtins.k:61

```k
   61   rule <k> #iterDone ~> #allCont => true ... </k>
```

### RULE reference-semantics/semantics/builtins.k:62

```k
   62   rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
   63        requires truthy(V)
```

### RULE reference-semantics/semantics/builtins.k:64

```k
   64   rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
   65        requires notBool truthy(V)
```

### SYNTAX reference-semantics/semantics/builtins.k:67

```k
   67   syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### RULE reference-semantics/semantics/builtins.k:68

```k
   68   rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### RULE reference-semantics/semantics/builtins.k:69

```k
   69   rule <k> #iterDone ~> #anyCont => false ... </k>
```

### RULE reference-semantics/semantics/builtins.k:70

```k
   70   rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
   71        requires truthy(V)
```

### RULE reference-semantics/semantics/builtins.k:72

```k
   72   rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
   73        requires notBool truthy(V)
```

### SYNTAX reference-semantics/semantics/builtins.k:76

```k
   76   syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### RULE reference-semantics/semantics/builtins.k:77

```k
   77   rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### RULE reference-semantics/semantics/builtins.k:78

```k
   78   rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
   79        requires isInt(V)
```

### RULE reference-semantics/semantics/builtins.k:80

```k
   80   rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### RULE reference-semantics/semantics/builtins.k:81

```k
   81   rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### RULE reference-semantics/semantics/builtins.k:82

```k
   82   rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
   83         => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
   84        requires isInt(V)
```

### SYNTAX reference-semantics/semantics/builtins.k:86

```k
   86   syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### RULE reference-semantics/semantics/builtins.k:87

```k
   87   rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### RULE reference-semantics/semantics/builtins.k:88

```k
   88   rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
   89        requires isInt(V)
```

### RULE reference-semantics/semantics/builtins.k:90

```k
   90   rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### RULE reference-semantics/semantics/builtins.k:91

```k
   91   rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### RULE reference-semantics/semantics/builtins.k:92

```k
   92   rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
   93         => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
   94        requires isInt(V)
```

### SYNTAX reference-semantics/semantics/builtins.k:97 attrs=function

```k
   97   syntax Int ::= maxVals(Int, Vals) [function]
```

### RULE reference-semantics/semantics/builtins.k:98

```k
   98   rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### RULE reference-semantics/semantics/builtins.k:99

```k
   99   rule maxVals(M:Int, .Vals)           => M
```

### RULE reference-semantics/semantics/builtins.k:100

```k
  100   rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### SYNTAX reference-semantics/semantics/builtins.k:102 attrs=function

```k
  102   syntax Int ::= minVals(Int, Vals) [function]
```

### RULE reference-semantics/semantics/builtins.k:103

```k
  103   rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### RULE reference-semantics/semantics/builtins.k:104

```k
  104   rule minVals(M:Int, .Vals)           => M
```

### RULE reference-semantics/semantics/builtins.k:105

```k
  105   rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

### RULE reference-semantics/semantics/builtins.k:108

```k
  108   rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
  109        requires N >=Int 0
```

### RULE reference-semantics/semantics/builtins.k:111

```k
  111   rule applyBuiltin("bin", N:Int, .Vals)
  112     => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
  113        requires N <Int 0
```

### SYNTAX reference-semantics/semantics/builtins.k:114 attrs=function,total

```k
  114   syntax IntSeq ::= binCodes(Int) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:115

```k
  115   rule binCodes(0) => iCons(48, .IntSeq)
```

### RULE reference-semantics/semantics/builtins.k:116

```k
  116   rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### SYNTAX reference-semantics/semantics/builtins.k:117 attrs=function,total

```k
  117   syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:118

```k
  118   rule binAcc(0, ACC:IntSeq) => ACC
```

### RULE reference-semantics/semantics/builtins.k:119

```k
  119   rule binAcc(N:Int, ACC:IntSeq)
  120     => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
  121        requires N >Int 0
```

### RULE reference-semantics/semantics/builtins.k:124

```k
  124   rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
  125         => #alloc(list(enumVS(VS, 0))) ... </k>
```

### SYNTAX reference-semantics/semantics/builtins.k:126 attrs=function,total

```k
  126   syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:127

```k
  127   rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### RULE reference-semantics/semantics/builtins.k:128

```k
  128   rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
  129     => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

### RULE reference-semantics/semantics/builtins.k:132

```k
  132   rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
  133         => #alloc(list(mapStrVS(VS))) ... </k>
```

### SYNTAX reference-semantics/semantics/builtins.k:134 attrs=function,total

```k
  134   syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:135

```k
  135   rule mapStrVS(.ValSeq) => .ValSeq
```

### RULE reference-semantics/semantics/builtins.k:136

```k
  136   rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### RULE reference-semantics/semantics/builtins.k:137

```k
  137   rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

### RULE reference-semantics/semantics/builtins.k:140

```k
  140   rule applyBuiltin("int", I:Int, .Vals) => I
```

### RULE reference-semantics/semantics/builtins.k:143

```k
  143   rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### RULE reference-semantics/semantics/builtins.k:144

```k
  144   rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
  145        requires 0 <=Int I andBool I <Int 128
```

### RULE reference-semantics/semantics/builtins.k:148

```k
  148   rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### RULE reference-semantics/semantics/builtins.k:149

```k
  149   rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

### RULE reference-semantics/semantics/builtins.k:152

```k
  152   rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
  153        requires 48 <=Int C andBool C <=Int 57
```

### RULE reference-semantics/semantics/builtins.k:156

```k
  156   rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
  157        requires isLen(CS) >=Int 2
```

### SYNTAX reference-semantics/semantics/builtins.k:158 attrs=function,total

```k
  158   syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:159

```k
  159   rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### RULE reference-semantics/semantics/builtins.k:160

```k
  160   rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

### RULE reference-semantics/semantics/builtins.k:163

```k
  163   rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### RULE reference-semantics/semantics/builtins.k:164

```k
  164   rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

### RULE reference-semantics/semantics/builtins.k:167

```k
  167   rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
  168         => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### RULE reference-semantics/semantics/builtins.k:169

```k
  169   rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### RULE reference-semantics/semantics/builtins.k:170

```k
  170   rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### RULE reference-semantics/semantics/builtins.k:171

```k
  171   rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
  172         => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### RULE reference-semantics/semantics/builtins.k:173

```k
  173   rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### RULE reference-semantics/semantics/builtins.k:174

```k
  174   rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

### RULE reference-semantics/semantics/builtins.k:177

```k
  177   rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### RULE reference-semantics/semantics/builtins.k:178

```k
  178   rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### RULE reference-semantics/semantics/builtins.k:179

```k
  179   rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
  180        requires S =/=Int 0
```

### RULE reference-semantics/semantics/builtins.k:187

```k
  187   rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### SYNTAX reference-semantics/semantics/builtins.k:188 attrs=function

```k
  188   syntax Int ::= evalArith(IntSeq) [function]
```

### RULE reference-semantics/semantics/builtins.k:189

```k
  189   rule evalArith(CS:IntSeq)
  190     => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### SYNTAX reference-semantics/semantics/builtins.k:192

```k
  192   syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### SYNTAX reference-semantics/semantics/builtins.k:194 attrs=function,total

```k
  194   syntax Bool ::= evDigit(Int) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:195

```k
  195   rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### SYNTAX reference-semantics/semantics/builtins.k:196 attrs=function,total

```k
  196   syntax Bool ::= evHead42(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:197

```k
  197   rule evHead42(iCons(42, _:IntSeq)) => true
```

### RULE reference-semantics/semantics/builtins.k:198 attrs=owise

```k
  198   rule evHead42(_:IntSeq)            => false [owise]
```

### SYNTAX reference-semantics/semantics/builtins.k:199 attrs=function,total

```k
  199   syntax Bool ::= evHead47(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:200

```k
  200   rule evHead47(iCons(47, _:IntSeq)) => true
```

### RULE reference-semantics/semantics/builtins.k:201 attrs=owise

```k
  201   rule evHead47(_:IntSeq)            => false [owise]
```

### SYNTAX reference-semantics/semantics/builtins.k:203 attrs=function,total

```k
  203   syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:204

```k
  204   rule tokOps(.IntSeq)                 => .OpSeq
```

### RULE reference-semantics/semantics/builtins.k:205

```k
  205   rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### RULE reference-semantics/semantics/builtins.k:206

```k
  206   rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### RULE reference-semantics/semantics/builtins.k:207

```k
  207   rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### RULE reference-semantics/semantics/builtins.k:208

```k
  208   rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### RULE reference-semantics/semantics/builtins.k:209

```k
  209   rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### RULE reference-semantics/semantics/builtins.k:210

```k
  210   rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### RULE reference-semantics/semantics/builtins.k:211

```k
  211   rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### RULE reference-semantics/semantics/builtins.k:212

```k
  212   rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### SYNTAX reference-semantics/semantics/builtins.k:214 attrs=function,total

```k
  214   syntax IntSeq ::= tokNds(IntSeq) [function, total]
  215                   | tokNdAcc(Int, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:216

```k
  216   rule tokNds(.IntSeq)                => .IntSeq
```

### RULE reference-semantics/semantics/builtins.k:217

```k
  217   rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### RULE reference-semantics/semantics/builtins.k:218

```k
  218   rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### RULE reference-semantics/semantics/builtins.k:219

```k
  219   rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
  220        requires notBool evDigit(C) andBool C =/=Int 32
```

### RULE reference-semantics/semantics/builtins.k:221

```k
  221   rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
  222        requires evDigit(C)
```

### RULE reference-semantics/semantics/builtins.k:223 attrs=owise

```k
  223   rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### SYNTAX reference-semantics/semantics/builtins.k:225

```k
  225   syntax EvPair ::= evp(OpSeq, IntSeq)
```

### SYNTAX reference-semantics/semantics/builtins.k:226 attrs=function,total

```k
  226   syntax Int ::= firstNdE(EvPair) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:227

```k
  227   rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### RULE reference-semantics/semantics/builtins.k:228 attrs=owise

```k
  228   rule firstNdE(_:EvPair) => 0 [owise]
```

### SYNTAX reference-semantics/semantics/builtins.k:230 attrs=function,total

```k
  230   syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:231

```k
  231   rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### RULE reference-semantics/semantics/builtins.k:232

```k
  232   rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### RULE reference-semantics/semantics/builtins.k:233

```k
  233   rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### RULE reference-semantics/semantics/builtins.k:234

```k
  234   rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### RULE reference-semantics/semantics/builtins.k:235

```k
  235   rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### RULE reference-semantics/semantics/builtins.k:236 attrs=owise

```k
  236   rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### SYNTAX reference-semantics/semantics/builtins.k:238 attrs=function,total

```k
  238   syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:239

```k
  239   rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### RULE reference-semantics/semantics/builtins.k:240

```k
  240   rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### RULE reference-semantics/semantics/builtins.k:241

```k
  241   rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
  242        requires O =/=String "**"
```

### RULE reference-semantics/semantics/builtins.k:243 attrs=owise

```k
  243   rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### SYNTAX reference-semantics/semantics/builtins.k:244 attrs=function,total

```k
  244   syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:245

```k
  245   rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### RULE reference-semantics/semantics/builtins.k:246

```k
  246   rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### SYNTAX reference-semantics/semantics/builtins.k:247 attrs=function,total

```k
  247   syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:248

```k
  248   rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### SYNTAX reference-semantics/semantics/builtins.k:250 attrs=function,total

```k
  250   syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:251

```k
  251   rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### RULE reference-semantics/semantics/builtins.k:252

```k
  252   rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### RULE reference-semantics/semantics/builtins.k:253

```k
  253   rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### RULE reference-semantics/semantics/builtins.k:254

```k
  254   rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### SYNTAX reference-semantics/semantics/builtins.k:255 attrs=function,total

```k
  255   syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:256

```k
  256   rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### RULE reference-semantics/semantics/builtins.k:257

```k
  257   rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
  258     => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
  259        requires inLevelE(L, O)
```

### RULE reference-semantics/semantics/builtins.k:260

```k
  260   rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
  261     => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
  262        requires notBool inLevelE(L, O)
```

### RULE reference-semantics/semantics/builtins.k:263 attrs=owise

```k
  263   rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
  264     => evp(OO, appendIE(ON, CUR)) [owise]
```

### SYNTAX reference-semantics/semantics/builtins.k:265 attrs=function,total

```k
  265   syntax Bool ::= inLevelE(String, String) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:266

```k
  266   rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### RULE reference-semantics/semantics/builtins.k:267

```k
  267   rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### RULE reference-semantics/semantics/builtins.k:268 attrs=owise

```k
  268   rule inLevelE(_:String, _:String) => false [owise]
```

### SYNTAX reference-semantics/semantics/builtins.k:269 attrs=function,total

```k
  269   syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:270

```k
  270   rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### RULE reference-semantics/semantics/builtins.k:271

```k
  271   rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### SYNTAX reference-semantics/semantics/builtins.k:272 attrs=function,total

```k
  272   syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### RULE reference-semantics/semantics/builtins.k:273

```k
  273   rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### RULE reference-semantics/semantics/builtins.k:274

```k
  274   rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

### SYNTAX reference-semantics/semantics/builtins.k:279

```k
  279   syntax KItem ::= "#md5"
```

### RULE reference-semantics/semantics/builtins.k:280 attrs=priority

```k
  280   rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
  281        [priority(40)]
```

### RULE reference-semantics/semantics/builtins.k:282

```k
  282   rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### SYNTAX reference-semantics/semantics/builtins.k:283

```k
  283   syntax Val ::= md5Obj(IntSeq)
```

### RULE reference-semantics/semantics/builtins.k:284

```k
  284   rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### SYNTAX reference-semantics/semantics/builtins.k:285 attrs=function,total,symbol,no-evaluators

```k
  285   syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

### RULE reference-semantics/semantics/builtins.k:291

```k
  291   rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### RULE reference-semantics/semantics/builtins.k:292

```k
  292   rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### SYNTAX reference-semantics/semantics/builtins.k:293 attrs=function

```k
  293   syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### RULE reference-semantics/semantics/builtins.k:294

```k
  294   rule isIntV(_:Int)         => true
```

### RULE reference-semantics/semantics/builtins.k:295 attrs=owise

```k
  295   rule isIntV(_:Val)         => false [owise]
```

### RULE reference-semantics/semantics/builtins.k:296

```k
  296   rule isStrV(str(_:IntSeq)) => true
```

### RULE reference-semantics/semantics/builtins.k:297 attrs=owise

```k
  297   rule isStrV(_:Val)         => false [owise]
  298 endmodule
```

## reference-semantics/semantics/call.k
Declaration anchors: 24

### RULE reference-semantics/semantics/call.k:16

```k
   16   rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

### SYNTAX reference-semantics/semantics/call.k:19

```k
   19   syntax KItem ::= #callee(Exprs)
```

### RULE reference-semantics/semantics/call.k:20 attrs=owise

```k
   20   rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### RULE reference-semantics/semantics/call.k:21

```k
   21   rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

### RULE reference-semantics/semantics/call.k:24

```k
   24   rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### RULE reference-semantics/semantics/call.k:26

```k
   26   rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### RULE reference-semantics/semantics/call.k:27

```k
   27   rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### RULE reference-semantics/semantics/call.k:28

```k
   28   rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### RULE reference-semantics/semantics/call.k:29

```k
   29   rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### RULE reference-semantics/semantics/call.k:30

```k
   30   rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### RULE reference-semantics/semantics/call.k:31 attrs=owise

```k
   31   rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### RULE reference-semantics/semantics/call.k:32

```k
   32   rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

### RULE reference-semantics/semantics/call.k:38 attrs=priority

```k
   38   rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
   39         => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
   40        <heap> ... H |-> V:Val ... </heap>
   41        [priority(40)]
```

### RULE reference-semantics/semantics/call.k:42 attrs=priority

```k
   42   rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
   43         => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
   44        <heap> ... H |-> V:Val ... </heap>
   45        requires notBool isRefV(A)
   46        [priority(40)]
```

### RULE reference-semantics/semantics/call.k:47 attrs=priority

```k
   47   rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
   48         => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
   49        <heap> ... H |-> V:Val ... </heap>
   50        [priority(40)]
```

### SYNTAX reference-semantics/semantics/call.k:52 attrs=function,total

```k
   52   syntax Bool ::= isMutMethod(String) [function, total]
```

### RULE reference-semantics/semantics/call.k:53

```k
   53   rule isMutMethod(M:String)
   54     => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
   55        orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### RULE reference-semantics/semantics/call.k:56 attrs=priority

```k
   56   rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
   57         => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
   58        <heap> ... H |-> V:Val ... </heap>
   59        requires notBool isMutMethod(M)
   60        [priority(40)]
```

### RULE reference-semantics/semantics/call.k:63 attrs=priority

```k
   63   rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
   64         => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
   65        <heap> ... H |-> V:Val ... </heap>
   66        requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
   67        [priority(40)]
```

### RULE reference-semantics/semantics/call.k:69

```k
   69   rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
   70         => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
   71        <env>     CALLERL:Int => NEWL </env>
   72        <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
   73        <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
   74        <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### RULE reference-semantics/semantics/call.k:80

```k
   80   rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
   81         => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
   82        <env>     CALLERL:Int => NEWL </env>
   83        <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
   84        <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
   85        <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### SYNTAX reference-semantics/semantics/call.k:87

```k
   87   syntax KItem ::= #allocCells(ParamNames)
```

### RULE reference-semantics/semantics/call.k:88

```k
   88   rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### RULE reference-semantics/semantics/call.k:89

```k
   89   rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
   90        <env> L:Int </env>
   91        <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
   92        <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
   93        <heapLoc> N:Int => N +Int 1 </heapLoc>
   94        requires notBool N in_keys(H)
   95 endmodule
```

## reference-semantics/semantics/comprehension.k
Declaration anchors: 10

### RULE reference-semantics/semantics/comprehension.k:11

```k
   11   rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### RULE reference-semantics/semantics/comprehension.k:12

```k
   12   rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### SYNTAX reference-semantics/semantics/comprehension.k:14 attrs=macro

```k
   14   syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### RULE reference-semantics/semantics/comprehension.k:15

```k
   15   rule compBody(Gs:CompFors, ELT:Expr)
   16     => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### SYNTAX reference-semantics/semantics/comprehension.k:18 attrs=macro

```k
   18   syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### RULE reference-semantics/semantics/comprehension.k:19

```k
   19   rule compNest(.CompFors, ELT:Expr)
   20     => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### RULE reference-semantics/semantics/comprehension.k:21

```k
   21   rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
   22     => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### SYNTAX reference-semantics/semantics/comprehension.k:24 attrs=macro

```k
   24   syntax Expr ::= compGuard(Exprs) [macro]
```

### RULE reference-semantics/semantics/comprehension.k:25

```k
   25   rule compGuard(.Exprs)             => Bool(true)
```

### RULE reference-semantics/semantics/comprehension.k:26

```k
   26   rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
   27 endmodule
```

## reference-semantics/semantics/concrete.k
Declaration anchors: 21

### RULE reference-semantics/semantics/concrete.k:13

```k
   13   rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
   14        <heap> HP:Map </heap>
   15        requires hasRefVS(A) orBool hasRefVS(B)
```

### RULE reference-semantics/semantics/concrete.k:16

```k
   16   rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
   17        <heap> HP:Map </heap>
   18        requires hasRefVS(A) orBool hasRefVS(B)
```

### SYNTAX reference-semantics/semantics/concrete.k:25

```k
   25   syntax Val ::= kvP(Val, Val)
```

### SYNTAX reference-semantics/semantics/concrete.k:26

```k
   26   syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
   27                  | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### RULE reference-semantics/semantics/concrete.k:28 attrs=priority

```k
   28   rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
   29         => #ksort(VS, KV, .ValSeq, false) ... </k>
   30        [priority(40)]
```

### RULE reference-semantics/semantics/concrete.k:31 attrs=priority

```k
   31   rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
   32         => #ksort(VS, KV, .ValSeq, RB) ... </k>
   33        [priority(40)]
```

### RULE reference-semantics/semantics/concrete.k:34

```k
   34   rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
   35         => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### RULE reference-semantics/semantics/concrete.k:36

```k
   36   rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
   37         => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### RULE reference-semantics/semantics/concrete.k:38

```k
   38   rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
   39         => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
   40        requires notBool isKwV(K)
```

### SYNTAX reference-semantics/semantics/concrete.k:42 attrs=function

```k
   42   syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### RULE reference-semantics/semantics/concrete.k:43

```k
   43   rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### RULE reference-semantics/semantics/concrete.k:44

```k
   44   rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
   45     => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
   46        requires kLt(K, K2)
```

### RULE reference-semantics/semantics/concrete.k:47

```k
   47   rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
   48     => vCons(kvP(K2, V2), insPair(R, K, V))
   49        requires notBool kLt(K, K2)
```

### SYNTAX reference-semantics/semantics/concrete.k:51 attrs=function

```k
   51   syntax Bool ::= kLt(Val, Val) [function]
```

### RULE reference-semantics/semantics/concrete.k:52

```k
   52   rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### RULE reference-semantics/semantics/concrete.k:53

```k
   53   rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### RULE reference-semantics/semantics/concrete.k:54

```k
   54   rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### SYNTAX reference-semantics/semantics/concrete.k:56 attrs=function,total

```k
   56   syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### RULE reference-semantics/semantics/concrete.k:57

```k
   57   rule unpairVS(.ValSeq) => .ValSeq
```

### RULE reference-semantics/semantics/concrete.k:58

```k
   58   rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### RULE reference-semantics/semantics/concrete.k:59 attrs=owise

```k
   59   rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
   60 endmodule
```

## reference-semantics/semantics/controls.k
Declaration anchors: 37

### RULE reference-semantics/semantics/controls.k:9

```k
    9   rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
   10        <env> L:Int </env>
   11        <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### RULE reference-semantics/semantics/controls.k:12 attrs=priority

```k
   12   rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
   13        <env> L:Int </env>
   14        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
   15        requires "$cells" in_keys(M)
   16         andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
   17         andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
   18        [priority(40)]
```

### RULE reference-semantics/semantics/controls.k:20

```k
   20   rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
   21        <env> L:Int </env>
   22        <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
   23        requires X in_keys(M)
```

### RULE reference-semantics/semantics/controls.k:27 attrs=priority

```k
   27   rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
   28        <env> L:Int </env>
   29        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
   30        requires X in_keys(M) andBool isRefV({M[X]}:>Val)
   31        [priority(40)]
```

### RULE reference-semantics/semantics/controls.k:35

```k
   35   rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### RULE reference-semantics/semantics/controls.k:36 attrs=owise

```k
   36   rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### SYNTAX reference-semantics/semantics/controls.k:37

```k
   37   syntax KItem ::= #bindImports(ParamNames)
```

### RULE reference-semantics/semantics/controls.k:38

```k
   38   rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### RULE reference-semantics/semantics/controls.k:39

```k
   39   rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
   40        <env> L:Int </env>
   41        <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
   42        requires N ==String "floor" orBool N ==String "ceil"
```

### RULE reference-semantics/semantics/controls.k:43

```k
   43   rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
   44        requires notBool (N ==String "floor" orBool N ==String "ceil")
```

### RULE reference-semantics/semantics/controls.k:48

```k
   48   rule <k> Expr(_:Val) => .K ... </k>
```

### SYNTAX reference-semantics/semantics/controls.k:51

```k
   51   syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### RULE reference-semantics/semantics/controls.k:52

```k
   52   rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### RULE reference-semantics/semantics/controls.k:53

```k
   53   rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### RULE reference-semantics/semantics/controls.k:54

```k
   54   rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

### RULE reference-semantics/semantics/controls.k:57

```k
   57   rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
   58        requires truthy(V)
```

### RULE reference-semantics/semantics/controls.k:59

```k
   59   rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
   60        requires notBool truthy(V)
```

### SYNTAX reference-semantics/semantics/controls.k:65

```k
   65   syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
   66                  | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
   67                  | #loopLbl(K) | "#cont" | "#brk"
```

### RULE reference-semantics/semantics/controls.k:69

```k
   69   rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### RULE reference-semantics/semantics/controls.k:71

```k
   71   rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### RULE reference-semantics/semantics/controls.k:72

```k
   72   rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### RULE reference-semantics/semantics/controls.k:73

```k
   73   rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
   74         => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

### RULE reference-semantics/semantics/controls.k:77

```k
   77   rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### RULE reference-semantics/semantics/controls.k:78

```k
   78   rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### RULE reference-semantics/semantics/controls.k:79

```k
   79   rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
   80        requires truthy(V)
```

### RULE reference-semantics/semantics/controls.k:81

```k
   81   rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
   82        requires notBool truthy(V)
```

### RULE reference-semantics/semantics/controls.k:85

```k
   85   rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### RULE reference-semantics/semantics/controls.k:86

```k
   86   rule <k> Continue => #cont ... </k>
```

### RULE reference-semantics/semantics/controls.k:87

```k
   87   rule <k> Break => #brk ... </k>
```

### RULE reference-semantics/semantics/controls.k:88

```k
   88   rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### RULE reference-semantics/semantics/controls.k:89 attrs=owise

```k
   89   rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### RULE reference-semantics/semantics/controls.k:90

```k
   90   rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### RULE reference-semantics/semantics/controls.k:91 attrs=owise

```k
   91   rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

### RULE reference-semantics/semantics/controls.k:95 attrs=priority

```k
   95   rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
   96        <heap> ... H |-> V:Val ... </heap>
   97        [priority(40)]
```

### RULE reference-semantics/semantics/controls.k:98 attrs=priority

```k
   98   rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
   99        <heap> ... H |-> V:Val ... </heap>
  100        [priority(40)]
```

### RULE reference-semantics/semantics/controls.k:101 attrs=priority

```k
  101   rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
  102        <heap> ... H |-> V:Val ... </heap>
  103        [priority(40)]
```

### RULE reference-semantics/semantics/controls.k:106 attrs=priority

```k
  106   rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
  107        <heap> ... H |-> V:Val ... </heap>
  108        [priority(40)]
  109 endmodule
```

## reference-semantics/semantics/core.k
Declaration anchors: 84

### SYNTAX reference-semantics/semantics/core.k:13

```k
   13   syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### SYNTAX reference-semantics/semantics/core.k:14

```k
   14   syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### SYNTAX reference-semantics/semantics/core.k:15

```k
   15   syntax Str    ::= str(IntSeq)
```

### SYNTAX reference-semantics/semantics/core.k:18

```k
   18   syntax Iterable ::= list(ValSeq)
   19                     | tuple(ValSeq)
   20                     | Str
   21                     | rangeObj(Int, Int, Int)
   22                     | zipObj(ValSeq, ValSeq)
   23                     | zipObjS(IntSeq, IntSeq)
```

### SYNTAX reference-semantics/semantics/core.k:25

```k
   25   syntax Val      ::= Int
   26                     | Bool
   27                     | "noneV"
   28                     | Iterable
   29                     | ref(Int)          // a heap object: <heap> holds its list(VS)
   30                     | cellRef(Int)      // a closure cell: <heap> holds cellV(V)
   31                     | closureVal(ParamNames, Stmts, Int)
   32                     | typeV(String)     // a type object (int/str), resolved from the builtins frame
   33                     | builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough)
   34                     | boundMethodV(Val, String)   // a cooled Attribute: obj.method
```

### SYNTAX reference-semantics/semantics/core.k:36

```k
   36   syntax Parent   ::= "root" | parent(Int)
```

### SYNTAX reference-semantics/semantics/core.k:37

```k
   37   syntax Scope    ::= scope(Map, Parent)
```

### SYNTAX reference-semantics/semantics/core.k:38

```k
   38   syntax KResult  ::= Val
```

### SYNTAX reference-semantics/semantics/core.k:39

```k
   39   syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### SYNTAX reference-semantics/semantics/core.k:40

```k
   40   syntax Vals     ::= List{Val, ","}
```

### SYNTAX reference-semantics/semantics/core.k:41

```k
   41   syntax Exc      ::= "NoExc" | "AssertionError"
```

### SYNTAX reference-semantics/semantics/core.k:42

```k
   42   syntax RetState ::= "noRet" | retV(Val)
```

### CONFIGURATION reference-semantics/semantics/core.k:49

```k
   49   configuration
   50     <k>       #loadAll($PGM:Module) </k>
   51     <env>     0 </env>
   52     <scopes>   0     |-> scope(.Map, parent(-1))
   53               -1    |-> builtinsScope </scopes>
   54     <scopeLoc> 1 </scopeLoc>
   55     <heap>    .Map </heap>
   56     <heapLoc> 0 </heapLoc>
   57     <stack>   .List </stack>
   58     <ret>     noRet </ret>
   59     <exc>     NoExc </exc>
   60     <exit-code exit=""> 0 </exit-code>
```

### SYNTAX reference-semantics/semantics/core.k:68 attrs=function,total

```k
   68   syntax Bool ::= isRefV(Val) [function, total]
```

### RULE reference-semantics/semantics/core.k:69

```k
   69   rule isRefV(ref(_:Int)) => true
```

### RULE reference-semantics/semantics/core.k:70 attrs=owise

```k
   70   rule isRefV(_:Val)      => false [owise]
```

### SYNTAX reference-semantics/semantics/core.k:75

```k
   75   syntax HeapVal ::= cellV(Val)
```

### SYNTAX reference-semantics/semantics/core.k:76 attrs=function,total

```k
   76   syntax Bool ::= isCellRef(Val) [function, total]
```

### RULE reference-semantics/semantics/core.k:77

```k
   77   rule isCellRef(cellRef(_:Int)) => true
```

### RULE reference-semantics/semantics/core.k:78 attrs=owise

```k
   78   rule isCellRef(_:Val)          => false [owise]
```

### RULE reference-semantics/semantics/core.k:85 attrs=priority

```k
   85   rule <k> cellRef(H:Int) => V ... </k>
   86        <env> L:Int </env>
   87        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
   88        <heap> ... H |-> cellV(V:Val) ... </heap>
   89        requires "$cells" in_keys(M)
   90        [priority(40)]
```

### SYNTAX reference-semantics/semantics/core.k:95

```k
   95   syntax Val ::= kwV(String, Val)
```

### SYNTAX reference-semantics/semantics/core.k:96

```k
   96   syntax KItem ::= #kwTag(String)
```

### RULE reference-semantics/semantics/core.k:97

```k
   97   rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### RULE reference-semantics/semantics/core.k:98

```k
   98   rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
   99        requires notBool isKwV(V)
```

### SYNTAX reference-semantics/semantics/core.k:100 attrs=function,total

```k
  100   syntax Bool ::= isKwV(Val) [function, total]
```

### RULE reference-semantics/semantics/core.k:101

```k
  101   rule isKwV(kwV(_:String, _:Val)) => true
```

### RULE reference-semantics/semantics/core.k:102 attrs=owise

```k
  102   rule isKwV(_:Val)                => false [owise]
```

### SYNTAX reference-semantics/semantics/core.k:106

```k
  106   syntax Val ::= cellsMark(ParamNames)
```

### SYNTAX reference-semantics/semantics/core.k:107 attrs=function

```k
  107   syntax ParamNames ::= cellsOf(Val) [function]
```

### RULE reference-semantics/semantics/core.k:108

```k
  108   rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### SYNTAX reference-semantics/semantics/core.k:109 attrs=function,total

```k
  109   syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### RULE reference-semantics/semantics/core.k:110

```k
  110   rule pnMember(_:String, .ParamNames) => false
```

### RULE reference-semantics/semantics/core.k:111

```k
  111   rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### SYNTAX reference-semantics/semantics/core.k:113

```k
  113   syntax KItem ::= #cellW(Val, Val)
```

### RULE reference-semantics/semantics/core.k:114

```k
  114   rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
  115        <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### SYNTAX reference-semantics/semantics/core.k:117

```k
  117   syntax KItem ::= #alloc(Val)
```

### RULE reference-semantics/semantics/core.k:118

```k
  118   rule <k> #alloc(V:Val) => ref(N) ... </k>
  119        <heap>    H:Map => (N |-> V) H </heap>
  120        <heapLoc> N:Int => N +Int 1 </heapLoc>
  121        requires notBool N in_keys(H)
```

### SYNTAX reference-semantics/semantics/core.k:124

```k
  124   syntax KItem ::= #loadAll(Module)
```

### RULE reference-semantics/semantics/core.k:125

```k
  125   rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### RULE reference-semantics/semantics/core.k:126

```k
  126   rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### RULE reference-semantics/semantics/core.k:127

```k
  127   rule <k> .Stmts => .K ... </k>
```

### SYNTAX reference-semantics/semantics/core.k:130

```k
  130   syntax KItem ::= #look(String, Int)
```

### RULE reference-semantics/semantics/core.k:131

```k
  131   rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### RULE reference-semantics/semantics/core.k:132

```k
  132   rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
  133        <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
  134        requires X in_keys(M)
```

### RULE reference-semantics/semantics/core.k:145 attrs=priority

```k
  145   rule <k> #look(X:String, L:Int) => V ... </k>
  146        <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
  147        <heap> ... H |-> cellV(V:Val) ... </heap>
  148        requires X in_keys(M) andBool "$cells" in_keys(M)
  149         andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
  150         andBool {M[X]}:>Val ==K cellRef(H)
  151        [priority(40)]
```

### RULE reference-semantics/semantics/core.k:152

```k
  152   rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
  153        <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
  154        requires notBool (X in_keys(M))
```

### SYNTAX reference-semantics/semantics/core.k:157 attrs=function,total

```k
  157   syntax Scope ::= "builtinsScope" [function, total]
```

### RULE reference-semantics/semantics/core.k:158

```k
  158   rule builtinsScope
  159     => scope(.Map [ "len"    <- builtinV("len")    ]
  160                   [ "set"    <- builtinV("set")    ]
  161                   [ "sum"    <- builtinV("sum")    ]
  162                   [ "abs"    <- builtinV("abs")    ]
  163                   [ "min"    <- builtinV("min")    ]
  164                   [ "max"    <- builtinV("max")    ]
  165                   [ "ord"    <- builtinV("ord")    ]
  166                   [ "chr"    <- builtinV("chr")    ]
  167                   [ "range"  <- builtinV("range")  ]
  168                   [ "all"    <- builtinV("all")    ]
  169                   [ "any"    <- builtinV("any")    ]
  170                   [ "zip"    <- builtinV("zip")    ]
  171                   [ "isinstance" <- builtinV("isinstance") ]
  172                   [ "sorted" <- builtinV("sorted") ]
  173                   [ "list"   <- builtinV("list")   ]
  174                   [ "round"  <- builtinV("round")  ]
  175                   [ "bin"    <- builtinV("bin")    ]
  176                   [ "enumerate" <- builtinV("enumerate") ]
  177                   [ "map"    <- builtinV("map")    ]
  178                   [ "eval"   <- builtinV("eval")   ]
  179                   [ "int"    <- typeV("int")       ]
  180                   [ "str"    <- typeV("str")       ]
  181                   [ "float"  <- typeV("float")     ], root)
```

### SYNTAX reference-semantics/semantics/core.k:185

```k
  185   syntax ApplyK ::= toCall(Val)
```

### SYNTAX reference-semantics/semantics/core.k:186

```k
  186   syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
  187                   | #evalArgCont(Exprs, Vals, ApplyK)
  188                   | #applyK(ApplyK, Vals)
```

### RULE reference-semantics/semantics/core.k:189

```k
  189   rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### RULE reference-semantics/semantics/core.k:190

```k
  190   rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### RULE reference-semantics/semantics/core.k:191

```k
  191   rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

### RULE reference-semantics/semantics/core.k:194

```k
  194   rule <k> Int(I:Int)   => I ... </k>
```

### RULE reference-semantics/semantics/core.k:195

```k
  195   rule <k> Bool(B:Bool) => B ... </k>
```

### RULE reference-semantics/semantics/core.k:196

```k
  196   rule <k> NoneVal      => noneV ... </k>
```

### SYNTAX reference-semantics/semantics/core.k:199 attrs=function

```k
  199   syntax Bool ::= truthy(Val) [function]
```

### RULE reference-semantics/semantics/core.k:200

```k
  200   rule truthy(B:Bool)          => B
```

### RULE reference-semantics/semantics/core.k:201

```k
  201   rule truthy(noneV)           => false
```

### RULE reference-semantics/semantics/core.k:202

```k
  202   rule truthy(I:Int)           => I =/=Int 0
```

### RULE reference-semantics/semantics/core.k:203

```k
  203   rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### RULE reference-semantics/semantics/core.k:204

```k
  204   rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### RULE reference-semantics/semantics/core.k:205

```k
  205   rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

### SYNTAX reference-semantics/semantics/core.k:208 attrs=function

```k
  208   syntax Val  ::= applyUn(String, Val) [function]
```

### SYNTAX reference-semantics/semantics/core.k:209 attrs=function

```k
  209   syntax Val  ::= applyBin(String, Val, Val) [function]
```

### SYNTAX reference-semantics/semantics/core.k:210 attrs=function

```k
  210   syntax Bool ::= applyCmp(String, Val, Val) [function]
```

### SYNTAX reference-semantics/semantics/core.k:213 attrs=function,total

```k
  213   syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### RULE reference-semantics/semantics/core.k:214

```k
  214   rule appendVal(.Vals, V:Val)              => V , .Vals
```

### RULE reference-semantics/semantics/core.k:215

```k
  215   rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### SYNTAX reference-semantics/semantics/core.k:217 attrs=function,total

```k
  217   syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### RULE reference-semantics/semantics/core.k:218

```k
  218   rule vals2valSeq(.Vals)            => .ValSeq
```

### RULE reference-semantics/semantics/core.k:219

```k
  219   rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

### SYNTAX reference-semantics/semantics/core.k:223 attrs=function,total

```k
  223   syntax Int ::= vsLen(ValSeq) [function, total]
```

### RULE reference-semantics/semantics/core.k:224

```k
  224   rule vsLen(.ValSeq)                => 0
```

### RULE reference-semantics/semantics/core.k:225

```k
  225   rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### SYNTAX reference-semantics/semantics/core.k:227 attrs=function,total

```k
  227   syntax Int ::= isLen(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/core.k:228

```k
  228   rule isLen(.IntSeq)                => 0
```

### RULE reference-semantics/semantics/core.k:229

```k
  229   rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

### SYNTAX reference-semantics/semantics/core.k:233 attrs=function,total

```k
  233   syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### RULE reference-semantics/semantics/core.k:234

```k
  234   rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### RULE reference-semantics/semantics/core.k:235

```k
  235   rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### RULE reference-semantics/semantics/core.k:236

```k
  236   rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
  237        requires I >Int 0
```

### RULE reference-semantics/semantics/core.k:238

```k
  238   rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
  239        requires I <Int 0
  240 endmodule
```

## reference-semantics/semantics/dict.k
Declaration anchors: 40

### SYNTAX reference-semantics/semantics/dict.k:20

```k
   20   syntax Val ::= dictV(ValSeq, ValSeq)
```

### SYNTAX reference-semantics/semantics/dict.k:23

```k
   23   syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
   24                  | #dictKey(Expr, Entries, ValSeq, ValSeq)
   25                  | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### RULE reference-semantics/semantics/dict.k:26

```k
   26   rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### RULE reference-semantics/semantics/dict.k:27

```k
   27   rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### RULE reference-semantics/semantics/dict.k:28

```k
   28   rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
   29         => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### RULE reference-semantics/semantics/dict.k:30

```k
   30   rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
   31         => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### RULE reference-semantics/semantics/dict.k:32

```k
   32   rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
   33         => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

### SYNTAX reference-semantics/semantics/dict.k:37 attrs=function,total

```k
   37   syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### RULE reference-semantics/semantics/dict.k:38

```k
   38   rule dHasKey(.ValSeq, _:Val)                => false
```

### RULE reference-semantics/semantics/dict.k:39

```k
   39   rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### RULE reference-semantics/semantics/dict.k:40

```k
   40   rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

### SYNTAX reference-semantics/semantics/dict.k:43 attrs=function,total

```k
   43   syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### RULE reference-semantics/semantics/dict.k:44

```k
   44   rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### RULE reference-semantics/semantics/dict.k:45

```k
   45   rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

### SYNTAX reference-semantics/semantics/dict.k:49 attrs=function,total

```k
   49   syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### RULE reference-semantics/semantics/dict.k:50

```k
   50   rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
   51        requires A ==K K
```

### RULE reference-semantics/semantics/dict.k:52

```k
   52   rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
   53        requires notBool (A ==K K)
```

### RULE reference-semantics/semantics/dict.k:54 attrs=owise

```k
   54   rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

### RULE reference-semantics/semantics/dict.k:58 attrs=priority

```k
   58   rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
   59         => #alloc(list(KS)) ... </k>
   60        [priority(40)]
```

### RULE reference-semantics/semantics/dict.k:63

```k
   63   rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### SYNTAX reference-semantics/semantics/dict.k:64 attrs=function

```k
   64   syntax Val ::= applyIndexD(Val, Val) [function]
```

### RULE reference-semantics/semantics/dict.k:65 attrs=priority

```k
   65   rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
   66        [priority(45)]
```

### SYNTAX reference-semantics/semantics/dict.k:70 attrs=function

```k
   70   syntax Val ::= dictSet(Val, Val, Val) [function]
```

### RULE reference-semantics/semantics/dict.k:71

```k
   71   rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

### SYNTAX reference-semantics/semantics/dict.k:76

```k
   76   syntax KItem ::= #dsetK(String, Val)
```

### RULE reference-semantics/semantics/dict.k:77

```k
   77   rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### RULE reference-semantics/semantics/dict.k:78

```k
   78   rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
   79        <env> L:Int </env>
   80        <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
   81        requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### RULE reference-semantics/semantics/dict.k:82

```k
   82   rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
   83        <env> L:Int </env>
   84        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
   85        requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### SYNTAX reference-semantics/semantics/dict.k:86

```k
   86   syntax KItem ::= #dsetV(Val, Val, Val)
```

### RULE reference-semantics/semantics/dict.k:87

```k
   87   rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
   88        <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

### SYNTAX reference-semantics/semantics/dict.k:90 attrs=function,total

```k
   90   syntax Int ::= normIdxD(Int, Int) [function, total]
```

### RULE reference-semantics/semantics/dict.k:91

```k
   91   rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### RULE reference-semantics/semantics/dict.k:92

```k
   92   rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

### RULE reference-semantics/semantics/dict.k:95

```k
   95   rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
   96     => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### SYNTAX reference-semantics/semantics/dict.k:97 attrs=function

```k
   97   syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### RULE reference-semantics/semantics/dict.k:98

```k
   98   rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### RULE reference-semantics/semantics/dict.k:99

```k
   99   rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
  100     => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### SYNTAX reference-semantics/semantics/dict.k:101 attrs=function

```k
  101   syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### RULE reference-semantics/semantics/dict.k:102

```k
  102   rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### RULE reference-semantics/semantics/dict.k:103

```k
  103   rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
  104 endmodule
```

## reference-semantics/semantics/float.k
Declaration anchors: 155

### SYNTAX reference-semantics/semantics/float.k:20

```k
   20   syntax Val ::= Float
```

### RULE reference-semantics/semantics/float.k:21

```k
   21   rule <k> Float(F:Float) => F ... </k>
```

### SYNTAX reference-semantics/semantics/float.k:24 attrs=function,total,symbol,no-evaluators

```k
   24   syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:25 attrs=concrete

```k
   25   rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### RULE reference-semantics/semantics/float.k:27

```k
   27   rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

### SYNTAX reference-semantics/semantics/float.k:30 attrs=function,total,symbol,no-evaluators

```k
   30   syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:31 attrs=concrete

```k
   31   rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### RULE reference-semantics/semantics/float.k:32

```k
   32   rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

### SYNTAX reference-semantics/semantics/float.k:37 attrs=function,total,symbol,no-evaluators

```k
   37   syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:38 attrs=concrete

```k
   38   rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### RULE reference-semantics/semantics/float.k:39

```k
   39   rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

### RULE reference-semantics/semantics/float.k:43

```k
   43   rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### RULE reference-semantics/semantics/float.k:44

```k
   44   rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

### SYNTAX reference-semantics/semantics/float.k:50 attrs=function,total,symbol,no-evaluators

```k
   50   syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:51 attrs=concrete

```k
   51   rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### RULE reference-semantics/semantics/float.k:52

```k
   52   rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### SYNTAX reference-semantics/semantics/float.k:54 attrs=function,total,symbol,no-evaluators

```k
   54   syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:55 attrs=concrete

```k
   55   rule absF(F:Float) => absFloat(F) [concrete]
```

### RULE reference-semantics/semantics/float.k:56

```k
   56   rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

### RULE reference-semantics/semantics/float.k:61

```k
   61   rule <k> Import(_:String) => .K ... </k>
```

### SYNTAX reference-semantics/semantics/float.k:65

```k
   65   syntax KItem ::= "#mathCeil"
```

### RULE reference-semantics/semantics/float.k:66 attrs=priority

```k
   66   rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### RULE reference-semantics/semantics/float.k:67

```k
   67   rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

### SYNTAX reference-semantics/semantics/float.k:70

```k
   70   syntax KItem ::= "#mathFloor"
```

### RULE reference-semantics/semantics/float.k:71 attrs=priority

```k
   71   rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### RULE reference-semantics/semantics/float.k:72

```k
   72   rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### SYNTAX reference-semantics/semantics/float.k:73 attrs=function,total,symbol

```k
   73   syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### RULE reference-semantics/semantics/float.k:74 attrs=concrete

```k
   74   rule floorFI(I:Int)   => I                        [concrete]
```

### RULE reference-semantics/semantics/float.k:75 attrs=concrete

```k
   75   rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

### RULE reference-semantics/semantics/float.k:78

```k
   78   rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### RULE reference-semantics/semantics/float.k:79

```k
   79   rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

### SYNTAX reference-semantics/semantics/float.k:82

```k
   82   syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### RULE reference-semantics/semantics/float.k:83 attrs=priority

```k
   83   rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### RULE reference-semantics/semantics/float.k:84

```k
   84   rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### RULE reference-semantics/semantics/float.k:85

```k
   85   rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### SYNTAX reference-semantics/semantics/float.k:86 attrs=function,total,symbol

```k
   86   syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### RULE reference-semantics/semantics/float.k:87 attrs=concrete

```k
   87   rule toF(F:Float) => F        [concrete]
```

### RULE reference-semantics/semantics/float.k:88 attrs=concrete

```k
   88   rule toF(I:Int)   => intToF(I) [concrete]
```

### SYNTAX reference-semantics/semantics/float.k:93 attrs=function,total,symbol

```k
   93   syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### RULE reference-semantics/semantics/float.k:94 attrs=concrete

```k
   94   rule ceilF(I:Int)   => I                       [concrete]
```

### RULE reference-semantics/semantics/float.k:95 attrs=concrete

```k
   95   rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

### RULE reference-semantics/semantics/float.k:99

```k
   99   rule applyUn("-", F:Float) => 0.0 -Float F
```

### SYNTAX reference-semantics/semantics/float.k:103 attrs=function,total,symbol,no-evaluators

```k
  103   syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:104 attrs=concrete

```k
  104   rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### RULE reference-semantics/semantics/float.k:105

```k
  105   rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### SYNTAX reference-semantics/semantics/float.k:107 attrs=function,total,symbol,no-evaluators

```k
  107   syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:108 attrs=concrete

```k
  108   rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### RULE reference-semantics/semantics/float.k:109

```k
  109   rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### SYNTAX reference-semantics/semantics/float.k:111 attrs=function,total,symbol,no-evaluators

```k
  111   syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:112 attrs=concrete

```k
  112   rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### RULE reference-semantics/semantics/float.k:113

```k
  113   rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### SYNTAX reference-semantics/semantics/float.k:115 attrs=function,total,symbol,no-evaluators

```k
  115   syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:116 attrs=concrete

```k
  116   rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### RULE reference-semantics/semantics/float.k:117

```k
  117   rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### SYNTAX reference-semantics/semantics/float.k:119 attrs=function,total,symbol,no-evaluators

```k
  119   syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:120 attrs=concrete

```k
  120   rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### RULE reference-semantics/semantics/float.k:121

```k
  121   rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

### SYNTAX reference-semantics/semantics/float.k:125 attrs=function,total,symbol,no-evaluators

```k
  125   syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:126 attrs=concrete

```k
  126   rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### RULE reference-semantics/semantics/float.k:127

```k
  127   rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### RULE reference-semantics/semantics/float.k:128

```k
  128   rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### RULE reference-semantics/semantics/float.k:129

```k
  129   rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

### RULE reference-semantics/semantics/float.k:132

```k
  132   rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:133

```k
  133   rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### RULE reference-semantics/semantics/float.k:134

```k
  134   rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:135

```k
  135   rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### RULE reference-semantics/semantics/float.k:136

```k
  136   rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:137

```k
  137   rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### RULE reference-semantics/semantics/float.k:138

```k
  138   rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:139

```k
  139   rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

### SYNTAX reference-semantics/semantics/float.k:142 attrs=function,total,symbol,no-evaluators

```k
  142   syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:143 attrs=concrete

```k
  143   rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### RULE reference-semantics/semantics/float.k:144

```k
  144   rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:145

```k
  145   rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### RULE reference-semantics/semantics/float.k:146

```k
  146   rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:147

```k
  147   rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### RULE reference-semantics/semantics/float.k:148

```k
  148   rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:149

```k
  149   rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### RULE reference-semantics/semantics/float.k:150

```k
  150   rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:151

```k
  151   rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

### RULE reference-semantics/semantics/float.k:154

```k
  154   rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### RULE reference-semantics/semantics/float.k:155

```k
  155   rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

### SYNTAX reference-semantics/semantics/float.k:160 attrs=function,total,symbol,no-evaluators

```k
  160   syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:161 attrs=concrete

```k
  161   rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### RULE reference-semantics/semantics/float.k:162 attrs=concrete

```k
  162   rule decStrToF(CS:IntSeq)
  163     => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
  164        requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### SYNTAX reference-semantics/semantics/float.k:165 attrs=function

```k
  165   syntax Int ::= headIS(IntSeq) [function]
```

### RULE reference-semantics/semantics/float.k:166

```k
  166   rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### SYNTAX reference-semantics/semantics/float.k:167 attrs=function,total

```k
  167   syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### RULE reference-semantics/semantics/float.k:168

```k
  168   rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### RULE reference-semantics/semantics/float.k:169

```k
  169   rule intPartAcc(.IntSeq, A:Int) => A
```

### RULE reference-semantics/semantics/float.k:170

```k
  170   rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### RULE reference-semantics/semantics/float.k:171

```k
  171   rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
  172        requires C =/=Int 46
```

### SYNTAX reference-semantics/semantics/float.k:173 attrs=function,total

```k
  173   syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### RULE reference-semantics/semantics/float.k:174

```k
  174   rule fracPart(.IntSeq) => 0
```

### RULE reference-semantics/semantics/float.k:175

```k
  175   rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### RULE reference-semantics/semantics/float.k:176

```k
  176   rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### RULE reference-semantics/semantics/float.k:177

```k
  177   rule fracAcc(.IntSeq, A:Int) => A
```

### RULE reference-semantics/semantics/float.k:178

```k
  178   rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### SYNTAX reference-semantics/semantics/float.k:179 attrs=function,total

```k
  179   syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### RULE reference-semantics/semantics/float.k:180

```k
  180   rule fracScale(.IntSeq) => 1
```

### RULE reference-semantics/semantics/float.k:181

```k
  181   rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### RULE reference-semantics/semantics/float.k:182

```k
  182   rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### RULE reference-semantics/semantics/float.k:183

```k
  183   rule fscAcc(.IntSeq, A:Int) => A
```

### RULE reference-semantics/semantics/float.k:184

```k
  184   rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### RULE reference-semantics/semantics/float.k:185

```k
  185   rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### RULE reference-semantics/semantics/float.k:186

```k
  186   rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### RULE reference-semantics/semantics/float.k:187

```k
  187   rule applyBuiltin("float", F:Float, .Vals)        => F
```

### SYNTAX reference-semantics/semantics/float.k:190 attrs=function,total,symbol,no-evaluators

```k
  190   syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:191 attrs=concrete

```k
  191   rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### RULE reference-semantics/semantics/float.k:192

```k
  192   rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

### SYNTAX reference-semantics/semantics/float.k:195 attrs=function,total,symbol,no-evaluators

```k
  195   syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:196 attrs=concrete

```k
  196   rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### RULE reference-semantics/semantics/float.k:197

```k
  197   rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:198

```k
  198   rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### RULE reference-semantics/semantics/float.k:199

```k
  199   rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:200

```k
  200   rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### RULE reference-semantics/semantics/float.k:201

```k
  201   rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:202

```k
  202   rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### RULE reference-semantics/semantics/float.k:203

```k
  203   rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:204

```k
  204   rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### RULE reference-semantics/semantics/float.k:205

```k
  205   rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### RULE reference-semantics/semantics/float.k:206

```k
  206   rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

### SYNTAX reference-semantics/semantics/float.k:209 attrs=function,total,symbol,no-evaluators

```k
  209   syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:210 attrs=concrete

```k
  210   rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### RULE reference-semantics/semantics/float.k:211

```k
  211   rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### RULE reference-semantics/semantics/float.k:213

```k
  213   rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### RULE reference-semantics/semantics/float.k:214

```k
  214   rule applyBuiltin("float", F:Float, .Vals) => F
```

### SYNTAX reference-semantics/semantics/float.k:217 attrs=function,total,symbol,no-evaluators

```k
  217   syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:218 attrs=concrete

```k
  218   rule roundF(F:Float)
  219     => #if (F -Float floorFloat(F)) ==Float 0.5
  220        #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
  221               #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
  222        #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### SYNTAX reference-semantics/semantics/float.k:223 attrs=function,total,symbol,no-evaluators

```k
  223   syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:224 attrs=concrete

```k
  224   rule roundFN(F:Float, N:Int)
  225     => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
  226        /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### RULE reference-semantics/semantics/float.k:227

```k
  227   rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### RULE reference-semantics/semantics/float.k:228

```k
  228   rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### SYNTAX reference-semantics/semantics/float.k:230 attrs=function,total,symbol,no-evaluators

```k
  230   syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### RULE reference-semantics/semantics/float.k:231 attrs=concrete

```k
  231   rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### SYNTAX reference-semantics/semantics/float.k:232

```k
  232   syntax KItem ::= "#mathSqrt"
```

### RULE reference-semantics/semantics/float.k:233 attrs=priority

```k
  233   rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### RULE reference-semantics/semantics/float.k:234

```k
  234   rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### RULE reference-semantics/semantics/float.k:235

```k
  235   rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

### SYNTAX reference-semantics/semantics/float.k:243

```k
  243   syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### RULE reference-semantics/semantics/float.k:244

```k
  244   rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### RULE reference-semantics/semantics/float.k:245

```k
  245   rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### RULE reference-semantics/semantics/float.k:246

```k
  246   rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### RULE reference-semantics/semantics/float.k:247

```k
  247   rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
  248        requires isFloat(V)
```

### SYNTAX reference-semantics/semantics/float.k:250

```k
  250   syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### RULE reference-semantics/semantics/float.k:251

```k
  251   rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### RULE reference-semantics/semantics/float.k:252

```k
  252   rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### RULE reference-semantics/semantics/float.k:253

```k
  253   rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### RULE reference-semantics/semantics/float.k:254

```k
  254   rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
  255        requires isFloat(V)
```

### SYNTAX reference-semantics/semantics/float.k:261

```k
  261   syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### RULE reference-semantics/semantics/float.k:262

```k
  262   rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
  263         => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
  264        requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### RULE reference-semantics/semantics/float.k:265

```k
  265   rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### RULE reference-semantics/semantics/float.k:266

```k
  266   rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### RULE reference-semantics/semantics/float.k:267

```k
  267   rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
  268         => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
  269        requires isFloat(V)
```

### RULE reference-semantics/semantics/float.k:270

```k
  270   rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
  271         => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
  272        requires isInt(V) orBool isBool(V)
  273 endmodule
```

## reference-semantics/semantics/functions.k
Declaration anchors: 19

### SYNTAX reference-semantics/semantics/functions.k:8

```k
    8   syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
    9                  | #bindP(ParamNames, Vals)
   10                  | "#pop"
   11                  | "#endcall"
```

### RULE reference-semantics/semantics/functions.k:14

```k
   14   rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
   15        <env> L:Int </env>
   16        <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### SYNTAX reference-semantics/semantics/functions.k:18

```k
   18   syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### RULE reference-semantics/semantics/functions.k:19

```k
   19   rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
   20        <env> L:Int </env>
```

### SYNTAX reference-semantics/semantics/functions.k:27

```k
   27   syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

### SYNTAX reference-semantics/semantics/functions.k:31

```k
   31   syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
   32                  | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### RULE reference-semantics/semantics/functions.k:33

```k
   33   rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
   34                    FreeVars(FVS:ParamNames), BODY:Stmts)
   35         => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### RULE reference-semantics/semantics/functions.k:36

```k
   36   rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
   37                       (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
   38         => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
   39        <env> L:Int </env>
   40        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
   41        requires FV in_keys(M)
```

### RULE reference-semantics/semantics/functions.k:42

```k
   42   rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
   43                       .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
   44        <env> L:Int </env>
   45        <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### RULE reference-semantics/semantics/functions.k:47

```k
   47   rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
   48         => closureVal(PNS, Return(E) .Stmts, L) ... </k>
   49        <env> L:Int </env>
```

### RULE reference-semantics/semantics/functions.k:50

```k
   50   rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
   51                   FreeVars(FVS:ParamNames), E:Expr)
   52         => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### RULE reference-semantics/semantics/functions.k:53

```k
   53   rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
   54                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
   55         => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
   56        <env> L:Int </env>
   57        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
   58        requires FV in_keys(M)
```

### RULE reference-semantics/semantics/functions.k:59

```k
   59   rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
   60         => closureValC(PNS, CVS, BODY, CM) ... </k>
```

### RULE reference-semantics/semantics/functions.k:63

```k
   63   rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### RULE reference-semantics/semantics/functions.k:64

```k
   64   rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
   65        <env> L:Int </env>
   66        <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

### RULE reference-semantics/semantics/functions.k:68 attrs=priority

```k
   68   rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
   69         => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
   70        <env> L:Int </env>
   71        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
   72        requires "$cells" in_keys(M)
   73         andBool pnMember(P, cellsOf({M["$cells"]}:>Val))
   74         andBool P in_keys(M) andBool isCellRef({M[P]}:>Val)
   75        [priority(40)]
```

### RULE reference-semantics/semantics/functions.k:78

```k
   78   rule <k> Return(V:Val) ~> _ => #pop </k>
   79        <ret> noRet => retV(V) </ret>
```

### RULE reference-semantics/semantics/functions.k:80

```k
   80   rule <k> #endcall => #pop ... </k>
   81        <ret> noRet => retV(noneV) </ret>
```

### RULE reference-semantics/semantics/functions.k:85

```k
   85   rule <k> #pop => V ~> CONT </k>
   86        <ret>   retV(V) => noRet </ret>
   87        <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
   88        <env>   L:Int => CALLERL </env>
   89        <scopes> SC:Map => SC [ L <- undef ] </scopes>
   90        <scopeLoc> _ => SAVEDL </scopeLoc>
   91 endmodule
```

## reference-semantics/semantics/int.k
Declaration anchors: 17

### RULE reference-semantics/semantics/int.k:7

```k
    7   rule applyUn("-", I:Int) => 0 -Int I
```

### RULE reference-semantics/semantics/int.k:9

```k
    9   rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

### RULE reference-semantics/semantics/int.k:11

```k
   11   rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### RULE reference-semantics/semantics/int.k:12

```k
   12   rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### RULE reference-semantics/semantics/int.k:13

```k
   13   rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### RULE reference-semantics/semantics/int.k:14

```k
   14   rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### RULE reference-semantics/semantics/int.k:15

```k
   15   rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### RULE reference-semantics/semantics/int.k:16

```k
   16   rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### RULE reference-semantics/semantics/int.k:17

```k
   17   rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### SYNTAX reference-semantics/semantics/int.k:19 attrs=function

```k
   19   syntax Int ::= pyMod(Int, Int) [function]
```

### RULE reference-semantics/semantics/int.k:20

```k
   20   rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### RULE reference-semantics/semantics/int.k:22

```k
   22   rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### RULE reference-semantics/semantics/int.k:23

```k
   23   rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### RULE reference-semantics/semantics/int.k:24

```k
   24   rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### RULE reference-semantics/semantics/int.k:25

```k
   25   rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### RULE reference-semantics/semantics/int.k:26

```k
   26   rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### RULE reference-semantics/semantics/int.k:27

```k
   27   rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
   28 endmodule
```

## reference-semantics/semantics/iter.k
Declaration anchors: 1

### SYNTAX reference-semantics/semantics/iter.k:8

```k
    8   syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
    9 endmodule
```

## reference-semantics/semantics/list.k
Declaration anchors: 32

### RULE reference-semantics/semantics/list.k:9

```k
    9   rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### RULE reference-semantics/semantics/list.k:10

```k
   10   rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

### SYNTAX reference-semantics/semantics/list.k:13

```k
   13   syntax ApplyK ::= "toList"
```

### RULE reference-semantics/semantics/list.k:14

```k
   14   rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### RULE reference-semantics/semantics/list.k:15

```k
   15   rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

### SYNTAX reference-semantics/semantics/list.k:18 attrs=function,total

```k
   18   syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### RULE reference-semantics/semantics/list.k:19

```k
   19   rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### RULE reference-semantics/semantics/list.k:20

```k
   20   rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

### RULE reference-semantics/semantics/list.k:24 attrs=priority

```k
   24   rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
   25        [priority(45)]
```

### RULE reference-semantics/semantics/list.k:27

```k
   27   rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### RULE reference-semantics/semantics/list.k:28

```k
   28   rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

### SYNTAX reference-semantics/semantics/list.k:33 attrs=function,total

```k
   33   syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### RULE reference-semantics/semantics/list.k:34

```k
   34   rule hasRefVS(.ValSeq)                => false
```

### RULE reference-semantics/semantics/list.k:35

```k
   35   rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### SYNTAX reference-semantics/semantics/list.k:37 attrs=function

```k
   37   syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
   38                 | deepEqV(Val, Val, Map)        [function]
```

### RULE reference-semantics/semantics/list.k:39

```k
   39   rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### RULE reference-semantics/semantics/list.k:40

```k
   40   rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### RULE reference-semantics/semantics/list.k:41

```k
   41   rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### RULE reference-semantics/semantics/list.k:42

```k
   42   rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
   43     => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### RULE reference-semantics/semantics/list.k:45

```k
   45   rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
   46        requires H in_keys(HP)
```

### RULE reference-semantics/semantics/list.k:47

```k
   47   rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
   48        requires notBool isRefV(A) andBool H in_keys(HP)
```

### RULE reference-semantics/semantics/list.k:49

```k
   49   rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### RULE reference-semantics/semantics/list.k:50 attrs=owise

```k
   50   rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

### RULE reference-semantics/semantics/list.k:53 attrs=priority

```k
   53   rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
   54        <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
   55        [priority(40)]
```

### SYNTAX reference-semantics/semantics/list.k:58

```k
   58   syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### RULE reference-semantics/semantics/list.k:59

```k
   59   rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### RULE reference-semantics/semantics/list.k:60

```k
   60   rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### RULE reference-semantics/semantics/list.k:61

```k
   61   rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### RULE reference-semantics/semantics/list.k:62

```k
   62   rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### RULE reference-semantics/semantics/list.k:63

```k
   63   rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
   64        requires E ==K V
```

### RULE reference-semantics/semantics/list.k:65

```k
   65   rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
   66        requires notBool (E ==K V)
```

### RULE reference-semantics/semantics/list.k:67

```k
   67   rule <k> B:Bool ~> #notB => notBool B ... </k>
   68 endmodule
```

## reference-semantics/semantics/methods.k
Declaration anchors: 102

### SYNTAX reference-semantics/semantics/methods.k:10 attrs=function

```k
   10   syntax Val ::= applyMethod(Val, String, Vals) [function]
```

### RULE reference-semantics/semantics/methods.k:13

```k
   13   rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### RULE reference-semantics/semantics/methods.k:14

```k
   14   rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### RULE reference-semantics/semantics/methods.k:15

```k
   15   rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### RULE reference-semantics/semantics/methods.k:16

```k
   16   rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

### RULE reference-semantics/semantics/methods.k:19

```k
   19   rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### RULE reference-semantics/semantics/methods.k:20

```k
   20   rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### RULE reference-semantics/semantics/methods.k:21

```k
   21   rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

### RULE reference-semantics/semantics/methods.k:26

```k
   26   rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### SYNTAX reference-semantics/semantics/methods.k:27 attrs=function,total

```k
   27   syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### RULE reference-semantics/semantics/methods.k:28

```k
   28   rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### RULE reference-semantics/semantics/methods.k:29

```k
   29   rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### RULE reference-semantics/semantics/methods.k:30

```k
   30   rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
   31     => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

### RULE reference-semantics/semantics/methods.k:34

```k
   34   rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### SYNTAX reference-semantics/semantics/methods.k:35 attrs=function

```k
   35   syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### RULE reference-semantics/semantics/methods.k:36

```k
   36   rule cntSub(.IntSeq, _:IntSeq) => 0
```

### RULE reference-semantics/semantics/methods.k:37

```k
   37   rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
   38        requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### RULE reference-semantics/semantics/methods.k:39

```k
   39   rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
   40        requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### SYNTAX reference-semantics/semantics/methods.k:41 attrs=function,total

```k
   41   syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### RULE reference-semantics/semantics/methods.k:42

```k
   42   rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### RULE reference-semantics/semantics/methods.k:43 attrs=owise

```k
   43   rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### RULE reference-semantics/semantics/methods.k:44

```k
   44   rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

### RULE reference-semantics/semantics/methods.k:47

```k
   47   rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### SYNTAX reference-semantics/semantics/methods.k:48 attrs=function,total

```k
   48   syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/methods.k:49

```k
   49   rule trimWS(.IntSeq) => .IntSeq
```

### RULE reference-semantics/semantics/methods.k:50

```k
   50   rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### RULE reference-semantics/semantics/methods.k:51

```k
   51   rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### SYNTAX reference-semantics/semantics/methods.k:52 attrs=function,total

```k
   52   syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/methods.k:53

```k
   53   rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### RULE reference-semantics/semantics/methods.k:54

```k
   54   rule revISAcc(.IntSeq, A:IntSeq) => A
```

### RULE reference-semantics/semantics/methods.k:55

```k
   55   rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

### RULE reference-semantics/semantics/methods.k:58

```k
   58   rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

### RULE reference-semantics/semantics/methods.k:61

```k
   61   rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

### RULE reference-semantics/semantics/methods.k:64

```k
   64   rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### SYNTAX reference-semantics/semantics/methods.k:65 attrs=function,total

```k
   65   syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### RULE reference-semantics/semantics/methods.k:66

```k
   66   rule cntOccVS(.ValSeq, _:Val)                => 0
```

### RULE reference-semantics/semantics/methods.k:67

```k
   67   rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### RULE reference-semantics/semantics/methods.k:68

```k
   68   rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

### RULE reference-semantics/semantics/methods.k:72 attrs=priority

```k
   72   rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
   73         => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
   74        [priority(40)]
```

### SYNTAX reference-semantics/semantics/methods.k:75 attrs=function

```k
   75   syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### RULE reference-semantics/semantics/methods.k:76

```k
   76   rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### RULE reference-semantics/semantics/methods.k:77

```k
   77   rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
   78        requires isWSC(C)
```

### RULE reference-semantics/semantics/methods.k:79

```k
   79   rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
   80        requires notBool isWSC(C)
```

### SYNTAX reference-semantics/semantics/methods.k:82 attrs=function

```k
   82   syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### RULE reference-semantics/semantics/methods.k:83

```k
   83   rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### RULE reference-semantics/semantics/methods.k:84

```k
   84   rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### SYNTAX reference-semantics/semantics/methods.k:85 attrs=function,total

```k
   85   syntax Bool ::= isWSC(Int) [function, total]
```

### RULE reference-semantics/semantics/methods.k:86

```k
   86   rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

### RULE reference-semantics/semantics/methods.k:89 attrs=priority

```k
   89   rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
   90         => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
   91        [priority(39)]
```

### RULE reference-semantics/semantics/methods.k:94 attrs=priority

```k
   94   rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
   95         => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
   96        [priority(40)]
```

### SYNTAX reference-semantics/semantics/methods.k:97 attrs=function

```k
   97   syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### RULE reference-semantics/semantics/methods.k:98

```k
   98   rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### RULE reference-semantics/semantics/methods.k:99

```k
   99   rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
  100        requires C ==Int SEP
```

### RULE reference-semantics/semantics/methods.k:101

```k
  101   rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
  102        requires notBool (C ==Int SEP)
```

### RULE reference-semantics/semantics/methods.k:104

```k
  104   rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
  105     => str(replaceC(CS, A, B))
```

### SYNTAX reference-semantics/semantics/methods.k:106 attrs=function,total

```k
  106   syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### RULE reference-semantics/semantics/methods.k:107

```k
  107   rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### RULE reference-semantics/semantics/methods.k:108

```k
  108   rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### RULE reference-semantics/semantics/methods.k:109

```k
  109   rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

### SYNTAX reference-semantics/semantics/methods.k:112 attrs=function,total

```k
  112   syntax Bool ::= isUpperC(Int) [function, total]
```

### RULE reference-semantics/semantics/methods.k:113

```k
  113   rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### SYNTAX reference-semantics/semantics/methods.k:115 attrs=function,total

```k
  115   syntax Bool ::= isLowerC(Int) [function, total]
```

### RULE reference-semantics/semantics/methods.k:116

```k
  116   rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### SYNTAX reference-semantics/semantics/methods.k:118 attrs=function,total

```k
  118   syntax Bool ::= isAlphaC(Int) [function, total]
```

### RULE reference-semantics/semantics/methods.k:119

```k
  119   rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### SYNTAX reference-semantics/semantics/methods.k:121 attrs=function,total

```k
  121   syntax Bool ::= isDigitC(Int) [function, total]
```

### RULE reference-semantics/semantics/methods.k:122

```k
  122   rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### SYNTAX reference-semantics/semantics/methods.k:124 attrs=function,total

```k
  124   syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/methods.k:125

```k
  125   rule hasUpper(.IntSeq) => false
```

### RULE reference-semantics/semantics/methods.k:126

```k
  126   rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### SYNTAX reference-semantics/semantics/methods.k:128 attrs=function,total

```k
  128   syntax Bool ::= hasLower(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/methods.k:129

```k
  129   rule hasLower(.IntSeq) => false
```

### RULE reference-semantics/semantics/methods.k:130

```k
  130   rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### SYNTAX reference-semantics/semantics/methods.k:132 attrs=function,total

```k
  132   syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/methods.k:133

```k
  133   rule allAlpha(.IntSeq) => true
```

### RULE reference-semantics/semantics/methods.k:134

```k
  134   rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### SYNTAX reference-semantics/semantics/methods.k:136 attrs=function,total

```k
  136   syntax Bool ::= allDigit(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/methods.k:137

```k
  137   rule allDigit(.IntSeq) => true
```

### RULE reference-semantics/semantics/methods.k:138

```k
  138   rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### SYNTAX reference-semantics/semantics/methods.k:140 attrs=function,total

```k
  140   syntax Int ::= lowerC(Int) [function, total]
```

### RULE reference-semantics/semantics/methods.k:142

```k
  142   rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### RULE reference-semantics/semantics/methods.k:143 attrs=owise

```k
  143   rule lowerC(C:Int) => C         [owise]
```

### SYNTAX reference-semantics/semantics/methods.k:145 attrs=function,total

```k
  145   syntax Int ::= upperC(Int) [function, total]
```

### RULE reference-semantics/semantics/methods.k:146

```k
  146   rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### RULE reference-semantics/semantics/methods.k:147 attrs=owise

```k
  147   rule upperC(C:Int) => C         [owise]
```

### SYNTAX reference-semantics/semantics/methods.k:149 attrs=function,total

```k
  149   syntax Int ::= swapC(Int) [function, total]
```

### RULE reference-semantics/semantics/methods.k:150

```k
  150   rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### RULE reference-semantics/semantics/methods.k:151

```k
  151   rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### RULE reference-semantics/semantics/methods.k:152 attrs=owise

```k
  152   rule swapC(C:Int) => C         [owise]
```

### SYNTAX reference-semantics/semantics/methods.k:154 attrs=function,total

```k
  154   syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/methods.k:155

```k
  155   rule mapLower(.IntSeq) => .IntSeq
```

### RULE reference-semantics/semantics/methods.k:156

```k
  156   rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### SYNTAX reference-semantics/semantics/methods.k:158 attrs=function,total

```k
  158   syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/methods.k:159

```k
  159   rule mapUpper(.IntSeq) => .IntSeq
```

### RULE reference-semantics/semantics/methods.k:160

```k
  160   rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### SYNTAX reference-semantics/semantics/methods.k:162 attrs=function,total

```k
  162   syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### RULE reference-semantics/semantics/methods.k:163

```k
  163   rule mapSwap(.IntSeq) => .IntSeq
```

### RULE reference-semantics/semantics/methods.k:164

```k
  164   rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### SYNTAX reference-semantics/semantics/methods.k:166 attrs=function,total

```k
  166   syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/methods.k:167

```k
  167   rule startsWith(.IntSeq, _:IntSeq)               => true
```

### RULE reference-semantics/semantics/methods.k:168

```k
  168   rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### RULE reference-semantics/semantics/methods.k:169

```k
  169   rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
  170 endmodule
```

## reference-semantics/semantics/operators.k
Declaration anchors: 12

### RULE reference-semantics/semantics/operators.k:10

```k
   10   rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### RULE reference-semantics/semantics/operators.k:12

```k
   12   rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

### CONTEXT reference-semantics/semantics/operators.k:15

```k
   15   context Compare(HOLE, _)
```

### CONTEXT reference-semantics/semantics/operators.k:16

```k
   16   context Compare(_:Val, CmpOp(_, HOLE))
```

### RULE reference-semantics/semantics/operators.k:17 attrs=owise

```k
   17   rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### RULE reference-semantics/semantics/operators.k:19

```k
   19   rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### RULE reference-semantics/semantics/operators.k:20

```k
   20   rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

### RULE reference-semantics/semantics/operators.k:25 attrs=priority

```k
   25   rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
   26        <heap> ... H |-> V:Val ... </heap>
   27        [priority(40)]
```

### RULE reference-semantics/semantics/operators.k:28 attrs=priority

```k
   28   rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
   29        <heap> ... H |-> V:Val ... </heap>
   30        requires notBool isRefV(L)
   31        [priority(40)]
```

### RULE reference-semantics/semantics/operators.k:34 attrs=priority

```k
   34   rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
   35        <heap> ... H |-> V:Val ... </heap>
   36        requires OP =/=String "in" andBool OP =/=String "not in"
   37        [priority(40)]
```

### RULE reference-semantics/semantics/operators.k:38 attrs=priority

```k
   38   rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
   39        <heap> ... H |-> V:Val ... </heap>
   40        requires notBool isRefV(L)
   41         orBool OP ==String "in" orBool OP ==String "not in"
   42        [priority(40)]
```

### RULE reference-semantics/semantics/operators.k:44 attrs=priority

```k
   44   rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
   45        <heap> ... H |-> V:Val ... </heap>
   46        [priority(40)]
   47 endmodule
```

## reference-semantics/semantics/range.k
Declaration anchors: 8

### SYNTAX reference-semantics/semantics/range.k:9 attrs=function,total

```k
    9   syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### RULE reference-semantics/semantics/range.k:10

```k
   10   rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### SYNTAX reference-semantics/semantics/range.k:12 attrs=function

```k
   12   syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### RULE reference-semantics/semantics/range.k:13

```k
   13   rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
   14        requires ST >Int 0 andBool HI >Int LO
```

### RULE reference-semantics/semantics/range.k:15

```k
   15   rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
   16        requires ST <Int 0 andBool HI <Int LO
```

### RULE reference-semantics/semantics/range.k:17

```k
   17   rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
   18        requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### RULE reference-semantics/semantics/range.k:20

```k
   20   rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
   21         => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
   22        requires inRange(I, HI, ST)
```

### RULE reference-semantics/semantics/range.k:23

```k
   23   rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
   24        requires notBool inRange(I, HI, ST)
   25 endmodule
```

## reference-semantics/semantics/set.k
Declaration anchors: 18

### SYNTAX reference-semantics/semantics/set.k:8

```k
    8   syntax Val ::= setV(IntSeq)
```

### SYNTAX reference-semantics/semantics/set.k:11 attrs=function,total

```k
   11   syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/set.k:12

```k
   12   rule codeIn(_:Int, .IntSeq)                => false
```

### RULE reference-semantics/semantics/set.k:13

```k
   13   rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

### SYNTAX reference-semantics/semantics/set.k:16 attrs=function,total

```k
   16   syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
   17                   | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### RULE reference-semantics/semantics/set.k:18

```k
   18   rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### RULE reference-semantics/semantics/set.k:19

```k
   19   rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### RULE reference-semantics/semantics/set.k:20

```k
   20   rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
   21        requires codeIn(C, ACC)
```

### RULE reference-semantics/semantics/set.k:22

```k
   22   rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
   23        requires notBool codeIn(C, ACC)
```

### SYNTAX reference-semantics/semantics/set.k:25 attrs=function,total

```k
   25   syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### RULE reference-semantics/semantics/set.k:26

```k
   26   rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### RULE reference-semantics/semantics/set.k:27

```k
   27   rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

### SYNTAX reference-semantics/semantics/set.k:31 attrs=function,total

```k
   31   syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/set.k:32

```k
   32   rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### RULE reference-semantics/semantics/set.k:33

```k
   33   rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### SYNTAX reference-semantics/semantics/set.k:35 attrs=function,total

```k
   35   syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/set.k:36

```k
   36   rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

### RULE reference-semantics/semantics/set.k:39

```k
   39   rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
   40 endmodule
```

## reference-semantics/semantics/sort.k
Declaration anchors: 25

### SYNTAX reference-semantics/semantics/sort.k:18 attrs=function,total,symbol,no-evaluators

```k
   18   syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### SYNTAX reference-semantics/semantics/sort.k:19 attrs=function

```k
   19   syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### RULE reference-semantics/semantics/sort.k:20 attrs=concrete

```k
   20   rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### RULE reference-semantics/semantics/sort.k:21 attrs=concrete

```k
   21   rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### RULE reference-semantics/semantics/sort.k:22 attrs=concrete

```k
   22   rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### RULE reference-semantics/semantics/sort.k:23 attrs=concrete

```k
   23   rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### RULE reference-semantics/semantics/sort.k:24 attrs=concrete

```k
   24   rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

### SYNTAX reference-semantics/semantics/sort.k:26 attrs=function

```k
   26   syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### RULE reference-semantics/semantics/sort.k:27 attrs=concrete

```k
   27   rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### RULE reference-semantics/semantics/sort.k:28 attrs=concrete

```k
   28   rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### RULE reference-semantics/semantics/sort.k:29 attrs=concrete

```k
   29   rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
   30        requires strLt(A, B) orBool A ==K B [concrete]
```

### RULE reference-semantics/semantics/sort.k:31 attrs=concrete

```k
   31   rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
   32        requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

### RULE reference-semantics/semantics/sort.k:36

```k
   36   rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
   37         => #alloc(list(sortVS(VS))) ... </k>
```

### RULE reference-semantics/semantics/sort.k:40 attrs=priority

```k
   40   rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
   41        <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
   42        [priority(40)]
```

### SYNTAX reference-semantics/semantics/sort.k:49 attrs=function,total,symbol,no-evaluators

```k
   49   syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### SYNTAX reference-semantics/semantics/sort.k:51 attrs=function,total

```k
   51   syntax ValSeq ::= revVS(ValSeq) [function, total]
   52                   | revVSAcc(ValSeq, ValSeq) [function, total]
```

### RULE reference-semantics/semantics/sort.k:53

```k
   53   rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### RULE reference-semantics/semantics/sort.k:54

```k
   54   rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### RULE reference-semantics/semantics/sort.k:55

```k
   55   rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### SYNTAX reference-semantics/semantics/sort.k:57 attrs=function,total

```k
   57   syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### RULE reference-semantics/semantics/sort.k:58

```k
   58   rule condRev(S:ValSeq, false) => S
```

### RULE reference-semantics/semantics/sort.k:59

```k
   59   rule condRev(S:ValSeq, true)  => revVS(S)
```

### RULE reference-semantics/semantics/sort.k:61

```k
   61   rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
   62         => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### RULE reference-semantics/semantics/sort.k:63

```k
   63   rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
   64         => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### RULE reference-semantics/semantics/sort.k:65

```k
   65   rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
   66         => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
   67 
   68   // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
   69   // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
   70   // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
   71   // their postcondition directly as valSeqAt(sortVS(VS), …).
   72 endmodule
```

## reference-semantics/semantics/str.k
Declaration anchors: 33

### RULE reference-semantics/semantics/str.k:8

```k
    8   rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### RULE reference-semantics/semantics/str.k:9

```k
    9   rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
   10         => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

### SYNTAX reference-semantics/semantics/str.k:13 attrs=function

```k
   13   syntax IntSeq ::= strToCodes(String) [function]
```

### RULE reference-semantics/semantics/str.k:14

```k
   14   rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### RULE reference-semantics/semantics/str.k:15

```k
   15   rule strToCodes("") => .IntSeq
```

### RULE reference-semantics/semantics/str.k:16

```k
   16   rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
   17     requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

### SYNTAX reference-semantics/semantics/str.k:20 attrs=function,total

```k
   20   syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/str.k:21

```k
   21   rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### RULE reference-semantics/semantics/str.k:22

```k
   22   rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### RULE reference-semantics/semantics/str.k:24

```k
   24   rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### RULE reference-semantics/semantics/str.k:25

```k
   25   rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### RULE reference-semantics/semantics/str.k:26

```k
   26   rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

### RULE reference-semantics/semantics/str.k:29

```k
   29   rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### RULE reference-semantics/semantics/str.k:30

```k
   30   rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### SYNTAX reference-semantics/semantics/str.k:32 attrs=function,total

```k
   32   syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/str.k:33

```k
   33   rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### RULE reference-semantics/semantics/str.k:34

```k
   34   rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### RULE reference-semantics/semantics/str.k:35

```k
   35   rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### SYNTAX reference-semantics/semantics/str.k:37 attrs=function,total

```k
   37   syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/str.k:38

```k
   38   rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### RULE reference-semantics/semantics/str.k:39

```k
   39   rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### RULE reference-semantics/semantics/str.k:40

```k
   40   rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
   41        requires notBool strPrefix(P, iCons(C, Xs))
```

### SYNTAX reference-semantics/semantics/str.k:48 attrs=function,total

```k
   48   syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### RULE reference-semantics/semantics/str.k:49

```k
   49   rule strLt(.IntSeq, .IntSeq)                => false
```

### RULE reference-semantics/semantics/str.k:50

```k
   50   rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### RULE reference-semantics/semantics/str.k:51

```k
   51   rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### RULE reference-semantics/semantics/str.k:52

```k
   52   rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### RULE reference-semantics/semantics/str.k:53

```k
   53   rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### RULE reference-semantics/semantics/str.k:54

```k
   54   rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### RULE reference-semantics/semantics/str.k:56

```k
   56   rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### RULE reference-semantics/semantics/str.k:57

```k
   57   rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### RULE reference-semantics/semantics/str.k:58

```k
   58   rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### RULE reference-semantics/semantics/str.k:59

```k
   59   rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
   60 endmodule
```

## reference-semantics/semantics/subscript.k
Declaration anchors: 57

### SYNTAX reference-semantics/semantics/subscript.k:11 attrs=function,total

```k
   11   syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### RULE reference-semantics/semantics/subscript.k:12

```k
   12   rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### RULE reference-semantics/semantics/subscript.k:13

```k
   13   rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
   14        requires I >Int 0
```

### SYNTAX reference-semantics/semantics/subscript.k:16 attrs=function

```k
   16   syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### RULE reference-semantics/semantics/subscript.k:17

```k
   17   rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### RULE reference-semantics/semantics/subscript.k:18

```k
   18   rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
   19        requires I >Int 0
```

### SYNTAX reference-semantics/semantics/subscript.k:21 attrs=function,total

```k
   21   syntax Int ::= normIdx(Int, Int) [function, total]
```

### RULE reference-semantics/semantics/subscript.k:22

```k
   22   rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### RULE reference-semantics/semantics/subscript.k:23

```k
   23   rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

### CONTEXT reference-semantics/semantics/subscript.k:27

```k
   27   context Subscript(HOLE, _)
```

### CONTEXT reference-semantics/semantics/subscript.k:28

```k
   28   context Subscript(_:Val, HOLE:Expr)
```

### RULE reference-semantics/semantics/subscript.k:31 attrs=priority

```k
   31   rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
   32        <heap> ... H |-> V:Val ... </heap>
   33        [priority(40)]
```

### RULE reference-semantics/semantics/subscript.k:35

```k
   35   rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### SYNTAX reference-semantics/semantics/subscript.k:37 attrs=function

```k
   37   syntax Val ::= applyIndex(Val, Int) [function]
```

### RULE reference-semantics/semantics/subscript.k:38

```k
   38   rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### RULE reference-semantics/semantics/subscript.k:39

```k
   39   rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### RULE reference-semantics/semantics/subscript.k:40

```k
   40   rule applyIndex(str(IS:IntSeq),   I:Int)
   41     => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

### SYNTAX reference-semantics/semantics/subscript.k:44

```k
   44   syntax KItem ::= #evalB(Bound) | "#toSome"
   45                  | #slLo(Val, Bound, Bound)
   46                  | #slHi(Val, OptInt, Bound)
   47                  | #slStep(Val, OptInt, OptInt)
```

### SYNTAX reference-semantics/semantics/subscript.k:49

```k
   49   syntax OptInt ::= "noB" | someB(Int)
```

### RULE reference-semantics/semantics/subscript.k:50

```k
   50   rule <k> #evalB(NoBound)  => noB ... </k>
```

### RULE reference-semantics/semantics/subscript.k:51

```k
   51   rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### RULE reference-semantics/semantics/subscript.k:52

```k
   52   rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### RULE reference-semantics/semantics/subscript.k:54

```k
   54   rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### RULE reference-semantics/semantics/subscript.k:55

```k
   55   rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### RULE reference-semantics/semantics/subscript.k:56

```k
   56   rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

### RULE reference-semantics/semantics/subscript.k:58 attrs=priority

```k
   58   rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
   59         => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
   60        [priority(45)]
```

### RULE reference-semantics/semantics/subscript.k:61

```k
   61   rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### SYNTAX reference-semantics/semantics/subscript.k:63 attrs=function

```k
   63   syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### RULE reference-semantics/semantics/subscript.k:64

```k
   64   rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
   65     => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### RULE reference-semantics/semantics/subscript.k:66

```k
   66   rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
   67     => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### RULE reference-semantics/semantics/subscript.k:68

```k
   68   rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
   69     => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

### SYNTAX reference-semantics/semantics/subscript.k:72 attrs=function,total

```k
   72   syntax Int ::= slStep(OptInt) [function, total]
```

### RULE reference-semantics/semantics/subscript.k:73

```k
   73   rule slStep(noB)          => 1
```

### RULE reference-semantics/semantics/subscript.k:74

```k
   74   rule slStep(someB(S:Int)) => S
```

### SYNTAX reference-semantics/semantics/subscript.k:76 attrs=function

```k
   76   syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### RULE reference-semantics/semantics/subscript.k:77

```k
   77   rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
   78        requires slStep(ST) >Int 0
```

### RULE reference-semantics/semantics/subscript.k:79

```k
   79   rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
   80        requires slStep(ST) <Int 0
```

### RULE reference-semantics/semantics/subscript.k:81

```k
   81   rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### SYNTAX reference-semantics/semantics/subscript.k:83 attrs=function

```k
   83   syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### RULE reference-semantics/semantics/subscript.k:84

```k
   84   rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
   85        requires slStep(ST) >Int 0
```

### RULE reference-semantics/semantics/subscript.k:86

```k
   86   rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
   87        requires slStep(ST) <Int 0
```

### RULE reference-semantics/semantics/subscript.k:88

```k
   88   rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### SYNTAX reference-semantics/semantics/subscript.k:90 attrs=function,total

```k
   90   syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### RULE reference-semantics/semantics/subscript.k:91

```k
   91   rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
   92        requires I  <Int 0
```

### RULE reference-semantics/semantics/subscript.k:93

```k
   93   rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
   94        requires I >=Int 0
```

### SYNTAX reference-semantics/semantics/subscript.k:96 attrs=function,total

```k
   96   syntax Int ::= clampLo(Int, Int) [function, total]
```

### RULE reference-semantics/semantics/subscript.k:97

```k
   97   rule clampLo(J:Int, _STEP:Int) => J
   98        requires J >=Int 0
```

### RULE reference-semantics/semantics/subscript.k:99

```k
   99   rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
  100        requires J <Int 0
```

### SYNTAX reference-semantics/semantics/subscript.k:102 attrs=function,total

```k
  102   syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### RULE reference-semantics/semantics/subscript.k:103

```k
  103   rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
  104        requires I  <Int LEN
```

### RULE reference-semantics/semantics/subscript.k:105

```k
  105   rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
  106        requires I >=Int LEN
```

### SYNTAX reference-semantics/semantics/subscript.k:109 attrs=function

```k
  109   syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### RULE reference-semantics/semantics/subscript.k:110

```k
  110   rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
  111     => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
  112        requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### RULE reference-semantics/semantics/subscript.k:113

```k
  113   rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
  114        requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### SYNTAX reference-semantics/semantics/subscript.k:116 attrs=function

```k
  116   syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### RULE reference-semantics/semantics/subscript.k:117

```k
  117   rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
  118     => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
  119        requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### RULE reference-semantics/semantics/subscript.k:120

```k
  120   rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
  121        requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
  122 endmodule
```

## reference-semantics/semantics/syntax.k
Declaration anchors: 16

### SYNTAX reference-semantics/semantics/syntax.k:9 attrs=strict,seqstrict,macro

```k
    9   syntax Expr ::= "Int"      "(" Int ")"
   10                 | "Float"    "(" Float ")"
   11                 | "Bool"     "(" Bool ")"
   12                 | "Name"     "(" String ")"
   13                 | "Str"      "(" String ")"
   14                 | "UnaryOp"  "(" String "," Expr ")" [strict(2)]
   15                 | "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)]
   16                 | "BoolOp"    "(" String "," Exprs ")"
   17                 | "ListExpr"  "(" Exprs ")"
   18                 | "DictExpr"  "(" Entries ")"
   19                 | "ListComp"  "(" Expr "," CompFors ")" [macro]
   20                 | "GenExp"    "(" Expr "," CompFors ")" [macro]
   21                 | "TupleExpr" "(" Exprs ")"
   22                 | "Subscript" "(" Expr "," Index ")"
   23                 | "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)]
   24                 | "Lambda"    "(" Params "," Expr ")"
   25                 | "KwArg"     "(" String "," Expr ")"
   26                 | "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")"
   27                 | "NoneVal"
   28                 | "Call"      "(" Expr "," Exprs ")"
   29                 | "Attribute" "(" Expr "," String ")" [strict(1)]
   30                 | "Compare"   "(" Expr "," CmpOp ")"
```

### SYNTAX reference-semantics/semantics/syntax.k:32

```k
   32   syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### SYNTAX reference-semantics/semantics/syntax.k:33

```k
   33   syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### SYNTAX reference-semantics/semantics/syntax.k:34

```k
   34   syntax Entries  ::= List{Entry, ","}
```

### SYNTAX reference-semantics/semantics/syntax.k:35

```k
   35   syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### SYNTAX reference-semantics/semantics/syntax.k:36

```k
   36   syntax CompFors ::= List{CompFor, ""}
```

### SYNTAX reference-semantics/semantics/syntax.k:37

```k
   37   syntax Exprs    ::= List{Expr, ","}
```

### SYNTAX reference-semantics/semantics/syntax.k:38

```k
   38   syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### SYNTAX reference-semantics/semantics/syntax.k:39

```k
   39   syntax Bound    ::= Expr | "NoBound"
```

### SYNTAX reference-semantics/semantics/syntax.k:41 attrs=strict

```k
   41   syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)]
   42                 | "Import"    "(" String ")"
   43                 | "ImportFrom" "(" String "," ParamNames ")"
   44                 | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)]
   45                 | "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)]
   46                 | "While"     "(" Expr "," Stmts ")"
   47                 | "Break"
   48                 | "Continue"
   49                 | "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)]
   50                 | "Return"    "(" Expr ")" [strict]
   51                 | "Assert"    "(" Expr ")" [strict]
   52                 | "Expr"      "(" Expr ")" [strict]
   53                 | "FuncDef"   "(" String "," Params "," Stmts ")"
   54                 | "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"
```

### SYNTAX reference-semantics/semantics/syntax.k:56

```k
   56   syntax Stmts      ::= List{Stmt, ""}
```

### SYNTAX reference-semantics/semantics/syntax.k:57

```k
   57   syntax Params     ::= "Params" "(" ParamNames ")"
```

### SYNTAX reference-semantics/semantics/syntax.k:58

```k
   58   syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### SYNTAX reference-semantics/semantics/syntax.k:59

```k
   59   syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### SYNTAX reference-semantics/semantics/syntax.k:60

```k
   60   syntax ParamNames ::= List{String, ","}
```

### SYNTAX reference-semantics/semantics/syntax.k:61

```k
   61   syntax Module     ::= "Module" "(" Stmts ")"
   62 endmodule
```

## reference-semantics/semantics/tuple.k
Declaration anchors: 25

### RULE reference-semantics/semantics/tuple.k:10

```k
   10   rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### RULE reference-semantics/semantics/tuple.k:11

```k
   11   rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

### SYNTAX reference-semantics/semantics/tuple.k:14

```k
   14   syntax ApplyK ::= "toTuple"
```

### RULE reference-semantics/semantics/tuple.k:15

```k
   15   rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### RULE reference-semantics/semantics/tuple.k:16

```k
   16   rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### RULE reference-semantics/semantics/tuple.k:18

```k
   18   rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

### RULE reference-semantics/semantics/tuple.k:20

```k
   20   rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### RULE reference-semantics/semantics/tuple.k:21

```k
   21   rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

### RULE reference-semantics/semantics/tuple.k:23

```k
   23   rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### SYNTAX reference-semantics/semantics/tuple.k:24 attrs=function

```k
   24   syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### RULE reference-semantics/semantics/tuple.k:25

```k
   25   rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### RULE reference-semantics/semantics/tuple.k:26

```k
   26   rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
   27        requires notBool (A ==K V)
```

### RULE reference-semantics/semantics/tuple.k:28

```k
   28   rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

### SYNTAX reference-semantics/semantics/tuple.k:31

```k
   31   syntax KItem ::= #bindTgt(Expr, Val)
```

### RULE reference-semantics/semantics/tuple.k:32

```k
   32   rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
   33        <env> L:Int </env>
   34        <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### RULE reference-semantics/semantics/tuple.k:35 attrs=priority

```k
   35   rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
   36        <env> L:Int </env>
   37        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
   38        requires "$cells" in_keys(M)
   39         andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
   40         andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
   41        [priority(40)]
```

### RULE reference-semantics/semantics/tuple.k:42

```k
   42   rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### RULE reference-semantics/semantics/tuple.k:43

```k
   43   rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### RULE reference-semantics/semantics/tuple.k:44 attrs=priority

```k
   44   rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
   45        <heap> ... H |-> V:Val ... </heap>
   46        [priority(40)]
```

### SYNTAX reference-semantics/semantics/tuple.k:49

```k
   49   syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### RULE reference-semantics/semantics/tuple.k:50

```k
   50   rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### RULE reference-semantics/semantics/tuple.k:51

```k
   51   rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### RULE reference-semantics/semantics/tuple.k:52 attrs=priority

```k
   52   rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
   53        <heap> ... H |-> V:Val ... </heap>
   54        [priority(40)]
```

### RULE reference-semantics/semantics/tuple.k:55

```k
   55   rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
   56         => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### RULE reference-semantics/semantics/tuple.k:57

```k
   57   rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
   58 endmodule
```

## reference-semantics/semantics.k
Declaration anchors: 0

## verification.k
Declaration anchors: 9

### SYNTAX verification.k:6 attrs=function,total

```k
    6   syntax ValSeq ::= intersperseAcc(ValSeq, ValSeq, Int) [function, total]
```

### RULE verification.k:7

```k
    7   rule intersperseAcc(ACC:ValSeq, .ValSeq, _:Int) => ACC
```

### RULE verification.k:8

```k
    8   rule intersperseAcc(.ValSeq, vCons(V:Val, REST:ValSeq), D:Int)
    9     => intersperseAcc(vCons(V, .ValSeq), REST, D)
```

### RULE verification.k:10

```k
   10   rule intersperseAcc(vCons(A:Val, AS:ValSeq),
   11                       vCons(V:Val, REST:ValSeq), D:Int)
   12     => intersperseAcc(
   13          valSeqConcat(
   14            valSeqConcat(vCons(A, AS), vCons(D, .ValSeq)),
   15            vCons(V, .ValSeq)),
   16          REST,
   17          D)
```

### SYNTAX verification.k:19 attrs=function,total

```k
   19   syntax ValSeq ::= intersperseVS(ValSeq, Int) [function, total]
```

### RULE verification.k:20

```k
   20   rule intersperseVS(NUMBERS:ValSeq, D:Int)
   21     => intersperseAcc(.ValSeq, NUMBERS, D)
```

### SYNTAX verification.k:23 attrs=function,total

```k
   23   syntax Val ::= lastNumber(Val, ValSeq) [function, total]
```

### RULE verification.k:24

```k
   24   rule lastNumber(OLD:Val, .ValSeq) => OLD
```

### RULE verification.k:25

```k
   25   rule lastNumber(_:Val, vCons(V:Val, REST:ValSeq))
   26     => lastNumber(V, REST)
   27 endmodule
```

