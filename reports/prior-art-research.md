# Prior-Art Research

## Single-entry routing decision

The current package is intentionally kept as the Xiaohongshu-material specialist rather than a second general writing entry. `$lvsea-writing` is the primary user-facing router; `lvsea-xiezuo` is invoked only when the task needs keyword/angle collection, interaction gates, comment evidence, Feishu shaping, or a source-backed writing handoff. Final drafting and late Humanizer editing remain downstream.

## Search method

On 2026-08-25, `find-skills` was read first and the Skills CLI was used for three read-only queries:

- `xiaohongshu content`
- `content research writing`
- `feishu bitable`

The results were treated as discovery signals, not proof of quality. Public source trees, README/SKILL files, license metadata, stars, update date and install counts were separated.

## Shortlist and synthesis

| Candidate | Discovery signal | Keep | Adapt | Reject |
| --- | --- | --- | --- | --- |
| [autoclaw-cc/xiaohongshu-mcp-skills](https://github.com/autoclaw-cc/xiaohongshu-mcp-skills) | `xiaohongshu` 3K installs; MIT; 248 stars at research time | provider/login preflight, search then detail, source IDs/tokens from results, read-only boundary | use provider-neutral wording and local import fallback | hard requirement on one MCP, direct interaction/publishing routes |
| [redfox-data/redfox-community xiaohongshu-rewrite](https://github.com/redfox-data/redfox-community/tree/main/skills/xiaohongshu-rewrite) | `xiaohongshu-rewrite` 297 installs; 367 stars for repository | compact writing rules, local standard-library helper pattern, four concrete scenarios | replace style-only rewrite with source basis, metrics gate and evidence cards | third-party API reporting and API-key requirement inside the core workflow |
| [vivy-yi/xiaohongshu-skills](https://github.com/vivy-yi/xiaohongshu-skills) | `content-performance-analysis` 293 installs; repository 390 stars; large multi-skill tree | separate engagement data, content structure and pattern extraction; repurposing adds new value | require source-specific evidence and label inference/open questions | broad performance claims and generic ROI/case-study claims without current user data |
| [PostPlusAI/postplus-skills benchmark-to-brief](https://github.com/PostPlusAI/postplus-skills/blob/main/skills/40-creative/benchmark-to-brief/SKILL.md) | structured benchmark-to-brief contract | fact-grounded brief, narrow concept, source basis, test variable, stop conditions | apply to Xiaohongshu material cards and writing candidates | media-production-only routing and unpublished provider assumptions |
| [alextangson/feishu_skills feishu-bitable](https://github.com/alextangson/feishu_skills/blob/main/feishu-bitable/SKILL.md) | `feishu-bitable` 863 installs; MIT; 65 stars | field types, numeric/date discipline, batch and permission cautions | export-only CSV first; remote sync remains explicit adapter | shipping credentials, auto-creating tables, or silently writing remote data |

## Invented for this package

- The article-derived interaction gate with `eligible`, `local_review` and `excluded` states.
- A normalized record contract that keeps source facts, analysis fields and rights boundary together.
- A deterministic local pipeline: validate -> gate -> brief -> Feishu-compatible CSV.
- A no-provider fallback that is still runnable with user-owned JSON/CSV, while keeping real provider and human output evidence separate.

## Generalization decision

The retained mechanisms are domain-neutral behaviors: preflight the source, keep the source basis, separate fact from inference, make missing evidence visible, and stop before external writes. The article's volumes and screenshots are treated as task-specific evidence and defaults, not global performance rules.

## Incremental research: Zhiyu333 / lieflat-less-ai-tone

On 2026-09-16, the public X status [2099746344466579566](https://x.com/Zhiyu333/status/2099746344466579566) was checked. Direct X access returned HTTP 403 in the current environment, so the status metadata and linked public article were read through a read-only public mirror/API path. The article points to [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone), reviewed at commit `27d29232f10124db904ca9c0536d0b67cb3b2833` under its MIT license.

The source repository reports a 629-article, 2.826-million-character, 95,551-sentence corpus, with 300 AI texts and 329 human texts. It reports 26 candidate features, 11 retained signals and 15 unsupported general rules. These are source-reported study results, not a universal detector or a quality truth. The repository also warns about denominator choice, model variation and false positives; its operating guidance emphasizes whitelist-only edits, information conservation and auditing a sample before trusting a new operator.

| Decision | Applied to `lvsea-xiezuo` |
| --- | --- |
| `keep` | late-stage only, whitelist-style editing; preserve information and source attribution; treat statistical features as review signals |
| `adapt` | expose a writing handoff after evidence/brief generation, so `$lvsea-writing` can perform the full upstream re-check and final Humanizer stage |
| `reject` | copying the third-party Skill, corpus, scripts, thresholds or claims into this package; early “humanization” before task/structure/evidence |
| `invent` | `scripts/build_writing_handoff.py` plus an explicit field map and a trigger boundary that keeps Xiaohongshu radar separate from general writing |

The resulting architecture is intentionally two-stage: `lvsea-xiezuo` owns platform-specific material intelligence; [lvsea-writing](https://github.com/lhylvsea/lvsea-writing) owns general writing and the final editing gate. No real provider run, Feishu sync, generated article or human blind review is claimed by this research update.
