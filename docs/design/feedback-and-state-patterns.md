# Ritucast Feedback and State Patterns Specification

## 1. Executive Summary & State Design System

This specification defines the visual treatments, iconography, copy hierarchy, and interaction affordances for the 14 application states established in [Phase 6: Interaction & State Specification](file:///Users/kazi/Projects/RITUCAST/docs/ux/interaction-and-state-specification.md).

### Non-Negotiable UX Integrity Rules
1. **Never Show Blank Whitespace on Failure**: Every failure or empty state must display a helpful, polite explanation with a concrete next action.
2. **Never Masquerade Stale Data as Current**: Data exceeding freshness thresholds must prominently display a sync age badge and timestamp.
3. **Never Fabricate Data**: Zero placeholder values or simulated mock numbers may appear in empty or error states.

---

## 2. Visual Blueprint for Critical UI States

---

### 2.1 State: Skeleton Loading (`ST-02`)
- **Visual Presentation**: Pulsing rectangular blocks with subtle shimmer gradient, matching the exact height and border-radius of the final cards.
- **CSS Styling**:
  ```css
  .skeleton-box {
    background: linear-gradient(90deg, #E2E8F0 25%, #F1F5F9 50%, #E2E8F0 75%);
    background-size: 200% 100%;
    animation: skeleton-pulse 1.5s ease-in-out infinite;
    border-radius: var(--radius-md);
  }
  @keyframes skeleton-pulse {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }
  ```
- **Time Threshold**: If loading exceeds 3.5 seconds, display a secondary retry button: *"সংযোগ ধীরগতির। [পুনরায় লোড করুন]"*.

---

### 2.2 State: Stale Data Warning (`ST-08`)
- **Trigger**: Upstream weather $>24\text{h}$ old or satellite $>36\text{h}$ old.
- **Visual Presentation**:
  - Prominent orange indicator pill anchored to card header:
    `<span class="badge badge-stale"><svg>🕒</svg> উপাত্ত কিছুটা পুরনো (আপডেট প্রক্রিয়াধীন)</span>`
  - Observation timestamp highlighted in warm amber text.
- **User Action**: Pull-down to refresh or tap *"আপডেট যাচাই করুন"*.
- **Integrity Rule**: Cached data is displayed, but must **never** appear as live or current.

---

### 2.3 State: Offline Mode (`ST-12`)
- **Trigger**: `navigator.onLine === false`.
- **Visual Presentation**:
  - Sticky top status bar anchored directly below the header:
    ```
    ┌────────────────────────────────────────────────────────────────────────┐
    │ 📡 অফলাইন মোড: সংরক্ষিত তথ্য প্রদর্শিত হচ্ছে (সর্বশেষ আপডেট: সকাল ০৮:০০)  │
    └────────────────────────────────────────────────────────────────────────┘
    ```
  - Background: `#0F172A` (Slate Navy); Text: `#FFFFFF`; Icon: Antenna dish `[📡]`.
  - Refresh actions are disabled; cached advisories and AWD tube guides remain fully interactive.

---

### 2.4 State: Unsupported Geographic Area (`ST-05`)
- **Trigger**: User searches for an Upazila outside the two pilot zones.
- **Visual Presentation**:
  - Centered illustration card in bottom sheet modal:
    - Icon: Map pin with dotted outline `[📍]`.
    - Title: **"পাইলট বহির্ভূত এলাকা"**.
    - Body: *"রিতুকাস্ট বর্তমানে বরেন্দ্র অঞ্চল (গোদাগাড়ী, তানোর) এবং হাওর অঞ্চলে (সুনামগঞ্জ সদর, তাহিরপুর) পরীক্ষামূলকভাবে সেবা দিচ্ছে। খুব শীঘ্রই আপনার উপজেলায় সেবা চালু করা হবে।"*
    - Action Chips: `[ গোদাগাড়ী দেখুন ]` `[ তাহিরপুর দেখুন ]`

---

### 2.5 State: Recoverable Network Error (`ST-13`)
- **Trigger**: Network drop or 504 Gateway Timeout during advisory fetch.
- **Visual Presentation**:
  - Standard card container with light gray background:
    - Icon: Alert triangle `[⚠️]` in cool slate.
    - Title: **"তথ্য লোড করা সম্ভব হয়নি"**.
    - Body: *"সার্ভারের সাথে সংযোগ সাময়িকভাবে বিচ্ছিন্ন। অনুগ্রহ করে আপনার ইন্টারনেট সংযোগ পরীক্ষা করুন।"*
    - Primary Action: High-contrast button: **[ পুনরায় চেষ্টা করুন ]** (Retry).

---

### 2.6 State: Unrecoverable Client Crash Screen (`ST-14`)
- **Trigger**: Uncaught JavaScript runtime exception in React Error Boundary.
- **Visual Presentation**:
  - Clean, non-alarming full-viewport crash screen:
    - Logo: Ritucast icon.
    - Title: **"অ্যাপটিতে সাময়িক সমস্যা দেখা দিয়েছে"**.
    - Body: *"আপনার তথ্যের কোনো ক্ষতি হয়নি। অ্যাপটি পুনরায় চালু করতে নিচের বাটনে চাপুন।"*
    - Primary CTA: **[ অ্যাপ রিস্টার্ট করুন ]** (Clears corrupted state and navigates to `/`).
