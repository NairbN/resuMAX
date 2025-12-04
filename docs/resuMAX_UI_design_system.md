# resuMAX UI Design System

## 1. Color System
- **Palettes**
  - Primary: teal `#12B8A6` (cta/link), deep navy `#0F172A` (headings/text)
  - Secondary: sky `#38BDF8` (info/illustrations), graphite `#1F2937` (neutral emphasis)
  - Neutrals/surfaces: level-0 `#0B1220`, level-1 `#111827`, level-2 `#161E2E`, level-3 `#1F2937`, level-4 `#E5E7EB`, level-5 `#F8FAFC`
- **Functional states**
  - Success `#22C55E`
  - Warning `#F59E0B`
  - Error `#EF4444`
  - Info `#38BDF8`
- **Borders/hover/focus**
  - Border-default `#D0D5DD`
  - Border-strong `#94A3B8`
  - Hover-tint: lighten primary by 6% (`#17C3B0`)
  - Focus ring: 2px `#38BDF8` at 50% alpha
- **Tokens**
  ```css
  :root {
    /* brand */
    --color-primary: #12B8A6;
    --color-primary-strong: #0F172A;
    --color-secondary: #38BDF8;

    /* functional */
    --color-success: #22C55E;
    --color-warning: #F59E0B;
    --color-error: #EF4444;
    --color-info: #38BDF8;

    /* surfaces */
    --surface-0: #0B1220;
    --surface-1: #111827;
    --surface-2: #161E2E;
    --surface-3: #1F2937;
    --surface-4: #E5E7EB;
    --surface-5: #F8FAFC;

    /* utility */
    --border-default: #D0D5DD;
    --border-strong: #94A3B8;
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-muted: #64748B;
  }
  ```

## 2. Typography System
- **Families**
  - Headings: `Sora`, fallback `Inter`, sans-serif
  - Body/UI: `Work Sans`, fallback `Inter`, sans-serif
  - Monospace (diffs/status): `JetBrains Mono`, monospace
- **Scale (desktop)**
  - H1: 32/40, weight 700, tracking -1%
  - H2: 28/36, weight 700
  - H3: 24/32, weight 600
  - H4: 20/28, weight 600
  - H5: 18/26, weight 600
  - H6: 16/24, weight 600
  - Body L: 16/24, weight 500
  - Body M: 14/22, weight 400
  - Caption: 12/18, weight 500
  - Micro/Helper: 11/16, weight 500, uppercase optional for labels
- **Semantic usage**
  - H1/H2: Page titles, dashboard headers, modal titles
  - H3/H4: Section titles, card headers, summary panels
  - H5/H6: Inline labels, chip text, column titles
  - Body L: Primary body copy, instructions, button text
  - Body M: Secondary descriptions, table cells
  - Caption/Micro: Helper text, validation, timestamps, badge labels
- **Mobile**
  - Reduce each level by 2px, maintain line-height ratio; keep H1 max 28/34

## 3. Spacing & Layout Rules
- **Base unit**: 8px (use 4px for micro-alignment).
- **Grid**: 12 columns, 24px gutters desktop; 6 columns, 16px gutters tablet; 4 columns, 12px gutters mobile.
- **Vertical rhythm**: sections separated by 24-40px depending on hierarchy; maintain 4px baseline alignment for text and controls.
- **Padding rules**
  - Cards/modals: 24px desktop, 16px mobile
  - Inputs/buttons: 12px vertical x 16px horizontal (dense), 14px x 18px (regular)
  - Sticky footers/toolbars: 16px padding, 8px between controls
- **Element spacing**
  - Form fields stack with 12-16px gaps
  - Chips/badges 8px apart
  - Grids/lists: 16px row gap, 20-24px column gap on desktop
- **Breakpoint guidance**
  - Desktop >= 1200px, Tablet 768-1199px, Mobile <= 767px
  - Collapse dual-column layouts to single column on mobile with priority ordering: primary content first, helpers below

## 4. Component System Specification
Use the template for each component:
```
Component: [Name]
Purpose:
States:
- default
- hover
- active
- disabled
- error
- loading skeleton
Usage guidance:
```

### Primary Button
- Purpose: Main affirmative action (Upload, Optimize, Save version, Download).
- States: default (solid primary), hover (6% lighter fill + shadow), active (pressed tint), disabled (30% opacity, no shadow), error (use danger fill when destructive), loading skeleton (spinner replaces label, width locks).
- Usage guidance: One primary per view/section; prevent double submits during loading; always include focus ring.

### Secondary Button
- Purpose: Secondary actions (Cancel, Back, View details).
- States: default (outline primary), hover (tint background), active (darker outline), disabled (reduced opacity), error (outline danger for destructive), loading skeleton (spinner left of label).
- Usage guidance: Pair with primary; keep spacing 8-12px between buttons; avoid competing with primary for color weight.

