---
title: Argumentation Layer — How Distillary Captures Evidence
---

# Argumentation Layer

Distillary doesn't just capture **what** authors claim — it captures **why** they believe it, **how strong** the evidence is, and **what** they argued against.

## The Problem

A claim like "الإجماع حجة ملزمة" is an assertion. But the author didn't just assert it — they backed it with a Quranic verse, a hadith, and a logical argument. Without capturing that structure, you can't answer "what's the daleel?" and you can't compare argument quality across sources.

## The Solution: `backing:` Field

Every atom claim in the brain can have a `backing:` field in its frontmatter. Each entry captures one piece of evidence:

```yaml
backing:
  - category: textual
    subtype: ayah
    ref: "النساء:115"
    snippet: "ومن يشاقق الرسول من بعد ما تبيّن له الهدى..."
    strength: definitive
    warrant: "الآية تحذر من اتباع غير سبيل المؤمنين مما يثبت حجية الإجماع"
  - category: transmitted
    subtype: hadith_sahih
    ref: "سنن ابن ماجه"
    snippet: "لا تجتمع أمتي على ضلالة"
    strength: strong
    warrant: "عصمة الأمة من الاجتماع على الخطأ تثبت أن إجماعها حجة"
```

## The 5 Fields

### category

One of 9 universal types that cover every domain:

| Category | What it means | Islamic example | Academic example |
|---|---|---|---|
| **textual** | Citation from authoritative text | آية قرآنية | Primary source quote |
| **transmitted** | Report through chain of people | حديث نبوي | Reported data |
| **consensus** | Collective agreement of experts | إجماع العلماء | Scientific consensus |
| **analogical** | Extension from known to unknown case | قياس شرعي | Comparative study |
| **empirical** | Direct observation or measurement | استقراء | Experiment, RCT |
| **rational** | Logical deduction or induction | دليل عقلي | Formal proof |
| **experiential** | First-hand lived experience | — | Case study |
| **authority** | Statement from recognized expert | أثر صحابي | Expert opinion |
| **silence** | Absence of evidence IS the evidence | لم يرد نص | No studies exist |

These 9 categories are exhaustive and domain-agnostic. The same framework works for Islamic jurisprudence, academic research, legal texts, philosophy, and business books.

### subtype

The domain-specific label. This is freeform — it captures the vocabulary natural to each field:

- Islamic: `ayah`, `hadith_sahih`, `hadith_hasan`, `hadith_daif`, `ijma`, `qiyas`, `athar`
- Academic: `rct`, `meta_analysis`, `cohort_study`, `case_study`
- Legal: `statute`, `binding_precedent`, `legislative_history`
- Business: `anecdote`, `market_data`, `case_study`

### ref

Citation reference. Where to find the evidence:
- `"سورة النساء:115"` or `"صحيح البخاري 1117"` or `"Smith et al., 2020"`

### snippet

The first ~15 words of the actual evidence text. Enough to identify it:
- `"ومن يشاقق الرسول من بعد ما تبيّن له الهدى ويتبع غير سبيل المؤمنين..."`

### strength

How strong this evidence is, on a universal 5-level scale:

| Strength | Meaning | Examples |
|---|---|---|
| **definitive** | Virtually undisputed | آية صريحة، حديث متواتر، meta-analysis |
| **strong** | Widely accepted, minor debate | حديث صحيح، إجماع، well-powered RCT |
| **moderate** | Reasonable but contested | حديث حسن، cohort study، strong analogy |
| **weak** | Some value but unreliable alone | حديث ضعيف، anecdote، expert opinion |
| **contested** | Actively disputed | Conflicting studies, disputed hadith |

This is the **author's** assessment (or the field's standard), not ours.

### warrant

The most important field. A single sentence answering: **why does this evidence support THIS claim?**

The same hadith can support completely different claims depending on the warrant:

```
Evidence: "لا تجتمع أمتي على ضلالة"

Warrant A: "عصمة الأمة تثبت أن إجماعها حجة"
  → Claim: الإجماع حجة ملزمة

Warrant B: "إذا كانت الأمة معصومة حين تجتمع، فتفرّقها عن الحق يسقط هذه العصمة"
  → Claim: ترك الإنكار يسقط الحماية الإلهية
```

