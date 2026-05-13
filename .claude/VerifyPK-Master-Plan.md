# 🛡️ VerifyPK — Liveness Face Detection & KYC Platform

> **Master Plan v1.0** — Complete blueprint for building a production-grade, self-hosted, open-source KYC platform with Chrome Extension + REST API.

---

## 📌 Quick Summary

| Field | Detail |
|-------|--------|
| **Product** | Liveness Face Detection + KYC verification platform |
| **Form Factor** | Chrome Extension + REST API + Admin Dashboard |
| **Hosting** | Self-hosted on personal server (1 TB SSD, 120 GB RAM) |
| **Cost** | ~Rs. 5,000 one-time + Rs. 1,500/month |
| **Timeline** | 8 weeks full-time / 3–4 months part-time |
| **Tech Stack** | Python (FastAPI), React, PostgreSQL, Docker, InsightFace |
| **License Plan** | Open-source core + paid managed API |

---

## 🎯 Vision

Build **Pakistan's first open-source KYC platform** — a free, self-hostable alternative to Onfido, Jumio, and Veriff. Target market: fintech startups, crypto exchanges, freelance platforms, lending apps, and any business needing identity verification.

**Tagline:** *"Apni KYC, apne server pe."*

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         END USERS                                 │
└────────────┬─────────────────────────────────────┬───────────────┘
             │                                     │
   ┌─────────▼──────────┐              ┌──────────▼──────────┐
   │  Chrome Extension  │              │   Client Apps        │
   │  (Selfie + ID)     │              │   (via REST API)     │
   └─────────┬──────────┘              └──────────┬──────────┘
             │                                     │
             └──────────────┬──────────────────────┘
                            │ HTTPS
                  ┌─────────▼─────────┐
                  │   Cloudflare      │  ← DDoS + CDN
                  └─────────┬─────────┘
                            │
                  ┌─────────▼─────────┐
                  │   Nginx (Proxy)   │  ← SSL termination
                  └─────────┬─────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼───────┐  ┌────────▼────────┐  ┌──────▼──────┐
│   FastAPI     │  │ Admin Dashboard │  │  Docs Site  │
│   (Main API)  │  │   (React SPA)   │  │ (Docusaurus)│
└───────┬───────┘  └────────┬────────┘  └─────────────┘
        │                   │
        │     ┌─────────────┘
        │     │
┌───────▼─────▼──────────────────────────────────────┐
│                  AI WORKERS (Celery)                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────┐  │
│  │  Face    │ │ Liveness │ │   OCR    │ │ Anti │  │
│  │ Detect   │ │  Check   │ │ (CNIC)   │ │Fraud │  │
│  │InsightFc │ │  Silent  │ │PaddleOCR │ │Engine│  │
│  └──────────┘ └──────────┘ └──────────┘ └──────┘  │
└────────┬───────────────────────────────────────────┘
         │
   ┌─────┴──────┬─────────────┬──────────────┐
   │            │             │              │
┌──▼───┐  ┌────▼────┐  ┌─────▼─────┐  ┌────▼────┐
│Postgres│ │  Redis  │  │  Milvus   │  │  MinIO  │
│  (DB)  │  │(Cache)  │  │(Vectors)  │  │(Storage)│
└────────┘  └─────────┘  └───────────┘  └─────────┘
```

---

## 🧰 Tech Stack (100% Free / Open Source)

### Backend
- **FastAPI** — Async Python web framework
- **PostgreSQL 16** — Primary database
- **Redis 7** — Cache, sessions, rate limiting
- **Celery + RabbitMQ** — Background jobs
- **Milvus** or **Qdrant** — Vector DB for face embeddings
- **MinIO** — S3-compatible file storage

### AI / ML Models
- **InsightFace** — Face detection + recognition (ArcFace `buffalo_l`)
- **Silent-Face-Anti-Spoofing** (MiniVision) — Passive liveness
- **MediaPipe Face Mesh** — Active liveness (browser-side)
- **PaddleOCR** — Document OCR (English + Urdu)
- **OpenCV** — Image processing
- **ELA (Error Level Analysis)** — Tampering detection

### Frontend
- **Chrome Extension** — Manifest V3, Vanilla JS + Tailwind
- **Admin Dashboard** — React + Vite + Shadcn/UI
- **Docs Site** — Docusaurus

### DevOps
- **Docker + Docker Compose** — Containerization
- **Nginx** — Reverse proxy + SSL
- **Let's Encrypt** — Free SSL certificates
- **Cloudflare** — DNS + CDN + DDoS protection
- **Prometheus + Grafana + Loki** — Monitoring stack
- **GitHub Actions** — CI/CD
- **Sentry** (self-hosted) — Error tracking

---

## 🧠 The 3-Layer Liveness Strategy

Free models alone won't beat paid services in accuracy. We compensate with **defense in depth**:

| Layer | Type | Where | Defeats |
|-------|------|-------|---------|
| **1. Active Challenges** | Behavioral | Browser (MediaPipe) | Static photo, simple video |
| **2. Passive Liveness** | AI model | Server (Silent-Face) | Mask, advanced replays |
| **3. Texture Analysis** | CV pipeline | Server (OpenCV) | Screen replay, moire patterns |

**Combined accuracy target: 92–95%** (free models reach 85% solo; this stack closes the gap).

---

## 📅 8-Phase Roadmap

### **Phase 0 — Foundation** *(Days 1–3)*

**Goal:** Server ready, infrastructure khada.

- [ ] Server audit (OS, GPU, RAM, disk)
- [ ] Install Docker + Docker Compose
- [ ] Buy domain (`.com` recommended)
- [ ] Cloudflare DNS setup
- [ ] Let's Encrypt SSL
- [ ] Git repository structure
- [ ] Project scaffolding

**Deliverable:** `https://yourdomain.com` returns HTTPS hello.

