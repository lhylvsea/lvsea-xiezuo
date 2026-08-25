# Creation Handoff

## Result

- Skill: `lvsea-xiezuo` v0.1.1
- Owner: 海洋哥 / `lhylvsea`
- Job: build a source-backed Xiaohongshu material radar and derivative-writing brief workflow
- Local source: `work/lvsea-xiezuo`
- Publication: public GitHub repository and v0.1.0 release completed; v0.1.1 is the documentation-corrected revision

## Reference skills studied

- `autoclaw-cc/xiaohongshu-mcp-skills`: provider/login and read-only operation boundaries.
- `redfox-data/redfox-community` rewrite/analyzer: concise platform writing workflow; third-party API reporting intentionally excluded.
- `vivy-yi/xiaohongshu-skills`: performance dimensions and repurposing adds value; unsupported impact claims excluded.
- `PostPlusAI/postplus-skills`: evidence-backed brief and stop conditions.
- `alextangson/feishu_skills`: Bitable field and permission constraints; remote writes remain opt-in.

## Absorbed and rejected

- `keep`: source preflight, structured fields, source basis, separate analysis, read-only default.
- `adapt`: platform-specific search/detail into provider-neutral input plus local JSON/CSV fallback; benchmark brief into Chinese Xiaohongshu writing.
- `reject`: automatic posting/commenting, hard dependency on one MCP, third-party API keys, unsupported growth claims, direct copy.
- `invent`: article-derived metric gate, local review quarantine, deterministic CSV/brief pipeline and governed evidence reports.

## Advantages and evidence

- `design advantage`: missing metrics are quarantined instead of silently exported; supported by screenshot observation and unit tests.
- `design advantage`: a user can run the data/brief pipeline without network credentials; supported by standard-library smoke tests.
- `hypothesis`: better reviewability and less copying risk; requires real provider runs and human blind review (`missing_evidence`).

## Verification and limits

- Local package gate: PASS; 5 unit tests: PASS; trigger regression: 13/13 PASS; context budget: PASS.
- `Test-SkillInstall.ps1` in an isolated Codex home: PASS; `npx skills` public discovery: PASS; clean install: PASS.
- Public release evidence: [PR #1](https://github.com/lhylvsea/lvsea-xiezuo/pull/1) merged and [v0.1.0](https://github.com/lhylvsea/lvsea-xiezuo/releases/tag/v0.1.0) released. This v0.1.1 patch corrects this handoff text without overwriting the released version.
- Real Xiaohongshu provider, real Feishu sync, human output quality and account performance are not verified in this package.
- Deliberately excluded: credentials, private data, platform bypass, automatic public posting and unreviewed third-party code execution.