Without the warrant, you can't understand HOW the author connects evidence to conclusion.

## Evidence Chains

Sometimes evidence builds on prior evidence. A hadith specifies a general ayah, then ijma confirms the understanding, then qiyas extends it. This isn't 4 independent backings — it's a chain.

Use `depends_on` to represent chains:

```yaml
backing:
  - category: textual           # step 1
    subtype: ayah
    ref: "النساء:11"
    strength: definitive
    warrant: "النص يثبت أصل الميراث"

  - category: transmitted        # step 2 — builds on step 1
    subtype: hadith_sahih
    ref: "صحيح البخاري"
    strength: strong
    warrant: "الحديث يخصّص عموم الآية"
    depends_on: 0               # depends on backing[0]
```

## Counter-Arguments (Rebuttals)

Authors — especially in Islamic jurisprudence — argue dialogically. "فإن قال قائل..." is half of al-Risala. Distillary captures these as separate claims:

```yaml
tags:
  - role/rebuttal
  - rebuttal/defeated
rebuts: "[[الإجماع حجة ملزمة]]"
```

Tags:
- `role/rebuttal` — this is a counter-argument
- `rebuttal/defeated` — the author answered it successfully
- `rebuttal/acknowledged` — the author concedes partially

## Silence as Evidence

"No text addresses this" is itself evidence in some domains:

```yaml
backing:
  - category: silence
    subtype: no_text
    scope: "لم يرد نص من القرآن أو السنة في هذه المسألة"
    strength: moderate
    warrant: "انعدام النص يبيح الاجتهاد بالقياس"
```

## How the Extract Agent Captures This

The extract agent (v3.0) automatically identifies evidence patterns in text:

| Text pattern | Category | Subtype |
|---|---|---|
| "قال الله تعالى" | textual | ayah |
| "قال رسول الله" / "روى" | transmitted | hadith |
| "أجمع العلماء" / "لا خلاف" | consensus | ijma |
| "قياساً على" / "بجامع العلة" | analogical | qiyas |
| "قال ابن عباس" / "قال مالك" | authority | athar |
| "studies show" / "N%" | empirical | study |
| "لأن" / "therefore" | rational | argument |
| "فإن قال قائل" | → separate rebuttal claim | |

Claims with no identifiable evidence get no `backing:` field — that's fine. Not every claim needs formal evidence.

## Why 9 Universal Categories Instead of Domain-Specific Profiles

Every domain has its own evidence vocabulary (ayah vs. statute vs. RCT), but there are only 9 ways humans argue. The universal `category` enables cross-domain queries and comparison, while the freeform `subtype` preserves domain-specific precision.

| Aspect | What it enables |
|---|---|
| `category` | "Show all claims backed by textual evidence" — works across ALL sources |
| `subtype` | "Show all claims backed by hadith sahih" — domain-specific filter |
| `strength` | "Show only definitive claims" — universal quality filter |
| `warrant` | "How does Source A use this evidence vs Source B?" — cross-source comparison |

## Shared Evidence Hubs

When the same evidence (same hadith, same verse) is cited by multiple sources, it becomes a shared evidence hub in `brain/shared/evidence/`. These are a new bridge dimension — deeper than conceptual similarity because they share the same textual foundation.

## What This Enables

| Query | How |
|---|---|
| "ما الدليل على حجية الإجماع؟" | Find claims → return backing entries |
| "Show only definitive claims" | Filter by `strength/definitive` |
| "Same evidence, different conclusions?" | Shared evidence hubs with warrant comparison |
| "How does al-Shafi'i argue vs Ibn Qayyim?" | Compare backing category distributions |
| "What claims have no evidence?" | Claims without `backing:` field |

## Stats from Current Brain

Ibn Qayyim's الداء والدواء (78 claims, re-extracted with v3.0):
- 52 claims with backing (67%)
- 67 backing entries: 32 transmitted, 17 rational, 12 textual, 5 authority, 1 experiential
- 67 warrants (100% of backings)
- 28 definitive, 33 strong, 6 moderate

Al-Shafi'i's الرسالة (79 claims, re-extracted with v3.0):
- 79 claims with backing (100%)
- 87 backing entries with warrants
