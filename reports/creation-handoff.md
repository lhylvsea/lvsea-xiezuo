# Creation Handoff

Version: `0.1.3`

This package is a downstream Xiaohongshu material specialist. The primary user entry for combined writing is `$lvsea-writing`; this package is called directly only for material radar, evidence cards, rewrite briefs, and writing handoffs.

## Result

- Skill: `lvsea-xiezuo` v0.1.3
- Owner: 海洋哥 / `lhylvsea`
- Job: build a source-backed Xiaohongshu material radar and derivative-writing brief workflow
- Local source: `work/lvsea-xiezuo`
- Publication: public GitHub repository; v0.1.3 makes `lvsea-writing` the single user-facing entry and narrows this package to the evidence-preserving material handoff

## Reference skills studied

- `autoclaw-cc/xiaohongshu-mcp-skills`: provider/login and read-only operation boundaries.
- `redfox-data/redfox-community` rewrite/analyzer: concise platform writing workflow; third-party API reporting intentionally excluded.
- `vivy-yi/xiaohongshu-skills`: performance dimensions and repurposing adds value; unsupported impact claims excluded.
- `PostPlusAI/postplus-skills`: evidence-backed brief and stop conditions.
- `alextangson/feishu_skills`: Bitable field and permission constraints; remote writes remain opt-in.
- [Zhiyu333 / lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone): late-stage, whitelist-style editing and information-conservation research; imported as a bounded reference, not copied as a second Skill.
- [lhylvsea/lvsea-writing](https://github.com/lhylvsea/lvsea-writing): downstream general writing route; receives the new source-backed handoff package.

## Absorbed and rejected

- `keep`: source preflight, structured fields, source basis, separate analysis, read-only default.
- `adapt`: platform-specific search/detail into provider-neutral input plus local JSON/CSV fallback; benchmark brief into Chinese Xiaohongshu writing.
- `reject`: automatic posting/commenting, hard dependency on one MCP, third-party API keys, unsupported growth claims, direct copy.
- `invent`: article-derived metric gate, local review quarantine, deterministic CSV/brief pipeline, governed evidence reports and `lvsea-xiezuo -> lvsea-writing` handoff.

## Advantages and evidence

- `design advantage`: missing metrics are quarantined instead of silently exported; supported by screenshot observation and unit tests.
- `design advantage`: a user can run the data/brief pipeline without network credentials; supported by standard-library smoke tests.
- `hypothesis`: better reviewability and less copying risk; requires real provider runs and human blind review (`missing_evidence`).

## Verification and limits

- Local package gate: PASS; 6 unit tests: PASS; trigger regression: 14/14 PASS; context budget: PASS; Skill IR regenerated with v0.1.2 outputs.
- The target-native `scripts/check_package.py` is the structural gate. The current `lvsea-zao-skill` `validate_skill.py` / `release_check.py` adapter is hard-coded to the name `lvsea-zao-skill`, so it reports a package-name mismatch for `lvsea-xiezuo`; that adapter result is not treated as a target-package failure.
- `Test-SkillInstall.ps1` in an isolated Codex home, public discovery and clean install are run after the v0.1.2 release and recorded below.
- Public release evidence for the prior baseline: [PR #1](https://github.com/lhylvsea/lvsea-xiezuo/pull/1) merged and [v0.1.0](https://github.com/lhylvsea/lvsea-xiezuo/releases/tag/v0.1.0) released; v0.1.1 was the documentation-corrected revision. v0.1.2 must be released separately.
- Real Xiaohongshu provider, real Feishu sync, human output quality and account performance are not verified in this package.
- Deliberately excluded: credentials, private data, platform bypass, automatic public posting and unreviewed third-party code execution.
