/**
 * Ritucast Bilingual Translations Dictionary (Bangla 'bn' and English 'en')
 * Adheres to AGENTS.md, DEC-08, DEC-10, and DEC-17.
 * Brand name in Bangla: ঋতুকাস্ট
 * Brand name in English: Ritucast
 */

export type Language = 'bn' | 'en'

export interface TranslationDictionary {
  // Brand & Accessibility
  brand_name: string
  brand_tagline: string
  skip_to_content: string
  home_aria_label: string

  // Navigation
  nav_advisories: string
  nav_weather: string
  nav_water_balance: string
  nav_flood: string
  nav_provenance: string
  nav_menu_open: string
  nav_menu_close: string

  // Status Badge
  status_checking: string
  status_live: string
  status_live_title: string
  status_degraded: string
  status_degraded_title: string

  // Theme & Language Controls
  theme_label: string
  theme_system: string
  theme_light: string
  theme_dark: string
  lang_label: string
  lang_bn: string
  lang_en: string

  // Context Selector
  context_section_label: string
  division_label: string
  district_label: string
  upazila_label: string
  upazila_field_label: string
  search_placeholder: string
  search_no_results: string
  search_type_upazila: string
  search_type_district: string
  search_hint: string
  all_divisions: string
  select_division: string
  select_district: string
  select_upazila: string
  search_filter_active: string
  clear_search: string
  pilot_badge: string
  national_badge: string
  upazila_count_suffix: string
  crop_label: string
  crop_calibrated_badge: string
  crop_regional_badge: string
  crop_category_all: string
  crop_category_cereals: string
  crop_category_cash: string
  crop_category_tubers: string
  crop_category_pulses: string
  crop_category_oilseeds: string
  crop_category_vegetables: string
  crop_category_fruits: string
  date_range_label: string
  start_date_label: string
  end_date_label: string
  date_preset_7d: string
  date_preset_14d: string
  date_preset_30d: string
  date_default_notice: string
  date_latency_notice: string
  date_err_start_after_end: string
  date_err_future: string
  planting_date_label: string
  planting_date_hint: string
  growth_stage_manual: string
  growth_stage_derived: string
  stage_label: string
  refresh_btn: string
  refresh_loading: string
  refresh_aria_label: string
  current_zone: string
  primary_risk_label: string
  primary_risk_drought: string
  primary_risk_flood: string
  gating_verified: string
  zone_barind: string
  zone_haor: string

  // Growth Stages
  stage_tillering: string
  stage_booting: string
  stage_flowering: string
  stage_dough: string
  stage_maturity: string

  // Advisory Hub
  advisory_error_title: string
  suppression_title: string
  suppression_body: string
  tier_1_title: string
  tier_2_title: string
  tier_3_title: string
  tier_4_title: string
  rule_id_prefix: string
  action_items_heading: string
  rationale_heading: string
  pumping_savings_prefix: string
  field_verification_heading: string
  supporting_tiers_heading: string
  tier_1_source_label: string
  tier_1_rainfall_7d: string
  tier_2_method_label: string
  tier_2_deficit_label: string
  tier_3_model_label: string
  tier_3_rain_prob_label: string
  hazard_eval_heading: string
  hazard_eval_overall: string
  hazard_domain: string
  hazard_tier: string
  hazard_metric: string
  hazard_threshold: string
  hazard_action: string
  hazard_action_warranted: string
  hazard_action_not_warranted: string
  scientific_disclaimer_heading: string

  // Weather View
  weather_error_title: string
  weather_obs_title: string
  weather_obs_source: string
  weather_fcst_title: string
  weather_fcst_models: string
  weather_max_temp: string
  weather_min_temp: string
  weather_precip_24h: string
  weather_solar_rad: string
  weather_rh_mean: string
  weather_wind_speed: string
  weather_lead_time: string
  weather_qpf: string
  weather_rain_prob: string
  weather_confidence: string

  // Water Balance View
  water_error_title: string
  water_title: string
  water_awd_drying_ok: string
  water_awd_irrigation_needed: string
  water_awd_desc_ok: string
  water_awd_desc_needed: string
  water_deficit_label: string
  water_et0_label: string
  water_kc_label: string
  water_etc_label: string
  water_taw_label: string
  water_raw_label: string
  water_budget_heading: string