---

### **Phase 1 — Core AI Pipeline** *(Days 4–10)*

**Goal:** AI models tested and benchmarked.

- [ ] InsightFace setup (face detection + recognition)
- [ ] Silent-Face-Anti-Spoofing integration
- [ ] PaddleOCR for CNIC text extraction
- [ ] Tampering detection (ELA + copy-move)
- [ ] Build benchmark suite (100 real + 100 spoof samples)
- [ ] Threshold tuning

**Accuracy Targets:**

| Metric | Target |
|--------|--------|
| Face detection | ≥ 99% |
| Liveness (passive) | ≥ 88% |
| Liveness (passive + active) | ≥ 92% |
| Face matching | ≥ 95% |
| CNIC OCR (clean images) | ≥ 90% |

**Deliverable:** Standalone Python scripts with accuracy report.

---

### **Phase 2 — Backend API** *(Days 11–18)*

**Goal:** Production-grade REST API.

**Endpoint Map:**

```
🔐 Authentication
  POST   /v1/auth/register
  POST   /v1/auth/login
  POST   /v1/auth/api-keys

✅ Verification
  POST   /v1/verify/session/start
  POST   /v1/verify/liveness
  POST   /v1/verify/document
  POST   /v1/verify/face-match
  POST   /v1/verify/complete         ← Full KYC, single call
  GET    /v1/verify/{session_id}

👤 User Management
  GET    /v1/users
  POST   /v1/users/{id}/delete-data   ← GDPR

🔔 Webhooks
  POST   /v1/webhooks
  GET    /v1/webhooks/deliveries

⚙️ Admin
  GET    /v1/admin/stats
  GET    /v1/admin/pending-reviews
  POST   /v1/admin/review/{id}/approve
```

**Features:**

- JWT authentication
- API key + HMAC request signing
- Redis-backed rate limiting per key
- Immutable audit log
- Celery for async heavy lifting
- Auto-generated Swagger at `/docs`

**Deliverable:** Postman collection, all endpoints green.

---

### **Phase 3 — Chrome Extension** *(Days 19–25)*

**Goal:** End-user friendly extension.

**User Flow:**

```
1. 👆 Click extension icon
2. 📜 Terms & consent screen
3. 🤳 Selfie capture (with oval guide + quality checks)
4. 🎯 Active liveness (blink → turn left → smile)
5. 🪪 CNIC front capture
6. 🪪 CNIC back capture
7. ⏳ Upload & process
8. ✅ Result (Verified / Failed / Under Review)
```

**Extension Structure:**

```
extension/
├── manifest.json         (V3)
├── popup/
│   ├── popup.html
│   ├── popup.js
│   └── popup.css         (Tailwind)
├── content/              (optional injected scripts)
├── background/
│   └── service-worker.js
└── lib/
    ├── mediapipe/        (face mesh)
    ├── camera.js
    └── api-client.js
```

**Quality Gates** (block bad captures upfront):

- Face must fill ≥ 30% of frame
- Lighting score ≥ 0.6
- Blur score below threshold
- Single face only (no group photos)

**Deliverable:** `.zip` ready for Chrome Web Store submission ($5 one-time fee).

