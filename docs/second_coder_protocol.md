# Protocol for the second human coder

The second coder was a colleague who had not taken part in designing the codebook or in the first round of coding. The coder worked blind and independently: the coding file contained only a row number, the review identifier (`rid`), and the review text. App name, date, star rating, the model's label, and the first coder's label were withheld.

**Task.** Assign each of the 200 reviews to exactly one of three groups (column `kelompok`):

| Value | Use when the review… |
|---|---|
| `kebijakan` (policy grievance) | rejects or questions the obligation or the policy (coercion); **or** complains that the procedure is cumbersome, slow, or costly without naming a specific fault (burden); **or** accuses the agency of bad intent such as corruption, fraud, or profit-seeking (distrust) |
| `teknis` (technical failure) | reports that the app does not work: failed login, one-time password not received, errors, crashes, endless loading, failed registration because of the system |
| `lain` (other) | anything else: acceptance or praise, privacy concern, groups that cannot comply, exit or workaround, unclear or unrelated text |

**Priority order when a review mentions several things** (stop at the first "yes"): (1) unrelated or unreadable → `lain`; (2) rejects the obligation or policy → `kebijakan`; (3) accuses the agency of bad intent → `kebijakan`; (4) names a group that cannot comply → `lain`; (5) privacy concern → `lain`; (6) stops using or circumvents → `lain`; (7) cumbersome without a specific fault → `kebijakan`; (8) app does not work → `teknis`; (9) accepts or praises → `lain`. One-word reviews such as "ok" → `lain`.

The three groups collapse the nine-label codebook in `docs/codebook.md` (coercion + burden + distrust = policy grievance; technical failure; all other labels).
