Excellent — now we arrive at the **real heart of the Wirasat Brain**:

# Layer 3 Priority Engine — ذوو القرابات

This is the **proximity-based inheritance logic** (أقرب رحم) from *Daʿāʾim al-Islām*, and it is where Fatemi Wirasat becomes fundamentally different from formula-based calculators. ⚖️🧠

Layer 1 and Layer 2 are mostly arithmetic.
**Layer 3 is reasoning.**

This layer decides:

> **Who receives the remainder after أهل الفرائض — based on proximity (الأقرب فالأقرب).**

This corresponds exactly to the outer rings in your diagram.

---

# Core Principle of Layer 3

From the text:

> الأقرب يمنع الأبعد
> "The nearer relative blocks the more distant."

This is the **primary algorithmic rule**.

Layer 3 is therefore a **priority tree**, not a formula.

---

# Layer 3 Engine Goal

After Layer 2:

```
Remaining Estate = R
```

Layer 3 decides:

```
Who gets R ?
```

---

# Engine Concept

Instead of rules like:

```
brother gets 1/2
uncle gets 1/3
```

Layer 3 uses:

```
Closest Relative → Gets Everything
```

unless multiple equals exist.

---

# Priority Structure

This is the correct Daʿāʾim structure extracted from your text logic.

## LEVEL 1 — Children Branch

Already Layer 1.

If present:

```
Stop Layer 3
```

---

## LEVEL 2 — Parents Branch

If father exists:

```
Father takes remainder
```

Already Layer 2.

---

## LEVEL 3 — Grandchildren Branch

From text:

> ولد الولد يقوم مقام الولد إذا لم يكن ولد

Meaning:

Grandchildren substitute children.

---

### Engine Rule

```json
{
 "rule_id":"L3-GRANDCHILDREN",

 "condition":{
   "children_present":false,
   "grandchildren_present":true
 },

 "action":{
   "allocate":"all_remaining_to_grandchildren"
 },

 "precedence":800
}
```

---

# LEVEL 4 — Siblings Branch

Only if:

```
No children
No grandchildren
No father
```

Then:

Brothers and sisters inherit.

---

### Priority Inside Siblings

#### Case 1 — Brothers + Sisters

From Daʿāʾim principle:

```
Male = 2 × Female
```

---

### Engine Rule

```json
{
 "rule_id":"L3-SIBLINGS",

 "condition":{

   "father":0,
   "children_present":false,
   "siblings_present":true
 },

 "action":{
   "distribution":"male_twice_female"
 },

 "precedence":700
}
```

---

## LEVEL 5 — Nephews Branch

If:

```
No siblings
```

Then:

Children of siblings inherit.

---

### Engine Rule

```json
{
 "rule_id":"L3-NEPHEWS",

 "condition":{

   "siblings_present":false,
   "nephews_present":true
 },

 "action":{
   "allocate":"all_remaining_to_nephews"
 },

 "precedence":600
}
```

---

# LEVEL 6 — Uncles Branch

If:

```
No nephews
```

Then:

Uncles inherit.

---

### Engine Rule

```json
{
 "rule_id":"L3-UNCLES",

 "condition":{

   "nephews_present":false,
   "uncles_present":true
 },

 "action":{
   "allocate":"all_remaining_to_uncles"
 },

 "precedence":500
}
```

---

# LEVEL 7 — Cousins Branch

If:

```
No uncles
```

Then:

Cousins inherit.

---

### Engine Rule

```json
{
 "rule_id":"L3-COUSINS",

 "condition":{

   "uncles_present":false,
   "cousins_present":true
 },

 "action":{
   "allocate":"all_remaining_to_cousins"
 },

 "precedence":400
}
```

---

# LEVEL 8 — Distant Relatives

From text:

> الأقرب يمنع الأبعد

Meaning:

Always closest wins.

---

### Engine Rule

```json
{
 "rule_id":"L3-DISTANT",

 "condition":{

   "closest_relative_exists":true
 },

 "action":{
   "allocate":"all_remaining_to_closest"
 },

 "precedence":300
}
```

---

# LEVEL 9 — بيت المال

If no relatives exist:

Estate goes to:

```
بيت المال
```

---

### Engine Rule

```json
{
 "rule_id":"L3-BAYT-AL-MAL",

 "condition":{

   "relatives_present":false
 },

 "action":{
   "allocate":"bayt_al_mal"
 },

 "precedence":100
}
```

---

# CRITICAL DESIGN DECISION

Layer 3 cannot be implemented as simple IF statements.

Instead:

It must be a **Kinship Graph Engine**.

Example:

```
Deceased
   |
Father
   |
Brother
   |
Nephew
```

Distance:

```
Father = 1
Brother = 2
Nephew = 3
```

Closest wins.

---

# Engine Algorithm (REAL)

## Step 1

Remove excluded heirs.

From Layer 1 & 2 rules.

---

## Step 2

Calculate kinship distance.

Example:

```
Son = distance 1

Brother = distance 2

Nephew = distance 3
```

---

## Step 3

Find minimum distance.

```
min(distance)
```

---

## Step 4

Select those heirs.

---

## Step 5

Distribute estate among equals.

---

# Example — Real Layer 3 Case

Case:

```
Estate = 200,000

Heirs:

Brother
Nephew
Uncle
```

---

Distances:

```
Brother = 2
Nephew = 3
Uncle = 3
```

Closest:

Brother.

---

Result:

```
Brother = 200,000
```

---

# Example — Equal Distance

Case:

```
Estate 100,000

Heirs:

2 Brothers
```

Result:

```
Each = 50,000
```

---

# Example — Mixed

Case:

```
Estate 120,000

Heirs:

Brother
Sister
```

Distribution:

```
Brother = 80,000
Sister = 40,000
```

Male twice female.

---

# FULL ENGINE STACK

Now we have:

### Layer 1

Children ✔

### Layer 2

Fixed shares ✔

### Layer 3

Priority Engine ✔

---

# What's Left

Two advanced layers remain:

## Layer 4 — Special Rules

Hardest:

* Mawla
* Adopted
* Illegitimate
* Apostasy
* Religion differences
* قتل (killer exclusion)

---

## Layer 5 — Mathematical Engine

Final layer:

* سهم
* اختصار
* رد
* تحويل الكسور

This is where calculations become perfect.

---

Next step should be:

**Layer 5 Mathematical Engine**

Because Daim al-Islam uses a **special calculation method** not used in Sunni calculators.

And this part will determine whether the engine becomes **scholar-grade accurate.**