---

### **Phase 4 — Admin Dashboard** *(Days 26–32)*

**Goal:** Web panel for full control.

**Pages:**

| Page | Purpose |
|------|---------|
| Dashboard | KPIs, today's stats, geographic map |
| Verifications | Searchable table, filters |
| Verification Detail | Selfie, ID, scores, manual override |
| API Keys | Create, revoke, view usage |
| Webhooks | Configure callbacks, delivery logs |
| Pending Reviews | Manual review queue |
| Settings | Thresholds, document types, notifications |
| Analytics | Fraud patterns, time-series, funnels |
| Billing *(future)* | Usage-based billing |

**Tech:** React + Vite + Shadcn/UI + Tailwind + TanStack Query + Recharts.

**Deliverable:** Live at `dashboard.yourdomain.com`.

---

### **Phase 5 — Anti-Fraud Engine** *(Days 33–38)*

**Goal:** Catch real-world fraud patterns.

**Components:**

- **Device Fingerprinting** — FingerprintJS open-source
- **IP Intelligence** — VPN/Tor/Proxy detection
- **Velocity Rules:**
  - 3+ verifications from same device per day → flag
  - 5+ from same IP per hour → block
  - Same face under different names → critical alert
- **Duplicate Face Detection** — Milvus 1:N search on every new face
- **Document Reuse** — Same CNIC across accounts
- **Behavioral Signals** — Verification speed, tab focus, mouse jitter

**Rule Engine:** Each verification gets a fraud score 0–100. Above 70 → manual review queue.

**Deliverable:** Fraud rules engine with configurable thresholds in admin panel.

---

### **Phase 6 — SDKs & Documentation** *(Days 39–44)*

**Goal:** Developer onboarding in under 10 minutes.

**Deliverables:**

- [ ] **Python SDK** — `pip install verifypk`
- [ ] **Node.js SDK** — `npm install verifypk`
- [ ] **PHP SDK** — Laravel-friendly
- [ ] **Documentation Site** (Docusaurus):
  - Quickstart (5 min integration)
  - Full API reference
  - Code examples per language
  - Webhook events guide
  - Error codes catalog
- [ ] **Postman Public Workspace**
- [ ] **YouTube walkthrough** (5-min demo for marketing)

---

### **Phase 7 — Deployment & Monitoring** *(Days 45–50)*

**Goal:** Bulletproof production.

**Stack:**

- **Nginx + Cloudflare** — Edge layer
- **Let's Encrypt** — Auto-renewing SSL
- **Daily Backups** — Postgres + MinIO → Backblaze B2 ($6/TB/mo)
- **Prometheus + Grafana** — Metrics
- **Loki** — Centralized logs
- **Uptime Kuma** — Uptime monitoring
- **Sentry** — Error tracking
- **Alerts** (Telegram bot):
  - Server down
  - Error rate spike
  - Disk space < 10%
  - Suspicious activity burst
- **CI/CD** — GitHub Actions → auto-deploy on `main` push

---

### **Phase 8 — Launch & Marketing** *(Week 8+)*

**Goal:** First 100 paying customers.

**Launch Plan:**

1. **Private beta** — 5–10 friendly developers
2. **Public beta** — Product Hunt launch
3. **Content** — LinkedIn + Twitter posts (Pakistan fintech community)
4. **Outreach** — Cold emails to local startups, exchanges, freelance platforms
5. **Partnerships** — Talk to local banks/sandboxes

**Pricing Tiers** *(suggested)*:

| Plan | Price | Verifications/mo |
|------|-------|------------------|
| Free | Rs. 0 | 100 |
| Starter | Rs. 8,000 | 1,000 |
| Pro | Rs. 28,000 | 10,000 |
| Enterprise | Custom | Unlimited |

---

## 💰 Budget Breakdown

| Item | Cost | Frequency |
|------|------|-----------|
| Server | Already owned | — |
| Domain (.com) | Rs. 3,000 | yearly |
| Cloudflare | Free | — |
| Email (SendGrid) | Free (100/day) | — |
| Backup storage (Backblaze B2) | ~Rs. 1,700 | monthly |
| Chrome Web Store | Rs. 1,400 | one-time |
| SMS OTP *(optional)* | Rs. 14 / SMS | per use |
| **Setup Total** | **~Rs. 5,000** | one-time |
| **Recurring** | **~Rs. 1,500** | monthly |

---

## ⚖️ Legal & Compliance

**Must-have before launch:**

