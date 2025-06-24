# 🏆 Chess-Leaderboard

**A serverless leaderboard that ingests public Chess.com archives, stores game stats in DynamoDB, and exposes a JSON/GraphQL API for player rankings.**

[![build](https://github.com/yourGitHub/chess-leaderboard/actions/workflows/ci.yml/badge.svg)](../../actions)

---

## ✨ Project Highlights
- **One-shot CLI** (`cmd/cli`) to pull any player/month archive.
- **Scheduled ingest** (`cmd/ingest`) *coming soon* — keeps DynamoDB in sync.
- **REST / FastAPI endpoint** (`cmd/api`) *coming soon* — serves `/leaderboard`.
- **Infrastructure-as-Code** (Terraform) in `infra/` for easy AWS deploy.
- **Fully containerised** — `docker compose up` spins up the stack locally.

> **Status:** 🛠️ *Early prototype – core fetch CLI works; ingest + API next.*

---

## ⚡ Quick-start (local)

```bash
# clone & enter
git clone https://github.com/yourGitHub/chess-leaderboard.git
cd chess-leaderboard

# create a virtual env
python -m venv .venv
source .venv/bin/activate             # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt       # requests, click, etc.

# run the CLI demo (prints first finished game)
python cmd/cli/main.py hikaru 2025/06
