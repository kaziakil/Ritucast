# Ritucast Agricultural Insight Information Model

## 1. Executive Summary & Information Hierarchy

This specification defines the information architecture for agricultural insight presentation in Ritucast.

To ensure agronomic safety and prevent misleading or overconfident advice (`DEC-08`, `DEC-10`), every insight is structured according to an **8-Layer Information Hierarchy**. The user interface must never blur or interchange these layers.

---

## 2. The 8 Conceptual Information Layers

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. Current Context      : উপজেলা, সক্রিয় ফসল ও বর্তমান বৃদ্ধির ধাপ     │
├────────────────────────────────────────────────────────────────────────┤
│ 2. Observed Conditions  : প্রত্যক্ষ পরিমাপকৃত উপাত্ত (বৃষ্টি, তাপমাত্রা)  │
├────────────────────────────────────────────────────────────────────────┤
│ 3. Derived Indicators   : হিসাবকৃত সূচক (বাষ্পীভবন ET₀, মাটির আর্দ্রতা ঘাটতি)│
├────────────────────────────────────────────────────────────────────────┤
│ 4. Interpretation       : বাস্তব কৃষি তাৎপর্য (মাটিতে রস পর্যাপ্ত/ঘাটতি)│
├────────────────────────────────────────────────────────────────────────┤
│ 5. Risk Assessment      : সম্ভাব্য ঝুঁকি মাত্রা (স্বাভাবিক/সতর্কতা/জরুরি)│
├────────────────────────────────────────────────────────────────────────┤
│ 6. Recommendation       : সুনির্দিষ্ট কর্মপরিকল্পনা (সেচ স্থগিত/ধান কর্তন)│
├────────────────────────────────────────────────────────────────────────┤
│ 7. Explanation          : বৈজ্ঞানিক যুক্তি ও উৎস ("কেন এই পরামর্শ?")    │
├────────────────────────────────────────────────────────────────────────┤
│ 8. Limitations & Safety : পূর্বাভাস অনিশ্চয়তা ও জমিতে রস পরীক্ষার নির্দেশ│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Specifications for Core Insight Types

---

### 3.1 Insight Type 1: Barind Irrigation Scheduling Advisory (`RULE-IRR-01`)
- **Primary Message**: *"আজ সেচ দেওয়ার প্রয়োজন নেই — আগামী ৪৮ ঘণ্টার মধ্যে মাঝারি বৃষ্টির সম্ভাবনা রয়েছে এবং জমিতে পর্যাপ্ত রস বিদ্যমান।"*
- **8-Layer Representation**:
  1. *Current Context*: গোদাগাড়ী উপজেলা | ফসল: বোরো ধান | ধাপ: থোড় পর্যায় (Panicle Initiation).
  2. *Observed Conditions (Tier 1)*: বর্তমান তাপমাত্রা: ২৮° সে | বিগত ২৪ ঘণ্টার বৃষ্টি: ০ মিমি.
  3. *Derived Indicators (Tier 2)*: রেফারেন্স বাষ্পীভবন ($ET_0$): ৪.২ মিমি/দিন | ফসলের পানি চাহিদা ($ET_c$): ৪.৮ মিমি/দিন | মাটির রস ঘাটতি ($D_t$): ১৬ মিমি ($RAW = 28$ মিমি).
  4. *Interpretation*: ধানের শিকড় অঞ্চলে এখনো পর্যাপ্ত রস রয়েছে এবং তা সংকটজনক ঘাটতি সীমায় পৌঁছায়নি.
  5. *Risk Assessment*: খরা বা পানিশূন্যতার কোনো তাৎক্ষণিক ঝুঁকি নেই.
  6. *Recommendation (Tier 4)*: **"সেচ স্থগিত রাখুন (কমপক্ষে ২৪ ঘণ্টা)"**.
  7. *Explanation*: আগামীকালের সম্ভাব্য ২০ মিমি বৃষ্টি মাটির আর্দ্রতা পূরণ করবে; আজ সেচ দিলে পাম্পের ডিজেল/বিদ্যুৎ খরচ অপচয় হবে.
  8. *Limitations & Safety*:
     > *"⚠️ সতর্কবার্তা: সেচ বন্ধ করার আগে আপনার জমির আইল ও মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*
- **User Actions**:
  - Primary: `[ পরামর্শ শেয়ার করুন ]` (WhatsApp share).
  - Secondary: `[ মাটির রস পরীক্ষা নির্দেশিকা ]` (AWD field guide drawer).

---

