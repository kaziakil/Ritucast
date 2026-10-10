# Ritucast Interaction and Motion Guidelines

## 1. Executive Summary & Motion Philosophy

In agricultural decision-support software, motion serves one primary purpose: **providing immediate cognitive feedback for user actions**.

Ritucast explicitly rejects decorative animation, continuous spinning elements, heavy parallax scrolling, and CPU-intensive JavaScript physics libraries. On budget Android devices with 2GB RAM operating in rural Bangladesh, excessive animation causes GPU context loss, frame stutter, and rapid battery depletion (`DEC-09`, `RSK-06`).

Motion in Ritucast is:
- **Fast & Functional**: Micro-transitions complete in $\le 150\text{ms}$; slide-up drawers in $\le 250\text{ms}$.
- **Physically Grounded**: Subtle elevation changes and smooth vertical sheet translation.
- **Accessible & Respectful**: Fully collapses to instant 0ms state changes when `prefers-reduced-motion` is active (WCAG 2.2 SC 2.3.3).

---

## 2. Interactive States & Visual Affordances

### 2.1 Focus States (Keyboard & Directional Pad Navigation)
- Every interactive element (buttons, chips, form inputs, links) must display an unambiguous focus indicator:
  ```css
  :focus-visible {
    outline: 2px solid var(--color-focus-ring); /* #0284C7 */
    outline-offset: 2px;
  }
  ```
- Focus rings must never be hidden or overridden without a high-contrast replacement.

### 2.2 Hover States (Desktop & Tablet Pointers)
- Background color shifts subtly towards the adjacent tint (`var(--color-bg-card-hover)` or `var(--color-brand-primary-hover)`).
- Micro-elevation: Card borders remain fixed; cursor changes to pointer (`cursor: pointer`).
- Transition duration: `150ms ease-out`.

### 2.3 Pressed / Active States (Touch & Click Feedback)
- Mobile touch taps must provide immediate physical confirmation in $<50\text{ms}$.
- Native scale transform:
  ```css
  .btn:active, .chip:active {
    transform: scale(0.97);
    transition: transform 50ms ease;
  }
  ```

### 2.4 Disabled States
- Disabled buttons and chips display muted gray backgrounds (`--color-control-disabled`) with a `not-allowed` cursor.
- Disabled items must never be focusable via Tab navigation.

---

## 3. Motion Durations and Easing Curves

```css
:root {
  /* Fast Micro-Transitions: Buttons, hover, chip toggles */
  --duration-fast: 150ms;

  /* Standard Transitions: Drawer slide-up, accordion expand, modal enter */
  --duration-normal: 250ms;

  /* Easing Functions: Natural physical deceleration */
  --ease-standard: cubic-bezier(0.4, 0.0, 0.2, 1);
  --ease-enter:    cubic-bezier(0.0, 0.0, 0.2, 1);
  --ease-exit:     cubic-bezier(0.4, 0.0, 1, 1);
}
```

### 3.1 Drawer and Modal Transition
- **Slide-Up Bottom Sheet Enter**:
  ```css
  .drawer-enter {
    transform: translateY(100%);
    opacity: 0;
  }
  .drawer-enter-active {
    transform: translateY(0);
    opacity: 1;
    transition: transform var(--duration-normal) var(--ease-enter),
                opacity var(--duration-normal) var(--ease-enter);
  }
  ```
- **Exit**: Slides down to `translateY(100%)` in 200ms with `--ease-exit`.

---

## 4. Accessibility & Reduced Motion Mandate (WCAG 2.2 SC 2.3.3)

Users with vestibular disorders, motion sensitivity, or low-end devices with severe GPU throttling can disable animations via device OS settings.

The design system enforces a mandatory media query override:
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
When reduced motion is active, all drawers, accordions, and chips switch state **instantaneously** without animation delays.