  // Flood Hazard View
  flood_error_title: string
  flood_title: string
  flood_not_applicable_title: string
  flood_not_applicable_desc: string
  flood_index_label: string
  flood_tier_label: string
  flood_early_harvest_label: string
  flood_early_harvest_trigger: string
  flood_early_harvest_safe: string

  // Provenance View
  prov_error_title: string
  prov_title: string
  prov_system_name: string
  prov_version: string
  prov_generated: string
  prov_datasets_heading: string
  prov_methods_heading: string
  prov_boundaries_heading: string
  prov_col_dataset: string
  prov_col_source: string
  prov_col_resolution: string
  prov_col_latency: string
  prov_col_status: string

  // Footer
  footer_platform_desc: string
  footer_sub: string
  footer_partners: string
  footer_version: string
  footer_disclaimer: string
}

export const translations: Record<Language, TranslationDictionary> = {
  bn: {
    // Brand & Accessibility
    brand_name: 'ঋতুকাস্ট',
    brand_tagline: 'Ritucast',
    skip_to_content: 'মূল বিষয়বস্তুতে সরাসরি প্রবেশ (Skip to main content)',
    home_aria_label: 'ঋতুকাস্ট হোমপেইজে যান',

    // Navigation
    nav_advisories: 'পরামর্শ কেন্দ্র',
    nav_weather: 'আবহাওয়া',
    nav_water_balance: 'মাটির আর্দ্রতা (AWD)',
    nav_flood: 'হাওড় বন্যা ঝুঁকি',
    nav_provenance: 'স্বচ্ছতা ও তথ্যসূত্র',
    nav_menu_open: 'মেনু খুলুন',
    nav_menu_close: 'মেনু বন্ধ করুন',

    // Status Badge
    status_checking: 'যাচাই হচ্ছে...',
    status_live: 'সচল (লাইভ)',
    status_live_title: 'সবগুলো ডেটাসেট ও অ্যানালিটিক্স সচল রয়েছে',
    status_degraded: 'সীমাবদ্ধ',
    status_degraded_title: 'কিছু নির্ভরতা অনুপস্থিত',

    // Theme & Language Controls
    theme_label: 'থিম পরিবর্তন',
    theme_system: 'সিস্টেম',
    theme_light: 'লাইট',
    theme_dark: 'ডার্ক',
    lang_label: 'ভাষা নির্বাচন',
    lang_bn: 'বাংলা',
    lang_en: 'English',

    // Context Selector
    context_section_label: 'Context Selection',
    division_label: 'বিভাগ:',
    district_label: 'জেলা:',
    upazila_label: 'উপজেলা (পাইলট অঞ্চল):',
    upazila_field_label: 'উপজেলা:',
    search_placeholder: 'উপজেলা বা জেলা অনুসন্ধান করুন...',
    search_no_results: 'কোনো উপজেলা বা জেলা পাওয়া যায়নি',
    search_type_upazila: 'উপজেলা',
    search_type_district: 'জেলা',
    search_hint: 'বাছাই করতে ↑ / ↓ চাপুন, নির্বাচন করতে Enter, বন্ধ করতে Esc',
    all_divisions: 'সকল বিভাগ (৮টি)',
    select_division: 'বিভাগ নির্বাচন করুন',
    select_district: 'জেলা নির্বাচন করুন',
    select_upazila: 'উপজেলা নির্বাচন করুন',
    search_filter_active: 'অনুসন্ধানের ফলাফল',
    clear_search: 'মুছুন',
    pilot_badge: 'পাইলট টেস্টবেড',
    national_badge: 'জাতীয় কভারেজ',
    upazila_count_suffix: 'টি উপজেলা',
    crop_label: 'ফসল (ক্যালিব্রেটেড):',
    crop_calibrated_badge: 'পূর্ণাঙ্গ ক্যালিব্রেশন',
    crop_regional_badge: 'আঞ্চলিক সহায়তা',
    crop_category_all: 'সকল ফসল',
    crop_category_cereals: 'দানাশস্য',
    crop_category_cash: 'অর্থকরী ফসল',
    crop_category_tubers: 'কন্দজাতীয় ফসল',
    crop_category_pulses: 'ডাল ফসল',
    crop_category_oilseeds: 'তৈলবীজ',
    crop_category_vegetables: 'শাকসবজি',
    crop_category_fruits: 'ফলমূল',
    date_range_label: 'বিশ্লেষণ সময়কাল (কাস্টম তারিখ সীমা):',
    start_date_label: 'শুরুর তারিখ:',
    end_date_label: 'শেষের তারিখ:',
    date_preset_7d: 'বিগত ৭ দিন (ডিফল্ট)',
    date_preset_14d: 'বিগত ১৪ দিন',
    date_preset_30d: 'বিগত ৩০ দিন',
    date_default_notice: 'আজকের দিন বাদ দিয়ে বিগত ৭টি পূর্ণাঙ্গ দিনের রেকর্ড ডিফল্ট হিসেবে ধার্য।',
    date_latency_notice: 'স্যাটেলাইট বৃষ্টিপাত ও কৃষি আবহাওয়া উপাত্ত ২৪-৪৮ ঘণ্টা প্রক্রিয়াকরণ বিলম্বযুক্ত; বিগত পূর্ণাঙ্গ দিনের পর্যবেক্ষণ প্রদর্শিত হচ্ছে।',
    date_err_start_after_end: 'শুরুর তারিখ শেষের তারিখের চেয়ে পরবর্তী হতে পারবে না।',
    date_err_future: 'আজ বা ভবিষ্যতের তারিখ নির্বাচন করা যাবে না (কেবল বিগত পূর্ণাঙ্গ দিন প্রযোজ্য)।',
    planting_date_label: 'বপন / রোপণের তারিখ (ঐচ্ছিক):',
    planting_date_hint: 'বপনের তারিখ দিলে বৃদ্ধির পর্যায় স্বয়ংক্রিয়ভাবে হিসাব করা হবে।',
    growth_stage_manual: 'সরাসরি পর্যায় নির্বাচন',
    growth_stage_derived: 'রোপণ তারিখ থেকে অনুমিত',
    stage_label: 'ফসলের বৃদ্ধির বর্তমান পর্যায় (DEC-17):',
    refresh_btn: 'বিশ্লেষণ হালনাগাদ',
    refresh_loading: 'লোড হচ্ছে...',
    refresh_aria_label: 'হালনাগাদ তথ্য আনুন',
    current_zone: 'বর্তমান অঞ্চল:',
    primary_risk_label: 'মূল প্রাকৃতিক ঝুঁকি:',
    primary_risk_drought: 'ভূগর্ভস্থ পানির ঘাটতি ও খরা',
    primary_risk_flood: 'আকস্মিক বন্যা',
    gating_verified: 'প্রসঙ্গ-ভিত্তিক যাচাই (DEC-17): সক্রিয় ও সম্পূর্ণ',
    zone_barind: 'বরেন্দ্র',
    zone_haor: 'হাওড়',

    // Growth Stages
    stage_tillering: 'কুশি পর্যায় (বৃদ্ধি)',
    stage_booting: 'থোর পর্যায় (গর্ভকাল)',
    stage_flowering: 'ফুল ফোটা পর্যায় (পরাগায়ন)',
    stage_dough: 'দুধ/দানা গঠন পর্যায়',
    stage_maturity: 'পাকা পর্যায় (কর্তন)',

    // Advisory Hub
    advisory_error_title: 'পরামর্শ লোড করা সম্ভব হয়নি',
    suppression_title: 'পরামর্শ সাময়িকভাবে স্থগিত (স্বয়ংক্রিয় সুরক্ষা নীতি DEC-10)',
    suppression_body:
      'আবহাওয়া পূর্বাভাস মডেলসমূহের মধ্যকার অনিশ্চয়তা (≥ 50%) অথবা সংগৃহীত উপাত্তের সময়কাল ৩৬ ঘণ্টার বেশি হওয়ায় কৃষকদের সুরক্ষার্থে এই পরামর্শটি স্থগিত করা হয়েছে। সেচ বা কর্তন সংক্রান্ত যেকোনো জরুরি সিদ্ধান্তে স্থানীয় উপসহকারী কৃষি কর্মকর্তার (SAAO) সরাসরি পরামর্শ গ্রহণ করুন।',
    tier_1_title: '১ম স্তর: প্রত্যক্ষ পর্যবেক্ষণ (Tier 1)',
    tier_2_title: '২য় স্তর: হিসাবকৃত সূচক (Tier 2)',
    tier_3_title: '৩য় স্তর: আবহাওয়া পূর্বাভাস (Tier 3)',
    tier_4_title: 'চতুর্থ স্তর: কার্যকর পরামর্শ (Tier 4)',
    rule_id_prefix: 'বিধি নং:',
    action_items_heading: 'করণীয় পদক্ষেপসমূহ:',
    rationale_heading: 'বৈজ্ঞানিক ও অর্থনৈতিক বিশ্লেষণ:',
    pumping_savings_prefix: 'সম্ভাব্য জ্বালানি ও সেচ খরচ সাশ্রয়:',
    field_verification_heading: 'মাঠ যাচাইয়ের বাধ্যবাধকতা:',
    supporting_tiers_heading: 'পরামর্শের ৩-স্তর ভিত্তি ও প্রমাণ বিশ্লেষণ (DEC-08)',
    tier_1_source_label: 'উৎস: NASA POWER / বিএমডি রাডার ও বৃষ্টিমাপক',
    tier_1_rainfall_7d: 'বিগত ৭ দিনের মোট বৃষ্টি:',
    tier_2_method_label: 'পদ্ধতি: FAO-56 পেনম্যান-মন্টিথ ET₀ ও মাটির আর্দ্রতা ঘাটতি (Dₜ)',
    tier_2_deficit_label: 'বর্তমান ঘাটতি (Dₜ):',
    tier_3_model_label: 'মডেল: ECMWF IFS / NOAA GFS এনসেম্বল',
    tier_3_rain_prob_label: 'বৃষ্টির সম্ভাবনা (৪৮ ঘণ্টা):',
    hazard_eval_heading: 'পরিবেশগত চরম ঝুঁকি মূল্যায়ন (Physical Hazard Evaluation)',
    hazard_eval_overall: 'সামগ্রিক ঝুঁকি:',
    hazard_domain: 'ঝুঁকির ক্ষেত্র',
    hazard_tier: 'ঝুঁকির মাত্রা',
    hazard_metric: 'পরিমাপক মান',
    hazard_threshold: 'নির্ধারিত সীমা',
    hazard_action: 'পদক্ষেপ আবশ্যক?',
    hazard_action_warranted: 'হ্যাঁ (পদক্ষেপ নিন)',
    hazard_action_not_warranted: 'না (স্বাভাবিক)',
    scientific_disclaimer_heading: 'বিজ্ঞানভিত্তিক সতর্কতা (DEC-06):',

    // Weather View
    weather_error_title: 'আবহাওয়া তথ্য লোড করা যায়নি',
    weather_obs_title: 'বিগত ২৪ ঘণ্টার প্রত্যক্ষ আবহাওয়া পর্যবেক্ষণ (Tier 1)',
    weather_obs_source: 'উৎস:',
    weather_fcst_title: 'আগামী ৭২ ঘণ্টার সম্ভাব্যতাভিত্তিক আবহাওয়া পূর্বাভাস (Tier 3)',
    weather_fcst_models: 'এনসেম্বল মডেল:',
    weather_max_temp: 'সর্বোচ্চ তাপমাত্রা',
    weather_min_temp: 'সর্বনিম্ন তাপমাত্রা',
    weather_precip_24h: 'বিগত ২৪ ঘণ্টার বৃষ্টিপাত',
    weather_solar_rad: 'সৌর বিকিরণ',
    weather_rh_mean: 'গড় আপেক্ষিক আর্দ্রতা',
    weather_wind_speed: 'বাতাসের গতিবেগ',
    weather_lead_time: 'অগ্রবর্তী সময়কাল',
    weather_qpf: 'বৃষ্টির পরিমাণ (QPF)',
    weather_rain_prob: 'বৃষ্টির সম্ভাবনা',
    weather_confidence: 'নির্ভরযোগ্যতা',

    // Water Balance View
    water_error_title: 'মাটির আর্দ্রতা ও বাষ্পীভবন তথ্য পাওয়া যায়নি',
    water_title: 'মৃত্তিকা পানি ঘাটতি ও AWD সেচ ব্যবস্থাপনা সূচক (Tier 2)',
    water_awd_drying_ok: 'AWD শুকানো অনুমোদিত - সেচ অপ্রয়োজনীয়',
    water_awd_irrigation_needed: 'সেচ প্রয়োগ অবিলম্বে আবশ্যক',
    water_awd_desc_ok:
      'মাটির বর্তমান পানি ঘাটতি নিরাপদে শুকানোর অনুমোদিত সীমার (RAW) মধ্যে রয়েছে। এখন সেচ বন্ধ রেখে ডিজেল ও বিদ্যুৎ খরচ বাঁচান।',
    water_awd_desc_needed:
      'মাটির পানি ঘাটতি অনুমোদিত সীমা অতিক্রম করেছে। কুশি ও ফলন সুরক্ষায় ৫ সেমি উচ্চতায় অবিলম্বে সেচ প্রদান করুন।',
    water_deficit_label: 'শিকড় অঞ্চলের পানি ঘাটতি নির্দেশক',
    water_et0_label: 'রেফারেন্স বাষ্পীভবন (FAO-56 ET₀)',
    water_kc_label: 'ফসলের সহগ সূচক (K꜀)',
    water_etc_label: 'ফসলের প্রস্বেদন চাহিদা (ET꜀)',
    water_taw_label: 'মোট ধারণক্ষম পানি (TAW)',
    water_raw_label: 'সহজে ব্যবহারযোগ্য পানি (RAW)',
    water_budget_heading: 'দৈনিক মৃত্তিকা পানি বাজেট বিশ্লেষণ',

    // Flood Hazard View
    flood_error_title: 'বন্যা ঝুঁকি নির্দেশক পাওয়া যায়নি',
    flood_title: 'হাওড় অববাহিকা আকস্মিক বন্যা ঝুঁকি সূচক (Tier 2)',
    flood_not_applicable_title: 'হাওড় আকস্মিক বন্যা ঝুঁকি সূচক প্রযোজ্য নয়',
    flood_not_applicable_desc:
      'নির্বাচিত উপজেলাটি উচ্চ বরেন্দ্র অঞ্চলের (AEZ-26) অন্তর্গত। এখানে ভূগর্ভস্থ পানির ঘাটতি ও খরা প্রধান ঝুঁকি; হাওড় নদী অববাহিকার আকস্মিক বন্যা ঝুঁকি শুধুমাত্র সিলেট বিভাগের হাওড় অঞ্চলের (AEZ-21: তাহিরপুর, সুনামগঞ্জ সদর) জন্য কার্যকর।',
    flood_index_label: 'আকস্মিক বন্যা ঝুঁকি সূচক (I_flood)',
    flood_tier_label: 'ঝুঁকির মাত্রা',
    flood_early_harvest_label: 'জরুরি আগাম কর্তন সতর্কতা',
    flood_early_harvest_trigger: 'সতর্কতা সক্রিয়: ৮০% পরিপক্ব ধান দ্রুত কাটুন',
    flood_early_harvest_safe: 'স্বাভাবিক: আগাম কর্তনের প্রয়োজন নেই',

    // Provenance View
    prov_error_title: 'সিস্টেম স্বচ্ছতা ও তথ্যসূত্র পাওয়া যায়নি',
    prov_title: 'সিস্টেম স্বচ্ছতা, তথ্যসূত্র ও বৈজ্ঞানিক ভিত্তি (DEC-08/18)',
    prov_system_name: 'প্ল্যাটফর্মের নাম',
    prov_version: 'সংস্করণ',
    prov_generated: 'উপাত্ত উৎপাদনের সময়কাল (BST)',
    prov_datasets_heading: 'সংগৃহীত উপগ্রহ ও আবহাওয়া ডেটাসেটসমূহ',
    prov_methods_heading: 'প্রয়োগকৃত বিজ্ঞানভিত্তিক অ্যালগরিদম ও রেফারেন্স মান',
    prov_boundaries_heading: 'বৈজ্ঞানিক সীমানা ও দায়িত্ব সীমাবদ্ধতা (DEC-06)',
    prov_col_dataset: 'ডেটাসেট',
    prov_col_source: 'উৎস সংস্থা',
    prov_col_resolution: 'রেজোলিউশন',
    prov_col_latency: 'দেরি (ঘণ্টা)',
    prov_col_status: 'অবস্থা',

    // Footer
    footer_platform_desc: 'ঋতুকাস্ট (Ritucast) • বাংলাদেশ কৃষি আবহাওয়া প্ল্যাটফর্ম',
    footer_sub: 'উপগ্রহ পর্যবেক্ষণ, সংখ্যাসূচক আবহাওয়া পূর্বাভাস ও মৃত্তিকা আর্দ্রতা মডেলের সমন্বয়।',
    footer_partners: 'সহযোগী সংস্থা: কৃষি সম্প্রসারণ অধিদপ্তর (DAE) • বিআরআরআই (BRRI) • বিএমডি (BMD)',
    footer_version: 'সংস্করণ: ১.০.০ (ফেজ ১১ ফ্রন্টএন্ড কোর) • লাইসেন্স: ওপেন অ্যাক্সেস',
    footer_disclaimer:
      'সতর্কতা: ঋতুকাস্ট একটি বৈজ্ঞানিক সিদ্ধান্ত সহায়তা ব্যবস্থা। মাঠে যেকোনো চূড়ান্ত পদক্ষেপ নেওয়ার পূর্বে আইল ও মাটির রস সরাসরি পরীক্ষা করুন।',
  },

  en: {
    // Brand & Accessibility
    brand_name: 'Ritucast',
    brand_tagline: 'ঋতুকাস্ট',
    skip_to_content: 'Skip to main content',
    home_aria_label: 'Go to Ritucast Home',

    // Navigation
    nav_advisories: 'Advisory Hub',
    nav_weather: 'Weather Feed',
    nav_water_balance: 'Soil Moisture (AWD)',
    nav_flood: 'Haor Flood Hazard',
    nav_provenance: 'Transparency & Data',
    nav_menu_open: 'Open navigation menu',
    nav_menu_close: 'Close navigation menu',

    // Status Badge
    status_checking: 'Checking...',
    status_live: 'Live (Active)',
    status_live_title: 'All verified datasets and analytical pipelines are operational',
    status_degraded: 'Degraded',
    status_degraded_title: 'Some upstream feeds or dependencies are degraded',

    // Theme & Language Controls
    theme_label: 'Switch theme',
    theme_system: 'System',
    theme_light: 'Light',
    theme_dark: 'Dark',
    lang_label: 'Select language',
    lang_bn: 'বাংলা',
    lang_en: 'English',

    // Context Selector
    context_section_label: 'Context Selection',
    division_label: 'Division:',
    district_label: 'District:',
    upazila_label: 'Upazila (Pilot Region):',
    upazila_field_label: 'Upazila:',
    search_placeholder: 'Search Upazila or District...',
    search_no_results: 'No matching upazila or district found',
    search_type_upazila: 'Upazila',
    search_type_district: 'District',
    search_hint: 'Use ↑ / ↓ to navigate, Enter to select, Esc to close',
    all_divisions: 'All Divisions (8)',
    select_division: 'Select Division',
    select_district: 'Select District',
    select_upazila: 'Select Upazila',
    search_filter_active: 'Search Results',
    clear_search: 'Clear',
    pilot_badge: 'Pilot Testbed',
    national_badge: 'National Coverage',
    upazila_count_suffix: 'Upazilas',
    crop_label: 'Active Crop (Calibrated):',
    crop_calibrated_badge: 'Full Calibration',
    crop_regional_badge: 'Regional Support',
    crop_category_all: 'All Crops',
    crop_category_cereals: 'Cereals & Grains',
    crop_category_cash: 'Cash Crops',
    crop_category_tubers: 'Tubers & Roots',
    crop_category_pulses: 'Pulses & Legumes',
    crop_category_oilseeds: 'Oilseeds',
    crop_category_vegetables: 'Vegetables',
    crop_category_fruits: 'Fruits',
    date_range_label: 'Analysis Time Window (Custom Date Range):',
    start_date_label: 'Start Date:',
    end_date_label: 'End Date:',
    date_preset_7d: 'Previous 7 Days (Default)',
    date_preset_14d: 'Previous 14 Days',
    date_preset_30d: 'Previous 30 Days',
    date_default_notice: 'Defaults to previous seven complete days, excluding today.',
    date_latency_notice: 'Satellite and gridded meteorological datasets have a 24-48h processing latency; reporting reflects completed days.',
    date_err_start_after_end: 'Start date cannot be after end date.',
    date_err_future: 'Future or current dates cannot be selected (historical complete days only).',
    planting_date_label: 'Planting / Sowing Date (Optional):',
    planting_date_hint: 'Growth stage will be automatically estimated from planting date.',
    growth_stage_manual: 'Manual Stage Selection',
    growth_stage_derived: 'Derived from Planting Date',
    stage_label: 'Crop Growth Stage (DEC-17):',
    refresh_btn: 'Refresh Analysis',
    refresh_loading: 'Loading...',
    refresh_aria_label: 'Fetch updated agronomic intelligence',
    current_zone: 'Current Agro-Zone:',
    primary_risk_label: 'Primary Natural Hazard:',
    primary_risk_drought: 'Groundwater Deficit & Drought',
    primary_risk_flood: 'Flash Flood',
    gating_verified: 'Contextual Gating (DEC-17): Active & Complete',
    zone_barind: 'Barind',
    zone_haor: 'Haor',

    // Growth Stages
    stage_tillering: 'Tillering (Vegetative Growth)',
    stage_booting: 'Booting (Reproductive Phase)',
    stage_flowering: 'Flowering (Anthesis / Pollination)',
    stage_dough: 'Dough Stage (Grain Filling)',
    stage_maturity: 'Maturity (Harvest Ready)',

    // Advisory Hub
    advisory_error_title: 'Unable to Load Advisory Guidance',
    suppression_title: 'Advisory Temporarily Suppressed (Safety Policy DEC-10)',
    suppression_body:
      'Advisory generation is temporarily suppressed because numerical weather prediction ensemble spread exceeds 50% or sensor latency exceeds 36 hours. To safeguard crops, consult your local Sub-Assistant Agriculture Officer (SAAO) before critical field interventions.',
    tier_1_title: 'Tier 1: Sensor Observations (Tier 1)',
    tier_2_title: 'Tier 2: Derived Agronomic Indicators (Tier 2)',
    tier_3_title: 'Tier 3: Probabilistic Weather Forecasts (Tier 3)',
    tier_4_title: 'Tier 4: Actionable Advisory (Tier 4)',
    rule_id_prefix: 'Rule ID:',
    action_items_heading: 'Action Directives:',
    rationale_heading: 'Scientific & Economic Rationale:',
    pumping_savings_prefix: 'Estimated Pumping & Fuel Savings:',
    field_verification_heading: 'Mandatory Field Inspection:',
    supporting_tiers_heading: '3-Tier Scientific Evidentiary Foundation (DEC-08)',
    tier_1_source_label: 'Source: NASA POWER / BMD Weather Station & Radar',
    tier_1_rainfall_7d: 'Preceding 7-Day Cumulative Rainfall:',
    tier_2_method_label: 'Method: FAO-56 Penman-Monteith ET₀ & Soil Water Deficit (Dₜ)',
    tier_2_deficit_label: 'Current Soil Water Deficit (Dₜ):',
    tier_3_model_label: 'Model: ECMWF IFS / NOAA GFS Multi-Model Ensemble',
    tier_3_rain_prob_label: '48h Rainfall Probability:',
    hazard_eval_heading: 'Physical Hazard Evaluation & Extreme Risk Bounds',
    hazard_eval_overall: 'Overall Hazard:',
    hazard_domain: 'Hazard Domain',
    hazard_tier: 'Hazard Level',
    hazard_metric: 'Observed Metric',
    hazard_threshold: 'Physical Threshold',
    hazard_action: 'Action Warranted?',
    hazard_action_warranted: 'Yes (Intervention Needed)',
    hazard_action_not_warranted: 'No (Within Safe Range)',
    scientific_disclaimer_heading: 'Scientific Guardrails (DEC-06):',

    // Weather View
    weather_error_title: 'Unable to Load Weather Feed',
    weather_obs_title: 'Preceding 24h Sensor Observations (Tier 1)',
    weather_obs_source: 'Source:',
    weather_fcst_title: 'Next 72-Hour Probabilistic Forecasts (Tier 3)',
    weather_fcst_models: 'Ensemble Feeds:',
    weather_max_temp: 'Maximum Temp',
    weather_min_temp: 'Minimum Temp',
    weather_precip_24h: 'Preceding 24h Rain',
    weather_solar_rad: 'Solar Radiation',
    weather_rh_mean: 'Mean Relative Humidity',
    weather_wind_speed: 'Wind Velocity',
    weather_lead_time: 'Lead Time',
    weather_qpf: 'Quantitative Precip (QPF)',
    weather_rain_prob: 'Rain Probability',
    weather_confidence: 'Confidence',

    // Water Balance View
    water_error_title: 'Unable to Retrieve Soil Moisture & Water Balance Data',
    water_title: 'Soil Water Deficit & AWD Irrigation Scheduling (Tier 2)',
    water_awd_drying_ok: 'AWD Drying Permissible — Irrigation Postponed',
    water_awd_irrigation_needed: 'Immediate Irrigation Application Required',
    water_awd_desc_ok:
      'Current root-zone soil water deficit remains within the permissible drying threshold (RAW). Cease tubewell pumping to conserve diesel and electricity.',
    water_awd_desc_needed:
      'Soil water deficit has surpassed the permissible threshold. Apply supplemental irrigation to 5 cm depth to protect panicle initiation and yield.',
    water_deficit_label: 'Root Zone Soil Water Deficit Indicator',
    water_et0_label: 'Reference Evapotranspiration (FAO-56 ET₀)',
    water_kc_label: 'Crop Coefficient (K꜀)',
    water_etc_label: 'Crop Water Demand (ET꜀)',
    water_taw_label: 'Total Available Water (TAW)',
    water_raw_label: 'Readily Available Water (RAW)',
    water_budget_heading: 'Daily Root-Zone Water Budget Simulation',

    // Flood Hazard View
    flood_error_title: 'Flood Hazard Intelligence Unavailable',
    flood_title: 'Haor Basin Flash Flood Hazard Index (Tier 2)',
    flood_not_applicable_title: 'Haor Flash Flood Hazard Index Not Applicable',
    flood_not_applicable_desc:
      'The selected upazila is located within the High Barind Tract (AEZ-26), where groundwater depletion and drought are primary risks. Transboundary flash flood indices apply exclusively to the Haor Basin (AEZ-21: Tahirpur, Sunamganj Sadar).',
    flood_index_label: 'Flash Flood Hazard Index (I_flood)',
    flood_tier_label: 'Hazard Level',
    flood_early_harvest_label: 'Emergency Early Harvest Trigger',
    flood_early_harvest_trigger: 'Trigger Activated: Accelerate harvesting of 80% ripe Boro crop',
    flood_early_harvest_safe: 'Normal Condition: Emergency harvest trigger not active',

    // Provenance View
    prov_error_title: 'Provenance & Data Lineage Unavailable',
    prov_title: 'System Provenance, Data Lineage & Scientific Boundaries (DEC-08/18)',
    prov_system_name: 'Platform Designation',
    prov_version: 'Architecture Version',
    prov_generated: 'Generation Timestamp (BST)',
    prov_datasets_heading: 'Ingested Satellite Observations & Upstream Datasets',
    prov_methods_heading: 'Applied Scientific Methodologies & Reference Standards',
    prov_boundaries_heading: 'Scientific Scope & Liability Guardrails (DEC-06)',
    prov_col_dataset: 'Dataset',
    prov_col_source: 'Provider Agency',
    prov_col_resolution: 'Resolution',
    prov_col_latency: 'Latency (h)',
    prov_col_status: 'State',

    // Footer
    footer_platform_desc: 'Ritucast • Bangladesh Agro-Meteorological Intelligence Platform',
    footer_sub: 'Synthesizing satellite observations, numerical weather predictions, and soil-moisture physics.',
    footer_partners: 'Partner Institutions: Department of Agricultural Extension (DAE) • BRRI • BMD',
    footer_version: 'Version: 1.0.0 (Phase 11 Frontend Core) • License: Open Access',
    footer_disclaimer:
      'Safety Disclaimer: Ritucast is an evidence-based decision-support system. Inspect bunds and soil moisture in the field before executing final agronomic actions.',
  },
}

export const STAGE_TRANSLATIONS: Record<Language, Record<string, string>> = {
  bn: {
    Tillering: 'কুশি পর্যায় (বৃদ্ধি)',
    Booting: 'থোর পর্যায় (গর্ভকাল)',
    Flowering: 'ফুল ফোটা পর্যায় (পরাগায়ন)',
    Dough: 'দুধ/দানা গঠন পর্যায়',
    Maturity: 'পাকা পর্যায় (কর্তন)',
  },
  en: {
    Tillering: 'Tillering (Vegetative Growth)',
    Booting: 'Booting (Reproductive Phase)',
    Flowering: 'Flowering (Anthesis / Pollination)',
    Dough: 'Dough Stage (Grain Filling)',
    Maturity: 'Maturity (Harvest Ready)',
  },
}
