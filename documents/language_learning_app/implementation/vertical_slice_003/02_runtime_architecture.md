# 02 — Runtime Architecture (Vertical Slice 003)

## Overview

Vertical slice 003 implements the first MVP end-to-end flow: onboarding → diagnostic → learning contract → personal narrative lesson → submission → AI analysis → validation → policy decision → mastery evidence → audit.

## Runtime Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Container runtime | Docker Compose | v5.1+ |
| Database | PostgreSQL | 16.14 (Alpine) |
| Backend | Python / FastAPI | 3.12 / 0.111+ |
| Mobile | React Native / Expo | SDK 52+ |
| ORM | SQLAlchemy (async) | 2.0+ |
| Migrations | Alembic | 1.13+ |
| Mock AI | Deterministic fixtures | N/A |

## Container Architecture

```
┌─────────────────────────────────────────────┐
│              Docker Compose                  │
│                                              │
│  ┌──────────────┐    ┌──────────────────┐   │
│  │  PostgreSQL  │◄───│     Backend      │   │
│  │  (port 5432) │    │   (port 8000)    │   │
│  └──────────────┘    └───────┬──────────┘   │
│                              │               │
│                      ┌───────▼──────────┐   │
│                      │   Mobile App     │   │
│                      │  (Expo/RN)       │   │
│                      └──────────────────┘   │
└─────────────────────────────────────────────┘
```

## Data Flow

```
Mobile → HTTP REST → FastAPI → SQLAlchemy → PostgreSQL
                         ↓
                    Mock AI Gateway (deterministic)
                         ↓
                    Linguistic Validation
                         ↓
                    Pedagogical Validation
                         ↓
                    Policy Engine
                         ↓
                    Mastery Evidence + Audit
```

## Verified
- Docker Compose build/start: PASSED
- PostgreSQL 16.14 health: PASSED
- Backend health: PASSED
- Migration upgrade/downgrade: PASSED
- All 17 tables exist: PASSED
- All 109 integration tests: PASSED