### Upload Tile
- Purpose: Drag-drop/picker for resumes (PDF/DOCX <= 5 MB) and JDs (PDF/DOCX/text <= 10 MB).
- States: default (dashed border, muted icon), hover (accent border, subtle shadow), active (pressed border), disabled (lower opacity), error (red border + helper text), loading skeleton (shimmer tile with progress placeholder).
- Usage guidance: Persist file name on errors; show privacy note inline; keep retry CTA visible without clearing prior selection.

### Resume Card
- Purpose: Display resumes/JDs/versions with status, score, and actions.
- States: default (neutral border), hover (shadow + accent top/left rail), active/selected (solid accent rail), disabled (dimmed for unavailable), error (red badge + warning border), loading skeleton (card placeholder with bars).
- Usage guidance: Include timestamp and status chip; overflow menu for rename/delete; maintain consistent card width in grids.

### Modal
- Purpose: Confirmations (delete, apply-all), gates (credits), reassurance (privacy).
- States: default, hover/active on buttons inside, disabled actions, error/warning/success variants (icon + accent border), loading skeleton (header + body placeholders).
- Usage guidance: 12px radius, 24px padding; trap focus; primary CTA right-aligned; destructive actions styled with error colors.

### Alert Banner / Toast
- Purpose: Inline or toast feedback for success/info/warning/error.
- States: default variant color, hover (toast pause on hover), active (link/cta focusable), disabled not applicable, error variant, loading skeleton (bar placeholder).
- Usage guidance: Auto-dismiss toasts after ~6s; allow manual close; include short action link for recoverable errors; stack without overlap.

### Progress Indicator
- Purpose: Show pipeline status (queued > parsing > optimizing > ready) and uploads.
- States: default (segmented or spinner), hover n/a, active n/a, disabled n/a, error (red segment + retry link), loading skeleton (placeholder bar).
- Usage guidance: Pair long operations with time hint ("under 20s typical"); keep visible in sticky header/footer while running.

### Input Field
- Purpose: Text inputs (email, password, metadata), textareas (JD paste), select controls.
- States: default (neutral border), hover (darkened border), active/focus (accent ring), disabled (muted text/background), error (red border/message), loading skeleton (line placeholders).
- Usage guidance: Inline validation under field; preserve typed/pasted content on errors; require title for JD saving; support clear button where useful.

### Nav Bar
- Purpose: Global navigation with logo, credit badge, help, profile menu.
- States: default (solid surface-1), hover (menu items underline/tint), active (current page indicator), disabled n/a, error (show banner below for blocking issues), loading skeleton (logo + pill placeholders).
- Usage guidance: Right-align utilities; keep credit pill visible when billing enabled; surface latency/privacy hints via help dropdown.

### Progress/Stepper (flow)
- Purpose: Show multi-step flow (Upload > JD > Optimize > Download).
- States: default, hover n/a, active (current step accent), disabled (future steps muted), error (step marked with warning), loading skeleton (dimmed segments).
- Usage guidance: Place above workspace content; clickable only for completed steps; keep label short.

### Alert Toast (if separate from banner)
- Already covered; ensure accessible live-region.

## 5. Shape Language & Icon Rules
- **Radius tokens**: `--r-2: 2px` (chips), `--r-4: 4px` (inputs), `--r-8: 8px` (buttons), `--r-12: 12px` (cards/modals), `--r-16: 16px` (hero tiles).
- **Elevation**
  - Level 0: none
  - Level 1: `0 4px 12px rgba(15, 23, 42, 0.10)` for cards/hover
  - Level 2: `0 12px 24px rgba(15, 23, 42, 0.12)` for modals/dropdowns
  - Level 3: `0 16px 32px rgba(15, 23, 42, 0.16)` for toasts/overlays
- **Icons**
  - Stroke weight 2px, rounded caps; sizes 16/20/24; align to 2px grid.
  - Use accent color on active/positive cues; neutral on default; fill only for critical error success icons.
  - Avoid decorative overload; place lock/shield icons near privacy/storage actions.

## 6. Voice & Tone Guidelines
- Professional, concise, reassuring; avoid hype.
- Highlight user control ("You decide which changes to apply").
- Set expectations ("Most optimizations finish in under 20s").
- Encourage, not command ("Ready to optimize?" instead of "You must optimize").
- Acknowledge safety and privacy ("Only you can see this file").
- Keep CTAs action-led and short ("Save version", "Retry upload").

## 7. Design Principles
- Make next step obvious: primary CTA consistently placed and labeled.
- Reduce friction: validate early (file type/size, required title) and inline.
- Preserve context: never drop user inputs; keep selections across retries/timeouts.
- Show truth and trust: diff-first previews, conservative AI tone, privacy cues near uploads.
- Communicate status: chips/steppers/toasts with explicit states and time hints.
- Keep users in control: accept-all vs per-change, cancel upload, retry optimization.
- Consistent hierarchy: heading scale, surface levels, and spacing create clear priority.
- Mobile-resilient: single-column with sticky actions; avoid hidden gates on small screens.
- Progressive disclosure: show advanced options after basics are complete (pairing before optimize).
- Safe actions first: destructive paths require confirmation and danger styling.