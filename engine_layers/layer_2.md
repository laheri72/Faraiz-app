Excellent — now we build the **Layer 2 Engine (أهل الفرائض)** — the **core fixed-share inheritance engine** according to your extracted **Daʿāʾim al-Islām Bab al-Faraiz** text.

This layer is the **mathematical backbone** of the Wirasat Brain 🧠⚖️ — it determines the **fixed shares before radd (ردّ) and before extended relatives.**

You already saw Layer 1 (children).
Now this is the **complete Layer 2 specification** — structured exactly how the engine will run.

This is the **first truly stable inheritance engine layer.**

---

# LAYER 2 ENGINE — أهل الفرائض

## Purpose

Layer 2 calculates:

> The fixed shares before remainder distribution.

This includes:

* Husband
* Wife
* Father
* Mother
* Grandparents (partial)
* Fixed-share daughters (already extracted)

---

# ENGINE ORDER (CRITICAL)

The engine must execute Layer 2 in **this exact order**:

### STEP 1 — Identify fixed heirs

```text
Check existence of:

Husband
Wife
Mother
Father
Grandparents
Children
```

---

### STEP 2 — Apply fixed shares

Then assign:

```text
Husband/Wife first
Mother/Father second
Children shares third
```

This order is confirmed by:

> "بدئ بفريضته"

Meaning:

> Fixed shares applied first.

---

# RULE L2-1 — Husband Share

### Rule

If husband exists:

### Case 1 — No children

Husband:

1/2

---

### Case 2 — Children exist

Husband:

1/4

---

### Engine Rule

```json
{
 "rule_id":"L2-HUSBAND",
 "type":"fixed_share",

 "cases":[

   {
     "condition":{
        "husband":1,
        "children_present":false
     },

     "share":"1/2"
   },

   {
     "condition":{
        "husband":1,
        "children_present":true
     },

     "share":"1/4"
   }

 ],

 "precedence":900,
 "layer":"Layer2"
}
```

---

# RULE L2-2 — Wife Share

### Case 1 — No children

Wife:

1/4

---

### Case 2 — Children exist

Wife:

1/8

---

### Engine Rule

```json
{
 "rule_id":"L2-WIFE",
 "type":"fixed_share",

 "cases":[

  {
   "condition":{
     "wife":1,
     "children_present":false
   },

   "share":"1/4"
  },

  {
   "condition":{
     "wife":1,
     "children_present":true
   },

   "share":"1/8"
  }

 ],

 "precedence":900
}
```

---

# RULE L2-3 — Mother Share

### Case 1 — No children

Mother:

1/3

---

### Case 2 — Children exist

Mother:

1/6

---

### Engine Rule

```json
{
 "rule_id":"L2-MOTHER",

 "cases":[

 {
   "condition":{
     "mother":1,
     "children_present":false
   },

   "share":"1/3"
 },

 {
   "condition":{
     "mother":1,
     "children_present":true
   },

   "share":"1/6"
 }

 ],

 "precedence":850
}
```

---

# RULE L2-4 — Father Share

Fatemi fiqh is **different from Sunni here.**

Father can be:

* Fixed heir
* Residual heir

---

### Case 1 — Parents only

Mother:

1/3

Father:

2/3

(Confirmed from paragraph 1336 earlier)

---

### Case 2 — Children exist

Father:

Residual after fixed shares.

---

### Engine Rule

```json
{
 "rule_id":"L2-FATHER",

 "cases":[

 {
   "condition":{
      "father":1,
      "mother":1,
      "children_present":false
   },

   "shares":[
      {"mother":"1/3"},
      {"father":"2/3"}
   ]
 },

 {
   "condition":{
      "father":1,
      "children_present":true
   },

   "share":"residuary"
 }

 ],

 "precedence":850
}
```

---

# RULE L2-5 — Fixed Heirs Priority

From text:

> بدئ بفريضته

Meaning:

Fixed shares always paid first.

---

### Engine Rule

```json
{
 "rule_id":"L2-FARAID-FIRST",

 "type":"procedure",

 "steps":[

   "apply_fixed_shares",

   "calculate_remaining",

   "apply_radd_or_residuary"

 ],

 "precedence":1000
}
```

---

# RULE L2-6 — Radd Trigger Rule

From text:

> ويرد عليها

Meaning:

Remainder returned to closest kin.

---

### Engine Rule

```json
{
 "rule_id":"L2-RADD",

 "condition":{
   "remaining_estate":">0"
 },

 "action":{
   "return_to":"closest_kin"
 }
}
```

---

# COMPLETE LAYER 2 ENGINE FLOW

Engine runs exactly like this:

```
INPUT:

Estate = X

Heirs = List
```

---

## Step 1

Identify:

```
Fixed heirs
```

---

## Step 2

Assign:

```
Spouse shares
```

---

## Step 3

Assign:

```
Mother/Father shares
```

---

## Step 4

Assign:

```
Children shares
```

---

## Step 5

Compute:

```
Remaining estate
```

---

## Step 6

If remainder:

```
Apply Radd
```

---

# REAL EXAMPLE (Layer 2)

Case:

```
Estate 120,000

Heirs:

Wife
Mother
Son
```

---

### Step 1

Wife:

1/8

= 15,000

---

### Step 2

Mother:

1/6

= 20,000

---

### Step 3

Remaining:

120000

−15000

−20000

= 85,000

---

### Step 4

Son:

85,000

---

### Final Output

```
Wife = 15,000
Mother = 20,000
Son = 85,000
```

---

# CRITICAL OBSERVATION

We now have:

### Layer 1

Children Engine ✔

### Layer 2

Fixed Shares Engine ✔

---

Next layer is:

# LAYER 3 ENGINE

ذوو القرابات

This is the **hardest part**:

* Brothers
* Sisters
* Uncles
* Priority chains

Exactly like your diagram.

---

And that is where:

> The real "Wirasat Brain" begins.

Because Layer 3 is:

```
Graph reasoning
```

Not simple math.

---

Next step will define:

**Layer 3 Priority Engine (ذوو القرابات)**

That is the core of Daim al-Islam inheritance logic.
