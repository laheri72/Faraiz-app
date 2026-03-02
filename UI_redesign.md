✦ This document outlines the UI Architecture and Design Specification for the Fatemi Wirasat Engine frontend. This architecture ensures the
  system feels like a scholarly jurisprudence tool while maintaining modern technical standards.

  ---

  1 — UI Architecture & Component Tree

  The architecture follows a Strict Hierarchical Flow, ensuring data integrity across the multi-layer calculation process.


   App (Root)
   ├── JurisprudenceHeader (Identity & Progress)
   │   └── StepIndicator (Progress tracking: 1-4)
   ├── ViewManager (Conditional Render based on CurrentStep)
   │   ├── Home (Introduction & Intent)
   │   ├── EstateForm (Input: Value, Debts, Wasiyyah)
   │   ├── HeirSelector (Input: Relational counts & flags)
   │   │   ├── RelationCard (Touch-friendly selector)
   │   │   └── SelectionAudit (Live preview of entered heirs)
   │   ├── CaseSummary (Verification before engine execution)
   │   └── ResultsDisplay (Output)
   │       ├── ResultsTable (Distribution list)
   │       ├── VerificationPanel (Financial & Fraction Audit)
   │       └── RuleExplanationPanel (Arabic reasoning & Fiqh basis)
   └── JurisprudenceFooter (Legal notice & Research credits)

  ---

  2 — Page Layouts


   * Parchment Container: All core views are housed in a centered, maximum 900px width container to maintain focus and readability.
   * Logical Progression: Each page follows a "Statement -> Input -> Action" structure.
   * Scholarly Header: A persistent header that establishes the "Fatemi Wirasat Engine" identity.


  3 — Mobile Layout Design (Touch-First)


   * Touch Targets: All interactive elements (buttons, checkboxes) have a minimum size of 48x48px.
   * Vertical Stacking: Multi-column grids on desktop collapse into a single-column stack on mobile to prevent horizontal scrolling.
   * Sticky Actions: The "Next" and "Back" buttons are consistently placed at the bottom of the screen for easy thumb access.
   * Input Types: Numeric inputs trigger the decimal/numeric keypad automatically.

  4 — Desktop Layout Design


   * Side-by-Side Context: In the HeirSelector, the list of potential heirs is on the left, while the "Surviving Family" audit is on the right.
   * Enhanced Whitespace: Utilizes generous margins to prevent the "calculator clutter" common in financial apps.
   * Hover States: Subtle gold borders and parchment-depth shadows to indicate interactivity.

  ---

  5 — Component Definitions



  ┌───────────────────────┬───────────────────────────────────┬──────────────────────────────────┐
  │ Component             │ Purpose                           │ Key Props / State                │
  ├───────────────────────┼───────────────────────────────────┼──────────────────────────────────┤
  │ EstateForm        │ Collects financial data.          │ initialData, onUpdate        │
  │ HeirSelector      │ Manages the count of heirs.       │ currentHeirs, onHeirChange   │
  │ CaseSummary       │ Final review before API call.     │ caseState                      │
  │ ResultsTable      │ Displays individual shares.       │ results: CalculationResult[]   │
  │ VerificationPanel │ Displays sum of shares vs estate. │ verification: VerificationData │
  │ RuleExplanation   │ Renders Arabic text & logic.      │ reasoning: string[]            │
  └───────────────────────┴───────────────────────────────────┴──────────────────────────────────┘

  ---

  6 — Data Flow (Centralized State)


  The system uses a Single Source of Truth pattern.

   * State Object (`CaseState`):


       interface CaseState {
         step: 'HOME' | 'ESTATE' | 'HEIRS' | 'SUMMARY' | 'RESULTS';
         estate: { value: number; debts: number; wasiyyah: number };
         heirs: HeirInput[];
         calculationResponse: CalculationResponse | null;
       }
   * Uni-directional Flow: State resides in App.tsx. Components receive data via props and emit changes via onUpdate callbacks.
   * Persistence: (Optional) The CaseState can be synced to localStorage to prevent data loss on accidental refresh.

  ---

  7 — Visual Style Guide


   * Color Palette:
       * Primary: #064e3b (Emerald Green) — Represents growth and Fatemi tradition.
       * Secondary: #78350f (Deep Amber) — Used for scholarly accents.
       * Accent: #d4af37 (Gold) — Denotes precision and value.
       * Background: #fdfbf7 (Parchment) — Calm, readable, and scholarly.
   * Typography:
       * Headings: Serif (Georgia, Amiri) for a formal, authoritative feel.
       * Body: Sans-serif (Inter) for high readability on small screens.
   * Arabic Support: Right-to-Left (RTL) enabled for jurisprudence sections with specialized font-weight for clarity.

  ---

  8 — Suggested UI Improvements


   1. Instant Validation: Real-time feedback if Wasiyyah exceeds 1/3, providing a scholarly explanation of the limit.
   2. Exclusion Education: In the HeirSelector, add small "i" icons next to relations (e.g., Brother) that briefly explain when they might be
      excluded (e.g., "Excluded if a Son exists").
   3. Decree Export: A "Download Decree" button on the results page to generate a scholarly PDF of the distribution.
   4. Fraction Visualization: A simple pie chart or bar graph in the verification section to visually confirm the "Total = 1" logic.