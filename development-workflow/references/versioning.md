# Versioning and Releases

Read as needed. Follow this reference when the task requires external delivery, a release tag on the integration branch, or maintaining the project's CHANGELOG.

These conventions come from common community practices: [Semantic Versioning 2.0.0](https://semver.org/), [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/), [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), and mainstream practices in tools such as release-please, semantic-release, and changesets. The project's existing release process, versioning scheme (including CalVer), and release records take precedence over this reference.

## Choosing a Version Number

Format: `MAJOR.MINOR.PATCH`:

| Change | Version Component | Basis |
| --- | --- | --- |
| Incompatible API or behavior changes | MAJOR | Commit includes `!` or a `BREAKING CHANGE:` footer |
| Backward-compatible new features | MINOR | `feat` |
| Backward-compatible fixes or internal improvements | PATCH | `fix`, `perf`, `refactor`, `docs`, etc. |

Judge by the external contract, not the number of commits or amount of code:

- Internal refactoring, scaffolding adjustments, added tests, and documentation corrections are usually PATCH changes, even when extensive.
- Changing defaults, tightening validation, changing error codes, or removing deprecated exports can all be MAJOR changes, even if only one line changes.
- Classify security fixes by the usual rules, and describe them separately under `Security` in the CHANGELOG when needed; do not use security as a reason to avoid a MAJOR assessment.
- When releasing multiple changes together, use the highest component: any breaking change makes it MAJOR.

During the `0.y.z` stage, MINOR in `0.y.z` may include breaking changes, while PATCH should remain compatible. Whether to promote a breaking change in `0.x` to MAJOR depends on the project's documented policy; if none exists, follow this convention and clearly describe the impact in the release notes.

Use suffixes such as `-alpha.1`, `-beta.2`, or `-rc.1` for prereleases. Prereleases precede their corresponding stable versions; do not advance multiple prerelease identifiers simultaneously.

## Where Versions Are Recorded

- Language package manifests: `package.json`, `pyproject.toml`, `Cargo.toml`, `pom.xml`, and `*.gemspec`.
- Separate `VERSION`, `version.go`, or `__version__` entries.
- Version badges or references in project documentation.

Update every place that records the version number when releasing. Changing only one leaves inconsistencies, with downstream installations from the package manifest receiving a version different from the tag.

## Tag

Create an annotated tag on the integration branch:

```bash
git switch <integration-branch>
git pull --ff-only <remote> <integration-branch>
git tag -a v1.4.0 -m "v1.4.0"
git push <remote> v1.4.0
```

Rules:

- Create annotated tags with `-a`, not lightweight tags. Annotated tags include an author, date, and message; `git describe` and most release tools rely on this information.
- Follow the project's existing naming format (`v1.4.0` or `1.4.0`); do not mix formats.
- The tag points to the actual released commit on the integration branch, usually the version commit for this release.
- Do not move or overwrite pushed tags. Downstream users may already have built from them; issue a new PATCH release for corrections rather than changing an old tag.
- If a tag is incorrect and has not been pushed, simply delete and recreate it:
  ```bash
  git tag -d v1.4.0
  ```
- Use `git tag -s` when the team requires signing, and confirm that the local signing key is configured.

## CHANGELOG

Maintain it in [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format, for users rather than commit history:

```markdown
## [Unreleased]

## [1.4.0] - 2025-03-11

### Added
- Support exporting results with `--format json`

### Changed
- Change the default timeout from 30 seconds to 10 seconds

### Fixed
- Fix parsing failures caused by empty response bodies

### Security
- Upgrade a parsing dependency with known vulnerabilities
```

Key points:

- Use the categories `Added` / `Changed` / `Deprecated` / `Removed` / `Fixed` / `Security`; do not add custom categories.
- Describe user-visible changes rather than copying commit messages one by one. Squash Merge maps one PR/MR to one entry, matching this granularity.
- Use one second-level heading per release, with a date and version number, newest first.
- Keep an `Unreleased` section, recording day-to-day changes there first.
- List breaking changes separately under `Removed` / `Changed` and explain migration in the entries.
- Keep version comparison links at the bottom (if the project uses them).

## Release Steps

The full sequence for a manual release:

```bash
# 1. Confirm that the integration branch contains all changes for this release and the workspace is clean
git -C <main-worktree> switch <integration-branch>
git -C <main-worktree> pull --ff-only <remote> <integration-branch>
git -C <main-worktree> status --short

# 2. Update the version number everywhere it is recorded (package manifests, VERSION, etc.)

# 3. Move Unreleased content into a new version section and update comparison links

# 4. Commit version changes
git add CHANGELOG.md pyproject.toml
git commit -m "chore(release): 1.4.0"

# 5. Create an annotated tag
git tag -a v1.4.0 -m "v1.4.0"

# 6. Push the integration branch and tag (push the exact tag to avoid pushing unrelated tags)
git push <remote> <integration-branch>
git push <remote> v1.4.0
```

Run the project's build or packaging checks before pushing the tag. After releasing, confirm that the commit pointed to by the tag includes the version commit, and that the CHANGELOG version number, tag name, and package manifest all agree.

## Automation Options

There are three mainstream community approaches; choose based on the project's commit conventions and artifact structure:

- **release-please**: Infers the version component from Conventional Commits and generates a "release PR" containing version number and CHANGELOG changes; creates a tag and release after that PR is merged. Suitable for projects that still want human confirmation before releasing, with the most complete support for GitHub.
- **semantic-release**: Fully automates version inference, CHANGELOG generation, tagging, and publishing in CI. Suitable for projects with strict commit conventions that want no manual intervention; configuration errors directly affect release artifacts, so verify on a prerelease branch when first adopting it.
- **changesets**: Describes changes in explicit change files, then uses commands to aggregate versions and the CHANGELOG. Suitable for monorepos or multi-package repositories, with clear advantages when coordinating versions across packages.

The common prerequisite is commit messages following Conventional Commits—the direct reason this guide requires commit conventions. Before adopting automation, check how well the project's historical commits follow the conventions; otherwise, automatically generated version numbers and CHANGELOG entries will be inaccurate.

After choosing a tool, record it in project documentation and CI configuration; do not maintain two release mechanisms in parallel in the same repository.

## Relationship to the Merge Strategy

- The default Squash Merge leaves one commit per PR/MR on the integration branch, matching one CHANGELOG entry and one version decision.
- If the project switches to Rebase Merge or ordinary Merge, the integration branch accumulates intermediate development branch commits, and automatic version inference also considers commits such as `wip` and `fix typo`. In that case, either tidy commits before merging or switch to explicit change files (the changesets approach).
- After changing the merge strategy, recheck the versioning tool's source of evidence: tools that infer from commit messages rely on squash granularity.

## Common Mistakes

- Updating the version number in one place but missing the package manifest or `__version__`.
- Using lightweight tags, preventing release tools from reading tag messages.
- Moving or force-overwriting published tags.
- Listing commit messages directly in the CHANGELOG, or leaving it stale and filling it in only at release time.
- Recording breaking changes only in commits, without reflecting them in the CHANGELOG and bumping the appropriate version component.
- Tagging on the development branch before merging, leaving the tag pointing to a commit that has not reached the mainline.
- Continuing to update version numbers manually after automation takes over, causing conflicts between the tool and files.

## Official References

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [release-please](https://github.com/googleapis/release-please)
- [semantic-release](https://semantic-release.gitbook.io/semantic-release/)
- [changesets](https://github.com/changesets/changesets)