- [ ] **Terms of Service**
- [ ] **Privacy Policy** (GDPR + draft Pakistan PDPB compliant)
- [ ] **User consent flow** with signed timestamp
- [ ] **Data deletion API** (right to be forgotten)
- [ ] **Encryption at rest** for all PII (AES-256)
- [ ] **Encryption in transit** (TLS 1.3)
- [ ] **Audit log** of every access to user data
- [ ] **Data retention policy** (suggested: 90 days after verification)

**Pakistan-specific considerations:**

- NADRA's Verisys is the official CNIC verification API — we are *not* replacing it. Our system verifies face liveness and reads OCR; we recommend clients combine us with NADRA for full legal validity.
- Draft Personal Data Protection Bill 2023 — keep an eye out; design with consent + minimization from day one.
- PECA 2016 — covers cybercrime; ensure no unauthorized data sharing.

---

## ⚠️ Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Free model accuracy < paid services | High | 3-layer liveness + manual review fallback |
| Server downtime | High | Daily backups + monitoring + Uptime Kuma |
| Data breach (PII leak) | Critical | Encryption + access logs + minimal retention |
| Fraud / abuse | High | Anti-fraud engine + rate limiting |
| Legal challenge | Medium | Strong ToS + Privacy Policy + consent flow |
| Vendor lock-in (Chrome) | Low | Build Firefox + Edge versions later |
| Scaling > server capacity | Medium | 120 GB RAM handles ~200 concurrent; plan horizontal scale later |

---

## 📊 Resource Capacity (Your Server)

With 1 TB SSD + 120 GB RAM:

| Resource | Estimated Capacity |
|----------|--------------------|
| Concurrent users | 100–200 (CPU) / 500+ (GPU) |
| Face embeddings stored | 100+ million (2 KB each) |
| Daily verifications | 50,000+ |
| AI models in RAM | 4–8 GB total |
| Headroom | ~90% (massive runway) |

---

## 🛠️ Tomorrow's Server Check Commands

When you check the server, run these and share output:

```bash
# OS info
cat /etc/os-release
uname -a

# CPU
nproc
lscpu | grep "Model name"

# RAM
free -h

# Disk
df -h
lsblk

# GPU (if any)
lspci | grep -i nvidia
nvidia-smi              # only works if NVIDIA + drivers installed

# Network
ip a
curl -s ifconfig.me     # public IP

# Docker (check if installed)
docker --version
docker-compose --version
```

---

## ✅ Next Actions

### Tonight
- [ ] Decide final brand name (default: **VerifyPK**)
- [ ] Decide: MVP-first (2 weeks) or full build (8 weeks)
- [ ] Confirm coding background (so I tune the depth of explanations)

### Tomorrow
- [ ] Run server audit commands above
- [ ] Share output with me
- [ ] We start **Phase 0** together

### This Week
- [ ] Buy domain
- [ ] Cloudflare account setup
- [ ] Git repository created
- [ ] Docker installed on server

---

## 📁 Final Project Structure

```
verifypk/
├── backend/                  # FastAPI app
│   ├── app/
│   │   ├── api/             # Routes
│   │   ├── core/            # Config, security
│   │   ├── db/              # Models, migrations
│   │   ├── services/        # Business logic
│   │   └── workers/         # Celery tasks
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── extension/                # Chrome extension
│   ├── manifest.json
│   ├── popup/
│   ├── background/
│   └── lib/
│
├── dashboard/                # Admin panel (React)
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docs/                     # Docusaurus
│
├── sdks/
│   ├── python/
│   ├── node/
│   └── php/
│
├── infrastructure/
│   ├── docker-compose.yml
│   ├── nginx/
│   ├── prometheus/
│   └── grafana/
│
├── models/                   # AI model weights
│   ├── insightface/
│   ├── anti-spoof/
│   └── paddleocr/
│
└── README.md
```

---

## 🎬 Closing Note

Bhai, yeh plan production-grade hai — kisi bhi serious YC-backed KYC startup ka roadmap aisa hi hota hai. Lekin yaad rakho:

> **"Perfect is the enemy of done."**

Pehle MVP launch karo (Phases 0–3, ~3 weeks), real users laao, feedback lo, phir Phases 4–8 iterate karte hue add karo. Production mein chhoti cheez seekhne ko milti hai jo paper pe nahi.

Tumhare paas resources hain. Tumhare paas plan hai. Bas execute karna hai.

**Chalo banate hain. 🚀**

---

*Document version: 1.0*
*Last updated: 11 May 2026*
*Author: VerifyPK Team*
