"""
Enterprise Human Capital & Operational Efficiency Diagnostics
Module: generate_architecture_diagram.py
Purpose: Generates ultra-modern, high-fidelity vector diagrams (SVG)
         for the end-to-end data pipeline lifecycle and the Kimball Galaxy Schema.
Domain: Nexora Tech Solutions (Software House & L&D Academy Enterprise)
"""

import os
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = BASE_DIR / "docs" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def generate_lifecycle_diagram() -> str:
    """Generates the modern 5-tier End-to-End Lifecycle & System Architecture SVG."""
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 1440" width="2400" height="1440" style="background:#030712; font-family:'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <!-- Master Background Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="25%" stop-color="#070D21"/>
      <stop offset="60%" stop-color="#040818"/>
      <stop offset="100%" stop-color="#01030A"/>
    </linearGradient>

    <!-- Dot Grid Pattern -->
    <pattern id="dotGrid" x="0" y="0" width="32" height="32" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#334155" fill-opacity="0.35"/>
    </pattern>

    <!-- Stage Gradients -->
    <linearGradient id="gradStage1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>

    <linearGradient id="gradStage2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#C084FC"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>

    <linearGradient id="gradStage3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34D399"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>

    <linearGradient id="gradStage4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FBBF24"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>

    <linearGradient id="gradStage5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F472B6"/>
      <stop offset="100%" stop-color="#9333EA"/>
    </linearGradient>

    <!-- Header Gradient -->
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="25%" stop-color="#818CF8"/>
      <stop offset="50%" stop-color="#C084FC"/>
      <stop offset="75%" stop-color="#F472B6"/>
      <stop offset="100%" stop-color="#FBBF24"/>
    </linearGradient>

    <!-- Card Backgrounds -->
    <linearGradient id="cardDark" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#090E1A" stop-opacity="0.98"/>
    </linearGradient>
    <linearGradient id="cardInner" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1E293B" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.8"/>
    </linearGradient>

    <!-- Filters -->
    <filter id="shadowBox" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="14" stdDeviation="12" flood-color="#000000" flood-opacity="0.75"/>
    </filter>
    <filter id="glowCyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glowPurple" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <!-- Markers -->
    <marker id="arrowCyan" markerWidth="10" markerHeight="10" refX="7" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#38BDF8"/>
    </marker>
    <marker id="arrowPurple" markerWidth="10" markerHeight="10" refX="7" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#C084FC"/>
    </marker>
    <marker id="arrowEmerald" markerWidth="10" markerHeight="10" refX="7" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#34D399"/>
    </marker>
    <marker id="arrowAmber" markerWidth="10" markerHeight="10" refX="7" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#FBBF24"/>
    </marker>
  </defs>

  <!-- Background Base -->
  <rect width="2400" height="1440" fill="url(#bgGrad)"/>
  <rect width="2400" height="1440" fill="url(#dotGrid)"/>

  <!-- Ambient Glow Orbs -->
  <circle cx="250" cy="250" r="350" fill="#0284C7" fill-opacity="0.08" filter="blur(80px)"/>
  <circle cx="1200" cy="720" r="480" fill="#7C3AED" fill-opacity="0.06" filter="blur(100px)"/>
  <circle cx="2150" cy="1150" r="380" fill="#DB2777" fill-opacity="0.07" filter="blur(80px)"/>

  <!-- ========================================================================= -->
  <!-- HEADER SECTION                                                            -->
  <!-- ========================================================================= -->
  <g transform="translate(80, 50)">
    <!-- Corporate Pill Badge -->
    <rect x="0" y="0" width="370" height="34" rx="17" fill="#0F172A" stroke="#334155" stroke-width="1.2"/>
    <circle cx="18" cy="17" r="6" fill="#10B981" filter="url(#glowCyan)"/>
    <text x="34" y="22" fill="#E2E8F0" font-size="12" font-weight="700" letter-spacing="1.5">NEXORA TECH SOLUTIONS · ENTERPRISE PLATFORM</text>

    <!-- Main Title -->
    <text x="0" y="78" fill="url(#titleGrad)" font-size="34" font-weight="800" letter-spacing="-0.5">
      Human Capital &amp; Software House Operations: End-to-End Pipeline &amp; Galaxy Architecture
    </text>
    <text x="0" y="108" fill="#94A3B8" font-size="15" font-weight="400">
      6 Ingestion Feeds → Clean Architecture (src/enterprise_hr) → Microsoft SQL Server DWH (22 Tables · 322,217 Rows) → Kimball Galaxy (6 Dims / 5 Facts) → Power BI TMDL
    </text>

    <!-- Executive Metric Chips -->
    <g transform="translate(1380, 10)">
      <rect x="0" y="0" width="165" height="54" rx="12" fill="#0F172A" stroke="#1E293B"/>
      <text x="82" y="24" text-anchor="middle" fill="#38BDF8" font-size="18" font-weight="800">7,000</text>
      <text x="82" y="42" text-anchor="middle" fill="#64748B" font-size="10" font-weight="700">CORE EMPLOYEES</text>

      <rect x="175" y="0" width="165" height="54" rx="12" fill="#0F172A" stroke="#1E293B"/>
      <text x="257" y="24" text-anchor="middle" fill="#A855F7" font-size="18" font-weight="800">322,217</text>
      <text x="257" y="42" text-anchor="middle" fill="#64748B" font-size="10" font-weight="700">DWH TOTAL ROWS</text>

      <rect x="350" y="0" width="165" height="54" rx="12" fill="#0F172A" stroke="#1E293B"/>
      <text x="432" y="24" text-anchor="middle" fill="#10B981" font-size="18" font-weight="800">29 / 29</text>
      <text x="432" y="42" text-anchor="middle" fill="#64748B" font-size="10" font-weight="700">PYTESTS (100%)</text>

      <rect x="525" y="0" width="180" height="54" rx="12" fill="#0F172A" stroke="#1E293B"/>
      <text x="615" y="24" text-anchor="middle" fill="#F59E0B" font-size="18" font-weight="800">6 DIMS / 5 FACTS</text>
      <text x="615" y="42" text-anchor="middle" fill="#64748B" font-size="10" font-weight="700">KIMBALL GALAXY</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 5 HORIZONTAL STAGES                                                       -->
  <!-- ========================================================================= -->

  <!-- ── STAGE 1: RAW INGESTION LAYER ── -->
  <g transform="translate(80, 200)">
    <rect x="0" y="0" width="415" height="1180" rx="20" fill="url(#cardDark)" stroke="#1E293B" stroke-width="1.5" filter="url(#shadowBox)"/>
    
    <g transform="translate(25, 25)">
      <rect x="0" y="0" width="365" height="42" rx="10" fill="#0B1528" stroke="#0284C7" stroke-width="1.2"/>
      <circle cx="20" cy="21" r="5" fill="#38BDF8" filter="url(#glowCyan)"/>
      <text x="36" y="26" fill="#E2E8F0" font-size="13" font-weight="800" letter-spacing="1">1. HETEROGENEOUS INGESTION FEEDS</text>
    </g>

    <!-- Source 1: Core HR Master -->
    <g transform="translate(25, 85)">
      <rect x="0" y="0" width="365" height="160" rx="14" fill="url(#cardInner)" stroke="#0284C7" stroke-width="1"/>
      <rect x="15" y="12" width="75" height="22" rx="6" fill="#0369A1"/>
      <text x="52" y="27" text-anchor="middle" fill="#E0F2FE" font-size="10" font-weight="700">TEXT FILE</text>
      <text x="100" y="29" fill="#BAE6FD" font-size="13" font-weight="800">Core HR &amp; Workforce Master</text>
      <text x="15" y="58" fill="#7DD3FC" font-size="11" font-family="monospace">data/raw/employees_data_7000.txt</text>
      <text x="15" y="80" fill="#94A3B8" font-size="11">• 7,000 Authentic Tech Employees (Sequential IDs)</text>
      <text x="15" y="100" fill="#94A3B8" font-size="11">• Arabic Attributes: الاسم، الفرع، القسم، الراتب</text>
      <text x="15" y="120" fill="#94A3B8" font-size="11">• Ground Truth Baseline across all dimensions</text>
      <text x="15" y="142" fill="#38BDF8" font-size="11" font-weight="700">★ Single Source of Master Truth</text>
    </g>

    <!-- Source 2: IoT Turnstiles & Remote Gates -->
    <g transform="translate(25, 260)">
      <rect x="0" y="0" width="365" height="160" rx="14" fill="url(#cardInner)" stroke="#0284C7" stroke-width="1"/>
      <rect x="15" y="12" width="80" height="22" rx="6" fill="#0369A1"/>
      <text x="55" y="27" text-anchor="middle" fill="#E0F2FE" font-size="10" font-weight="700">REST / JSON</text>
      <text x="105" y="29" fill="#BAE6FD" font-size="13" font-weight="800">IoT Turnstiles &amp; Remote Gates</text>
      <text x="15" y="58" fill="#7DD3FC" font-size="11" font-family="monospace">api_badge_logs_202605.json</text>
      <text x="15" y="80" fill="#94A3B8" font-size="11">• 114,952 High-Frequency Clock Events</text>
      <text x="15" y="100" fill="#94A3B8" font-size="11">• CheckIn, CheckOut, BuildingID, Gate Mode</text>
      <text x="15" y="120" fill="#EF4444" font-size="11">• Flaws: 5% Forgotten Swipes (NULL Out)</text>
      <text x="15" y="142" fill="#38BDF8" font-size="11" font-weight="700">★ Physical Workplace Telemetry</text>
    </g>

    <!-- Source 3: Software House Client Projects -->
    <g transform="translate(25, 435)">
      <rect x="0" y="0" width="365" height="160" rx="14" fill="url(#cardInner)" stroke="#0284C7" stroke-width="1"/>
      <rect x="15" y="12" width="90" height="22" rx="6" fill="#0284C7"/>
      <text x="60" y="27" text-anchor="middle" fill="#E0F2FE" font-size="10" font-weight="700">JSON / CSV</text>
      <text x="115" y="29" fill="#BAE6FD" font-size="13" font-weight="800">Client Projects &amp; Freelance Tasks</text>
      <text x="15" y="58" fill="#7DD3FC" font-size="11" font-family="monospace">client_projects_tasks.csv</text>
      <text x="15" y="80" fill="#94A3B8" font-size="11">• 3,600 Milestone Client Deliverables (8 Projects)</text>
      <text x="15" y="100" fill="#94A3B8" font-size="11">• Offshore Clients: Aramco (KSA), Emirates (UAE), US</text>
      <text x="15" y="120" fill="#EF4444" font-size="11">• Flaws: 15% Scope Overruns, Overdue Deadlines</text>
      <text x="15" y="142" fill="#38BDF8" font-size="11" font-weight="700">★ Billable Velocity &amp; Bench Utilization</text>
    </g>

    <!-- Source 4: LMS Academy Platform -->
    <g transform="translate(25, 610)">
      <rect x="0" y="0" width="365" height="160" rx="14" fill="url(#cardInner)" stroke="#0284C7" stroke-width="1"/>
      <rect x="15" y="12" width="75" height="22" rx="6" fill="#0369A1"/>
      <text x="52" y="27" text-anchor="middle" fill="#E0F2FE" font-size="10" font-weight="700">REST API</text>
      <text x="100" y="29" fill="#BAE6FD" font-size="13" font-weight="800">LMS Academy &amp; Certifications</text>
      <text x="15" y="58" fill="#7DD3FC" font-size="11" font-family="monospace">lms_course_completions.csv</text>
      <text x="15" y="80" fill="#94A3B8" font-size="11">• 7,197 Certification Exam Attempts</text>
      <text x="15" y="100" fill="#94A3B8" font-size="11">• 10 Courses across Levels 1, 2, 3 (Azure, AWS, CKA)</text>
      <text x="15" y="120" fill="#EF4444" font-size="11">• Flaws: Retakes &amp; Failed Attempts (Score &lt; 70)</text>
      <text x="15" y="142" fill="#38BDF8" font-size="11" font-weight="700">★ Upskilling Velocity (ΔP ROI)</text>
    </g>

    <!-- Source 5: FP&A Budgets & Quotas -->
    <g transform="translate(25, 785)">
      <rect x="0" y="0" width="365" height="160" rx="14" fill="url(#cardInner)" stroke="#0284C7" stroke-width="1"/>
      <rect x="15" y="12" width="75" height="22" rx="6" fill="#0369A1"/>
      <text x="52" y="27" text-anchor="middle" fill="#E0F2FE" font-size="10" font-weight="700">EXCEL</text>
      <text x="100" y="29" fill="#BAE6FD" font-size="13" font-weight="800">FP&amp;A Department Budgets</text>
      <text x="15" y="58" fill="#7DD3FC" font-size="11" font-family="monospace">finance_budget_2026.xlsx</text>
      <text x="15" y="80" fill="#94A3B8" font-size="11">• 168 Wide Planning Records (2024-2026)</text>
      <text x="15" y="100" fill="#94A3B8" font-size="11">• Q1..Q4 Headcount &amp; Salary Targets</text>
      <text x="15" y="120" fill="#EF4444" font-size="11">• Flaws: Horizontal Quarters, Branch Typos</text>
      <text x="15" y="142" fill="#38BDF8" font-size="11" font-weight="700">★ Financial Run-Rate Quotas</text>
    </g>

    <!-- Source 6: FX Rates Feed -->
    <g transform="translate(25, 960)">
      <rect x="0" y="0" width="365" height="180" rx="14" fill="url(#cardInner)" stroke="#0284C7" stroke-width="1"/>
      <rect x="15" y="12" width="75" height="22" rx="6" fill="#0369A1"/>
      <text x="52" y="27" text-anchor="middle" fill="#E0F2FE" font-size="10" font-weight="700">CURRENCY</text>
      <text x="100" y="29" fill="#BAE6FD" font-size="13" font-weight="800">Central Bank FX Rates Feed</text>
      <text x="15" y="58" fill="#7DD3FC" font-size="11" font-family="monospace">dim_currency_rates.csv</text>
      <text x="15" y="80" fill="#94A3B8" font-size="11">• 6 Currencies: EGP, USD, EUR, GBP, SAR, AED</text>
      <text x="15" y="100" fill="#94A3B8" font-size="11">• Multi-currency spot rates &amp; multipliers</text>
      <text x="15" y="120" fill="#94A3B8" font-size="11">• Offshore revenue vs domestic payroll matching</text>
      <text x="15" y="145" fill="#38BDF8" font-size="11" font-weight="700">★ Global Multi-Currency Normalization</text>
    </g>
  </g>

  <!-- Connectors Stage 1 -> Stage 2 -->
  <path d="M 495 340 C 525 340, 525 400, 555 400" fill="none" stroke="url(#gradStage1)" stroke-width="2.5" marker-end="url(#arrowCyan)"/>
  <path d="M 495 515 C 525 515, 525 515, 555 515" fill="none" stroke="url(#gradStage1)" stroke-width="2.5" marker-end="url(#arrowCyan)"/>
  <path d="M 495 690 C 525 690, 525 640, 555 640" fill="none" stroke="url(#gradStage1)" stroke-width="2.5" marker-end="url(#arrowCyan)"/>
  <path d="M 495 865 C 525 865, 525 800, 555 800" fill="none" stroke="url(#gradStage1)" stroke-width="2.5" marker-end="url(#arrowCyan)"/>
  <path d="M 495 1050 C 525 1050, 525 960, 555 960" fill="none" stroke="url(#gradStage1)" stroke-width="2.5" marker-end="url(#arrowCyan)"/>

  <!-- ── STAGE 2: CLEAN ARCHITECTURE & QUALITY LAYER ── -->
  <g transform="translate(555, 200)">
    <rect x="0" y="0" width="415" height="1180" rx="20" fill="url(#cardDark)" stroke="#1E293B" stroke-width="1.5" filter="url(#shadowBox)"/>
    
    <g transform="translate(25, 25)">
      <rect x="0" y="0" width="365" height="42" rx="10" fill="#1C1033" stroke="#8B5CF6" stroke-width="1.2"/>
      <circle cx="20" cy="21" r="5" fill="#C084FC" filter="url(#glowPurple)"/>
      <text x="36" y="26" fill="#E2E8F0" font-size="13" font-weight="800" letter-spacing="1">2. CLEAN ARCHITECTURE &amp; CONTRACTS</text>
    </g>

    <!-- Transform 1: Python Clean Architecture Package -->
    <g transform="translate(25, 85)">
      <rect x="0" y="0" width="365" height="235" rx="14" fill="url(#cardInner)" stroke="#8B5CF6" stroke-width="1"/>
      <text x="15" y="26" fill="#E9D5FF" font-size="13" font-weight="800">src/enterprise_hr Architecture</text>
      <text x="15" y="46" fill="#C084FC" font-size="11" font-family="monospace">Clean Architecture &amp; SOLID Principles</text>
      <rect x="15" y="58" width="335" height="1" fill="#334155"/>
      <text x="15" y="80" fill="#CBD5E1" font-size="11">⚙ core/ : Pydantic Config, Constants, Logging</text>
      <text x="15" y="102" fill="#CBD5E1" font-size="11">💎 domain/ : Immutable Entities &amp; Contracts</text>
      <text x="15" y="124" fill="#CBD5E1" font-size="11">🔌 infrastructure/ : Database &amp; FileHandler</text>
      <text x="15" y="146" fill="#CBD5E1" font-size="11">🚀 pipelines/ : SqlBulkLoader &amp; Orchestrator</text>
      <text x="15" y="168" fill="#CBD5E1" font-size="11">⚡ cli.py : Unified enterprise-hr-cli Command Center</text>
      <rect x="15" y="180" width="335" height="1" fill="#334155"/>
      <text x="15" y="202" fill="#10B981" font-size="11" font-weight="700">✔ Full Type Annotations &amp; Structured Telemetry</text>
      <text x="15" y="222" fill="#38BDF8" font-size="11">✔ pyproject.toml &amp; run.ps1 Developer Tooling</text>
    </g>

    <!-- Transform 2: T-SQL Staging Transformation -->
    <g transform="translate(25, 335)">
      <rect x="0" y="0" width="365" height="235" rx="14" fill="url(#cardInner)" stroke="#8B5CF6" stroke-width="1"/>
      <text x="15" y="26" fill="#E9D5FF" font-size="13" font-weight="800">T-SQL Staging Transformation</text>
      <text x="15" y="46" fill="#C084FC" font-size="11" font-family="monospace">00_stg_hr_audit.sql &amp; Heuristics</text>
      <rect x="15" y="58" width="335" height="1" fill="#334155"/>
      <text x="15" y="80" fill="#CBD5E1" font-size="11">1. Deduplicate Retries on 5 Key Tuples</text>
      <text x="30" y="98" fill="#A855F7" font-size="11" font-weight="700">12,516 → 12,392 Staged Rows (0 Losses)</text>
      <text x="15" y="120" fill="#CBD5E1" font-size="11">2. Arabic Fuzzy Branch Normalization</text>
      <text x="30" y="138" fill="#94A3B8" font-size="11">Standardizes سموحة, المعادي, القرية الذكية</text>
      <text x="15" y="160" fill="#CBD5E1" font-size="11">3. SCD2 LEAD() Window Chaining</text>
      <text x="30" y="178" fill="#10B981" font-size="11" font-weight="700">ValidFrom ≤ ValidTo &amp; IsCurrent Flag</text>
      <text x="15" y="200" fill="#CBD5E1" font-size="11">4. Attendance Clock-Out Imputation:</text>
      <text x="30" y="218" fill="#38BDF8" font-size="11">COALESCE(CheckOut, CheckIn + 8 Hours)</text>
    </g>

    <!-- Transform 3: Automated Pytest Suite (29/29) -->
    <g transform="translate(25, 585)">
      <rect x="0" y="0" width="365" height="260" rx="14" fill="url(#cardInner)" stroke="#10B981" stroke-width="1.2"/>
      <rect x="15" y="15" width="125" height="22" rx="6" fill="#065F46"/>
      <text x="77" y="30" text-anchor="middle" fill="#A7F3D0" font-size="10" font-weight="800">CI/CD CONTRACTS</text>
      <text x="150" y="32" fill="#6EE7B7" font-size="13" font-weight="800">29/29 Pytests Passing</text>
      <text x="15" y="58" fill="#34D399" font-size="11" font-family="monospace">tests/ (100% Pass Rate)</text>
      <rect x="15" y="70" width="335" height="1" fill="#334155"/>
      <text x="15" y="92" fill="#CBD5E1" font-size="11">✔ Master Text Grounding (7,000 EMP IDs)</text>
      <text x="15" y="114" fill="#CBD5E1" font-size="11">✔ 0 Orphaned Foreign Keys across 5 Facts</text>
      <text x="15" y="136" fill="#CBD5E1" font-size="11">✔ SCD2 Interval Temporal Continuity</text>
      <text x="15" y="158" fill="#CBD5E1" font-size="11">✔ Pydantic Entity Validation &amp; Invariants</text>
      <text x="15" y="180" fill="#CBD5E1" font-size="11">✔ Atomic File Operations &amp; Safety Contracts</text>
      <text x="15" y="202" fill="#CBD5E1" font-size="11">✔ SQL Batch Parser &amp; DDL Idempotency</text>
      <text x="15" y="224" fill="#CBD5E1" font-size="11">✔ Currency Spot Rates &amp; Multiplier Checks</text>
      <text x="15" y="246" fill="#10B981" font-size="11" font-weight="700">✔ Execution Time: &lt; 2.5s via pytest runner</text>
    </g>

    <!-- Transform 4: Staging Materialization Tables -->
    <g transform="translate(25, 860)">
      <rect x="0" y="0" width="365" height="295" rx="14" fill="url(#cardInner)" stroke="#8B5CF6" stroke-width="1"/>
      <text x="15" y="28" fill="#E9D5FF" font-size="13" font-weight="800">Staging Layer Materialization</text>
      <text x="15" y="48" fill="#C084FC" font-size="11">Database Schema: [stg] (30,539 Rows)</text>
      <rect x="15" y="60" width="335" height="1" fill="#334155"/>
      <text x="15" y="86" fill="#F1F5F9" font-size="11" font-weight="700">1. stg.Stg_HR_Audit (12,392 rows)</text>
      <text x="28" y="104" fill="#94A3B8" font-size="11">SCD2 valid chain, indexed on (EmpID, Date)</text>
      <text x="15" y="128" fill="#F1F5F9" font-size="11" font-weight="700">2. stg.Client_Tasks_Clean (3,600 rows)</text>
      <text x="28" y="146" fill="#94A3B8" font-size="11">Milestone delivery tasks &amp; hourly rates</text>
      <text x="15" y="170" fill="#F1F5F9" font-size="11" font-weight="700">3. stg.Employees_Core (7,000 rows)</text>
      <text x="28" y="188" fill="#94A3B8" font-size="11">Arabic attribute UTF-8 mapped core</text>
      <text x="15" y="212" fill="#F1F5F9" font-size="11" font-weight="700">4. stg.Exit_Attrition_Records (350 rows)</text>
      <text x="28" y="230" fill="#94A3B8" font-size="11">Historical resignation &amp; severance audit</text>
      <text x="15" y="254" fill="#F1F5F9" font-size="11" font-weight="700">5. stg.LMS_Completions_Clean (7,197 rows)</text>
      <text x="28" y="272" fill="#94A3B8" font-size="11">Exam attempts deduplicated &amp; scored</text>
    </g>
  </g>

  <!-- Connectors Stage 2 -> Stage 3 -->
  <path d="M 970 450 C 1000 450, 1000 500, 1030 500" fill="none" stroke="url(#gradStage2)" stroke-width="2.5" marker-end="url(#arrowPurple)"/>
  <path d="M 970 725 C 1000 725, 1000 725, 1030 725" fill="none" stroke="url(#gradStage2)" stroke-width="2.5" marker-end="url(#arrowPurple)"/>
  <path d="M 970 1000 C 1000 1000, 1000 950, 1030 950" fill="none" stroke="url(#gradStage2)" stroke-width="2.5" marker-end="url(#arrowPurple)"/>

  <!-- ── STAGE 3: MICROSOFT SQL SERVER DWH ── -->
  <g transform="translate(1030, 200)">
    <rect x="0" y="0" width="415" height="1180" rx="20" fill="url(#cardDark)" stroke="#1E293B" stroke-width="1.5" filter="url(#shadowBox)"/>
    
    <g transform="translate(25, 25)">
      <rect x="0" y="0" width="365" height="42" rx="10" fill="#0D2818" stroke="#10B981" stroke-width="1.2"/>
      <circle cx="20" cy="21" r="5" fill="#10B981"/>
      <text x="36" y="26" fill="#E2E8F0" font-size="13" font-weight="800" letter-spacing="1">3. MICROSOFT SQL SERVER DWH</text>
    </g>

    <!-- DWH Sub-block: 3 Schemas -->
    <g transform="translate(25, 85)">
      <rect x="0" y="0" width="365" height="1060" rx="14" fill="url(#cardInner)" stroke="#10B981" stroke-width="1"/>
      
      <!-- Database Title -->
      <g transform="translate(20, 18)">
        <rect x="0" y="0" width="325" height="48" rx="8" fill="#042F2E" stroke="#0D9488"/>
        <text x="162" y="22" text-anchor="middle" fill="#5EEAD4" font-size="13" font-weight="800">EnterpriseHR_DWH</text>
        <text x="162" y="38" text-anchor="middle" fill="#99F6E4" font-size="10">22 Tables · 322,217 Rows · localhost:1433</text>
      </g>

      <!-- Schema 1: raw -->
      <g transform="translate(20, 78)">
        <rect x="0" y="0" width="325" height="235" rx="10" fill="#0F172A" stroke="#334155"/>
        <rect x="15" y="10" width="135" height="20" rx="4" fill="#1E293B"/>
        <text x="82" y="24" text-anchor="middle" fill="#38BDF8" font-size="10" font-weight="800">SCHEMA: raw (138,439)</text>
        <text x="15" y="52" fill="#E2E8F0" font-size="11" font-weight="700">• raw.Badge_Access_Logs</text>
        <text x="310" y="52" text-anchor="end" fill="#38BDF8" font-size="11" font-weight="700">114,952</text>
        <text x="15" y="75" fill="#E2E8F0" font-size="11" font-weight="700">• raw.HR_Audit_Events</text>
        <text x="310" y="75" text-anchor="end" fill="#38BDF8" font-size="11" font-weight="700">12,516</text>
        <text x="15" y="98" fill="#E2E8F0" font-size="11" font-weight="700">• raw.LMS_Certifications</text>
        <text x="310" y="98" text-anchor="end" fill="#38BDF8" font-size="11" font-weight="700">7,197</text>
        <text x="15" y="121" fill="#E2E8F0" font-size="11" font-weight="700">• raw.Client_Project_Tasks</text>
        <text x="310" y="121" text-anchor="end" fill="#38BDF8" font-size="11" font-weight="700">3,600</text>
        <text x="15" y="144" fill="#E2E8F0" font-size="11" font-weight="700">• raw.Finance_Budget_Plan</text>
        <text x="310" y="144" text-anchor="end" fill="#38BDF8" font-size="11" font-weight="700">168</text>
        <text x="15" y="167" fill="#E2E8F0" font-size="11" font-weight="700">• raw.Currency_Rates</text>
        <text x="310" y="167" text-anchor="end" fill="#38BDF8" font-size="11" font-weight="700">6</text>
        <rect x="15" y="178" width="295" height="1" fill="#1E293B"/>
        <text x="15" y="196" fill="#10B981" font-size="10" font-weight="700">✔ Idempotent Truncate &amp; Bulk Load</text>
        <text x="15" y="214" fill="#38BDF8" font-size="10">✔ Strict Data Types (No VARCHAR(MAX))</text>
      </g>

      <!-- Schema 2: stg -->
      <g transform="translate(20, 325)">
        <rect x="0" y="0" width="325" height="150" rx="10" fill="#0F172A" stroke="#334155"/>
        <rect x="15" y="10" width="135" height="20" rx="4" fill="#1E293B"/>
        <text x="82" y="24" text-anchor="middle" fill="#C084FC" font-size="10" font-weight="800">SCHEMA: stg (30,539)</text>
        <text x="15" y="52" fill="#E2E8F0" font-size="11" font-weight="700">• stg.Stg_HR_Audit</text>
        <text x="310" y="52" text-anchor="end" fill="#C084FC" font-size="11" font-weight="700">12,392</text>
        <text x="15" y="74" fill="#E2E8F0" font-size="11" font-weight="700">• stg.Employees_Core</text>
        <text x="310" y="74" text-anchor="end" fill="#C084FC" font-size="11" font-weight="700">7,000</text>
        <text x="15" y="96" fill="#E2E8F0" font-size="11" font-weight="700">• stg.Client_Tasks_Clean</text>
        <text x="310" y="96" text-anchor="end" fill="#C084FC" font-size="11" font-weight="700">3,600</text>
        <text x="15" y="118" fill="#E2E8F0" font-size="11" font-weight="700">• stg.Exit_Attrition_Records</text>
        <text x="310" y="118" text-anchor="end" fill="#C084FC" font-size="11" font-weight="700">350</text>
        <text x="15" y="140" fill="#10B981" font-size="10" font-weight="700">✔ Clustered PK + Temporal IX</text>
      </g>

      <!-- Schema 3: mart -->
      <g transform="translate(20, 485)">
        <rect x="0" y="0" width="325" height="555" rx="10" fill="#0F172A" stroke="#10B981" stroke-width="1.2"/>
        <rect x="15" y="10" width="145" height="20" rx="4" fill="#065F46"/>
        <text x="87" y="24" text-anchor="middle" fill="#6EE7B7" font-size="10" font-weight="800">SCHEMA: mart (153,239)</text>
        <text x="15" y="46" fill="#34D399" font-size="11" font-weight="700">6 CONFORMED DIMENSIONS</text>
        
        <text x="15" y="68" fill="#E2E8F0" font-size="11">• Dim_Employee (SCD2)</text>
        <text x="310" y="68" text-anchor="end" fill="#34D399" font-size="11">7,000</text>

        <text x="15" y="88" fill="#E2E8F0" font-size="11">• Dim_Department</text>
        <text x="310" y="88" text-anchor="end" fill="#34D399" font-size="11">6</text>

        <text x="15" y="108" fill="#E2E8F0" font-size="11">• Dim_Branch (Geographic)</text>
        <text x="310" y="108" text-anchor="end" fill="#34D399" font-size="11">14</text>

        <text x="15" y="128" fill="#E2E8F0" font-size="11">• Dim_Date (Calendar)</text>
        <text x="310" y="128" text-anchor="end" fill="#34D399" font-size="11">1,096</text>

        <text x="15" y="148" fill="#E2E8F0" font-size="11">• Dim_Course (L&amp;D Tiers)</text>
        <text x="310" y="148" text-anchor="end" fill="#34D399" font-size="11">10</text>

        <text x="15" y="168" fill="#E2E8F0" font-size="11">• Dim_CurrencyRates (FX)</text>
        <text x="310" y="168" text-anchor="end" fill="#34D399" font-size="11">6</text>

        <rect x="15" y="180" width="295" height="1" fill="#1E293B"/>
        <text x="15" y="202" fill="#FBBF24" font-size="11" font-weight="700">5 GALAXY FACT CONSTELLATIONS</text>

        <text x="15" y="224" fill="#E2E8F0" font-size="11">• Fact_WorkforceSnapshot</text>
        <text x="310" y="224" text-anchor="end" fill="#FBBF24" font-size="11">7,000</text>

        <text x="15" y="244" fill="#E2E8F0" font-size="11">• Fact_DailyAttendance</text>
        <text x="310" y="244" text-anchor="end" fill="#FBBF24" font-size="11">16,000</text>

        <text x="15" y="264" fill="#E2E8F0" font-size="11">• Fact_DepartmentBudget</text>
        <text x="310" y="264" text-anchor="end" fill="#FBBF24" font-size="11">672</text>

        <text x="15" y="284" fill="#E2E8F0" font-size="11">• Fact_TrainingCompletions</text>
        <text x="310" y="284" text-anchor="end" fill="#FBBF24" font-size="11">2,735</text>

        <text x="15" y="304" fill="#E2E8F0" font-size="11">• Fact_ProjectTasks (Client Delivery)</text>
        <text x="310" y="304" text-anchor="end" fill="#FBBF24" font-size="11">3,600</text>

        <rect x="15" y="318" width="295" height="1" fill="#1E293B"/>
        <text x="15" y="338" fill="#94A3B8" font-size="11">Operational Fact Views:</text>
        <text x="15" y="358" fill="#E2E8F0" font-size="11">• Fact_Daily_Badge</text>
        <text x="310" y="358" text-anchor="end" fill="#94A3B8" font-size="11">114,952</text>
        <text x="15" y="378" fill="#E2E8F0" font-size="11">• Fact_Employee_SCD2</text>
        <text x="310" y="378" text-anchor="end" fill="#94A3B8" font-size="11">12,392</text>

        <rect x="15" y="394" width="295" height="1" fill="#1E293B"/>
        <text x="15" y="420" fill="#F1F5F9" font-size="12" font-weight="800">DWH TOTAL: 322,217 ROWS</text>
        <text x="15" y="445" fill="#10B981" font-size="11" font-weight="700">★ 0 Referential Integrity Orphans</text>
        <text x="15" y="468" fill="#38BDF8" font-size="11">★ Fully Materialized via T-SQL &amp; Python</text>
        <text x="15" y="490" fill="#C084FC" font-size="11">★ Pipeline Runtime: &lt; 35 Seconds</text>
        <text x="15" y="512" fill="#F59E0B" font-size="11">★ 22 Tables Active in Microsoft SQL Server</text>
      </g>
    </g>
  </g>

  <!-- Connectors Stage 3 -> Stage 4 -->
  <path d="M 1445 450 C 1475 450, 1475 420, 1505 420" fill="none" stroke="url(#gradStage3)" stroke-width="2.5" marker-end="url(#arrowEmerald)"/>
  <path d="M 1445 750 C 1475 750, 1475 750, 1505 750" fill="none" stroke="url(#gradStage3)" stroke-width="2.5" marker-end="url(#arrowEmerald)"/>
  <path d="M 1445 1050 C 1475 1050, 1475 1000, 1505 1000" fill="none" stroke="url(#gradStage3)" stroke-width="2.5" marker-end="url(#arrowEmerald)"/>

  <!-- ── STAGE 4: KIMBALL GALAXY CONSTELLATION ── -->
  <g transform="translate(1505, 200)">
    <rect x="0" y="0" width="415" height="1180" rx="20" fill="url(#cardDark)" stroke="#1E293B" stroke-width="1.5" filter="url(#shadowBox)"/>
    
    <g transform="translate(25, 25)">
      <rect x="0" y="0" width="365" height="42" rx="10" fill="#2E1C07" stroke="#F59E0B" stroke-width="1.2"/>
      <circle cx="20" cy="21" r="5" fill="#F59E0B"/>
      <text x="36" y="26" fill="#E2E8F0" font-size="13" font-weight="800" letter-spacing="1">4. KIMBALL GALAXY CONSTELLATION</text>
    </g>

    <!-- Conformed Dimensions Overview -->
    <g transform="translate(25, 85)">
      <rect x="0" y="0" width="365" height="340" rx="14" fill="url(#cardInner)" stroke="#10B981" stroke-width="1.2"/>
      <text x="15" y="28" fill="#6EE7B7" font-size="13" font-weight="800">6 Shared Conformed Dimensions</text>
      <text x="15" y="48" fill="#94A3B8" font-size="11">Single Version of Truth across Operations &amp; HR</text>
      <rect x="15" y="60" width="335" height="1" fill="#334155"/>

      <!-- Dim 1 -->
      <g transform="translate(15, 75)">
        <polygon points="12,0 24,7 24,21 12,28 0,21 0,7" fill="#047857" stroke="#10B981" stroke-width="1"/>
        <text x="35" y="19" fill="#F1F5F9" font-size="12" font-weight="700">Dim_Employee (SCD-2 Hub)</text>
        <text x="325" y="19" text-anchor="end" fill="#34D399" font-size="11">7,000</text>
      </g>

      <!-- Dim 2 -->
      <g transform="translate(15, 115)">
        <polygon points="12,0 24,7 24,21 12,28 0,21 0,7" fill="#047857" stroke="#10B981" stroke-width="1"/>
        <text x="35" y="19" fill="#F1F5F9" font-size="12" font-weight="700">Dim_Department (6 Divisions)</text>
        <text x="325" y="19" text-anchor="end" fill="#34D399" font-size="11">6</text>
      </g>

      <!-- Dim 3 -->
      <g transform="translate(15, 155)">
        <polygon points="12,0 24,7 24,21 12,28 0,21 0,7" fill="#047857" stroke="#10B981" stroke-width="1"/>
        <text x="35" y="19" fill="#F1F5F9" font-size="12" font-weight="700">Dim_Branch (Egyptian Tech Hubs)</text>
        <text x="325" y="19" text-anchor="end" fill="#34D399" font-size="11">14</text>
      </g>

      <!-- Dim 4 -->
      <g transform="translate(15, 195)">
        <polygon points="12,0 24,7 24,21 12,28 0,21 0,7" fill="#047857" stroke="#10B981" stroke-width="1"/>
        <text x="35" y="19" fill="#F1F5F9" font-size="12" font-weight="700">Dim_Date (Enterprise Calendar)</text>
        <text x="325" y="19" text-anchor="end" fill="#34D399" font-size="11">1,096</text>
      </g>

      <!-- Dim 5 -->
      <g transform="translate(15, 235)">
        <polygon points="12,0 24,7 24,21 12,28 0,21 0,7" fill="#047857" stroke="#10B981" stroke-width="1"/>
        <text x="35" y="19" fill="#F1F5F9" font-size="12" font-weight="700">Dim_Course (LMS Tiers 1, 2, 3)</text>
        <text x="325" y="19" text-anchor="end" fill="#34D399" font-size="11">10</text>
      </g>

      <!-- Dim 6 -->
      <g transform="translate(15, 275)">
        <polygon points="12,0 24,7 24,21 12,28 0,21 0,7" fill="#047857" stroke="#10B981" stroke-width="1"/>
        <text x="35" y="19" fill="#F1F5F9" font-size="12" font-weight="700">Dim_CurrencyRates (FX Multiplier)</text>
        <text x="325" y="19" text-anchor="end" fill="#34D399" font-size="11">6</text>
      </g>
    </g>

    <!-- Star Schema Relationship Rules -->
    <g transform="translate(25, 445)">
      <rect x="0" y="0" width="365" height="230" rx="14" fill="url(#cardInner)" stroke="#F59E0B" stroke-width="1.2"/>
      <text x="15" y="28" fill="#FDE68A" font-size="13" font-weight="800">5 Specialized Fact Constellations</text>
      <text x="15" y="48" fill="#94A3B8" font-size="11">Multi-Grain Architecture with Zero Fact Joins</text>
      <rect x="15" y="60" width="335" height="1" fill="#334155"/>

      <text x="15" y="82" fill="#FBBF24" font-size="11" font-weight="700">1. Monthly Periodic Snapshot (7,000)</text>
      <text x="30" y="100" fill="#CBD5E1" font-size="11">Fact_WorkforceSnapshot (HC, Salary, Flight Risk)</text>

      <text x="15" y="122" fill="#FBBF24" font-size="11" font-weight="700">2. Daily IoT Clock-Ins (16,000)</text>
      <text x="30" y="140" fill="#CBD5E1" font-size="11">Fact_DailyAttendance (Turnstile &amp; Remote Gates)</text>

      <text x="15" y="162" fill="#FBBF24" font-size="11" font-weight="700">3. Quarterly FP&amp;A Run-Rate (672)</text>
      <text x="30" y="180" fill="#CBD5E1" font-size="11">Fact_DepartmentBudget (DAX Budget ÷ 3)</text>

      <text x="15" y="202" fill="#FBBF24" font-size="11" font-weight="700">4. Talent Certifications (2,735)</text>
      <text x="30" y="220" fill="#CBD5E1" font-size="11">Fact_TrainingCompletions (ΔP Talent ROI)</text>

      <text x="15" y="242" fill="#FBBF24" font-size="11" font-weight="700">5. Client Milestone Delivery (3,600)</text>
    </g>

    <!-- Galaxy Best Practices -->
    <g transform="translate(25, 695)">
      <rect x="0" y="0" width="365" height="450" rx="14" fill="url(#cardInner)" stroke="#F59E0B" stroke-width="1"/>
      <text x="15" y="28" fill="#FDE68A" font-size="13" font-weight="800">Galaxy Modeling Best Practices</text>
      <rect x="15" y="42" width="335" height="1" fill="#334155"/>

      <text x="15" y="70" fill="#38BDF8" font-size="11" font-weight="700">Rule 1: Single-Direction (1 → *)</text>
      <text x="15" y="90" fill="#CBD5E1" font-size="11">Conformed dims filter facts; bidirectional</text>
      <text x="15" y="106" fill="#CBD5E1" font-size="11">filtering is strictly prohibited to prevent loops.</text>

      <text x="15" y="135" fill="#38BDF8" font-size="11" font-weight="700">Rule 2: Fact-to-Fact Isolation</text>
      <text x="15" y="155" fill="#CBD5E1" font-size="11">Zero physical joins between facts in diagram.</text>
      <text x="15" y="171" fill="#CBD5E1" font-size="11">DAX dynamically evaluates cross-fact ratios</text>
      <text x="15" y="187" fill="#CBD5E1" font-size="11">(e.g. Budget Variance = [Actual] - [Budget]).</text>

      <text x="15" y="216" fill="#38BDF8" font-size="11" font-weight="700">Rule 3: Multi-Grain Apportionment</text>
      <text x="15" y="236" fill="#CBD5E1" font-size="11">Quarterly budget is divided by 3 dynamically</text>
      <text x="15" y="252" fill="#CBD5E1" font-size="11">in DAX to compare against monthly payroll.</text>

      <text x="15" y="281" fill="#38BDF8" font-size="11" font-weight="700">Rule 4: Multi-Currency Normalization</text>
      <text x="15" y="301" fill="#CBD5E1" font-size="11">Dim_CurrencyRates converts offshore USD</text>
      <text x="15" y="317" fill="#CBD5E1" font-size="11">billings &amp; local EGP payroll dynamically.</text>

      <rect x="15" y="335" width="335" height="1" fill="#334155"/>
      <text x="15" y="362" fill="#10B981" font-size="11" font-weight="700">✔ Eliminates Grain Mismatch &amp; Fan Traps</text>
      <text x="15" y="386" fill="#A855F7" font-size="11" font-weight="700">✔ Full Kimball Dimensional Standard</text>
      <text x="15" y="410" fill="#38BDF8" font-size="11" font-weight="700">✔ In-Memory Table.Buffer() Optimized</text>
      <text x="15" y="432" fill="#F59E0B" font-size="11" font-weight="700">✔ Docker &amp; Terraform Cloud IaC Ready</text>
    </g>
  </g>

  <!-- Connectors Stage 4 -> Stage 5 -->
  <path d="M 1920 350 C 1945 350, 1945 380, 1970 380" fill="none" stroke="url(#gradStage4)" stroke-width="2.5" marker-end="url(#arrowAmber)"/>
  <path d="M 1920 650 C 1945 650, 1945 650, 1970 650" fill="none" stroke="url(#gradStage4)" stroke-width="2.5" marker-end="url(#arrowAmber)"/>
  <path d="M 1920 950 C 1945 950, 1945 900, 1970 900" fill="none" stroke="url(#gradStage4)" stroke-width="2.5" marker-end="url(#arrowAmber)"/>

  <!-- ── STAGE 5: POWER BI ANALYTICAL DIAGNOSTICS ── -->
  <g transform="translate(1970, 200)">
    <rect x="0" y="0" width="350" height="1180" rx="20" fill="url(#cardDark)" stroke="#1E293B" stroke-width="1.5" filter="url(#shadowBox)"/>
    
    <g transform="translate(20, 25)">
      <rect x="0" y="0" width="310" height="42" rx="10" fill="#2D0B24" stroke="#EC4899" stroke-width="1.2"/>
      <circle cx="20" cy="21" r="5" fill="#EC4899"/>
      <text x="36" y="26" fill="#E2E8F0" font-size="12" font-weight="800" letter-spacing="1">5. EXECUTIVE POWER BI DIAGNOSTICS</text>
    </g>

    <!-- Semantic Model Box -->
    <g transform="translate(20, 85)">
      <rect x="0" y="0" width="310" height="135" rx="12" fill="url(#cardInner)" stroke="#EC4899" stroke-width="1"/>
      <text x="15" y="24" fill="#F472B6" font-size="12" font-weight="800">Git-Native Semantic Model</text>
      <text x="15" y="42" fill="#94A3B8" font-size="11">Format: PBIP &amp; TMDL Definitions</text>
      <rect x="15" y="52" width="280" height="1" fill="#334155"/>
      <text x="15" y="74" fill="#CBD5E1" font-size="11">• Calculation Groups: Time Intelligence</text>
      <text x="15" y="94" fill="#CBD5E1" font-size="11">• Field Parameters: Dynamic Visual Slicing</text>
      <text x="15" y="114" fill="#CBD5E1" font-size="11">• VertiPaq Columnar Compression Engine</text>
    </g>

    <!-- Diagnostic 1: Salary Compression -->
    <g transform="translate(20, 235)">
      <rect x="0" y="0" width="310" height="105" rx="12" fill="url(#cardInner)" stroke="#334155"/>
      <circle cx="20" cy="22" r="4" fill="#F43F5E"/>
      <text x="32" y="25" fill="#FDA4AF" font-size="11" font-weight="800">1. Salary Compression &amp; Flight Risk</text>
      <text x="15" y="48" fill="#94A3B8" font-size="10">Detects veteran engineers earning &lt; market</text>
      <text x="15" y="65" fill="#94A3B8" font-size="10">median of new hires in identical tech role.</text>
      <text x="15" y="86" fill="#FB7185" font-size="10" font-weight="700">Flight Risk Severity: 1-100 Score</text>
    </g>

    <!-- Diagnostic 2: Headcount & Budget Variance -->
    <g transform="translate(20, 355)">
      <rect x="0" y="0" width="310" height="105" rx="12" fill="url(#cardInner)" stroke="#334155"/>
      <circle cx="20" cy="22" r="4" fill="#F59E0B"/>
      <text x="32" y="25" fill="#FDE68A" font-size="11" font-weight="800">2. Headcount &amp; Budget Variance</text>
      <text x="15" y="48" fill="#94A3B8" font-size="10">Harmonizes monthly payroll vs quarterly</text>
      <text x="15" y="65" fill="#94A3B8" font-size="10">departmental budget quotas dynamically.</text>
      <text x="15" y="86" fill="#FBBF24" font-size="10" font-weight="700">Payroll Burn Rate % Thresholds</text>
    </g>

    <!-- Diagnostic 3: Ghost Workers & Zero-Swipe Audit -->
    <g transform="translate(20, 475)">
      <rect x="0" y="0" width="310" height="105" rx="12" fill="url(#cardInner)" stroke="#334155"/>
      <circle cx="20" cy="22" r="4" fill="#10B981"/>
      <text x="32" y="25" fill="#A7F3D0" font-size="11" font-weight="800">3. Ghost Worker &amp; Policy Audit</text>
      <text x="15" y="48" fill="#94A3B8" font-size="10">Cross-references active payroll records</text>
      <text x="15" y="65" fill="#94A3B8" font-size="10">against 0 turnstile swipes over &gt; 60 days.</text>
      <text x="15" y="86" fill="#34D399" font-size="10" font-weight="700">Automated Direct-Deposit Freeze Alert</text>
    </g>

    <!-- Diagnostic 4: Client Delivery & Bench Utilization -->
    <g transform="translate(20, 595)">
      <rect x="0" y="0" width="310" height="105" rx="12" fill="url(#cardInner)" stroke="#334155"/>
      <circle cx="20" cy="22" r="4" fill="#38BDF8"/>
      <text x="32" y="25" fill="#BAE6FD" font-size="11" font-weight="800">4. Client Delivery &amp; Bench Utilization</text>
      <text x="15" y="48" fill="#94A3B8" font-size="10">Billable hours realization vs bench cost.</text>
      <text x="15" y="65" fill="#94A3B8" font-size="10">Scope creep alerts and delivery deadlines.</text>
      <text x="15" y="86" fill="#38BDF8" font-size="10" font-weight="700">Client Satisfaction (CSAT) Metrics</text>
    </g>

    <!-- Diagnostic 5: Upskilling Velocity ROI -->
    <g transform="translate(20, 715)">
      <rect x="0" y="0" width="310" height="105" rx="12" fill="url(#cardInner)" stroke="#334155"/>
      <circle cx="20" cy="22" r="4" fill="#C084FC"/>
      <text x="32" y="25" fill="#E9D5FF" font-size="11" font-weight="800">5. Upskilling Velocity (ΔP ROI)</text>
      <text x="15" y="48" fill="#94A3B8" font-size="10">Appraisal rating uplift between certified</text>
      <text x="15" y="65" fill="#94A3B8" font-size="10">tech talent vs uncertified peers.</text>
      <text x="15" y="86" fill="#C084FC" font-size="10" font-weight="700">Cost per Rating Point Improvement</text>
    </g>

    <!-- Diagnostic 6: Multi-Currency Global Operations -->
    <g transform="translate(20, 835)">
      <rect x="0" y="0" width="310" height="105" rx="12" fill="url(#cardInner)" stroke="#334155"/>
      <circle cx="20" cy="22" r="4" fill="#FBBF24"/>
      <text x="32" y="25" fill="#FDE68A" font-size="11" font-weight="800">6. Multi-Currency FX Consolidated</text>
      <text x="15" y="48" fill="#94A3B8" font-size="10">Converts global USD/EUR client revenue</text>
      <text x="15" y="65" fill="#94A3B8" font-size="10">against local EGP software engineering cost.</text>
      <text x="15" y="86" fill="#FBBF24" font-size="10" font-weight="700">Gross Margin &amp; Hedging Realization</text>
    </g>

    <!-- UI/UX Executive Features -->
    <g transform="translate(20, 955)">
      <rect x="0" y="0" width="310" height="190" rx="12" fill="url(#cardInner)" stroke="#EC4899" stroke-width="1"/>
      <text x="15" y="25" fill="#F472B6" font-size="12" font-weight="800">Executive Glassmorphism UX</text>
      <rect x="15" y="36" width="280" height="1" fill="#334155"/>
      <text x="15" y="60" fill="#E2E8F0" font-size="10">• 1080p Canvas (1920 × 1080 16:9)</text>
      <text x="15" y="80" fill="#E2E8F0" font-size="10">• Dark Glassmorphism Navigation Bar</text>
      <text x="15" y="100" fill="#E2E8F0" font-size="10">• Hero Status Cards with Micro-Sparklines</text>
      <text x="15" y="120" fill="#E2E8F0" font-size="10">• 360° Employee Dossier Drill-Throughs</text>
      <text x="15" y="140" fill="#E2E8F0" font-size="10">• Dynamic Tooltip Micro-Visualizations</text>
      <text x="15" y="165" fill="#10B981" font-size="10" font-weight="700">★ Ready for Enterprise Boardroom</text>
    </g>
  </g>
