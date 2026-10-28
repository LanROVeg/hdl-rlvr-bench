# MASTER CONTEXT & BLUEPRINT: Hardware & EDA RLVR Environment Factory

## 1. Executive Summary & Core Objective
- **Primary Goal:** Generate **$10,000 in 90 days** ($3,333/month) starting late October 2026 while maintaining a full-time undergraduate Electrical Engineering schedule at Weber State University.
- **Core Strategy:** Build and operate an automated local **"RLVR (Reinforcement Learning with Verifiable Rewards) Hardware Benchmark Factory."** Instead of trading low-leverage hours or fighting saturated web-app SaaS markets, we mint containerized, deterministic evaluation environments for **Digital RTL (VHDL/Verilog)** and **Analog Circuits (SPICE)** and sell/contract them to funded AI labs, data brokers, and benchmark repositories.
- **Why This Works (The Unfair Moat):** 99% of AI prompt engineers and web developers do not know VHDL, GHDL, Yosys, or Ngspice AC phase-angle math. Conversely, 99% of traditional electrical engineers do not know how to wire up Dockerized Linux grading containers, dynamic Python anti-cheat testbenches, or Cursor/MCP automation pipelines. Sitting at the exact intersection of both allows 80–85% automation of tasks that pay $65–$160/hr on specialist platforms or $150–$400+ per packaged environment.

---

## 2. Operator Profile & Technical Stack
Any AI assistant reading this document must calibrate its responses to the operator's exact environment and background:
- **Operator:** Caden Egan (Electrical Engineering undergraduate, Weber State University).
- **Active EE Coursework (Raw Material for Tasks):** Digital Circuits (ECE 2700 — VHDL, 8-bit ALU, structural adders/subtractors, FSMs, Vivado 2026.1), Microelectronics & Analog Circuits (LTspice/Ngspice, AC phase angles, RC/RLC filters, Bode plots), Multivariable Calculus, Probability & Statistics.
- **Workstation Hardware:** Custom desktop running Windows 11 Pro + **WSL2 (Ubuntu 24.04)**, AMD Ryzen 7 5800X3D, AMD Radeon RX 6750 XT, 32GB DDR4 RAM, dual 32" 4K monitors (Alienware 240Hz OLED + Samsung 60Hz).
- **Development & AI Workflow:** Heavy user of **Cursor (Agent Mode)**, **Codex (GPT-6 Astra Ultra)**, and **Gemini Pro**; experienced in full-stack Node.js, TypeScript, React, Python, SQLite, and local MCP (Model Context Protocol) tooling (previously built `BonusProfitHub`).
- **Local Project Path:** `/home/caden/projects/RLVR` inside WSL Ubuntu (mapped to GitHub repo `hdl-rlvr-bench`).

---

## 3. Market Viability Audit: Why We Pivoted to RLVR Environments
We evaluated three distinct hardware/AI market gaps against five strict criteria (True Need, Sales Effort, Competition, Pull vs. Push Demand, and 90-Day Price Realism):

1. **Rejected Idea A — Standalone Paid EDA MCP Server SaaS ($39/mo):**
   - *Why we cut it as a standalone product:* Basic free open-source MCP wrappers (`coreyhahn/vivado_mcp`, `newtonsart/vivado-mcp-server`, `RFingAdam/mcp-ltspice-qucs`) already exist on GitHub. Charging individual students or engineers a monthly subscription for a local STDIO bridge requires heavy content marketing ("Push Selling") and fighting open-source culture.
   - *How we repurposed it:* Instead of selling the MCP server to consumers, we use a local MCP bridge *internally* inside Cursor so our own factory can generate and verify hardware tasks at 10x speed.
2. **Rejected Idea B — Datasheet-to-Code & BOM Arbitrage SaaS ($99/mo):**
   - *Why we cut it:* A VC-backed startup (`Embedder.com`) already dominates MCU C/C++ driver generation from PDF datasheets, holds SOC 2 Type II certification, and offers a free tier for individual developers. Competing against a free, funded product in a 90-day window is a trap.
