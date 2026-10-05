# Answer standard

**Audience: the teammate who picks up the case, not the requester.** An answer is a diagnosis plus the exact steps in Salesforce terms - field API names, flow names, buttons, permission sets. Precise beats thorough (owner 2026-10-04: the long eight-section format was "crammed"; the message was right, the shape was wrong).

Every answer has exactly **two sections** and stays **under 250 words** (target 120-200):

```
**Summary:** two to four sentences: what is actually wrong, the mechanism behind it (flow, rule, field, matrix), and what the data showed. Not what the requester asked.
**Suggested resolution:**
1. Ordered steps, one action each, in the imperative: the object, field, button or record to touch and the expected result.
2. Conditional branches as "If X: do Y" on their own step.
3. Last step when relevant: who to escalate to, or the one line to send the requester.
```

Three to eight steps. No other headings, no Check / Fix / Verify / Sources blocks. Mechanisms and sources are named inside the sentences ("the validation rule `Cant_Change_Send_to_bi_when_supply_deal` blocks…", "a closed case in July used the same export").

## Rules
- Never invent record IDs, amounts, dates or names. If a needed value is missing, make the step conditional or ask for it in the last step.
- Cite a record ID only if it appears in the case text or came back from a read-only lookup in this session.
- **Every case gets an answer.** An unapproved cluster, or no cluster at all, lowers the confidence; it never removes the answer. Research in the order set in `SKILL.md`. `No suggestion: …` is reserved for research that found nothing at all, and even then it lists what was checked.
- **Confidence is a whole percentage 0-100** (owner 2026-10-04), stored and shown as `85%`. Calibration:
  - 90-100: approved cluster covers the case exactly and the PROD data confirms the diagnosis.
  - 75-89: approved cluster with one assumption, or a pending cluster whose steps are confirmed by metadata, a closed case or u-know.
  - 50-74: research-built answer (no cluster, or cluster pattern only) with the mechanism found in metadata or a closed case.
  - 25-49: pattern match only; steps are the standard checklist, nothing verified for this case.
  - 0-24: nothing found; `No suggestion` fallback.
- End with `Confidence: <nn>%` and the cluster slug (or `unclustered`).

## Self-review before presenting an answer
1. Two sections, under 250 words, agent-facing, steps numbered.
2. Would the teammate know exactly which field, flow or button to touch next, and in what order?
3. Nothing asserted that the case data, a closed case, u-know or the metadata does not support.
4. The percentage matches the calibration table above.
