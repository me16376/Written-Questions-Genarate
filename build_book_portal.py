# -*- coding: utf-8 -*-
"""
Build Authentic Book/Guidebook View for somaj-seba-written.html
Transforms the dashboard/card interface into a realistic, elegant, print-quality Book layout:
- Looks and reads like a printed Bangladesh Job Guidebook (Professors / MP3 / Oracle style)
- Continuous book page layout with book headers, chapter rules, and running titles
- Real Bengali numbering (১।, ২।, ৩।...) and English numbering (1., 2., 3....)
- Two-Column Guidebook mode toggle (২-কলাম গাইড বই মোড)
- Reading font size adjusters (ছোট / স্বাভাবিক / বড়)
- Practice / Self-test mode (উত্তর লুকান / দেখান)
- Zero emojis anywhere in the interface
"""
import json
import os

workspace_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.join(workspace_dir, "somaj-seba-written")

# Collect all json data from somaj-seba-written
all_data = {
    "Bangla": {},
    "English": {},
    "Math": {},
    "Gk": {}
}

total_count = 0
for folder in ["Bangla", "English", "Math", "Gk"]:
    folder_path = os.path.join(source_dir, folder)
    if not os.path.exists(folder_path):
        continue
    for fname in sorted(os.listdir(folder_path)):
        if fname.endswith(".json"):
            key = fname.replace(".json", "")
            fpath = os.path.join(folder_path, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_data[folder][key] = data
                total_count += len(data.get("items", []))

print(f"Loaded all data. Total questions: {total_count}")
json_payload = json.dumps(all_data, ensure_ascii=False)

html_code = f"""<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>সমাজসেবা অধিদপ্তর ও লিখিত পরীক্ষার পূর্ণাঙ্গ সহায়িকা (বই সংস্করণ)</title>
  <meta name="description" content="সমাজসেবা অধিদপ্তরসহ সকল সরকারি নিয়োগ লিখিত পরীক্ষার জন্য বইয়ের মতো সম্পূর্ণ প্রশ্নব্যাংক ও সমাধানমালা।">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anek+Bangla:wght@400;500;600;700&family=Hind+Siliguri:wght@400;500;600;700&family=Noto+Sans+Bengali:wght@400;500;600;700&family=Noto+Serif+Bengali:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Tiro+Bangla&display=swap" rel="stylesheet">
  <style>
    :root {{
      --font-book-bn: 'Noto Sans Bengali', sans-serif;
      --font-book-en: 'Plus Jakarta Sans', Georgia, serif;
      
      /* Book Reading Palette */
      --book-desk-bg: #f1f5f9;
      --book-paper: #ffffff;
      --book-ink: #111827;
      --book-ink-muted: #4b5563;
      --book-rule: #cbd5e1;
      --book-accent: #0f172a;
      
      /* Guidebook ink tones */
      --ink-q: #0f172a;
      --ink-ans: #166534;
      --ink-ans-en: #1e40af;
      --ink-note: #6b7280;
      
      --base-font-size: 16.5px;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-book-bn);
      background-color: var(--book-desk-bg);
      color: var(--book-ink);
      line-height: 1.65;
      min-height: 100vh;
      font-size: var(--base-font-size);
    }}

    /* Top Book Navigation & Controls Bar (Sticky on Desktop) */
    .top-book-bar {{
      background: #1e293b;
      color: #f8fafc;
      padding: 12px 20px;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
    }}

    .top-bar-inner {{
      max-width: 1300px;
      width: 100%;
      margin: 0 auto;
      padding: 0 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }}

    .book-brand-title {{
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: 0.3px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .book-brand-badge {{
      background: #334155;
      color: #94a3b8;
      font-size: 0.8rem;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 600;
    }}

    .book-control-tools {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .font-picker-group {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #334155;
      border: 1px solid #475569;
      padding: 3px 8px;
      border-radius: 6px;
    }}

    .font-picker-label {{
      font-size: 0.84rem;
      color: #94a3b8;
      font-weight: 600;
    }}

    .font-picker-select {{
      background: #1e293b;
      border: 1px solid #475569;
      color: #ffffff;
      padding: 4px 8px;
      border-radius: 4px;
      font-family: inherit;
      font-size: 0.85rem;
      cursor: pointer;
      outline: none;
    }}

    .font-picker-select:focus {{
      border-color: #0284c7;
    }}

    .tool-btn {{
      background: #334155;
      border: 1px solid #475569;
      color: #f8fafc;
      padding: 6px 12px;
      border-radius: 6px;
      font-family: var(--font-book-bn);
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: background 0.15s ease;
    }}

    .tool-btn:hover {{
      background: #475569;
    }}

    .tool-btn.active {{
      background: #0284c7;
      border-color: #0284c7;
      color: #ffffff;
    }}

    .font-zoom-group {{
      display: flex;
      border: 1px solid #475569;
      border-radius: 6px;
      overflow: hidden;
    }}

    .font-zoom-btn {{
      background: #334155;
      border: none;
      color: #f8fafc;
      padding: 6px 10px;
      font-size: 0.85rem;
      font-weight: 700;
      cursor: pointer;
      border-right: 1px solid #475569;
    }}

    .font-zoom-btn:last-child {{
      border-right: none;
    }}

    .font-zoom-btn:hover {{
      background: #475569;
    }}

    /* Chapter & Subject Navigation Bar */
    .chapters-nav-bar {{
      background: #ffffff;
      border-bottom: 1px solid var(--book-rule);
      padding: 12px 0;
    }}

    .chapters-nav-inner {{
      max-width: 1300px;
      width: 100%;
      margin: 0 auto;
      padding: 0 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .subject-tabs {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .subject-tab {{
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      color: #334155;
      padding: 8px 16px;
      border-radius: 6px;
      font-family: var(--font-book-bn);
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .subject-tab:hover {{
      background: #e2e8f0;
    }}

    .subject-tab.active {{
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
    }}

    .topics-subnav {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px 10px;
      padding: 6px 0;
    }}

    .topic-link {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      color: #334155;
      padding: 6px 14px;
      border-radius: 6px;
      font-family: var(--font-book-bn);
      font-size: 0.92rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}

    .topic-link:hover {{
      background: #e2e8f0;
      color: #0f172a;
      border-color: #94a3b8;
    }}

    .topic-link.active {{
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
      font-weight: 700;
    }}

    .topic-pill-count {{
      font-size: 0.8rem;
      padding: 2px 7px;
      border-radius: 10px;
      background: #e2e8f0;
      color: #475569;
      font-weight: 700;
    }}

    .topic-link.active .topic-pill-count {{
      background: #334155;
      color: #f8fafc;
    }}

    /* Search bar inside navigation */
    .book-search-row {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 4px;
    }}

    .book-search-input {{
      width: 100%;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 8px 14px;
      font-family: var(--font-book-bn);
      font-size: 0.92rem;
      color: #0f172a;
      outline: none;
    }}

    .book-search-input:focus {{
      border-color: #0284c7;
      background: #ffffff;
    }}

    /* Main Book Layout Wrapper */
    .book-viewport {{
      max-width: 1300px;
      width: 100%;
      margin: 18px auto 60px;
      padding: 0 12px;
    }}

    /* The Authentic Book Page (বইয়ের পাতা) */
    .book-page {{
      width: 100%;
      background: var(--book-paper);
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
      padding: 44px 50px;
      min-height: 800px;
      position: relative;
    }}

    /* Running Header of Book Page */
    .book-page-running-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1.5px solid #1f2937;
      padding-bottom: 8px;
      margin-bottom: 24px;
      font-size: 0.85rem;
      color: #4b5563;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .running-book-title {{
      font-weight: 700;
      color: #111827;
    }}

    /* Chapter Title Block */
    .book-chapter-title-box {{
      text-align: center;
      margin-bottom: 28px;
      padding-bottom: 16px;
      border-bottom: 1px dashed #d1d5db;
    }}

    .book-chapter-badge {{
      font-size: 0.82rem;
      font-weight: 700;
      color: #4b5563;
      letter-spacing: 1px;
      text-transform: uppercase;
      display: block;
      margin-bottom: 4px;
    }}

    .book-chapter-title {{
      font-size: 1.85rem;
      font-weight: 700;
      color: #111827;
      margin-bottom: 6px;
    }}

    .book-chapter-desc {{
      font-size: 0.96rem;
      color: #4b5563;
      max-width: 780px;
      margin: 0 auto 8px;
      line-height: 1.55;
    }}

    .book-exam-hint {{
      font-size: 0.9rem;
      font-weight: 600;
      color: #92400e;
      background: #fffbeb;
      border: 1px solid #fef3c7;
      padding: 6px 16px;
      border-radius: 4px;
      display: inline-block;
      margin-top: 4px;
    }}

    /* Book Questions Flow (বইয়ের প্রশ্ন ও উত্তর তালিকা) */
    .book-content-stream {{
      display: block;
    }}

    /* Two-Column Mode (২-কলাম গাইড বই স্টাইল) */
    .book-content-stream.two-column {{
      column-count: 2;
      column-gap: 40px;
      column-rule: 1px solid #e5e7eb;
    }}

    /* Single Book Question Block */
    .book-entry {{
      padding: 12px 0 14px;
      border-bottom: 1px solid #f1f5f9;
      break-inside: avoid;
      page-break-inside: avoid;
    }}

    .book-entry:last-child {{
      border-bottom: none;
    }}

    .entry-header-row {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 4px;
    }}

    .entry-num {{
      font-weight: 700;
      color: #111827;
      margin-right: 6px;
      font-size: 1.05rem;
    }}

    .entry-bookmark-btn {{
      background: none;
      border: none;
      cursor: pointer;
      color: #d1d5db;
      font-size: 0.95rem;
      padding: 0 4px;
      line-height: 1;
      transition: color 0.15s ease;
    }}

    .entry-bookmark-btn:hover, .entry-bookmark-btn.bookmarked {{
      color: #d97706;
    }}

    .entry-question-text {{
      font-size: 1.06rem;
      font-weight: 700;
      color: var(--ink-q);
      line-height: 1.55;
    }}

    .entry-question-text.en {{
      font-family: var(--font-book-en);
      font-weight: 600;
    }}

    /* Book Answer Styling (খাতায় লেখার মতো বইয়ের প্রমিত রূপ) */
    .entry-answer-block {{
      margin-top: 5px;
      padding-left: 20px;
      position: relative;
    }}

    .entry-answer-block::before {{
      content: '';
      position: absolute;
      left: 6px;
      top: 6px;
      bottom: 6px;
      width: 2px;
      background: #cbd5e1;
    }}

    .entry-answer-text {{
      font-size: 1.02rem;
      color: var(--ink-ans);
      line-height: 1.6;
    }}

    .entry-answer-text.en {{
      font-family: var(--font-book-en);
      color: var(--ink-ans-en);
    }}

    .entry-sentence {{
      margin-top: 4px;
      color: #374151;
      font-size: 0.98rem;
    }}

    .entry-note {{
      font-size: 0.88rem;
      color: var(--ink-note);
      margin-top: 4px;
      line-height: 1.45;
    }}

    /* Math Solutions in Book Format */
    .math-solution-book {{
      background: #fbfbfa;
      border: 1px solid #e5e7eb;
      padding: 12px 16px;
      border-radius: 4px;
      margin-top: 6px;
    }}

    .math-step-line {{
      font-size: 0.98rem;
      line-height: 1.6;
      color: #1f2937;
    }}

    .math-ans-badge {{
      margin-top: 8px;
      font-weight: 700;
      color: #111827;
      border-top: 1px dashed #d1d5db;
      padding-top: 6px;
    }}

    /* Long Reading (ভাবসম্প্রসারণ / অনুচ্ছেদ / Essay in Book View) */
    .essay-book-box {{
      padding: 18px 0;
      border-bottom: 1.5px solid #e5e7eb;
    }}

    .essay-book-title {{
      font-size: 1.4rem;
      font-weight: 700;
      color: #111827;
      margin-bottom: 6px;
    }}

    .essay-book-points {{
      font-size: 0.9rem;
      color: #6b7280;
      margin-bottom: 12px;
      font-style: italic;
    }}

    .essay-book-body {{
      font-size: 1.04rem;
      line-height: 1.85;
      color: #1f2937;
      text-align: justify;
      white-space: pre-line;
      padding-left: 8px;
      border-left: 3px solid #94a3b8;
    }}

    /* Self-Test / Practice Mode (সম্পূর্ণ উত্তর গোপন - ব্লার ছাড়া কেবল প্রশ্ন দৃশ্যমান) */
    .hidden-answer {{
      display: none !important;
    }}

    .hidden-answer.revealed {{
      display: block !important;
      animation: fadeInAns 0.2s ease-in-out;
    }}

    @keyframes fadeInAns {{
      from {{
        opacity: 0;
        transform: translateY(-4px);
      }}
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}

    .practice-clickable {{
      cursor: pointer !important;
      border-radius: 4px;
      padding: 3px 6px;
      margin: -3px -6px 2px;
      transition: background-color 0.15s ease;
    }}

    .practice-clickable:hover {{
      background-color: #f1f5f9;
    }}

    /* Running Footer of Book Page */
    .book-page-footer {{
      margin-top: 40px;
      padding-top: 12px;
      border-top: 1px solid #e5e7eb;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.85rem;
      color: #6b7280;
    }}

    /* Empty state */
    .empty-book-state {{
      text-align: center;
      padding: 60px 20px;
      color: #6b7280;
    }}

    /* Print styles */
    @media print {{
      body {{
        background: #fff;
        color: #000;
        font-size: 14px;
      }}
      .top-book-bar, .chapters-nav-bar {{
        display: none !important;
      }}
      .book-viewport {{
        margin: 0;
        padding: 0;
        max-width: 100%;
      }}
      .book-page {{
        border: none;
        box-shadow: none;
        padding: 20px 0;
      }}
    }}

    @media (max-width: 768px) {{
      .book-page {{
        padding: 28px 20px;
      }}
      .book-content-stream.two-column {{
        column-count: 1;
      }}
      .book-chapter-title {{
        font-size: 1.45rem;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Sticky Reader Bar -->
  <header class="top-book-bar">
    <div class="top-bar-inner">
      <div class="book-brand-title">
        <span>সমাজসেবা অধিদপ্তর লিখিত সহায়িকা</span>
        <span class="book-brand-badge">বই সংস্করণ</span>
      </div>

      <div class="book-control-tools">
        <!-- Font Chooser Dropdown -->
        <div class="font-picker-group">
          <label for="bookFontSelectDropdown" class="font-picker-label">ফন্ট:</label>
          <select id="bookFontSelectDropdown" class="font-picker-select" onchange="changeBookFont(this.value)">
            <option value="'Noto Sans Bengali', sans-serif" selected>Noto Sans Bengali (ডিফল্ট)</option>
            <option value="'Hind Siliguri', sans-serif">Hind Siliguri</option>
            <option value="'Kalpurush', 'SolaimanLipi', sans-serif">Kalpurush / সোলাইমানলিপি</option>
            <option value="'Noto Serif Bengali', serif">Noto Serif Bengali (বই সেরিফ)</option>
            <option value="'Anek Bangla', sans-serif">Anek Bangla</option>
            <option value="'Tiro Bangla', serif">Tiro Bangla</option>
          </select>
        </div>

        <!-- Font Size Dropdown Number -->
        <div class="font-picker-group">
          <label for="bookFontSizeSelectDropdown" class="font-picker-label">সাইজ:</label>
          <select id="bookFontSizeSelectDropdown" class="font-picker-select" onchange="changeBookFontSize(this.value)">
            <option value="13">13 px</option>
            <option value="14">14 px</option>
            <option value="15">15 px</option>
            <option value="16">16 px</option>
            <option value="16.5" selected>16.5 px (ডিফল্ট)</option>
            <option value="17">17 px</option>
            <option value="18">18 px</option>
            <option value="19">19 px</option>
            <option value="20">20 px</option>
            <option value="22">22 px</option>
            <option value="24">24 px</option>
            <option value="26">26 px</option>
            <option value="28">28 px</option>
          </select>
        </div>

        <!-- 2 Column Guidebook Mode -->
        <button id="toggleColumnBtn" class="tool-btn" onclick="toggleColumnMode()">
          <span id="colModeText">২-কলাম মোড</span>
        </button>

        <!-- Self Test / Answer Mask -->
        <button id="togglePracticeBtn" class="tool-btn" onclick="togglePracticeMode()">
          <span id="practiceBtnText">উত্তর লুকান</span>
        </button>

        <!-- Bookmarks Filter -->
        <button id="toggleBookmarkFilterBtn" class="tool-btn" onclick="toggleBookmarkFilter()">
          <span id="bookmarkFilterText">বুকমার্ক দেখা</span>
        </button>

        <!-- Print -->
        <button class="tool-btn" onclick="window.print()">
          <span>প্রিন্ট / PDF</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Chapter & Subject Navigation Bar -->
  <nav class="chapters-nav-bar">
    <div class="chapters-nav-inner">
      <!-- Subject Tabs -->
      <div class="subject-tabs" id="subjectTabsContainer">
        <!-- Injected via JS -->
      </div>

      <!-- Topic Sub-navigation Links -->
      <div class="topics-subnav" id="topicsSubnavContainer">
        <!-- Injected via JS -->
      </div>

      <!-- Quick Search inside Chapter -->
      <div class="book-search-row">
        <input type="text" id="bookSearchInput" class="book-search-input" placeholder="অধ্যায়ের ভেতর শব্দ খুঁজুন (যেমন: তামার বিষ, সিংহাসন, preposition, শতকরা, বয়স্ক ভাতা, DSS...)" oninput="handleSearch()">
      </div>
    </div>
  </nav>

  <!-- Main Book Viewport -->
  <main class="book-viewport">
    <article class="book-page">
      
      <!-- Running Header -->
      <div class="book-page-running-header">
        <span class="running-book-title">সমাজসেবা অধিদপ্তর ও সরকারি নিয়োগ লিখিত গাইড</span>
        <span id="runningChapterName">বাংলা ব্যাকরণ ও সাহিত্য</span>
        <span id="runningMarksBadge">পূর্ণমান: ২০</span>
      </div>

      <!-- Chapter Title Block -->
      <div class="book-chapter-title-box">
        <span class="book-chapter-badge" id="chapterCategoryBadge">বিষয়: বাংলা</span>
        <h1 class="book-chapter-title" id="chapterHeading">অধ্যায় শিরোনাম</h1>
        <p class="book-chapter-desc" id="chapterDescription">অধ্যায়ের বিবরণ ও নির্দেশিকা</p>
        <div class="book-exam-hint" id="chapterExamTip">পরীক্ষার পরামর্শ</div>
      </div>

      <!-- Book Questions Content Stream -->
      <div class="book-content-stream" id="bookContentStream">
        <!-- Questions rendered here like a book -->
      </div>

      <!-- Running Footer -->
      <div class="book-page-footer">
        <span id="footerItemCounter">মোট প্রশ্ন: ০ টি</span>
        <span>১-৩ মাসের পূর্ণাঙ্গ লিখিত প্রস্তুতি সহায়িকা</span>
        <span id="footerBookmarkCounter">বুকমার্ক: ০</span>
      </div>

    </article>
  </main>

  <script>
    // Complete Question Bank Dataset
    const APP_DATA = {json_payload};

    // State
    let currentSubject = 'Bangla';
    let currentTopic = 'sondhi';
    let isTwoColumn = false;
    let isPracticeMode = false;
    let onlyBookmarks = false;
    let searchQuery = '';
    let bookmarkedIds = JSON.parse(localStorage.getItem('ss_book_bookmarks') || '[]');

    const SUBJECT_METADATA = {{
      Bangla: {{
        name: 'বাংলা',
        marks: '২০ নম্বর',
        category: 'প্রথম পত্র: বাংলা ভাষা ও সাহিত্য',
        runningName: 'সন্ধি, সমাস, কারক, বাগধারা, আবেদনপত্র ও দরখাস্ত, অনুচ্ছেদ, ব্যাকরণ'
      }},
      English: {{
        name: 'English',
        marks: '২০ নম্বর',
        category: 'Part II: English Language & Composition',
        runningName: 'Translation, Applications & Letters, Sentence Correction, Verbs, Idioms'
      }},
      Math: {{
        name: 'গণিত',
        marks: '১৫ নম্বর',
        category: 'তৃতীয় পত্র: পাটিগণিত, বীজগণিত ও জ্যামিতি',
        runningName: 'পাটিগণিত, বীজগণিত ও জ্যামিতি পূর্ণাঙ্গ সমাধানমালা'
      }},
      Gk: {{
        name: 'সাধারণ জ্ঞান',
        marks: '১৫ নম্বর',
        category: 'চতুর্থ পত্র: বাংলাদেশ, আন্তর্জাতিক, আইসিটি ও সমাজসেবা',
        runningName: 'বাংলাদেশ, আন্তর্জাতিক, সমাজসেবা, আইসিটি, পূর্ণরূপ ও টীকা'
      }}
    }};

    // Bengali Number Converter
    function toBnNum(num) {{
      const bnDigits = ['০','১','২','৩','৪','৫','৬','৭','৮','৯'];
      return String(num).replace(/[0-9]/g, d => bnDigits[d]);
    }}

    function changeBookFont(fontFamily) {{
      document.documentElement.style.setProperty('--font-book-bn', fontFamily);
      document.body.style.fontFamily = fontFamily;
      localStorage.setItem('ss_chosen_font', fontFamily);
    }}

    function changeBookFontSize(sizeVal) {{
      const sizeNum = parseFloat(sizeVal) || 16.5;
      const sizePx = sizeNum + 'px';
      document.documentElement.style.setProperty('--base-font-size', sizePx);
      document.documentElement.style.fontSize = sizePx;
      document.body.style.fontSize = sizePx;
      localStorage.setItem('ss_chosen_font_size', sizeVal);
      const sel = document.getElementById('bookFontSizeSelectDropdown');
      if (sel) sel.value = sizeVal;
    }}

    function setFontSize(size) {{
      if (size === 'small') changeBookFontSize('15');
      else if (size === 'large') changeBookFontSize('18.5');
      else changeBookFontSize('16.5');
    }}

    function applyColumnMode() {{
      const stream = document.getElementById('bookContentStream');
      const btn = document.getElementById('toggleColumnBtn');
      const text = document.getElementById('colModeText');
      if (!stream || !btn || !text) return;

      if (isTwoColumn) {{
        stream.classList.add('two-column');
        btn.classList.add('active');
        text.innerText = '১-কলাম মোড';
      }} else {{
        stream.classList.remove('two-column');
        btn.classList.remove('active');
        text.innerText = '২-কলাম মোড';
      }}
    }}

    function toggleColumnMode() {{
      isTwoColumn = !isTwoColumn;
      localStorage.setItem('ss_two_column_mode', isTwoColumn ? 'true' : 'false');
      applyColumnMode();
    }}

    function applyPracticeModeButton() {{
      const btn = document.getElementById('togglePracticeBtn');
      const text = document.getElementById('practiceBtnText');
      if (!btn || !text) return;

      if (isPracticeMode) {{
        btn.classList.add('active');
        text.innerText = 'উত্তর দেখান';
      }} else {{
        btn.classList.remove('active');
        text.innerText = 'উত্তর লুকান';
      }}
    }}

    function togglePracticeMode() {{
      isPracticeMode = !isPracticeMode;
      localStorage.setItem('ss_practice_mode', isPracticeMode ? 'true' : 'false');
      applyPracticeModeButton();
      renderBookPage();
    }}

    function toggleAnswer(answerElementId) {{
      if (!isPracticeMode) return;
      const el = document.getElementById(answerElementId);
      if (!el) return;
      el.classList.toggle('revealed');
    }}

    function applyBookmarkFilterButton() {{
      const btn = document.getElementById('toggleBookmarkFilterBtn');
      const text = document.getElementById('bookmarkFilterText');
      if (!btn || !text) return;

      if (onlyBookmarks) {{
        btn.classList.add('active');
        text.innerText = 'সব প্রশ্ন';
      }} else {{
        btn.classList.remove('active');
        text.innerText = 'বুকমার্ক দেখা';
      }}
    }}

    function toggleBookmarkFilter() {{
      onlyBookmarks = !onlyBookmarks;
      localStorage.setItem('ss_only_bookmarks', onlyBookmarks ? 'true' : 'false');
      applyBookmarkFilterButton();
      renderBookPage();
    }}

    function handleSearch() {{
      searchQuery = document.getElementById('bookSearchInput').value.trim().toLowerCase();
      renderBookPage();
    }}

    function toggleBookmark(uniqueKey) {{
      const idx = bookmarkedIds.indexOf(uniqueKey);
      if (idx > -1) {{
        bookmarkedIds.splice(idx, 1);
      }} else {{
        bookmarkedIds.push(uniqueKey);
      }}
      localStorage.setItem('ss_book_bookmarks', JSON.stringify(bookmarkedIds));
      updateBookmarkStats();
      renderBookPage();
    }}

    function updateBookmarkStats() {{
      const badge = document.getElementById('footerBookmarkCounter');
      if (badge) {{
        badge.innerText = `বুকমার্ক: ${{toBnNum(bookmarkedIds.length)}} টি`;
      }}
    }}

    function selectSubject(key) {{
      currentSubject = key;
      localStorage.setItem('ss_chosen_subject', key);

      const topics = Object.keys(APP_DATA[currentSubject] || {{}});
      const savedTopicForSubj = localStorage.getItem('ss_chosen_topic_' + key);
      if (savedTopicForSubj && topics.includes(savedTopicForSubj)) {{
        currentTopic = savedTopicForSubj;
      }} else {{
        currentTopic = topics.length > 0 ? topics[0] : '';
      }}
      localStorage.setItem('ss_chosen_topic', currentTopic);

      searchQuery = '';
      const sInput = document.getElementById('bookSearchInput');
      if (sInput) sInput.value = '';

      renderSubjectTabs();
      renderTopicSubnav();
      renderBookPage();
    }}

    function renderSubjectTabs() {{
      const container = document.getElementById('subjectTabsContainer');
      container.innerHTML = '';

      Object.keys(SUBJECT_METADATA).forEach(key => {{
        const meta = SUBJECT_METADATA[key];
        const isActive = key === currentSubject;

        const btn = document.createElement('button');
        btn.className = `subject-tab ${{isActive ? 'active' : ''}}`;
        btn.innerText = `${{meta.name}} (${{meta.marks}})`;
        btn.onclick = () => selectSubject(key);
        container.appendChild(btn);
      }});
    }}

    function selectTopic(key) {{
      currentTopic = key;
      localStorage.setItem('ss_chosen_topic', key);
      localStorage.setItem('ss_chosen_topic_' + currentSubject, key);

      searchQuery = '';
      const sInput = document.getElementById('bookSearchInput');
      if (sInput) sInput.value = '';

      renderTopicSubnav();
      renderBookPage();
    }}

    function renderTopicSubnav() {{
      const container = document.getElementById('topicsSubnavContainer');
      container.innerHTML = '';

      const topics = APP_DATA[currentSubject];
      Object.keys(topics).forEach(key => {{
        const tData = topics[key];
        const isActive = key === currentTopic;

        const btn = document.createElement('button');
        btn.className = `topic-link ${{isActive ? 'active' : ''}}`;
        const count = tData.items ? tData.items.length : 0;
        const numStr = currentSubject === 'English' ? count : toBnNum(count);
        
        let rawTopic = tData.topic || key;
        let cleanTopic = rawTopic.replace(/\\s*\\([০-৯0-9]+টি\\s*মাস্টার\\s*সেট\\)/g, '').trim();

        btn.innerHTML = `
          <span>${{cleanTopic}}</span>
          <span class="topic-pill-count">${{numStr}}</span>
        `;
        btn.onclick = () => selectTopic(key);
        container.appendChild(btn);
      }});
    }}

    function initApp() {{
      // 1. Restore Font Family
      const savedFont = localStorage.getItem('ss_chosen_font') || \"'Noto Sans Bengali', sans-serif\";
      changeBookFont(savedFont);
      const selFont = document.getElementById('bookFontSelectDropdown');
      if (selFont) selFont.value = savedFont;

      // 2. Restore Font Size
      const savedFontSize = localStorage.getItem('ss_chosen_font_size') || '16.5';
      changeBookFontSize(savedFontSize);

      // 3. Restore Selected Subject
      const savedSubject = localStorage.getItem('ss_chosen_subject');
      if (savedSubject && APP_DATA[savedSubject]) {{
        currentSubject = savedSubject;
      }}

      // 4. Restore Selected Topic
      const topics = Object.keys(APP_DATA[currentSubject] || {{}});
      const savedTopic = localStorage.getItem('ss_chosen_topic');
      if (savedTopic && topics.includes(savedTopic)) {{
        currentTopic = savedTopic;
      }} else if (topics.length > 0) {{
        currentTopic = topics[0];
      }}

      // 5. Restore Two-Column Mode
      isTwoColumn = localStorage.getItem('ss_two_column_mode') === 'true';
      applyColumnMode();

      // 6. Restore Practice / Hide Answer Mode
      isPracticeMode = localStorage.getItem('ss_practice_mode') === 'true';
      applyPracticeModeButton();

      // 7. Restore Only Bookmarks Filter
      onlyBookmarks = localStorage.getItem('ss_only_bookmarks') === 'true';
      applyBookmarkFilterButton();

      // 8. Initial Render
      updateBookmarkStats();
      renderSubjectTabs();
      renderTopicSubnav();
      renderBookPage();
    }}

    function renderBookPage() {{
      const subMeta = SUBJECT_METADATA[currentSubject];
      const topicData = APP_DATA[currentSubject][currentTopic] || {{ items: [] }};

      // Running Headers
      document.getElementById('runningChapterName').innerText = subMeta.runningName;
      document.getElementById('runningMarksBadge').innerText = `পূর্ণমান: ${{subMeta.marks}}`;

      // Chapter Titles
      document.getElementById('chapterCategoryBadge').innerText = subMeta.category;
      document.getElementById('chapterHeading').innerText = topicData.topic || currentTopic;
      document.getElementById('chapterDescription').innerText = topicData.description || 'লিখিত পরীক্ষার জন্য প্রমিত পাঠ ও সমাধান।';
      document.getElementById('chapterExamTip').innerText = topicData.exam_tip || 'পরীক্ষার খাতায় লেখার নিয়ম ও প্রমিত উপস্থাপনা।';

      const container = document.getElementById('bookContentStream');
      let items = topicData.items || [];

      // Filter by search
      if (searchQuery) {{
        items = items.filter(item => {{
          const str = JSON.stringify(item).toLowerCase();
          return str.includes(searchQuery);
        }});
      }}

      // Filter by bookmark
      if (onlyBookmarks) {{
        items = items.filter((item, idx) => {{
          const uniqueKey = `${{currentSubject}}_${{currentTopic}}_${{item.id || idx}}`;
          return bookmarkedIds.includes(uniqueKey);
        }});
      }}

      // Footer Stats
      const totalNumStr = currentSubject === 'English' ? items.length : toBnNum(items.length);
      document.getElementById('footerItemCounter').innerText = `মোট আইটেম: ${{totalNumStr}} টি`;

      if (items.length === 0) {{
        container.innerHTML = `
          <div class="empty-book-state">
            <h3>কোনো প্রশ্ন পাওয়া যায়নি</h3>
            <p>অনুসন্ধান ফিল্টার পরিবর্তন করে পুনরায় চেষ্টা করুন।</p>
          </div>
        `;
        return;
      }}

      // Essays / Paragraphs / Applications render in full-width single column
      if (currentTopic === 'bhabsomprosharon_onucched' || currentTopic === 'paragraph' || currentTopic === 'abedonpotro_dorkhasht' || currentTopic === 'formal_letter_application') {{
        container.className = 'book-content-stream';
        container.innerHTML = items.map((item, idx) => renderEssayBookEntry(item, idx)).join('');
      }} else {{
        container.className = isTwoColumn ? 'book-content-stream two-column' : 'book-content-stream';
        container.innerHTML = items.map((item, idx) => renderBookEntry(item, idx)).join('');
      }}
    }}

    function renderBookEntry(item, idx) {{
      const uniqueKey = `${{currentSubject}}_${{currentTopic}}_${{item.id || idx}}`;
      const isBookmarked = bookmarkedIds.includes(uniqueKey);
      const answerElementId = `ans_${{uniqueKey}}`;
      const hiddenClass = isPracticeMode ? 'hidden-answer' : '';

      const isEnglish = currentSubject === 'English';
      const numLabel = isEnglish ? `${{idx + 1}}.` : `${{toBnNum(idx + 1)}}।`;

      let qHtml = '';
      let aHtml = '';
      let noteHtml = '';

      switch (currentTopic) {{
        case 'sondhi':
          qHtml = `<span class="entry-question-text">${{item.word}}</span>`;
          aHtml = `<strong>সন্ধি বিচ্ছেদ:</strong> ${{item.word}} = <strong>${{item.breakdown}}</strong> (${{item.type}})`;
          if (item.rule) noteHtml = `নিয়ম: ${{item.rule}}`;
          break;

        case 'somas':
          qHtml = `<span class="entry-question-text">${{item.word}}</span>`;
          aHtml = `<strong>ব্যাসবাক্য:</strong> ${{item.vyasbakya}} &nbsp;|&nbsp; <strong>সমাস:</strong> ${{item.somas_type}}`;
          if (item.note) noteHtml = `নোট: ${{item.note}}`;
          break;

        case 'karok':
          const hlSent = item.sentence.replace(item.word, `<u><strong>${{item.word}}</strong></u>`);
          qHtml = `<span class="entry-question-text">${{hlSent}}</span>`;
          aHtml = `<strong>কারক ও বিভক্তি:</strong> ${{item.word}} &rarr; ${{item.karok}}-এ ${{item.bibhokti}}`;
          if (item.reason) noteHtml = `কারণ: ${{item.reason}}`;
          break;

        case 'ek_kothay_prokash':
          qHtml = `<span class="entry-question-text">"${{item.phrase}}"</span>`;
          aHtml = `<strong>এক কথায় প্রকাশ:</strong> <strong>${{item.result}}</strong>`;
          break;

        case 'bagdhara':
          qHtml = `<span class="entry-question-text">${{item.idiom}}</span>`;
          aHtml = `<strong>অর্থ:</strong> ${{item.meaning}}`;
          noteHtml = `<strong>বাক্য:</strong> "${{item.sentence}}"`;
          break;

        case 'biporit_shobdo':
          qHtml = `<span class="entry-question-text">${{item.given_word}}</span>`;
          aHtml = `<strong>বিপরীত শব্দ:</strong> <strong>${{item.opposite_word}}</strong>`;
          if (item.note) noteHtml = `প্রয়োগ: ${{item.note}}`;
          break;

        case 'somarthok_shobdo':
          qHtml = `<span class="entry-question-text">${{item.word}}</span>`;
          aHtml = `<strong>প্রতিশব্দ:</strong> <strong>${{item.synonyms}}</strong>`;
          if (item.model_note) noteHtml = `প্রমিত রূপ: ${{item.model_note}}`;
          break;

        case 'shuddhokoron':
          qHtml = `<span class="entry-question-text" style="color: #991b1b;">অশুদ্ধ: ${{item.incorrect}}</span>`;
          aHtml = `<strong>শুদ্ধ রূপ:</strong> <strong>${{item.correct}}</strong>`;
          if (item.rule) noteHtml = `নিয়ম: ${{item.rule}}`;
          break;

        case 'translation':
          qHtml = `<span class="entry-question-text">"${{item.bangla}}"</span>`;
          aHtml = `<strong>Translation:</strong> <strong>${{item.english}}</strong>`;
          if (item.grammar_note) noteHtml = `Grammar: ${{item.grammar_note}}`;
          break;

        case 'preposition_articles':
          qHtml = `<span class="entry-question-text en">${{item.question}}</span>`;
          const fullSent = item.question.replace('___', `[${{item.answer}}]`);
          aHtml = `<strong>Answer:</strong> <strong>${{item.answer}}</strong> (Sentence: <em>${{fullSent}}</em>)`;
          if (item.explanation) noteHtml = `Rule: ${{item.explanation}}`;
          break;

        case 'right_form_of_verbs':
          qHtml = `<span class="entry-question-text en">${{item.question}}</span>`;
          aHtml = `<strong>Correct Verb:</strong> <strong>${{item.answer}}</strong>`;
          if (item.rule) noteHtml = `Rule: ${{item.rule}}`;
          break;

        case 'idioms_phrases':
          qHtml = `<span class="entry-question-text en">${{item.idiom}}</span>`;
          aHtml = `<strong>Meaning:</strong> ${{item.meaning}}`;
          noteHtml = `<strong>Sentence:</strong> "${{item.sentence}}"`;
          break;

        case 'transformation_voice':
          qHtml = `<span class="entry-question-text en">${{item.question}}</span>`;
          aHtml = `<strong>Transformed:</strong> <strong>${{item.answer}}</strong>`;
          if (item.rule) noteHtml = `Rule: ${{item.rule}}`;
          break;

        case 'sentence_correction':
          qHtml = `<span class="entry-question-text en" style="color: #991b1b;">Incorrect: ${{item.incorrect}}</span>`;
          aHtml = `<strong>Correct:</strong> <strong style="color: #166534;">${{item.correct}}</strong>`;
          if (item.rule) noteHtml = `Rule: ${{item.rule}}`;
          break;

        case 'patigonit':
        case 'bijgonit':
          return `
            <div class="book-entry" style="border-bottom: 1.5px solid #e5e7eb;">
              <div class="entry-header-row ${{isPracticeMode ? 'practice-clickable' : ''}}" ${{isPracticeMode ? `onclick="toggleAnswer('${{answerElementId}}')\" title=\"ক্লিক করে সমাধান দেখুন/লুকান\"` : ''}}>
                <div>
                  <span class="entry-num">প্রশ্ন ${{numLabel}}</span>
                  <span class="entry-question-text">${{item.question}}</span>
                </div>
                <button class="entry-bookmark-btn ${{isBookmarked ? 'bookmarked' : ''}}" onclick="event.stopPropagation(); toggleBookmark('${{uniqueKey}}')" title="বুকমার্ক">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="${{isBookmarked ? '#d97706' : 'none'}}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
                  </svg>
                </button>
              </div>

              <div class="math-solution-book ${{hiddenClass}}" id="${{answerElementId}}" onclick="if(isPracticeMode) this.classList.remove('revealed')">
                <div style="font-weight: 700; color: #111827; margin-bottom: 6px;">সমাধান:</div>
                ${{item.solution_steps.map(step => `<div class="math-step-line">${{step}}</div>`).join('')}}
                <div class="math-ans-badge">উত্তর: ${{item.answer}}</div>
                ${{item.formula_used ? `<div class="entry-note" style="margin-top: 6px;">সূত্র: ${{item.formula_used}}</div>` : ''}}
              </div>
            </div>
          `;

        case 'jyamiti':
          return `
            <div class="book-entry" style="border-bottom: 1.5px solid #e5e7eb; padding: 14px 0;">
              <div class="entry-header-row ${{isPracticeMode ? 'practice-clickable' : ''}}" ${{isPracticeMode ? `onclick="toggleAnswer('${{answerElementId}}')\" title=\"ক্লিক করে সমাধান দেখুন/লুকান\"` : ''}}>
                <div>
                  <span class="entry-num">জ্যামিতি ${{numLabel}}</span>
                  <span class="entry-question-text" style="font-size: 1.15rem;">${{item.title}}</span>
                </div>
                <button class="entry-bookmark-btn ${{isBookmarked ? 'bookmarked' : ''}}" onclick="event.stopPropagation(); toggleBookmark('${{uniqueKey}}')" title="বুকমার্ক">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="${{isBookmarked ? '#d97706' : 'none'}}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
                  </svg>
                </button>
              </div>
              <div style="font-weight: 600; color: #1f2937; margin: 4px 0 6px;">প্রশ্ন: ${{item.question}}</div>
              <div class="entry-answer-block ${{hiddenClass}}" id="${{answerElementId}}" onclick="if(isPracticeMode) this.classList.remove('revealed')">
                <div style="font-size: 1.02rem; line-height: 1.6; color: #111827;">
                  <strong>সংজ্ঞা:</strong> ${{item.definition}}
                </div>
                <div style="margin-top: 4px; font-size: 0.95rem; color: #1e40af;">
                  <strong>সূত্র/বৈশিষ্ট্য:</strong> ${{item.formula}}
                </div>
                <div class="entry-note">
                  <strong>উদাহরণ:</strong> ${{item.example}}
                </div>
              </div>
            </div>
          `;

        case 'bangladesh_affairs':
        case 'international_affairs':
          qHtml = `<span class="entry-question-text">${{item.question}}</span>`;
          aHtml = `<strong>উত্তর:</strong> ${{item.answer}}`;
          break;

        case 'computer_ict':
          qHtml = `<span class="entry-question-text">${{item.question}}</span>`;
          aHtml = `<strong>উত্তর:</strong> ${{item.answer}}`;
          break;

        case 'somajseba_kormosuchi':
          qHtml = `<span class="entry-question-text">${{item.program_name}}</span>`;
          aHtml = `<strong>শুরুর বছর:</strong> ${{item.start_year}} &nbsp;|&nbsp; <strong>ভাতার হার:</strong> ${{item.current_rate}}`;
          noteHtml = `<strong>যোগ্যতা:</strong> ${{item.eligibility}}<br><span style="color: #374151;">${{item.details}}</span>`;
          break;

        case 'abbreviations_purnorup':
          qHtml = `<span class="entry-question-text en" style="font-size: 1.15rem;">${{item.abbreviation}}</span>`;
          aHtml = `<strong>Full Form:</strong> <strong>${{item.full_form}}</strong>`;
          if (item.bangla_meaning) noteHtml = `বিবরণ: ${{item.bangla_meaning}}`;
          break;

        case 'tika_short_notes':
          return `
            <div class="book-entry" style="border-bottom: 1.5px solid #e5e7eb; padding: 16px 0;">
              <div class="entry-header-row ${{isPracticeMode ? 'practice-clickable' : ''}}" ${{isPracticeMode ? `onclick="toggleAnswer('${{answerElementId}}')\" title=\"ক্লিক করে টীকা দেখুন/লুকান\"` : ''}}>
                <div>
                  <span class="entry-num">টীকা ${{numLabel}}</span>
                  <span class="entry-question-text" style="font-size: 1.25rem;">${{item.title}}</span>
                </div>
                <button class="entry-bookmark-btn ${{isBookmarked ? 'bookmarked' : ''}}" onclick="event.stopPropagation(); toggleBookmark('${{uniqueKey}}')" title="বুকমার্ক">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="${{isBookmarked ? '#d97706' : 'none'}}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
                  </svg>
                </button>
              </div>
              <div class="entry-answer-block ${{hiddenClass}}" id="${{answerElementId}}" onclick="if(isPracticeMode) this.classList.remove('revealed')">
                ${{item.key_facts ? `<div style="font-size: 0.9rem; color: #4b5563; margin: 4px 0 8px; font-style: italic;">মূল পয়েন্ট: ${{item.key_facts}}</div>` : ''}}
                <div style="font-size: 1.02rem; line-height: 1.8; color: #1f2937; text-align: justify;">
                  ${{item.model_answer}}
                </div>
              </div>
            </div>
          `;

        default:
          qHtml = `<span>${{JSON.stringify(item)}}</span>`;
      }}

      return `
        <div class="book-entry">
          <div class="entry-header-row ${{isPracticeMode ? 'practice-clickable' : ''}}" ${{isPracticeMode ? `onclick="toggleAnswer('${{answerElementId}}')\" title=\"ক্লিক করে উত্তর দেখুন/লুকান\"` : ''}}>
            <div>
              <span class="entry-num">${{numLabel}}</span>
              ${{qHtml}}
            </div>
            <button class="entry-bookmark-btn ${{isBookmarked ? 'bookmarked' : ''}}" onclick="event.stopPropagation(); toggleBookmark('${{uniqueKey}}')" title="বুকমার্ক">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="${{isBookmarked ? '#d97706' : 'none'}}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
              </svg>
            </button>
          </div>

          <div class="entry-answer-block ${{hiddenClass}}" id="${{answerElementId}}" onclick="if(isPracticeMode) this.classList.remove('revealed')">
            <div class="entry-answer-text ${{isEnglish ? 'en' : ''}}">${{aHtml}}</div>
            ${{noteHtml ? `<div class="entry-note">${{noteHtml}}</div>` : ''}}
          </div>
        </div>
      `;
    }}

    function renderEssayBookEntry(item, idx) {{
      const uniqueKey = `${{currentSubject}}_${{currentTopic}}_${{item.id || idx}}`;
      const isBookmarked = bookmarkedIds.includes(uniqueKey);
      const answerElementId = `ans_${{uniqueKey}}`;
      const hiddenClass = isPracticeMode ? 'hidden-answer' : '';

      const isEnglish = currentTopic === 'paragraph' || currentTopic === 'formal_letter_application';
      const numLabel = isEnglish ? `${{idx + 1}}.` : `${{toBnNum(idx + 1)}}।`;
      const title = item.title || item.topic;
      const content = item.model_answer || item.model_paragraph;

      return `
        <div class="essay-book-box">
          <div class="entry-header-row ${{isPracticeMode ? 'practice-clickable' : ''}}" ${{isPracticeMode ? `onclick="toggleAnswer('${{answerElementId}}')\" title=\"ক্লিক করে লেখা দেখুন/লুকান\"` : ''}}>
            <h2 class="essay-book-title">${{numLabel}} "${{title}}"</h2>
            <button class="entry-bookmark-btn ${{isBookmarked ? 'bookmarked' : ''}}" onclick="event.stopPropagation(); toggleBookmark('${{uniqueKey}}')" title="বুকমার্ক">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="${{isBookmarked ? '#d97706' : 'none'}}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
              </svg>
            </button>
          </div>

          <div class="${{hiddenClass}}" id="${{answerElementId}}" onclick="if(isPracticeMode) this.classList.remove('revealed')">
            ${{item.key_points ? `<div class="essay-book-points">পয়েন্ট ও মূল ধারণা: ${{item.key_points}}</div>` : ''}}
            <div class="essay-book-body ${{isEnglish ? 'en' : ''}}">
              ${{content}}
            </div>
          </div>
        </div>
      `;
    }}

    // Boot Book App
    window.addEventListener('DOMContentLoaded', initApp);
  </script>
</body>
</html>
"""

# Save to target locations
target_somaj = os.path.join(source_dir, "somaj-seba-written.html")
target_root = os.path.join(workspace_dir, "somaj-seba-written.html")
target_index = os.path.join(workspace_dir, "index.html")

with open(target_somaj, "w", encoding="utf-8") as f:
    f.write(html_code)
print(f"Updated book portal in somaj-seba-written/somaj-seba-written.html (Size: {len(html_code):,} bytes)")

with open(target_root, "w", encoding="utf-8") as f:
    f.write(html_code)
print(f"Updated book portal in root/somaj-seba-written.html (Size: {len(html_code):,} bytes)")

with open(target_index, "w", encoding="utf-8") as f:
    f.write(html_code)
print(f"Updated book portal in root/index.html (Size: {len(html_code):,} bytes)")