</svg>'''


def generate_galaxy_diagram() -> str:
    """Generates the modern Kimball Galaxy Schema (Fact Constellation) Diagram SVG with 6 Dims and 5 Facts."""
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 1440" width="2400" height="1440" style="background:#030712; font-family:'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="35%" stop-color="#070E22"/>
      <stop offset="70%" stop-color="#050A19"/>
      <stop offset="100%" stop-color="#010309"/>
    </linearGradient>

    <!-- Dot Grid Pattern -->
    <pattern id="dotGrid2" x="0" y="0" width="32" height="32" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#334155" fill-opacity="0.35"/>
    </pattern>

    <!-- Dimension Header Gradient (Emerald/Teal) -->
    <linearGradient id="dimHeaderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#047857"/>
    </linearGradient>

    <!-- Fact Header Gradient (Amber/Orange) -->
    <linearGradient id="factHeaderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>

    <!-- Title Gradient -->
    <linearGradient id="titleGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#34D399"/>
      <stop offset="35%" stop-color="#38BDF8"/>
      <stop offset="70%" stop-color="#A78BFA"/>
      <stop offset="100%" stop-color="#F472B6"/>
    </linearGradient>

    <!-- Card Backgrounds -->
    <linearGradient id="cardDark2" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" stop-opacity="0.94"/>
      <stop offset="100%" stop-color="#070C18" stop-opacity="0.98"/>
    </linearGradient>

    <!-- Drop Shadow Filter -->
    <filter id="shadowBox2" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="14" stdDeviation="12" flood-color="#000000" flood-opacity="0.7"/>
    </filter>

    <!-- Markers -->
    <marker id="arrowGreen" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#10B981"/>
    </marker>
    <marker id="arrowOrange" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#F59E0B"/>
    </marker>
  </defs>

  <rect width="2400" height="1440" fill="url(#bgGrad2)"/>
  <rect width="2400" height="1440" fill="url(#dotGrid2)"/>

  <!-- Ambient Glow Orbs -->
  <circle cx="1200" cy="680" r="520" fill="#059669" fill-opacity="0.05" filter="blur(100px)"/>
  <circle cx="400" cy="420" r="380" fill="#D97706" fill-opacity="0.04" filter="blur(80px)"/>
  <circle cx="2000" cy="950" r="380" fill="#2563EB" fill-opacity="0.04" filter="blur(80px)"/>

  <!-- ========================================================================= -->
  <!-- HEADER                                                                    -->
  <!-- ========================================================================= -->
  <g transform="translate(80, 45)">
    <rect x="0" y="0" width="460" height="32" rx="16" fill="#064E3B" stroke="#059669" stroke-width="1.2"/>
    <circle cx="16" cy="16" r="5" fill="#34D399"/>
    <text x="32" y="21" fill="#A7F3D0" font-size="11" font-weight="800" letter-spacing="1.5">KIMBALL GALAXY SCHEMA · 6 CONFORMED DIMS · 5 FACTS · 322,217 ROWS</text>

    <text x="0" y="74" fill="url(#titleGrad2)" font-size="34" font-weight="800">
      Nexora Tech Solutions: Conformed Dimensions &amp; Multi-Grain Fact Constellations
    </text>
    <text x="0" y="102" fill="#94A3B8" font-size="15">
      6 Conformed Dimensions (Green) Shared Across 5 Multi-Grain Fact Constellations (Amber) with Single-Direction (1 → *) Filter Propagation &amp; Table.Buffer() Caching
    </text>

    <!-- Advanced Architecture Badges -->
    <g transform="translate(1360, 10)">
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="195" height="40" rx="10" fill="#0F172A" stroke="#10B981" stroke-width="1.2"/>
        <circle cx="16" cy="20" r="5" fill="#10B981"/>
        <text x="30" y="25" fill="#D1FAE5" font-size="11" font-weight="700">In-Memory Table.Buffer()</text>
      </g>

      <g transform="translate(210, 0)">
        <rect x="0" y="0" width="195" height="40" rx="10" fill="#0F172A" stroke="#0284C7" stroke-width="1.2"/>
        <circle cx="16" cy="20" r="5" fill="#38BDF8"/>
        <text x="30" y="25" fill="#E0F2FE" font-size="11" font-weight="700">Dynamic Date Harvest</text>
      </g>

      <g transform="translate(420, 0)">
        <rect x="0" y="0" width="230" height="40" rx="10" fill="#0F172A" stroke="#F59E0B" stroke-width="1.2"/>
        <circle cx="16" cy="20" r="5" fill="#FBBF24"/>
        <text x="30" y="25" fill="#FEF3C7" font-size="11" font-weight="700">Multi-Currency (Dim_FX)</text>
      </g>

      <g transform="translate(665, 0)">
        <rect x="0" y="0" width="225" height="40" rx="10" fill="#0F172A" stroke="#8B5CF6" stroke-width="1.2"/>
        <circle cx="16" cy="20" r="5" fill="#C084FC"/>
        <text x="30" y="25" fill="#EDE9FE" font-size="11" font-weight="700">Docker &amp; Terraform IaC</text>
      </g>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 6 CONFORMED DIMENSIONS (GREEN THEME)                                      -->
  <!-- ========================================================================= -->

  <!-- DIMENSION 1: Dim_Employee (CENTER HUB) -->
  <g transform="translate(980, 500)" filter="url(#shadowBox2)">
    <rect x="0" y="0" width="440" height="410" rx="16" fill="url(#cardDark2)" stroke="#10B981" stroke-width="2"/>
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 424 0 C 432.84 0 440 7.16 440 16 L 440 50 L 0 50 Z" fill="url(#dimHeaderGrad)"/>
    <polygon points="25,18 35,24 35,36 25,42 15,36 15,24" fill="#064E3B" stroke="#34D399" stroke-width="1.5"/>
    <text x="45" y="32" fill="#FFFFFF" font-size="16" font-weight="800">Dim_Employee</text>
    <text x="420" y="32" text-anchor="end" fill="#D1FAE5" font-size="12" font-weight="700">7,000 Rows · SCD-2 Hub</text>

    <g transform="translate(20, 65)">
      <text x="0" y="20" fill="#34D399" font-size="12" font-weight="800">🔑 EmployeeKey (INT PK, Surrogate)</text>
      <text x="0" y="45" fill="#E2E8F0" font-size="12">EmployeeID (VARCHAR UK - EMP-10001..17000)</text>
      <text x="0" y="70" fill="#E2E8F0" font-size="12">FullName (NVARCHAR - Authentic Arabic Names)</text>
      <text x="0" y="95" fill="#E2E8F0" font-size="12">Age, Gender (ذكر / أنثى), MaritalStatus</text>
      <text x="0" y="120" fill="#E2E8F0" font-size="12">JobRole, ContractType (دوام كامل / هجين)</text>
      <text x="0" y="145" fill="#E2E8F0" font-size="12">BaseSalary_EGP, Currency (EGP / USD)</text>
      <text x="0" y="170" fill="#E2E8F0" font-size="12">HireDate, TenureYears, TenureMonths</text>
      <text x="0" y="195" fill="#E2E8F0" font-size="12">SalaryBand, PerformanceTier, FlightRiskIndex</text>
      <rect x="0" y="210" width="400" height="1" fill="#334155"/>
      <text x="0" y="235" fill="#FBBF24" font-size="12" font-weight="700">SCD Type 2 Validity Intervals:</text>
      <text x="0" y="255" fill="#94A3B8" font-size="11">EffectiveDate, ExpiryDate (9999-12-31), IsCurrent</text>
      <text x="0" y="280" fill="#38BDF8" font-size="11" font-weight="700">Grounded strictly on employees_data_7000.txt</text>
      <text x="0" y="305" fill="#10B981" font-size="11">Buffered in RAM via Table.Buffer() for fast merges</text>
    </g>
  </g>

  <!-- DIMENSION 2: Dim_Date (TOP CENTER) -->
  <g transform="translate(980, 180)" filter="url(#shadowBox2)">
    <rect x="0" y="0" width="440" height="260" rx="16" fill="url(#cardDark2)" stroke="#10B981" stroke-width="2"/>
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 424 0 C 432.84 0 440 7.16 440 16 L 440 50 L 0 50 Z" fill="url(#dimHeaderGrad)"/>
    <polygon points="25,18 35,24 35,36 25,42 15,36 15,24" fill="#064E3B" stroke="#34D399" stroke-width="1.5"/>
    <text x="45" y="32" fill="#FFFFFF" font-size="16" font-weight="800">Dim_Date (Enterprise Calendar)</text>
    <text x="420" y="32" text-anchor="end" fill="#D1FAE5" font-size="12" font-weight="700">1,096 Days</text>

    <g transform="translate(20, 65)">
      <text x="0" y="20" fill="#34D399" font-size="12" font-weight="800">🔑 DateKey (INT PK - YYYYMMDD)</text>
      <text x="0" y="45" fill="#E2E8F0" font-size="12">FullDate (DATE - Dynamically Harvested)</text>
      <text x="0" y="70" fill="#E2E8F0" font-size="12">CalendarYear, CalendarQuarter (Q1..Q4)</text>
      <text x="0" y="95" fill="#E2E8F0" font-size="12">MonthNumberOfYear (1..12), MonthName</text>
      <text x="0" y="120" fill="#E2E8F0" font-size="12">DayNumberOfWeek, DayNameOfWeek</text>
      <text x="0" y="145" fill="#94A3B8" font-size="11">Egyptian Weekend: IsWeekend = (Day ∈ [Fri, Sat])</text>
      <text x="0" y="170" fill="#38BDF8" font-size="11" font-weight="700">Boundaries auto-calculated from List.Min / List.Max</text>
    </g>
  </g>

  <!-- DIMENSION 3: Dim_Department (LEFT TOP) -->
  <g transform="translate(520, 180)" filter="url(#shadowBox2)">
    <rect x="0" y="0" width="380" height="230" rx="16" fill="url(#cardDark2)" stroke="#10B981" stroke-width="1.5"/>
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 364 0 C 372.84 0 380 7.16 380 16 L 380 48 L 0 48 Z" fill="url(#dimHeaderGrad)"/>
    <text x="20" y="30" fill="#FFFFFF" font-size="15" font-weight="800">Dim_Department</text>
    <text x="360" y="30" text-anchor="end" fill="#D1FAE5" font-size="11">6 Divisions</text>

    <g transform="translate(20, 65)">
      <text x="0" y="20" fill="#34D399" font-size="12" font-weight="800">🔑 DepartmentKey (INT PK)</text>
      <text x="0" y="45" fill="#E2E8F0" font-size="12">DepartmentID (DEPT-001..006)</text>
      <text x="0" y="70" fill="#E2E8F0" font-size="12">DepartmentName (Software Eng, AI...)</text>
      <text x="0" y="95" fill="#E2E8F0" font-size="12">Division (Tech Solutions, Cloud Services)</text>
      <text x="0" y="120" fill="#94A3B8" font-size="11">Conformed across Payroll, Budget &amp; Tasks</text>
    </g>
  </g>

  <!-- DIMENSION 4: Dim_Branch (RIGHT TOP) -->
  <g transform="translate(1500, 180)" filter="url(#shadowBox2)">
    <rect x="0" y="0" width="380" height="230" rx="16" fill="url(#cardDark2)" stroke="#10B981" stroke-width="1.5"/>
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 364 0 C 372.84 0 380 7.16 380 16 L 380 48 L 0 48 Z" fill="url(#dimHeaderGrad)"/>
    <text x="20" y="30" fill="#FFFFFF" font-size="15" font-weight="800">Dim_Branch (Geographic)</text>
    <text x="360" y="30" text-anchor="end" fill="#D1FAE5" font-size="11">14 Tech Hubs</text>

    <g transform="translate(20, 65)">
      <text x="0" y="20" fill="#34D399" font-size="12" font-weight="800">🔑 BranchKey (INT PK)</text>
      <text x="0" y="45" fill="#E2E8F0" font-size="12">BranchID (BR-001..014), BranchName</text>
      <text x="0" y="70" fill="#E2E8F0" font-size="12">Region (Cairo Smart Village, Alex, Assiut...)</text>
      <text x="0" y="95" fill="#E2E8F0" font-size="12">City (Cairo, Alexandria, Giza, Tanta, Mansoura)</text>
      <text x="0" y="120" fill="#94A3B8" font-size="11">DeskCapacity (On-site vs Hybrid allocations)</text>
    </g>
  </g>

  <!-- DIMENSION 5: Dim_Course (RIGHT BOTTOM) -->
  <g transform="translate(1500, 500)" filter="url(#shadowBox2)">
    <rect x="0" y="0" width="380" height="230" rx="16" fill="url(#cardDark2)" stroke="#10B981" stroke-width="1.5"/>
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 364 0 C 372.84 0 380 7.16 380 16 L 380 48 L 0 48 Z" fill="url(#dimHeaderGrad)"/>
    <text x="20" y="30" fill="#FFFFFF" font-size="15" font-weight="800">Dim_Course (LMS Academy)</text>
    <text x="360" y="30" text-anchor="end" fill="#D1FAE5" font-size="11">10 Courses · 3 Tiers</text>

    <g transform="translate(20, 65)">
      <text x="0" y="20" fill="#34D399" font-size="12" font-weight="800">🔑 CourseKey (INT PK)</text>
      <text x="0" y="45" fill="#E2E8F0" font-size="12">CourseID (CRS-101..303), CourseName</text>
      <text x="0" y="70" fill="#E2E8F0" font-size="12">CourseLevel (Level 1, Level 2, Level 3)</text>
      <text x="0" y="95" fill="#E2E8F0" font-size="12">SkillDomain (Cloud, Data/AI, DevOps, Cyber)</text>
      <text x="0" y="120" fill="#94A3B8" font-size="11">Accreditation: Microsoft, AWS, Databricks, CNCF</text>
    </g>
  </g>

  <!-- DIMENSION 6: Dim_CurrencyRates (RIGHT LOWER) -->
  <g transform="translate(1500, 770)" filter="url(#shadowBox2)">
    <rect x="0" y="0" width="380" height="230" rx="16" fill="url(#cardDark2)" stroke="#10B981" stroke-width="1.5"/>
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 364 0 C 372.84 0 380 7.16 380 16 L 380 48 L 0 48 Z" fill="url(#dimHeaderGrad)"/>
    <text x="20" y="30" fill="#FFFFFF" font-size="15" font-weight="800">Dim_CurrencyRates (FX)</text>
    <text x="360" y="30" text-anchor="end" fill="#D1FAE5" font-size="11">6 Currencies</text>

    <g transform="translate(20, 65)">
      <text x="0" y="20" fill="#34D399" font-size="12" font-weight="800">🔑 CurrencyKey (INT PK)</text>
      <text x="0" y="45" fill="#E2E8F0" font-size="12">CurrencyCode (EGP, USD, EUR, GBP, SAR, AED)</text>
      <text x="0" y="70" fill="#E2E8F0" font-size="12">RateToEGP, OneEGPInCurrency (Multiplier)</text>
      <text x="0" y="95" fill="#E2E8F0" font-size="12">RateType (Central Bank Spot / Base Peg)</text>
      <text x="0" y="120" fill="#38BDF8" font-size="11" font-weight="700">Dynamic DAX Multi-Currency Slicing</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 5 GALAXY FACT TABLES (AMBER/ORANGE THEME)                                 -->
  <!-- ========================================================================= -->

  <!-- FACT 1: Fact_WorkforceSnapshot (LEFT) -->
  <g transform="translate(60, 500)" filter="url(#shadowBox2)">
    <rect x="0" y="0" width="410" height="410" rx="16" fill="url(#cardDark2)" stroke="#F59E0B" stroke-width="2"/>
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 394 0 C 402.84 0 410 7.16 410 16 L 410 50 L 0 50 Z" fill="url(#factHeaderGrad)"/>
    <text x="20" y="32" fill="#FFFFFF" font-size="16" font-weight="800">Fact_WorkforceSnapshot</text>
    <text x="390" y="32" text-anchor="end" fill="#FEF3C7" font-size="12">Monthly</text>

    <g transform="translate(20, 65)">
      <text x="0" y="20" fill="#FBBF24" font-size="12" font-weight="800">🔑 SnapshotKey (BIGINT PK)</text>
      <rect x="0" y="30" width="370" height="1" fill="#334155"/>
      <text x="0" y="55" fill="#6EE7B7" font-size="12">🔗 EmployeeKey (FK → Dim_Employee)</text>
      <text x="0" y="80" fill="#6EE7B7" font-size="12">🔗 DepartmentKey (FK → Dim_Department)</text>
      <text x="0" y="105" fill="#6EE7B7" font-size="12">🔗 BranchKey (FK → Dim_Branch)</text>
      <text x="0" y="130" fill="#6EE7B7" font-size="12">🔗 SnapshotDateKey (FK → Dim_Date)</text>
      <text x="0" y="155" fill="#6EE7B7" font-size="12">🔗 CurrencyKey (FK → Dim_CurrencyRates)</text>
      <rect x="0" y="170" width="370" height="1" fill="#334155"/>
      <text x="0" y="195" fill="#F1F5F9" font-size="12" font-weight="700">Measures &amp; Flight Risk:</text>
      <text x="0" y="220" fill="#CBD5E1" font-size="12">• BaseSalary_EGP (Monthly Payroll Run-rate)</text>
      <text x="0" y="245" fill="#CBD5E1" font-size="12">• AnnualPerformanceRating (1.0..5.0)</text>
      <text x="0" y="270" fill="#CBD5E1" font-size="12">• SalaryPercentileInRole, TenureMonths</text>
      <text x="0" y="295" fill="#EF4444" font-size="12">• IsSalaryCompressed (Veteran Flight Risk Flag)</text>
      <text x="0" y="320" fill="#10B981" font-size="11" font-weight="700">Grain: 1 Row / Active Employee / Month (7,000 Rows)</text>
    </g>
  </g>

  <!-- FACT 2: Fact_DailyAttendance (BOTTOM CENTER) -->
  <g transform="translate(980, 960)" filter="url(#shadowBox2)">
    <rect x="0" y="0" width="440" height="380" rx="16" fill="url(#cardDark2)" stroke="#F59E0B" stroke-width="2"/>
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 424 0 C 432.84 0 440 7.16 440 16 L 440 50 L 0 50 Z" fill="url(#factHeaderGrad)"/>
    <text x="20" y="32" fill="#FFFFFF" font-size="16" font-weight="800">Fact_DailyAttendance</text>
    <text x="420" y="32" text-anchor="end" fill="#FEF3C7" font-size="12">Daily IoT</text>

    <g transform="translate(20, 65)">
      <text x="0" y="20" fill="#FBBF24" font-size="12" font-weight="800">🔑 AttendanceKey (BIGINT PK)</text>
      <rect x="0" y="30" width="400" height="1" fill="#334155"/>
      <text x="0" y="55" fill="#6EE7B7" font-size="12">🔗 EmployeeKey (FK → Dim_Employee)</text>
      <text x="0" y="80" fill="#6EE7B7" font-size="12">🔗 BranchKey (FK → Dim_Branch)</text>
      <text x="0" y="105" fill="#6EE7B7" font-size="12">🔗 AccessDateKey (FK → Dim_Date)</text>
      <rect x="0" y="120" width="400" height="1" fill="#334155"/>
      <text x="0" y="145" fill="#F1F5F9" font-size="12" font-weight="700">Measures &amp; Telemetry:</text>
      <text x="0" y="170" fill="#CBD5E1" font-size="12">• CheckInTime, CheckOutTime, DurationHours</text>
      <text x="0" y="195" fill="#CBD5E1" font-size="12">• DeclaredWorkMode vs ActualWorkMode</text>
      <text x="0" y="220" fill="#EF4444" font-size="12">• IsImputedClockOut (Recovered Forgotten Swipe)</text>
      <text x="0" y="245" fill="#EF4444" font-size="12">• IsTardyArrival (> 9:15 AM), OvertimeHours</text>
      <text x="0" y="270" fill="#10B981" font-size="11" font-weight="700">Grain: 1 Row / Employee / Badge Access Day (16,000 Rows)</text>
    </g>
  </g>

  <!-- FACT 3: Fact_DepartmentBudget (LEFT BOTTOM) -->
  <g transform="translate(520, 960)" filter="url(#shadowBox2)">
    <rect x="0" y="0" width="380" height="380" rx="16" fill="url(#cardDark2)" stroke="#F59E0B" stroke-width="2"/>
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 364 0 C 372.84 0 380 7.16 380 16 L 380 50 L 0 50 Z" fill="url(#factHeaderGrad)"/>
    <text x="20" y="32" fill="#FFFFFF" font-size="16" font-weight="800">Fact_DepartmentBudget</text>
    <text x="360" y="32" text-anchor="end" fill="#FEF3C7" font-size="12">Quarterly</text>

    <g transform="translate(20, 65)">
      <text x="0" y="20" fill="#FBBF24" font-size="12" font-weight="800">🔑 BudgetKey (INT PK)</text>
      <rect x="0" y="30" width="340" height="1" fill="#334155"/>
      <text x="0" y="55" fill="#6EE7B7" font-size="12">🔗 DepartmentKey (FK → Dim_Department)</text>
      <text x="0" y="80" fill="#6EE7B7" font-size="12">🔗 BranchKey (FK → Dim_Branch)</text>
      <text x="0" y="105" fill="#6EE7B7" font-size="12">🔗 DateKey (FK → Dim_Date, Quarter Start)</text>
      <text x="0" y="130" fill="#6EE7B7" font-size="12">🔗 CurrencyKey (FK → Dim_CurrencyRates)</text>
      <rect x="0" y="145" width="340" height="1" fill="#334155"/>
      <text x="0" y="170" fill="#F1F5F9" font-size="12" font-weight="700">Measures &amp; Quotas:</text>
      <text x="0" y="195" fill="#CBD5E1" font-size="12">• BudgetedHeadcount, HeadcountVariance</text>
      <text x="0" y="220" fill="#CBD5E1" font-size="12">• AllocatedSalaryBudget_EGP</text>
      <text x="0" y="245" fill="#38BDF8" font-size="11">Apportioned in DAX: Budget ÷ 3 = Monthly</text>
      <text x="0" y="270" fill="#10B981" font-size="11" font-weight="700">Grain: 1 Row / Dept / Branch / Quarter (672 Rows)</text>
    </g>
  </g>

  <!-- FACT 4: Fact_TrainingCompletions (FAR RIGHT TOP) -->
  <g transform="translate(1950, 180)" filter="url(#shadowBox2)">
    <rect x="0" y="0" width="390" height="380" rx="16" fill="url(#cardDark2)" stroke="#F59E0B" stroke-width="2"/>
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 374 0 C 382.84 0 390 7.16 390 16 L 390 50 L 0 50 Z" fill="url(#factHeaderGrad)"/>
    <text x="20" y="32" fill="#FFFFFF" font-size="15" font-weight="800">Fact_TrainingCompletions</text>
    <text x="370" y="32" text-anchor="end" fill="#FEF3C7" font-size="12">L&amp;D Events</text>

    <g transform="translate(20, 65)">
      <text x="0" y="20" fill="#FBBF24" font-size="12" font-weight="800">🔑 CompletionKey (INT PK)</text>
      <rect x="0" y="30" width="350" height="1" fill="#334155"/>
      <text x="0" y="55" fill="#6EE7B7" font-size="12">🔗 EmployeeKey (FK → Dim_Employee)</text>
      <text x="0" y="80" fill="#6EE7B7" font-size="12">🔗 CourseKey (FK → Dim_Course)</text>
      <text x="0" y="105" fill="#6EE7B7" font-size="12">🔗 CompletionDateKey (FK → Dim_Date)</text>
      <rect x="0" y="120" width="350" height="1" fill="#334155"/>
      <text x="0" y="145" fill="#F1F5F9" font-size="12" font-weight="700">Measures &amp; Scores:</text>
      <text x="0" y="170" fill="#CBD5E1" font-size="12">• Score (0.0 .. 100.0)</text>
      <text x="0" y="195" fill="#CBD5E1" font-size="12">• IsPassed (Score ≥ 70)</text>
      <text x="0" y="220" fill="#CBD5E1" font-size="12">• ScoreTier (Distinction / Proficient / Remediation)</text>
      <text x="0" y="245" fill="#CBD5E1" font-size="12">• CertificationCost_EGP</text>
      <text x="0" y="270" fill="#38BDF8" font-size="11">Talent ROI: Delta P (Upskilling Velocity)</text>
      <text x="0" y="295" fill="#10B981" font-size="11" font-weight="700">Grain: 1 Row / Certification Attempt (2,735 Rows)</text>
    </g>
  </g>

  <!-- FACT 5: Fact_ProjectTasks (FAR RIGHT LOWER) -->
  <g transform="translate(1950, 610)" filter="url(#shadowBox2)">
    <rect x="0" y="0" width="390" height="420" rx="16" fill="url(#cardDark2)" stroke="#F59E0B" stroke-width="2"/>
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 374 0 C 382.84 0 390 7.16 390 16 L 390 50 L 0 50 Z" fill="url(#factHeaderGrad)"/>
    <text x="20" y="32" fill="#FFFFFF" font-size="15" font-weight="800">Fact_ProjectTasks (Client Delivery)</text>
    <text x="370" y="32" text-anchor="end" fill="#FEF3C7" font-size="12">Tasks / SLAs</text>

    <g transform="translate(20, 65)">
      <text x="0" y="20" fill="#FBBF24" font-size="12" font-weight="800">🔑 TaskKey (INT PK) / TaskID</text>
      <rect x="0" y="30" width="350" height="1" fill="#334155"/>
      <text x="0" y="55" fill="#6EE7B7" font-size="12">🔗 EmployeeKey (FK → Dim_Employee)</text>
      <text x="0" y="80" fill="#6EE7B7" font-size="12">🔗 ProjectID (8 Enterprise Client Projects)</text>
      <text x="0" y="105" fill="#6EE7B7" font-size="12">🔗 DateKey (FK → Dim_Date, Delivery Date)</text>
      <text x="0" y="130" fill="#6EE7B7" font-size="12">🔗 CurrencyKey (FK → Dim_CurrencyRates, USD)</text>
      <rect x="0" y="145" width="350" height="1" fill="#334155"/>
      <text x="0" y="170" fill="#F1F5F9" font-size="12" font-weight="700">Measures &amp; Realization:</text>
      <text x="0" y="195" fill="#CBD5E1" font-size="12">• PlannedHours vs ActualHours</text>
      <text x="0" y="220" fill="#EF4444" font-size="12">• IsHoursOverrun (Scope Creep Alert)</text>
      <text x="0" y="245" fill="#CBD5E1" font-size="12">• BillableHourlyRate_USD, TotalBilling_USD</text>
      <text x="0" y="270" fill="#CBD5E1" font-size="12">• ClientSatisfactionRating (1.0..5.0 Stars)</text>
      <text x="0" y="295" fill="#38BDF8" font-size="11">Billable Realization vs Bench Cost Bleed</text>
      <text x="0" y="320" fill="#10B981" font-size="11" font-weight="700">Grain: 1 Row / Client Milestone Task (3,600 Rows)</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- SINGLE DIRECTION RELATIONSHIP CONNECTORS (1 → *)                          -->
  <!-- ========================================================================= -->

  <!-- Dim_Employee -> Fact_WorkforceSnapshot -->
  <path d="M 980 670 L 470 670" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
  <circle cx="975" cy="670" r="4" fill="#34D399"/>
  <text x="725" y="660" text-anchor="middle" fill="#6EE7B7" font-size="11" font-weight="800">1 → *</text>

  <!-- Dim_Employee -> Fact_DailyAttendance -->
  <path d="M 1200 910 L 1200 960" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
  <circle cx="1200" cy="915" r="4" fill="#34D399"/>
  <text x="1215" y="940" fill="#6EE7B7" font-size="11" font-weight="800">1 → *</text>

  <!-- Dim_Employee -> Fact_TrainingCompletions (Arching neatly above Dim_Course) -->
  <path d="M 1420 520 C 1460 450, 1900 450, 1950 370" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
  <circle cx="1425" cy="520" r="4" fill="#34D399"/>
  <text x="1680" y="440" fill="#6EE7B7" font-size="11" font-weight="800">1 → *</text>

  <!-- Dim_Employee -> Fact_ProjectTasks -->
  <path d="M 1420 720 C 1460 720, 1900 750, 1950 750" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
  <circle cx="1425" cy="720" r="4" fill="#34D399"/>
  <text x="1680" y="735" fill="#6EE7B7" font-size="11" font-weight="800">1 → *</text>

  <!-- Dim_Department -> Fact_WorkforceSnapshot (Clean arch) -->
  <path d="M 520 280 C 470 280, 470 420, 470 500" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrowGreen)"/>

  <!-- Dim_Department -> Fact_DepartmentBudget -->
  <path d="M 710 410 L 710 960" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
  <text x="725" y="690" fill="#6EE7B7" font-size="11" font-weight="800">1 → *</text>

  <!-- Dim_Branch -> Fact_WorkforceSnapshot (Clean top perimeter route) -->
  <path d="M 1500 200 C 1000 120, 300 120, 260 500" fill="none" stroke="#10B981" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrowGreen)"/>

  <!-- Dim_Branch -> Fact_DailyAttendance -->
  <path d="M 1650 410 C 1650 880, 1380 880, 1380 960" fill="none" stroke="#10B981" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrowGreen)"/>

  <!-- Dim_Branch -> Fact_DepartmentBudget -->
  <path d="M 1500 380 C 1460 480, 850 480, 850 960" fill="none" stroke="#10B981" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrowGreen)"/>

  <!-- Dim_Course -> Fact_TrainingCompletions -->
  <path d="M 1880 580 C 1910 580, 1910 420, 1950 420" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
  <text x="1900" y="500" fill="#6EE7B7" font-size="11" font-weight="800">1 → *</text>

  <!-- Dim_CurrencyRates -> Fact_WorkforceSnapshot (Clean bottom perimeter) -->
  <path d="M 1500 890 C 1440 940, 480 940, 470 820" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrowGreen)"/>

  <!-- Dim_CurrencyRates -> Fact_DepartmentBudget -->
  <path d="M 1500 850 C 1200 850, 880 880, 880 960" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrowGreen)"/>

  <!-- Dim_CurrencyRates -> Fact_ProjectTasks -->
  <path d="M 1880 880 C 1910 880, 1910 850, 1950 850" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrowGreen)"/>

  <!-- Dim_Date -> Fact_WorkforceSnapshot (Arches cleanly between dims) -->
  <path d="M 980 260 C 930 260, 930 460, 470 560" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrowGreen)"/>

  <!-- Dim_Date -> Fact_DailyAttendance -->
  <path d="M 1100 440 L 1100 960" fill="none" stroke="#10B981" stroke-width="2" stroke-dasharray="3,3" marker-end="url(#arrowGreen)"/>

  <!-- Dim_Date -> Fact_DepartmentBudget -->
  <path d="M 1000 440 C 850 550, 750 750, 680 960" fill="none" stroke="#10B981" stroke-width="2" stroke-dasharray="3,3" marker-end="url(#arrowGreen)"/>

  <!-- Dim_Date -> Fact_TrainingCompletions -->
  <path d="M 1420 220 L 1950 220" fill="none" stroke="#10B981" stroke-width="2" stroke-dasharray="3,3" marker-end="url(#arrowGreen)"/>

  <!-- Dim_Date -> Fact_ProjectTasks -->
  <path d="M 1420 280 C 1600 280, 1900 500, 1950 650" fill="none" stroke="#10B981" stroke-width="2" stroke-dasharray="3,3" marker-end="url(#arrowGreen)"/>

  <!-- ========================================================================= -->
  <!-- LEGEND & GOVERNANCE MATRIX                                                -->
  <!-- ========================================================================= -->
  <g transform="translate(60, 1260)">
    <rect x="0" y="0" width="1380" height="75" rx="14" fill="#0B1222" stroke="#1E293B"/>
    
    <circle cx="30" cy="37" r="7" fill="#10B981"/>
    <text x="45" y="42" fill="#E2E8F0" font-size="12" font-weight="700">Conformed Dimension (1 Side)</text>

    <circle cx="270" cy="37" r="7" fill="#F59E0B"/>
    <text x="285" y="42" fill="#E2E8F0" font-size="12" font-weight="700">Galaxy Fact Table (* Side)</text>

    <line x1="500" y1="37" x2="550" y2="37" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
    <text x="560" y="42" fill="#E2E8F0" font-size="12" font-weight="700">Single-Direction Filter (1 → *)</text>

    <rect x="760" y="22" width="125" height="32" rx="8" fill="#1E293B" stroke="#334155"/>
    <text x="822" y="42" text-anchor="middle" fill="#38BDF8" font-size="11" font-weight="700">VERTI-PAQ OPT</text>

    <rect x="895" y="22" width="145" height="32" rx="8" fill="#1E293B" stroke="#10B981"/>
    <text x="967" y="42" text-anchor="middle" fill="#34D399" font-size="11" font-weight="700">29/29 PYTESTS OK</text>

    <rect x="1050" y="22" width="155" height="32" rx="8" fill="#1E293B" stroke="#8B5CF6"/>
    <text x="1127" y="42" text-anchor="middle" fill="#C084FC" font-size="11" font-weight="700">DOCKER &amp; IAC READY</text>

    <rect x="1215" y="22" width="150" height="32" rx="8" fill="#1E293B" stroke="#F59E0B"/>
    <text x="1290" y="42" text-anchor="middle" fill="#FBBF24" font-size="11" font-weight="700">22 DWH TABLES</text>
  </g>
</svg>'''


def main():
    print("Generating updated, modern vector architecture diagrams (Nexora Tech Solutions)...")
    
    # 1. Lifecycle diagram
    lifecycle_svg = generate_lifecycle_diagram()
    lifecycle_path = ASSETS_DIR / "project_lifecycle_architecture.svg"
    with open(lifecycle_path, "w", encoding="utf-8") as f:
        f.write(lifecycle_svg)
    print(f"  [OK] Generated {lifecycle_path}")

    # 2. Galaxy Schema diagram
    galaxy_svg = generate_galaxy_diagram()
    galaxy_path = ASSETS_DIR / "enterprise_galaxy_architecture.svg"
    with open(galaxy_path, "w", encoding="utf-8") as f:
        f.write(galaxy_svg)
    print(f"  [OK] Generated {galaxy_path}")

    print("All architecture diagrams modernized successfully.")


if __name__ == "__main__":
    main()