### 3.2 Insight Type 2: Haor Pre-Monsoon Flash-Flood Early Alert (`RULE-FLD-01`, `DEC-16`)
- **Primary Message**: *"সতর্কবার্তা: আগামী ৪৮–৭২ ঘণ্টার মধ্যে তাহিরপুরের নিচু হাওরে আকস্মিক বন্যার মাঝারি ঝুঁকি রয়েছে।"*
- **8-Layer Representation**:
  1. *Current Context*: তাহিরপুর উপজেলা | ফসল: বোরো ধান | ধাপ: দানা শক্ত হওয়া / পাকা পর্যায়.
  2. *Observed Conditions (Tier 1)*: চেরাপুঞ্জি ও মেঘালয় ক্যাচমেন্টে বৃষ্টিপাত: ১৬৫ মিমি | সুরমা নদী পানি বৃদ্ধি: +০.৭৫ মিটার/২৪ ঘণ্টা.
  3. *Derived Indicators (Tier 2)*: আকস্মিক বন্যা ঝুঁকি সূচক ($I_{\text{flood}}$): ০.৬৮ (পরিসীমা ০–১.০).
  4. *Interpretation*: উজানের পাহাড়ি ঢল দ্রুত নেমে আসছে; নদীর পানি বিপদসীমার ০.৪০ মিটারের মধ্যে চলে এসেছে.
  5. *Risk Assessment*: **মাঝারি থেকে উচ্চ প্লাবন ঝুঁকি (সতর্কবার্তা স্তর)**.
  6. *Recommendation (Tier 4)*:
     - যদি ধান $\ge ৮০\%$ পাকা থাকে $\to$ **"অবিলম্বে ধান কেটে ঘরে তুলুন"**.
     - যদি ধান এখনো দুধ/দানা গঠন ধাপে থাকে $\to$ **"ফসলরক্ষা বাঁধ তদারকি করুন ও পানি নিষ্কাশন ব্যবস্থা প্রস্তুত রাখুন"**.
  7. *Explanation*: উজানের ভারী বৃষ্টিপাত ও সুরমা নদীর দ্রুত পানি বৃদ্ধি হাওরের ফসলরক্ষা বাঁধের ওপর তীব্র চাপ সৃষ্টি করছে.
  8. *Limitations & Safety*:
     > *"⚠️ সতর্কবার্তা: স্থানীয় পানি উন্নয়ন বোর্ড ও উপজেলা কৃষি অফিসের মাইকিং ও সতর্কবার্তার সাথে মিলিয়ে সিদ্ধান্ত নিন।"*
- **User Actions**:
  - Primary: `[ জরুরি ধান কর্তন নির্দেশনা ]`
  - Secondary: `[ বাঁধ ও নদীর পানি উচ্চতা বিশদ ]`

---

### 3.3 Insight Type 3: Temperature Extremes & Thermal Stress Alert (`RULE-STR-01`)
- **Primary Message**: *"সতর্কবার্তা: আগামী ৪৮ ঘণ্টায় উচ্চ তাপমাত্রা ($> ৩৫^\circ\text{C}$) ও তীব্র সূর্যালোকের কারণে ধানের শিষ ব্লাস্ট বা বন্ধ্যাত্ব ঝুঁকি রয়েছে।"*
- **8-Layer Representation**:
  1. *Current Context*: তানোর উপজেলা | ফসল: বোরো ধান | ধাপ: ফুল ফোটা পর্যায় (Flowering / Anthesis).
  2. *Observed Conditions (Tier 1)*: সর্বোচ্চ তাপমাত্রা: ৩৬.৫° সে | আর্দ্রতা: ৫৫%.
  3. *Derived Indicators (Tier 2)*: তাপমাত্রার ধারাবাহিকতা: একটানা ২ দিন $> ৩৫^\circ\text{C}$.
  4. *Interpretation*: ফুল ফোটার সময় ৩৫° সেলসিয়াসের বেশি তাপমাত্রা থাকলে ধানের পরাগায়ন ব্যাহত হয় এবং চিটা হওয়ার আশঙ্কা থাকে.
  5. *Risk Assessment*: **উচ্চ তাপপ্রবাহ ঝুঁকি (Thermal Stress)**.
  6. *Recommendation (Tier 4)*: **"জমিতে ৫–৭ সেমি পানি ধরে রাখুন"** (ক্ষেতে পর্যাপ্ত পানি থাকলে ফসলের মাইক্রোক্লাইমেট শীতল থাকে).
  7. *Explanation*: শিকড় অঞ্চলে পর্যাপ্ত পানি বাষ্পীভবনের মাধ্যমে ধানের শীষের তাপমাত্রা ২–৩ ডিগ্রি কমিয়ে রাখে.
  8. *Limitations & Safety*:
     > *"⚠️ সতর্কবার্তা: ফুল ফোটা অবস্থায় জমিতে কোনো রাসায়নিক স্প্রে করবেন না।"*

---

## 4. Card Presentation Specifications

Every insight card in the UI must feature:
1. **Tier Category Badge**: Small pill in top right indicating category (e.g., `হিসাবকৃত সূচক` or `পরামর্শ`).
2. **Clear Operational Banner**: High-contrast header stating the action.
3. **Plain Bangla Text**: Concise, grammatically clear sentences.
4. **Expandable Evidence Drawer**: Tapping reveals the Tier 1/2 underlying sensor numbers and data source timestamps.
5. **Mandatory Safety Notice**: Prominently rendered at the base of every Tier 4 card with a distinct alert icon.