3. **Selected Winner — Verified Hardware & EDA RLVR Environments (Pure Pull Demand):**
   - *The Market Bottleneck:* Frontier models (GPT-6 Astra, Claude Sonnet 5.5, Gemini 4) score 75–88% on web coding (React/Python), making generic coding data low-value. However, on October 2026 benchmarks like the **Vals AI Index**, **`Terminal-Bench-Science`**, **`Build-A-Chip-Bench`**, and **`Analog Design Bench`**, two-thirds of frontier models score **under 10%** in Engineering Sciences and hardware verification.
   - *Why Buyers Pay Immediately:* AI labs and data brokers (Mercor, Prime Intellect, Turing, Alignerr, Fleet AI, Bespoke Labs) have millions in allocated budget specifically to acquire **executable, non-flaky, containerized STEM/hardware grading environments** to train reasoning models via Reinforcement Learning with Verifiable Rewards (RLVR). There is zero cold-calling or consumer marketing required—if the container compiles deterministically and prevents reward hacking, buyers take every task you can mint.

---

## 4. Technical Architecture of a Hardware RLVR Deliverable
AI labs run thousands of Linux evaluation containers in parallel on cloud clusters. Therefore, deliverables **never** use bloated Windows GUIs (like 50GB Xilinx Vivado or Windows LTspice). Instead, every task is packaged as a lightweight, headless **Ubuntu 24.04 Docker container** following the **Harbor / Long-Horizon-Terminal-Bench 2.0 specification**.

### Standard 5-File Directory Structure
Each task lives in its own subdirectory (`/home/caden/projects/RLVR/<task-id>/`):
1. **`Dockerfile`:** Headless Ubuntu 24.04 environment with fast CLI simulators:
   - **Digital VHDL:** Uses `ghdl-mcode` (in-memory JIT compiler—avoids the Ubuntu 24.04 `ghdl-llvm` missing `libLLVM-18.so` bug, keeps the image small, and compiles in ~40ms) and optionally `yosys` for synthesis/latch checks.
   - **Digital Verilog/SystemVerilog:** Uses `iverilog` and `verilator`.
   - **Analog SPICE:** Uses `ngspice` (batch mode `-b`) + `python3-scipy` / `numpy`.
2. **`task.toml`:** Standardized metadata file defining `id`, `domain = "electrical_engineering"`, `subdomain`, `difficulty`, `[environment]` build configs, and `[verification]` commands (`python3 /tests/grade.py` and `solution/solve.sh`).
3. **`instruction.md`:** 100% unambiguous IEEE-style engineering specification handed to the AI agent (port maps, truth tables, opcodes, flag rules, or AC frequency/phase tolerances).
4. **`/workspace/`:** The initial directory visible to the AI agent. Contains either:
   - *Greenfield Stub:* An entity/netlist skeleton that compiles cleanly (`0.20` reward) but outputs zeros/defaults.
   - *Bug-Triage / Silicon Fault RTL:* A complete design injected with 3–4 realistic hardware bugs (e.g., swapped opcodes, wrong shift width, inverted flag checks) that the agent must diagnose and patch.
5. **`/solution/`:** Contains the golden reference file (e.g., `alu_8b_golden.vhd` or `filter_golden.cir`) and an executable `solve.sh` script that copies the golden file into `/workspace/` for automated CI verification.
6. **`/tests/grade.py`:** The isolated Python grading harness (mounted read-only at evaluation time and hidden from the agent during its run).

---

## 5. Grading Philosophy: Dense Rewards & Anti-Cheat ("Reward Hacking" Defense)
The difference between an amateur testbench and a **$250–$400 commercial RLVR environment** comes down to two mandatory rules implemented in `tests/grade.py`:

### Rule 1: 4-Stage Dense Process Rewards (`0.00` to `1.00`)
Binary pass/fail (`0` or `1`) gives zero learning signal during RL training if a task is difficult. Every `grade.py` script outputs a continuous JSON score (`{"reward": float, "details": {...}}`):
- **Stage 1 (`+0.20` to `+0.30`):** Code/netlist parses and compiles without syntax errors (`ghdl -a` or `ngspice -b` exits `0`).
- **Stage 2 (`+0.30` to `+0.40`):** Primary datapath / DC operating point / core functional accuracy across test vectors.
- **Stage 3 (`+0.30` to `+0.40`):** Exact hardware status flags (`NZVC`), cycle-accurate timing, or AC phase/gain margin tolerances across corner cases.

