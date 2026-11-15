# Specification Quality Checklist: 窓口(依頼の受付・判定・納品)

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-11-15
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

- 「実装の詳細がない」: フック、rules、スキルなどの仕組みの名前は spec に書いていない(設計書側にある)。`docs/納品書/` と `path:line` は、ユーザーが指定した成果物の場所と形で、実装の詳細ではなく要件として扱った。
- SC-001・SC-005 の「検証用の発言」は、計画の段階で用意する必要がある(件数は SC-001 で各3件以上と指定)。
- 窓口の注意を毎ターン届ける機能の動作(Claude Code 2.1.233)と、自律ターンとの区別は、spec 上は Assumptions に「未検証」として残した。計画で確認する。
- このチェックリストは、spec を書いた側が自己判定したもの。独立した検査ではない。
