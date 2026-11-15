# Specification Quality Checklist: 確かめる者(作られたものの独立した検査)

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

- 「実装の詳細がない」: エージェントの定義、ツール名、呼び出し方式(入れ子)は、spec の本文に書いていない(設計書側にある)。Assumptions に、入れ子の未検証だけを事実として残した。ソースファイルの拡張子とテストファイルの名前の線引きは、ユーザーが選んだ検査の対象の条件(要件)として扱った。
- 「`paths` 付きの rules が、サブエージェントで自動で読み込まれるか」「入れ子が動くか」「戻り値の長さの上限」は、未検証として Assumptions に残した。計画で確認する。
- SC-001〜SC-007 の「検証用の依頼」は、計画の段階で用意する必要がある。
- このチェックリストは、spec を書いた側が自己判定したもの。独立した検査ではない。
- 窓口の override の spec テンプレート(依頼票の節を持つもの)が、このフィーチャーの spec の作成で使われた。節の並びは、override と一致する。