### Rule 2: Anti-Cheat & Zero-Baseline Hardening
LLMs are notorious "reward hackers"—if a static testbench file sits in the workspace, the agent will read the expected outputs and hardcode a lookup table. Our factory prevents this via three mechanisms:
1. **Dynamic Testbench Synthesis:** `grade.py` dynamically writes a brand-new VHDL testbench (`alu_tb_eval.vhd`) inside a temporary directory (`tempfile.TemporaryDirectory()`) at grading time, combining explicit hardware corner cases (e.g., signed two's complement overflow `+127 + 1`, `-128 - 1`, unsigned borrow `5 - 10`, MSB/LSB shift carry) with **50+ randomized test vectors**.
2. **Gated Flag Scoring:** A lazy all-zero starter stub (`Result <= x"00"; NZVC <= "0000"`) will accidentally match `NZVC = "0000"` on ~25% of random vectors. To prevent inflated NOP scores, `grade.py` only awards status-flag points on a given vector **if the primary `Result` datapath also matches** (`if Result = expected_res and NZVC = expected_nzvc`).
3. **Mandatory Two-Point CI Verification:** Every task must pass two terminal checks before commit:
   - **The `NOP` Check (Starter Workspace):** Runs `grade.py` against the unmodified `/workspace/`. Must score low (`~0.20` for greenfield stubs; `~0.35–0.70` for multi-bug triage tasks) to prove the task isn't trivially solved.
   - **The `ORACLE` Check (Golden Solution):** Mounts the golden reference solution over `/workspace/` and runs `grade.py`. Must deterministically score `{"reward": 1.0}`.

---

## 6. Current Factory Inventory & Verified Status
The following tasks are already built, containerized, and verified inside `/home/caden/projects/RLVR` (Reference the actual files in the repo for exact code):

| Task Folder | Archetype | Simulator | NOP Score | Oracle Score | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`vhdl-alu-flags-001`** | **Greenfield RTL:** 8-Bit Combinational ALU with signed Two's Complement Overflow (`V`), Carry/Borrow (`C`), Negative (`N`), and Zero (`Z`) flags (`NZVC`). | `ghdl-mcode` (VHDL-2008) | `0.2467` (Stub compiles, fails vectors) | `1.0000` (`60/60` data, `60/60` flags) | **Verified & Built** |
| **`vhdl-alu-fault-002`** | **RTL Bug Triage:** Pre-populated 8-Bit ALU injected with 3 silicon bugs (swapped `AND`/`OR` opcodes, `SHR` shifting by 2 bits with wrong carry bit, inverted `Z` flag checking `x"FF"`). | `ghdl-mcode` (VHDL-2008) | `0.7133` (`40/60` data, `37/60` flags) | `1.0000` (`60/60` data, `60/60` flags) | **Verified & Built** |
| **`spice-rc-phase-003`** | **Analog AC Filter Tuning:** Single-pole RC low-pass filter netlist requiring component calculation ($R = 1591.5\ \Omega, C = 100\text{ nF}$) to hit $-3\text{ dB}$ ($0.7071\text{ V}$) and $-45^\circ \pm 2^\circ$ phase shift at $f_c = 1\text{ kHz}$ ($\omega = 2000\pi$). | `ngspice -b` (Headless AC sweep) | `0.3000` (Simulates, wrong $f_c$) | `1.0000` (Exact magnitude & phase match) | **Scaffolded** |

---

## 7. Known WSL / Docker Environment Quirks (Do Not Repeat)
When generating commands or scripts for this environment, keep these resolved fixes in mind:
1. **Native WSL Docker Engine:** We use native `docker-ce` inside WSL Ubuntu (`curl -fsSL https://get.docker.com | sudo sh`), NOT heavy Windows Docker Desktop.
2. **Socket Permissions:** If Docker ever throws `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock`, fix it immediately with:
   `sudo usermod -aG docker $USER && sudo chown root:docker /var/run/docker.sock && sudo chmod 660 /var/run/docker.sock && newgrp docker`
3. **User Context (`caden` vs `root`):** Always ensure terminal commands and `git` operations run under user `caden` inside `/home/caden/projects/RLVR`, never `/root`.
4. **GHDL Package Selection on Ubuntu 24.04:** Always install `ghdl-mcode` in Dockerfiles, **never** `ghdl-llvm` (which breaks due to missing `libLLVM-18.so.18.1` shared libraries in Ubuntu 24.04 apt repos).
5. **Avoid Complex Multi-Line `sed` Mutations on VHDL:** Single-line VHDL `if ... then ... end if;` statements break if `sed` injects `--` comments mid-line. Always generate mutated `.vhd` files cleanly via Python scripts or full `cat << 'EOF'` overwrites.

---

## 8. The 85% Automated Production Pipeline (How to Mint Tasks in 20 Mins)
Now that the base Dockerfiles and `grade.py` harnesses are built, we do not write tasks from scratch. We scale production using **Parameterized Archetype Mutation**:

1. **Step 1 — Pick a Coursework Seed (5 mins):** Take any lab, homework problem, or subsystem from ECE 2700 (Digital Circuits) or Analog Circuits:
   - *Digital Seeds:* $N$-bit generic barrel shifters, synchronous FIFOs with almost-full/almost-empty flags, UART/SPI TX/RX state machines, structural ripple-carry subtractors, priority encoders, sequence detectors, memory controller FSMs.
   - *Analog SPICE Seeds:* Sallen-Key active 2nd-order filters, RLC bandpass resonant circuits, op-amp lead/lag phase compensators, voltage-divider biasing with load-line constraints.
2. **Step 2 — Automated Multi-Variant Generation (5 mins):** Use Cursor (connected to local `ghdl` / `ngspice` CLI execution) to generate 3 instant variations from every 1 seed concept:
   - **Variant A (Greenfield Implementation):** Build from spec + empty port stub.
   - **Variant B (Silicon Bug Triage):** Inject 3 subtle RTL/netlist bugs into the golden solution and ask the agent to diagnose and fix.
   - **Variant C (Parameterized / Structural Constraint):** Require generic bit-widths (`generic (N : positive)`) tested across two hidden widths in `grade.py`, or require structural component instantiation without behavioral `+`/`-` operators.
3. **Step 3 — Automated Container Validation (2 mins):** Run the standard Docker build + NOP check + ORACLE check script to verify `NOP < 0.45` (or partial pass on bug triage) and `ORACLE == 1.0`.

---

## 9. Monetization & 90-Day $10,000 Execution Roadmap

### The Math to $10,000
- **Channel A — Specialist RL Environment & Hardware/STEM Contracting Pods ($5,000 – $7,000):**
  - **Target Platforms:** **Mercor** (RL Environment Engineering & Hardware Pods: $70–$160/hr), **Prime Intellect** (Environments Hub contributors & bounties), **Alignerr / Turing / micro1 / Outlier** (Verified STEM/HDL/C++ evaluation tracks: $55–$100/hr), and agentic environment startups (**Fleet AI, HUD, Veris AI, Bespoke Labs**).
  - **The Pitch Advantage:** 99% of applicants submit a plain resume. Submitting a live GitHub portfolio (`github.com/caden-egan/hdl-rlvr-bench`) containing production-ready, Harbor-compliant Dockerized VHDL & Ngspice RLVR environments with anti-cheat dynamic testbenches fast-tracks you directly into environment-building pods.
  - **Time/Yield:** Working 8–10 flexible hours/week on specialist environment contracting at an average of $85/hr yields **~$3,400/month ($10,200 over 90 days)**—and because your local factory automates 80% of testbench creation, your effective hourly output on per-task bounties ($200–$350/environment) exceeds **$300/hr**.
- **Channel B — Supplemental High-Velocity Cash Stack ($3,000 – $5,000 backup buffer):**
  - If contracting onboarding takes 2 weeks to ramp up, bridge the gap with zero-client-overhead plays already in your ecosystem:
    1. **2-Player Sweepstakes & VM GPT Arbitrage ($2,000+):** Run a second verified identity (roommate/family split) inside an isolated Hyper-V VM / static residential proxy using `BonusProfitHub` + automated mobile emulator game sprints.
    2. **Etsy ACH "Direct Deposit" Bank Bonus Cycling ($1,500+):** Route HumorHazard Etsy payouts through Chase, SoFi, BMO, and U.S. Bank Business checking promo offers.
    3. **Packaged `BonusProfitHub` Discord/Whop Release or Automated Q4 Printify Niche Script ($1,000+).**

### Immediate Next Actions for Any AI Assistant Continuing This Session
When assisting Caden in future sessions, prioritize:
1. Auditing and refining `spice-rc-phase-003` so its `ngspice` stdout parser in `tests/grade.py` hits `0.30` on NOP and `1.00` on ORACLE cleanly.
2. Writing a root `README.md` and a `run_all_benchmarks.sh` CI runner in `/home/caden/projects/RLVR` so external recruiters/buyers from Mercor, Prime Intellect, and Fleet AI can verify the entire benchmark suite with a single command.
3. Minting Tasks `004` through `010` (e.g., Synchronous FIFO, Structural Subtractor, Clocked FSM Controller, RLC Bandpass Filter) via automated Python generator scripts.