import os
import math

# Output SVG path
output_path = "docs/assets/project_lifecycle_architecture.svg"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

def hex_points(cx, cy, r):
    """Calculates flat-topped hexagon vertices."""
    pts = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        pts.append(f"{cx + r * math.cos(angle_rad):.1f},{cy + r * math.sin(angle_rad):.1f}")
    return " ".join(pts)

def diamond_points(cx, cy, w, h):
    """Calculates diamond vertices."""
    return f"{cx},{cy - h/2} {cx + w/2},{cy} {cx},{cy + h/2} {cx - w/2},{cy}"

def octagon_points(cx, cy, r):
    """Calculates octagon vertices."""
    pts = []
    for i in range(8):
        angle_deg = 45 * i + 22.5
        angle_rad = math.pi / 180 * angle_deg
        pts.append(f"{cx + r * math.cos(angle_rad):.1f},{cy + r * math.sin(angle_rad):.1f}")
    return " ".join(pts)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2200 1350" width="2200" height="1350">
  <defs>
    <!-- Master Gradients -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#050811"/>
      <stop offset="35%" stop-color="#0B1021"/>
      <stop offset="70%" stop-color="#080D1B"/>
      <stop offset="100%" stop-color="#04060C"/>
    </linearGradient>

    <!-- Stage 1 Cyan Gradient -->
    <linearGradient id="gradStage1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#0072F5"/>
    </linearGradient>

    <!-- Stage 2 Purple Gradient -->
    <linearGradient id="gradStage2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#C084FC"/>
      <stop offset="100%" stop-color="#7928CA"/>
    </linearGradient>

    <!-- Stage 3 Emerald Gradient -->
    <linearGradient id="gradStage3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#047857"/>
    </linearGradient>

    <!-- Stage 3 Amber Gradient -->
    <linearGradient id="gradStage3Fact" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FBBF24"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>

    <!-- Stage 4 Rose Gradient -->
    <linearGradient id="gradStage4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F43F5E"/>
      <stop offset="100%" stop-color="#BE123C"/>
    </linearGradient>

    <!-- Stage 5 Gold Gradient -->
    <linearGradient id="gradStage5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#EA580C"/>
    </linearGradient>

    <!-- Header Gradient -->
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="30%" stop-color="#818CF8"/>
      <stop offset="70%" stop-color="#C084FC"/>
      <stop offset="100%" stop-color="#FB7185"/>
    </linearGradient>

    <!-- Dark Card Gradients -->
    <linearGradient id="cardDark" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1E293B" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.95"/>
    </linearGradient>

    <!-- Filters -->
    <filter id="glowCyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glowPurple" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glowEmerald" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glowAmber" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="125%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>

  <style>
    .font-sans {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; }}
    .mono {{ font-family: 'Consolas', 'Fira Code', monospace; }}
  </style>

  <!-- Deep Obsidian Background Canvas -->
  <rect width="2200" height="1350" fill="url(#bgGrad)"/>

  <!-- Subtle Geometric Grid Background -->
  <g opacity="0.04" stroke="#FFFFFF" stroke-width="1">
    {' '.join([f'<line x1="{x}" y1="0" x2="{x}" y2="1350"/>' for x in range(0, 2201, 80)])}
    {' '.join([f'<line x1="0" y1="{y}" x2="2200" y2="{y}"/>' for y in range(0, 1351, 80)])}
  </g>

  <!-- Ambient Glow Conduits / Light Beams -->
  <circle cx="350" cy="650" r="300" fill="#0072F5" opacity="0.06" filter="url(#glowCyan)"/>
  <circle cx="800" cy="650" r="320" fill="#7928CA" opacity="0.06" filter="url(#glowPurple)"/>
  <circle cx="1300" cy="650" r="380" fill="#059669" opacity="0.06" filter="url(#glowEmerald)"/>
  <circle cx="1850" cy="650" r="320" fill="#D97706" opacity="0.06" filter="url(#glowAmber)"/>

  <!-- Top Geometric Banner & Title -->
  <g transform="translate(100, 50)">
    <!-- Stage Indicator Hexagon Clusters -->
    <polygon points="{hex_points(50, 45, 30)}" fill="#0F172A" stroke="#38BDF8" stroke-width="2.5" filter="url(#glowCyan)"/>
    <text x="50" y="52" fill="#38BDF8" font-size="20" font-weight="900" text-anchor="middle" class="font-sans">⬢</text>

    <text x="100" y="38" fill="url(#titleGrad)" font-size="34" font-weight="900" letter-spacing="-0.5" class="font-sans">
      ENTERPRISE DATA ARCHITECTURE &amp; PROJECT LIFECYCLE
    </text>
    <text x="100" y="66" fill="#94A3B8" font-size="15" font-weight="500" letter-spacing="1.5" class="font-sans">
      KIMBALL GALAXY CONSTELLATION &bull; 7,000 MASTER EMPLOYEES &bull; HEURISTIC CLEANSING &bull; POWER BI DIAGNOSTIC COCKPIT
    </text>

    <!-- Top Status Pills -->
    <g transform="translate(1550, 10)">
      <rect width="450" height="48" rx="24" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>
      <circle cx="30" cy="24" r="8" fill="#10B981" filter="url(#glowEmerald)"/>
      <text x="50" y="29" fill="#F8FAFC" font-size="13" font-weight="700" class="mono">STATUS: PRODUCTION ACTIVE (100% PASS)</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- LIFECYCLE STAGE CONDUITS (Horizontal Connecting Spine) -->
  <!-- ========================================================================= -->
  <g stroke="#334155" stroke-width="3" fill="none" opacity="0.7">
    <!-- Connecting Backbone -->
    <path d="M 330 650 L 680 650" stroke="#00F0FF" stroke-width="3" stroke-dasharray="8 6" opacity="0.8"/>
    <path d="M 940 650 L 1140 650" stroke="#C084FC" stroke-width="3" stroke-dasharray="8 6" opacity="0.8"/>
    <path d="M 1520 650 L 1680 650" stroke="#10B981" stroke-width="3" stroke-dasharray="8 6" opacity="0.8"/>
    <path d="M 1940 650 L 2020 650" stroke="#F59E0B" stroke-width="3" stroke-dasharray="8 6" opacity="0.8"/>
  </g>

  <!-- ========================================================================= -->
  <!-- STAGE 1: RAW INGESTION & MULTI-SOURCE HARVESTING (Cyan Geometry) -->
  <!-- ========================================================================= -->
  <g transform="translate(100, 160)">
    <!-- Stage Header Pill -->
    <rect width="260" height="42" rx="21" fill="#082F49" stroke="#00F0FF" stroke-width="1.5" filter="url(#glowCyan)"/>
    <text x="130" y="26" fill="#E0F2FE" font-size="13" font-weight="800" letter-spacing="2" text-anchor="middle" class="font-sans">
      STAGE 1: RAW HARVESTING
    </text>

    <!-- Node 1: Master HRIS Text File (Ground Truth Hexagon) -->
    <g transform="translate(130, 140)">
      <polygon points="{hex_points(0, 0, 75)}" fill="url(#cardDark)" stroke="#00F0FF" stroke-width="3.5" filter="url(#cardShadow)"/>
      <polygon points="{hex_points(0, 0, 60)}" fill="#0C4A6E" opacity="0.3"/>
      <text x="0" y="-18" fill="#38BDF8" font-size="24" text-anchor="middle">📄</text>
      <text x="0" y="6" fill="#F8FAFC" font-size="13" font-weight="800" text-anchor="middle" class="font-sans">HRIS MASTER</text>
      <text x="0" y="24" fill="#38BDF8" font-size="11" font-weight="700" text-anchor="middle" class="mono">7,000 EMPLOYEES</text>
      <text x="0" y="38" fill="#94A3B8" font-size="9" text-anchor="middle" class="mono">.TXT FLAT-FILE</text>
    </g>

    <!-- Node 2: IoT Badge Access (JSON Diamond) -->
    <g transform="translate(50, 340)">
      <polygon points="{diamond_points(0, 0, 130, 130)}" fill="url(#cardDark)" stroke="#0284C7" stroke-width="2.5" filter="url(#cardShadow)"/>
      <text x="0" y="-12" fill="#38BDF8" font-size="22" text-anchor="middle">⚡</text>
      <text x="0" y="8" fill="#F8FAFC" font-size="12" font-weight="800" text-anchor="middle" class="font-sans">IoT BADGE</text>
      <text x="0" y="24" fill="#7DD3FC" font-size="10" font-weight="700" text-anchor="middle" class="mono">TURNSTILE JSON</text>
      <text x="0" y="38" fill="#94A3B8" font-size="8.5" text-anchor="middle" class="mono">114K+ SWIPES</text>
    </g>

    <!-- Node 3: FP&A Budget (Excel Diamond) -->
    <g transform="translate(210, 340)">
      <polygon points="{diamond_points(0, 0, 130, 130)}" fill="url(#cardDark)" stroke="#0284C7" stroke-width="2.5" filter="url(#cardShadow)"/>
      <text x="0" y="-12" fill="#38BDF8" font-size="22" text-anchor="middle">📊</text>
      <text x="0" y="8" fill="#F8FAFC" font-size="12" font-weight="800" text-anchor="middle" class="font-sans">FP&amp;A BUDGET</text>
      <text x="0" y="24" fill="#7DD3FC" font-size="10" font-weight="700" text-anchor="middle" class="mono">PIVOTED EXCEL</text>
      <text x="0" y="38" fill="#94A3B8" font-size="8.5" text-anchor="middle" class="mono">WIDE MATRIX</text>
    </g>

    <!-- Node 4: LMS Certifications (Octagon) -->
    <g transform="translate(50, 540)">
      <polygon points="{octagon_points(0, 0, 60)}" fill="url(#cardDark)" stroke="#0284C7" stroke-width="2.5" filter="url(#cardShadow)"/>
      <text x="0" y="-12" fill="#38BDF8" font-size="22" text-anchor="middle">🎓</text>
      <text x="0" y="8" fill="#F8FAFC" font-size="12" font-weight="800" text-anchor="middle" class="font-sans">LMS TALENT</text>
      <text x="0" y="24" fill="#7DD3FC" font-size="10" font-weight="700" text-anchor="middle" class="mono">7,197 ATTEMPTS</text>
      <text x="0" y="38" fill="#94A3B8" font-size="8.5" text-anchor="middle" class="mono">CSV STREAM</text>
    </g>

    <!-- Node 5: Exit Audits (Octagon) -->
    <g transform="translate(210, 540)">
      <polygon points="{octagon_points(0, 0, 60)}" fill="url(#cardDark)" stroke="#0284C7" stroke-width="2.5" filter="url(#cardShadow)"/>
      <text x="0" y="-12" fill="#38BDF8" font-size="22" text-anchor="middle">🚪</text>
      <text x="0" y="8" fill="#F8FAFC" font-size="12" font-weight="800" text-anchor="middle" class="font-sans">EXIT AUDIT</text>
      <text x="0" y="24" fill="#7DD3FC" font-size="10" font-weight="700" text-anchor="middle" class="mono">350 EXITS</text>
      <text x="0" y="38" fill="#94A3B8" font-size="8.5" text-anchor="middle" class="mono">SQL STAGING</text>
    </g>

    <!-- Ingestion Convergence Flow Lines -->
    <path d="M 130 215 L 130 670" stroke="#00F0FF" stroke-width="2" stroke-dasharray="4 4" opacity="0.4"/>
    <path d="M 50 405 L 130 670" stroke="#00F0FF" stroke-width="2" stroke-dasharray="4 4" opacity="0.4"/>
    <path d="M 210 405 L 130 670" stroke="#00F0FF" stroke-width="2" stroke-dasharray="4 4" opacity="0.4"/>
    <path d="M 50 600 L 130 670" stroke="#00F0FF" stroke-width="2" stroke-dasharray="4 4" opacity="0.4"/>
    <path d="M 210 600 L 130 670" stroke="#00F0FF" stroke-width="2" stroke-dasharray="4 4" opacity="0.4"/>

    <!-- Convergence Node -->
    <circle cx="130" cy="670" r="14" fill="#00F0FF" filter="url(#glowCyan)"/>
    <circle cx="130" cy="670" r="6" fill="#FFFFFF"/>
  </g>

  <!-- ========================================================================= -->
  <!-- STAGE 2: HEURISTIC TRANSFORMATION & CLEANSING CORE (Violet Geometry) -->
  <!-- ========================================================================= -->
  <g transform="translate(560, 160)">
    <!-- Stage Header Pill -->
    <rect width="320" height="42" rx="21" fill="#3B0764" stroke="#C084FC" stroke-width="1.5" filter="url(#glowPurple)"/>
    <text x="160" y="26" fill="#F3E8FF" font-size="13" font-weight="800" letter-spacing="2" text-anchor="middle" class="font-sans">
      STAGE 2: HEURISTIC PIPELINE
    </text>

    <!-- Central Hexagonal Processing Engine -->
    <g transform="translate(160, 480)">
      <!-- Outer Rotating Rings -->
      <polygon points="{hex_points(0, 0, 150)}" fill="url(#cardDark)" stroke="#A855F7" stroke-width="3" filter="url(#cardShadow)"/>
      <polygon points="{hex_points(0, 0, 130)}" fill="#581C87" opacity="0.25"/>
      <circle cx="0" cy="0" r="110" fill="none" stroke="#C084FC" stroke-width="1.5" stroke-dasharray="6 6"/>

      <text x="0" y="-45" fill="#E9D5FF" font-size="28" text-anchor="middle">⚙️</text>
      <text x="0" y="-15" fill="#F8FAFC" font-size="16" font-weight="900" letter-spacing="1" text-anchor="middle" class="font-sans">
        DATA CLEANING
      </text>
      <text x="0" y="8" fill="#C084FC" font-size="14" font-weight="700" letter-spacing="0.5" text-anchor="middle" class="font-sans">
        &amp; HEURISTIC ENGINE
      </text>
      <text x="0" y="32" fill="#E2E8F0" font-size="11" font-weight="600" text-anchor="middle" class="mono">
        PIPELINE_RUNNER.PY
      </text>
      <rect x="-65" y="44" width="130" height="22" rx="11" fill="#7E22CE"/>
      <text x="0" y="59" fill="#FFFFFF" font-size="10" font-weight="800" text-anchor="middle" class="mono">
        100% REPRODUCIBLE
      </text>
    </g>

    <!-- Satellite Transformation Geometric Cards -->
    <!-- 1. Attendance Imputation -->
    <g transform="translate(20, 110)">
      <polygon points="{diamond_points(0, 0, 150, 90)}" fill="url(#cardDark)" stroke="#9333EA" stroke-width="2"/>
      <text x="0" y="-10" fill="#D8B4FE" font-size="11" font-weight="800" text-anchor="middle" class="font-sans">SHIFT IMPUTATION</text>
      <text x="0" y="6" fill="#94A3B8" font-size="9" text-anchor="middle" class="mono">Median 8.5h Fill</text>
      <text x="0" y="20" fill="#C084FC" font-size="8.5" text-anchor="middle" class="mono">Night Shift Wrap</text>
    </g>

    <!-- 2. Fuzzy Branch Standardizer -->
    <g transform="translate(290, 110)">
      <polygon points="{diamond_points(0, 0, 150, 90)}" fill="url(#cardDark)" stroke="#9333EA" stroke-width="2"/>
      <text x="0" y="-10" fill="#D8B4FE" font-size="11" font-weight="800" text-anchor="middle" class="font-sans">BRANCH NORMALIZER</text>
      <text x="0" y="6" fill="#94A3B8" font-size="9" text-anchor="middle" class="mono">14 Canonical Hubs</text>
      <text x="0" y="20" fill="#C084FC" font-size="8.5" text-anchor="middle" class="mono">Typo Harmonization</text>
    </g>

    <!-- 3. Budget Unpivoter -->
    <g transform="translate(-10, 270)">
      <polygon points="{diamond_points(0, 0, 150, 90)}" fill="url(#cardDark)" stroke="#9333EA" stroke-width="2"/>
      <text x="0" y="-10" fill="#D8B4FE" font-size="11" font-weight="800" text-anchor="middle" class="font-sans">MATRIX UNPIVOT</text>
      <text x="0" y="6" fill="#94A3B8" font-size="9" text-anchor="middle" class="mono">Melt Wide Quarters</text>
      <text x="0" y="20" fill="#C084FC" font-size="8.5" text-anchor="middle" class="mono">Row Granularity</text>
    </g>

    <!-- 4. LMS Deduplicator -->
    <g transform="translate(320, 270)">
      <polygon points="{diamond_points(0, 0, 150, 90)}" fill="url(#cardDark)" stroke="#9333EA" stroke-width="2"/>
      <text x="0" y="-10" fill="#D8B4FE" font-size="11" font-weight="800" text-anchor="middle" class="font-sans">LMS DEDUP ENGINE</text>
      <text x="0" y="6" fill="#94A3B8" font-size="9" text-anchor="middle" class="mono">Filter Retakes</text>
      <text x="0" y="20" fill="#C084FC" font-size="8.5" text-anchor="middle" class="mono">Highest Score Flag</text>
    </g>

    <!-- 5. Salary Compression & Percentile Analytics -->
    <g transform="translate(160, 750)">
      <polygon points="{diamond_points(0, 0, 200, 100)}" fill="url(#cardDark)" stroke="#A855F7" stroke-width="2.5" filter="url(#glowPurple)"/>
      <text x="0" y="-12" fill="#E9D5FF" font-size="12" font-weight="900" text-anchor="middle" class="font-sans">SALARY COMPRESSION</text>
      <text x="0" y="6" fill="#F8FAFC" font-size="10" font-weight="700" text-anchor="middle" class="mono">Role Percentile &bull; SII &lt; 1.0</text>
      <text x="0" y="22" fill="#C084FC" font-size="9" text-anchor="middle" class="mono">Tenure vs Market Rate</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- STAGE 3: ENTERPRISE DATA WAREHOUSE & GALAXY CONSTELLATION MART -->
  <!-- ========================================================================= -->
  <g transform="translate(1080, 160)">
    <!-- Stage Header Pill -->
    <rect width="400" height="42" rx="21" fill="#064E3B" stroke="#10B981" stroke-width="1.5" filter="url(#glowEmerald)"/>
    <text x="200" y="26" fill="#D1FAE5" font-size="13" font-weight="800" letter-spacing="2" text-anchor="middle" class="font-sans">
      STAGE 3: KIMBALL GALAXY CONSTELLATION
    </text>

    <!-- Central Schema Hub Container -->
    <rect x="-10" y="60" width="420" height="780" rx="28" fill="#0B132B" fill-opacity="0.75" stroke="#1E293B" stroke-width="2"/>

    <!-- Section A: Conformed Dimensions (Top Emerald Zone) -->
    <g transform="translate(200, 120)">
      <text x="0" y="-25" fill="#34D399" font-size="12" font-weight="800" letter-spacing="1.5" text-anchor="middle" class="font-sans">
        CONFORMED DIMENSIONS (5 TABLES)
      </text>

      <!-- Dim_Employee (SCD Type 2 Flagship Hexagon) -->
      <g transform="translate(-100, 35)">
        <polygon points="{hex_points(0, 0, 52)}" fill="url(#cardDark)" stroke="#10B981" stroke-width="2.5"/>
        <text x="0" y="-12" fill="#34D399" font-size="11" font-weight="800" text-anchor="middle" class="font-sans">DIM_EMPLOYEE</text>
        <text x="0" y="4" fill="#F8FAFC" font-size="9" font-weight="700" text-anchor="middle" class="mono">7,000 ROWS</text>
        <text x="0" y="18" fill="#6EE7B7" font-size="8" text-anchor="middle" class="mono">SCD TYPE 2</text>
      </g>

      <!-- Dim_Date -->
      <g transform="translate(100, 35)">
        <polygon points="{hex_points(0, 0, 52)}" fill="url(#cardDark)" stroke="#10B981" stroke-width="2.5"/>
        <text x="0" y="-12" fill="#34D399" font-size="11" font-weight="800" text-anchor="middle" class="font-sans">DIM_DATE</text>
        <text x="0" y="4" fill="#F8FAFC" font-size="9" font-weight="700" text-anchor="middle" class="mono">1,096 DAYS</text>
        <text x="0" y="18" fill="#6EE7B7" font-size="8" text-anchor="middle" class="mono">2024–2026 CAL</text>
      </g>

      <!-- Dim_Department -->
      <g transform="translate(-130, 155)">
        <polygon points="{hex_points(0, 0, 46)}" fill="url(#cardDark)" stroke="#059669" stroke-width="2"/>
        <text x="0" y="-8" fill="#A7F3D0" font-size="9.5" font-weight="800" text-anchor="middle" class="font-sans">DIM_DEPT</text>
        <text x="0" y="8" fill="#F8FAFC" font-size="8.5" font-weight="700" text-anchor="middle" class="mono">6 DEPTS</text>
      </g>

      <!-- Dim_Branch -->
      <g transform="translate(0, 155)">
        <polygon points="{hex_points(0, 0, 46)}" fill="url(#cardDark)" stroke="#059669" stroke-width="2"/>
        <text x="0" y="-8" fill="#A7F3D0" font-size="9.5" font-weight="800" text-anchor="middle" class="font-sans">DIM_BRANCH</text>
        <text x="0" y="8" fill="#F8FAFC" font-size="8.5" font-weight="700" text-anchor="middle" class="mono">14 HUBS</text>
      </g>

      <!-- Dim_Course -->
      <g transform="translate(130, 155)">
        <polygon points="{hex_points(0, 0, 46)}" fill="url(#cardDark)" stroke="#059669" stroke-width="2"/>
        <text x="0" y="-8" fill="#A7F3D0" font-size="9.5" font-weight="800" text-anchor="middle" class="font-sans">DIM_COURSE</text>
        <text x="0" y="8" fill="#F8FAFC" font-size="8.5" font-weight="700" text-anchor="middle" class="mono">10 COURSES</text>
      </g>
    </g>

    <!-- Star-to-Galaxy Connector Bus -->
    <path d="M 200 370 L 200 440" stroke="#F59E0B" stroke-width="3" stroke-dasharray="4 4"/>
    <polygon points="194,440 206,440 200,450" fill="#F59E0B"/>

    <!-- Section B: Fact Constellation (Bottom Gold Zone) -->
    <g transform="translate(200, 460)">
      <text x="0" y="-10" fill="#FBBF24" font-size="12" font-weight="800" letter-spacing="1.5" text-anchor="middle" class="font-sans">
        FACT CONSTELLATION (4 FACT TABLES)
      </text>

      <!-- Fact 1: Fact_WorkforceSnapshot -->
      <g transform="translate(-100, 60)">
        <polygon points="{octagon_points(0, 0, 56)}" fill="url(#cardDark)" stroke="#F59E0B" stroke-width="2.5"/>
        <text x="0" y="-14" fill="#FDE68A" font-size="10.5" font-weight="800" text-anchor="middle" class="font-sans">FACT_WORKFORCE</text>
        <text x="0" y="3" fill="#F8FAFC" font-size="9" font-weight="700" text-anchor="middle" class="mono">7,000 ROWS</text>
        <text x="0" y="18" fill="#FCD34D" font-size="8" text-anchor="middle" class="mono">MONTHLY GRAIN</text>
      </g>

      <!-- Fact 2: Fact_DailyAttendance -->
      <g transform="translate(100, 60)">
        <polygon points="{octagon_points(0, 0, 56)}" fill="url(#cardDark)" stroke="#F59E0B" stroke-width="2.5"/>
        <text x="0" y="-14" fill="#FDE68A" font-size="10.5" font-weight="800" text-anchor="middle" class="font-sans">FACT_ATTENDANCE</text>
        <text x="0" y="3" fill="#F8FAFC" font-size="9" font-weight="700" text-anchor="middle" class="mono">16,000 SWIPES</text>
        <text x="0" y="18" fill="#FCD34D" font-size="8" text-anchor="middle" class="mono">DAILY GRAIN</text>
      </g>

      <!-- Fact 3: Fact_DepartmentBudget -->
      <g transform="translate(-100, 195)">
        <polygon points="{octagon_points(0, 0, 56)}" fill="url(#cardDark)" stroke="#D97706" stroke-width="2.5"/>
        <text x="0" y="-14" fill="#FDE68A" font-size="10.5" font-weight="800" text-anchor="middle" class="font-sans">FACT_BUDGET</text>
        <text x="0" y="3" fill="#F8FAFC" font-size="9" font-weight="700" text-anchor="middle" class="mono">672 TARGETS</text>
        <text x="0" y="18" fill="#FCD34D" font-size="8" text-anchor="middle" class="mono">QUARTERLY GRAIN</text>
      </g>

      <!-- Fact 4: Fact_TrainingCompletions -->
      <g transform="translate(100, 195)">
        <polygon points="{octagon_points(0, 0, 56)}" fill="url(#cardDark)" stroke="#D97706" stroke-width="2.5"/>
        <text x="0" y="-14" fill="#FDE68A" font-size="10.5" font-weight="800" text-anchor="middle" class="font-sans">FACT_TRAINING</text>
        <text x="0" y="3" fill="#F8FAFC" font-size="9" font-weight="700" text-anchor="middle" class="mono">2,735 PASSES</text>
        <text x="0" y="18" fill="#FCD34D" font-size="8" text-anchor="middle" class="mono">EVENT GRAIN</text>
      </g>

      <!-- Database Badge -->
      <rect x="-140" y="295" width="280" height="32" rx="16" fill="#1E293B" stroke="#64748B"/>
      <text x="0" y="316" fill="#94A3B8" font-size="11" font-weight="700" text-anchor="middle" class="mono">
        SQL SERVER: ENTERPRISEHR_DWH
      </text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- STAGE 4: SEMANTIC DIAGNOSTIC FRAMEWORKS & ACTIONABLE KPIs -->
  <!-- ========================================================================= -->
  <g transform="translate(1640, 160)">
    <!-- Stage Header Pill -->
    <rect width="460" height="42" rx="21" fill="#881337" stroke="#F43F5E" stroke-width="1.5" filter="url(#glowAmber)"/>
    <text x="230" y="26" fill="#FFE4E6" font-size="13" font-weight="800" letter-spacing="2" text-anchor="middle" class="font-sans">
      STAGE 4: DIAGNOSTIC DECISION ENGINE
    </text>

    <!-- 4 Geometric Diagnostic Cards -->
    <!-- Diagnostic 1: Salary Compression & Flight Risk -->
    <g transform="translate(230, 110)">
      <polygon points="{diamond_points(0, 0, 360, 110)}" fill="url(#cardDark)" stroke="#F43F5E" stroke-width="2" filter="url(#cardShadow)"/>
      <text x="0" y="-16" fill="#FDA4AF" font-size="13" font-weight="900" text-anchor="middle" class="font-sans">
        DIAGNOSTIC 1: FLIGHT RISK &amp; COMPRESSION
      </text>
      <text x="0" y="6" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle" class="mono">
        Salary Inversion Index (SII &lt; 1.0)
      </text>
      <text x="0" y="24" fill="#94A3B8" font-size="10" text-anchor="middle" class="mono">
        High-Performer Retention Priority (Score &ge; 80)
      </text>
    </g>

    <!-- Diagnostic 2: Budget Burn Rate & Headcount Variance -->
    <g transform="translate(230, 260)">
      <polygon points="{diamond_points(0, 0, 360, 110)}" fill="url(#cardDark)" stroke="#F59E0B" stroke-width="2" filter="url(#cardShadow)"/>
      <text x="0" y="-16" fill="#FDE68A" font-size="13" font-weight="900" text-anchor="middle" class="font-sans">
        DIAGNOSTIC 2: HEADCOUNT &amp; BUDGET BURN
      </text>
      <text x="0" y="6" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle" class="mono">
        &Delta;HC = Actual Active &minus; Budget Quota
      </text>
      <text x="0" y="24" fill="#94A3B8" font-size="10" text-anchor="middle" class="mono">
        Payroll Burn Rate % (Alert if &gt; 105% or &lt; 90%)
      </text>
    </g>

    <!-- Diagnostic 3: Workplace Policy & Ghost Workers -->
    <g transform="translate(230, 410)">
      <polygon points="{diamond_points(0, 0, 360, 110)}" fill="url(#cardDark)" stroke="#06B6D4" stroke-width="2" filter="url(#cardShadow)"/>
      <text x="0" y="-16" fill="#A5F3FC" font-size="13" font-weight="900" text-anchor="middle" class="font-sans">
        DIAGNOSTIC 3: GHOST WORKERS &amp; POLICY
      </text>
      <text x="0" y="6" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle" class="mono">
        60+ Days Turnstile Inactivity on Active Payroll
      </text>
      <text x="0" y="24" fill="#94A3B8" font-size="10" text-anchor="middle" class="mono">
        Contract WorkMode Breach (Onsite vs Remote)
      </text>
    </g>

    <!-- Diagnostic 4: Upskilling ROI & Score Velocity -->
    <g transform="translate(230, 560)">
      <polygon points="{diamond_points(0, 0, 360, 110)}" fill="url(#cardDark)" stroke="#8B5CF6" stroke-width="2" filter="url(#cardShadow)"/>
      <text x="0" y="-16" fill="#DDD6FE" font-size="13" font-weight="900" text-anchor="middle" class="font-sans">
        DIAGNOSTIC 4: UPSKILLING ROI &amp; VELOCITY
      </text>
      <text x="0" y="6" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle" class="mono">
        Certification Pass Rate vs Appraisal Gain (+0.45)
      </text>
      <text x="0" y="24" fill="#94A3B8" font-size="10" text-anchor="middle" class="mono">
        Cost per Certified Headcount by Department
      </text>
    </g>

    <!-- Final Power BI Output Presentation Hexagon -->
    <g transform="translate(230, 750)">
      <polygon points="{hex_points(0, 0, 105)}" fill="url(#cardDark)" stroke="#F59E0B" stroke-width="3.5" filter="url(#glowAmber)"/>
      <text x="0" y="-30" fill="#FBBF24" font-size="32" text-anchor="middle">📊</text>
      <text x="0" y="5" fill="#F8FAFC" font-size="15" font-weight="900" letter-spacing="1" text-anchor="middle" class="font-sans">
        POWER BI COCKPIT
      </text>
      <text x="0" y="26" fill="#FDE68A" font-size="11" font-weight="700" text-anchor="middle" class="mono">
        EXECUTIVE DIAGNOSTICS
      </text>
      <text x="0" y="44" fill="#94A3B8" font-size="9.5" text-anchor="middle" class="mono">
        DIRECTQUERY &bull; DAX MEASURES
      </text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- BOTTOM ARCHITECTURAL FOOTER (Metrics & Guarantees) -->
  <!-- ========================================================================= -->
  <g transform="translate(100, 1220)">
    <rect width="2000" height="75" rx="16" fill="#0A0F1D" stroke="#1E293B" stroke-width="1.5"/>

    <g transform="translate(60, 42)">
      <polygon points="{hex_points(0, 0, 14)}" fill="#00F0FF"/>
      <text x="25" y="5" fill="#F8FAFC" font-size="12" font-weight="800" class="font-sans">
        DATA FIDELITY: 100% GROUNDED ON EMPLOYEES_DATA_7000.TXT
      </text>
    </g>

    <g transform="translate(560, 42)">
      <polygon points="{diamond_points(0, 0, 20, 20)}" fill="#A855F7"/>
      <text x="20" y="5" fill="#F8FAFC" font-size="12" font-weight="800" class="font-sans">
        ETL HEURISTICS: ZERO DATA LOSS &bull; DETERMINISTIC SEED 42
      </text>
    </g>

    <g transform="translate(1120, 42)">
      <polygon points="{octagon_points(0, 0, 12)}" fill="#10B981"/>
      <text x="20" y="5" fill="#F8FAFC" font-size="12" font-weight="800" class="font-sans">
        WAREHOUSE: KIMBALL GALAXY CONSTELLATION (10 TABLES)
      </text>
    </g>

    <g transform="translate(1620, 42)">
      <polygon points="{hex_points(0, 0, 14)}" fill="#F59E0B"/>
      <text x="25" y="5" fill="#F8FAFC" font-size="12" font-weight="800" class="font-sans">
        VALIDATION: 11/11 PYTEST SUITE PASSING
      </text>
    </g>
  </g>
</svg>'''

with open(output_path, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Successfully generated modern geometric lifecycle diagram at {output_path} ({len(svg)} bytes)")
