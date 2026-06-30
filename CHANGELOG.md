# Changelog

All notable changes to the Modjo Sales Agent are recorded here. This project follows
[semantic versioning](https://semver.org/).

## [0.2.0] — 2026-06-30

### Added
- **Artifact system spec.** A coherent model for what the plugin produces: a 4-class artifact
  taxonomy, a shared component vocabulary defined once across three forms (interactive / static
  widget / markdown), and a content-model→two-projection parity contract. New shared refs:
  `shared/content-model.md`, `shared/native-artifact.md`.
- **Native interactive artifacts** are now the headline output, with portable Markdown as the
  always-written fallback. The Munro design system gained an interactivity layer (interaction
  states, motion, data-viz tokens). A real, working reference artifact ships at
  `shared/reference/deal-review-beauhurst.html`.
- **New skill: `handle-the-objection`** (`/handle-objection`). An in-the-moment, output-driven
  rebuttal to a buyer's objection — classified, grounded in real call evidence and a won-deal
  precedent (or a labelled starter play), drafted in the rep's voice, and adapted to live
  (say-this talk-track) vs async (sendable reply + optional Gmail draft handoff). Brings the skill
  count to **21**.

### Fixed
- **Shared-ref resolution across all skills.** Skills referenced their shared docs with relative
  paths (`../../shared/…`), which Claude Code resolves against the session working directory rather
  than the skill directory — so a skill run from another CWD silently failed to load its frameworks
  and degraded to generic behavior. All 155 references across the skills now use the CWD-independent
  `${CLAUDE_PLUGIN_ROOT}/…` form (the anchor the command files already used).

### Changed
- `shared/output-modes.md` reframed around the 4 artifact classes; the unused dual-audience
  template replaced with the Manager-lens callout convention (hard rules preserved verbatim).
- `shared/widget-brevity.md` gained a collapsed-view rule for the interactive medium.
- Skill count updated to 21 across the README, `plugin.json`, and `marketplace.json` (also
  corrects a prior 19/20 drift in the marketplace description).

## [0.1.0]

- Initial release — 20 skills + router, eval harness, self-contained marketplace.

[0.2.0]: https://github.com/tdeschamps/modjo-sales-agent/releases/tag/v0.2.0
[0.1.0]: https://github.com/tdeschamps/modjo-sales-agent/releases/tag/v0.1.0
