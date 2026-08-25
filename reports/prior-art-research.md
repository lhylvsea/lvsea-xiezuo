# Prior-Art Research

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

