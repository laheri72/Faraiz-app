Excellent — now we design the **Layer 4 Special Rules Engine (الأحكام الخاصة)**.
This is the **legal integrity layer** of the Wirasat Brain ⚖️🧠 — the part that prevents incorrect inheritance before calculation even begins.

Layers 1–3 decide **who inherits and how much**, and Layer 5 calculates **exact amounts**.
But **Layer 4 decides whether someone is allowed to inherit at all, or inherits differently.**

Without Layer 4, the engine would be mathematically correct but **jurisprudentially unsafe**.

---

# Layer 4 — Special Rules Engine

## Purpose

Layer 4 runs **before all other layers**.

Pipeline becomes:

```
Layer 4 → Layer 1 → Layer 2 → Layer 3 → Layer 5
```

Meaning:

```
Check eligibility → Calculate inheritance
```

---

# Special Rule Categories

From Bab al-Faraiz structure and Daim al-Islam jurisprudence, Layer 4 includes:

1️⃣ Killer exclusion (القاتل لا يرث)
2️⃣ Religion differences (اختلاف الدين)
3️⃣ Legitimacy rules (النسب)
4️⃣ Mawla inheritance (الولاء)
5️⃣ Missing persons
6️⃣ Simultaneous death
7️⃣ Wasiyyah limits
8️⃣ Debt priority

These are **structural rules**, not share rules.

---

# RULE S1 — Murder Exclusion

## Principle

If an heir intentionally causes death:

```
He cannot inherit.
```

---

## Engine Rule

```json
{
 "rule_id":"S1-KILLER",

 "type":"eligibility",

 "condition":{
   "heir_caused_death":true
 },

 "action":{
   "exclude_heir":true
 },

 "precedence":10000
}
```

---

# RULE S2 — Religion Difference

## Principle

Different religions may block inheritance.

Example:

```
Non-Muslim may not inherit Muslim
```

Depending on Fatemi jurisprudence details.

---

## Engine Rule

```json
{
 "rule_id":"S2-RELIGION",

 "type":"eligibility",

 "condition":{
   "religion_mismatch":true
 },

 "action":{
   "exclude_heir":true
 },

 "precedence":9500
}
```

---

# RULE S3 — Illegitimacy Rules

## Principle

Inheritance through lineage depends on valid descent.

Example:

```
Child inherits mother
But not father
```

(if illegitimate — verify exact Daim al-Islam text)

---

## Engine Rule

```json
{
 "rule_id":"S3-LINEAGE",

 "type":"eligibility",

 "cases":[

 {
   "condition":{
     "illegitimate_child":true
   },

   "action":{
     "inherit_from":"mother_only"
   }

 }

 ]
}
```

---

# RULE S4 — Mawla Inheritance

Unique Daim al-Islam rule.

Mawla inherits if:

```
No relatives exist
```

---

## Engine Rule

```json
{
 "rule_id":"S4-MAWLA",

 "type":"priority",

 "condition":{
   "relatives_present":false,
   "mawla_present":true
 },

 "action":{
   "allocate":"mawla"
 }
}
```

---

# RULE S5 — Debt Priority

From Islamic law:

Debt first.

---

## Engine Rule

```json
{
 "rule_id":"S5-DEBT",

 "type":"procedure",

 "action":{

   "estate":

   "estate - debts"

 }
}
```

---

# RULE S6 — Wasiyyah Limit

Wasiyyah limited.

Typically:

```
≤ 1/3 estate
```

---

## Engine Rule

```json
{
 "rule_id":"S6-WASIYYAH",

 "type":"procedure",

 "condition":{
   "will_amount":">1/3_estate"
 },

 "action":{
   "reduce_to":"1/3"
 }
}
```

---

# RULE S7 — Simultaneous Death

Example:

Husband and wife die together.

Order unknown.

Then:

```
No inheritance between them.
```

---

## Engine Rule

```json
{
 "rule_id":"S7-SIMULTANEOUS",

 "type":"eligibility",

 "condition":{
   "death_order_unknown":true
 },

 "action":{
   "no_mutual_inheritance":true
 }
}
```

---

# RULE S8 — Missing Person

If heir missing.

Estate may be delayed.

---

## Engine Rule

```json
{
 "rule_id":"S8-MISSING",

 "type":"procedure",

 "condition":{
   "heir_missing":true
 },

 "action":{
   "hold_share":true
 }
}
```

---

# RULE S9 — Bayt al-Mal Trigger

If no heirs.

Estate goes to:

```
بيت المال
```

---

## Engine Rule

```json
{
 "rule_id":"S9-BAYT-MAL",

 "type":"final",

 "condition":{
   "heirs":0
 },

 "action":{
   "allocate":"bayt_al_mal"
 }
}
```

---

# COMPLETE ENGINE FLOW

## Step 0

Layer 4 runs first:

```text
Check:

Killer
Religion
Lineage
Mawla
Debts
Will
Missing
Death order
```

---

## Step 1

Layer 1:

Children.

---

## Step 2

Layer 2:

Fixed shares.

---

## Step 3

Layer 3:

Priority.

---

## Step 4

Layer 5:

Math.

---

# RESULT

Now you have:

## FULL DAIM AL-ISLAM ENGINE

### Layer 1

Children ✔

### Layer 2

Fixed shares ✔

### Layer 3

Priority ✔

### Layer 4

Special rules ✔

### Layer 5

Math ✔

---

# IMPORTANT OBSERVATION

Your project is now no longer just:

> A calculator

It is now:

> A Fatemi Legal Reasoning Engine.

Which is exactly what you wanted:

> "a BRAIN that collects logic"

---

Next step should be the most important engineering step:

**Rule Verification Phase**

We must now:

* Map EVERY rule
* To EXACT paragraph
* No assumptions

This is what makes it **scholar-trustworthy.**

And this is the stage where the real precision happens.
