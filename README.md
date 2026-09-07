<div align="center">

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/header.svg" width="100%" alt="abhishek kokadwar. data pipelines, backend, the boundaries between systems" />

<br/>

[![Portfolio](https://img.shields.io/badge/portfolio-0d1117?style=flat-square&logo=vercel&logoColor=white&labelColor=0d1117)](https://abhikokadwar.vercel.app/)
[![LinkedIn](https://img.shields.io/badge/linkedin-0d1117?style=flat-square&logo=linkedin&logoColor=white&labelColor=0d1117)](https://www.linkedin.com/in/abhishek-kokadwar/)
[![Email](https://img.shields.io/badge/email-0d1117?style=flat-square&logo=maildotru&logoColor=white&labelColor=0d1117)](mailto:abhikokadwar2@gmail.com)
[![PyPI](https://img.shields.io/badge/pypi-0d1117?style=flat-square&logo=pypi&logoColor=white&labelColor=0d1117)](https://pypi.org/project/mcp-ztgateway/)
[![Medium](https://img.shields.io/badge/medium-0d1117?style=flat-square&logo=medium&logoColor=white&labelColor=0d1117)](https://medium.com/@abhikokadwar2)

</div>

<br/>

Hi, I'm Abhishek.

I started with web apps, because that's where you can see what you built. Two internships in, the interesting part had quietly moved somewhere else: not the page, but the schema underneath it, and the question of how many round-trips it took to fill.

So now I spend most of my time on **data in motion** and on **trust boundaries** — the two places where a system is most likely to be confidently wrong. A dashboard that renders perfectly off a stale aggregate. A tool server that says it only needs to read one file.

The habit I'm trying to build is measuring the thing rather than assuming it. It's easy to write "real-time" in a README. It's harder to say what the watermark is, what happens to the packet that arrives four minutes late, and what the number looks like when you go back and check it.

---

## What I'm working on

### GridPulse — real-time IoT energy streaming

Live electrical telemetry from **42 smart sub-meters** across **19 campus buildings**, ingested, aggregated and served.

The pipeline is deliberately boring in shape and specific in its choices. A Python simulator produces per-meter readings into a containerized **Kafka** cluster running in KRaft mode, partitioned by meter ID so a single meter's events stay strictly ordered while different meters process in parallel. A **Spark Structured Streaming** job consumes the raw topic under a 5-minute sliding window with a 1-minute slide, and a 2-minute event-time watermark, because sensor packets do not arrive in the order they were measured and pretending otherwise gives you clean-looking numbers that are wrong.

Storage splits two ways. Hot path: aggregates land in **PostgreSQL** through tuned JDBC micro-batches — batch size 5,000, 15-second trigger — which is a deliberate trade of connection overhead against freshness, and holds sub-minute latency from meter to queryable table. Cold path: raw telemetry writes to **Parquet partitioned by year/month/day**, so the full history stays cheap to scan later instead of bloating the operational store.

A **Streamlit** dashboard reads the hot path with fragment-scoped polling, refreshing live aggregates every 3 seconds without re-rendering the layout around them.

`kafka` · `spark structured streaming` · `pyspark` · `postgres` · `parquet` · `docker` · `streamlit`

[Repo →](https://github.com/Abhishek86798/GridPulse)

---

### MCP Zero-Trust Gateway — kernel confinement for agent tools

An MCP tool server describes its own capabilities. That description is a claim, not a fact, and the gateway treats it that way: **declare, verify, confine.**

Each server is profiled under `strace` in a locked-down container, the observed syscalls are checked against what the server declared, and the verified result is compiled into a per-tool **seccomp-BPF** filter. Anything outside the declaration is denied at the kernel boundary, not by application code that can be talked out of it. Provenance gating on tool-call arguments and per-call manifest re-attestation close CVE-2025-54136.

The part I'd defend in an interview isn't the enforcement, it's the evaluation. A 7-corpus, 583-row harness that separates *detection* from *containment*, because a gateway that notices an attack and doesn't stop it deserves a different number than one that stops it. 84.6% runtime defence, 100% containment, 87.8% on MCPTox.

`python` · `fastapi` · `seccomp-bpf` · `landlock` · `docker` · [PyPI: mcp-ztgateway](https://pypi.org/project/mcp-ztgateway/)

[Repo →](https://github.com/Abhishek86798/MCP_Zero-Trust_Gateway_BTP) · [Evaluation results →](https://drive.google.com/drive/folders/1UxaBiMxdcX8KH6rdeaSiJ0nu2eWcyXNQ?usp=sharing)

---

### CIDRA — CI debugging and repair agent

A **LangGraph** pipeline that reads a failing GitHub Actions run, works out why, and then — the part that matters — reproduces the failure in a sandboxed Docker container and verifies the fix actually passes before proposing it. Model output is Pydantic-validated with bounded retry, so a malformed response is a retry rather than a crash.

100% Tier-1/2 diagnosis accuracy across 53+ tests, with zero false "verified" claims. The second number is the one I care about: an agent that confidently proposes a broken fix is worse than one that says it doesn't know.

`python` · `langgraph` · `claude api` · `docker` · `pydantic`

[Repo →](https://github.com/Abhishek86798/CIDRA)

---

### VyaparPragati — multi-tenant admin platform

Built at Trionix Technologies. 6 backend modules, 500+ users.

Tenant isolation is enforced with PostgreSQL **Row-Level Security** at the database layer rather than in application code, so a forgotten `WHERE` clause in some future handler can't leak another tenant's rows. Profiling the data access layer turned up N+1 patterns on server-rendered routes; restructuring the joins halved DB round-trips. Real-time updates moved from a manual polling loop to event-driven Firestore listeners.

`next.js` · `postgres` · `row-level security` · `firebase` · `typescript`

---

## Open source

**[kubeflow/trainer #3960](https://github.com/kubeflow/trainer/pull/3960)** — merged into the CNCF Kubeflow project's Kubernetes-native distributed ML training orchestrator.

<!-- Replace this line with 2–3 sentences on what the PR actually changed and why it was non-obvious.
     The specific bug is far more interesting than the fact that it merged. -->

Also: active **GSSoC** contributor, and a published inference model on [HuggingFace Hub](https://huggingface.co/abhishek1005).

---

## Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-0d1117?style=flat-square&logo=python&logoColor=white&labelColor=0d1117)
![SQL](https://img.shields.io/badge/SQL-0d1117?style=flat-square&logo=postgresql&logoColor=white&labelColor=0d1117)
![C++](https://img.shields.io/badge/C++-0d1117?style=flat-square&logo=cplusplus&logoColor=white&labelColor=0d1117)
![TypeScript](https://img.shields.io/badge/TypeScript-0d1117?style=flat-square&logo=typescript&logoColor=white&labelColor=0d1117)
![Bash](https://img.shields.io/badge/Bash-0d1117?style=flat-square&logo=gnubash&logoColor=white&labelColor=0d1117)

![Kafka](https://img.shields.io/badge/Kafka-0d1117?style=flat-square&logo=apachekafka&logoColor=white&labelColor=0d1117)
![Spark](https://img.shields.io/badge/Spark-0d1117?style=flat-square&logo=apachespark&logoColor=white&labelColor=0d1117)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-0d1117?style=flat-square&logo=postgresql&logoColor=white&labelColor=0d1117)
![Docker](https://img.shields.io/badge/Docker-0d1117?style=flat-square&logo=docker&logoColor=white&labelColor=0d1117)
![Linux](https://img.shields.io/badge/Linux-0d1117?style=flat-square&logo=linux&logoColor=white&labelColor=0d1117)
![AWS](https://img.shields.io/badge/AWS-0d1117?style=flat-square&logo=amazonwebservices&logoColor=white&labelColor=0d1117)

![FastAPI](https://img.shields.io/badge/FastAPI-0d1117?style=flat-square&logo=fastapi&logoColor=white&labelColor=0d1117)
![Next.js](https://img.shields.io/badge/Next.js-0d1117?style=flat-square&logo=nextdotjs&logoColor=white&labelColor=0d1117)
![Firebase](https://img.shields.io/badge/Firebase-0d1117?style=flat-square&logo=firebase&logoColor=white&labelColor=0d1117)
![LangChain](https://img.shields.io/badge/LangChain-0d1117?style=flat-square&logo=langchain&logoColor=white&labelColor=0d1117)
![HuggingFace](https://img.shields.io/badge/HuggingFace-0d1117?style=flat-square&logo=huggingface&logoColor=white&labelColor=0d1117)

</div>

---

## Lately

<div align="center">

<img height="150" src="https://github-readme-stats.vercel.app/api?username=Abhishek86798&show_icons=true&hide_border=true&bg_color=0d1117&title_color=58a6ff&icon_color=58a6ff&text_color=8b949e&count_private=true" />
<img height="150" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Abhishek86798&layout=compact&hide_border=true&bg_color=0d1117&title_color=58a6ff&text_color=8b949e&hide=html%2Cjupyter%20notebook&langs_count=6" />

<br/><br/>

<sub>B.Tech IT + MBA · IIITM Gwalior · graduating 2028 &nbsp;·&nbsp; 1,000+ DSA problems across <a href="https://leetcode.com/u/abhiii1005_/">LeetCode</a>, <a href="https://www.naukri.com/code360/profile/1d0eab26-a66e-4d90-99ed-46328d444eab">Code360</a> and <a href="https://www.geeksforgeeks.org/profile/abhi_iiitm">GeeksforGeeks</a></sub>

<br/>

<sub>if something here looks wrong, it probably is. <a href="https://github.com/Abhishek86798/Abhishek86798/issues">tell me</a></sub>

</div>
