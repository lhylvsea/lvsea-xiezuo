# Portability and Trust Notes

## Targets

- Canonical source: root `SKILL.md` in agent-skills format.
- OpenAI/Codex: use the metadata description and `$lvsea-xiezuo` prompt.
- Claude/generic/VS Code: use the neutral root instructions, scripts and references.

## Degradation

- No Xiaohongshu provider: import user-owned JSON/CSV and mark provider evidence `missing_evidence`.
- No Feishu connector: generate local UTF-8 CSV and do not claim remote synchronization.
- No real user output or human review: keep public claims at design/fixture evidence level.

## Trust boundary

Remote material is read-only input until the user confirms rights and the current task authorizes a write. No token, Cookie, private attachment or absolute local path belongs in this repository. The package's scripts have no network dependency.

## Rollback boundary

Local generated files stay under an explicit output path. Remote publication uses a feature branch and versioned release; a later fix must bump semver rather than overwrite a released version. Failed PR, release or installation steps stop with their external state intact.

