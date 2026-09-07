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

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/rule.svg" width="100%" alt="" />

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/h-built.svg" width="100%" alt="Things I've built" />

### GridPulse — real-time IoT energy streaming

Live electrical telemetry from **42 smart sub-meters** across **19 campus buildings**, ingested, aggregated and served.

The pipeline is deliberately boring in shape and specific in its choices. A Python simulator produces per-meter readings into a containerized **Kafka** cluster in KRaft mode, partitioned by meter ID so a single meter's events stay strictly ordered while different meters process in parallel. A **Spark Structured Streaming** job consumes the raw topic under a 5-minute sliding window with a 1-minute slide and a 2-minute event-time watermark — because sensor packets do not arrive in the order they were measured, and pretending otherwise gives you clean-looking numbers that are wrong.

<div align="center">

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/pipeline.svg" width="100%" alt="Meters into Kafka into Spark Structured Streaming, then forking into a hot path to Postgres and a cold path to date-partitioned Parquet, with a Streamlit dashboard reading the hot path." />

</div>

Storage splits two ways, and the split is the design. Hot path: aggregates land in **PostgreSQL** through tuned JDBC micro-batches — batch size 5,000, 15-second trigger — a deliberate trade of connection overhead against freshness that holds sub-minute latency from meter to queryable table. Cold path: raw telemetry writes to **Parquet partitioned by year/month/day**, so the full history stays cheap to scan later instead of bloating the operational store. A **Streamlit** dashboard reads the hot path with fragment-scoped polling, refreshing live aggregates every 3 seconds without re-rendering the layout around them.

`kafka` · `spark structured streaming` · `pyspark` · `postgres` · `parquet` · `docker` · `streamlit`

[Repo →](https://github.com/Abhishek86798/GridPulse)

---

### MCP Zero-Trust Gateway — kernel confinement for agent tools

An MCP tool server describes its own capabilities. That description is a claim, not a fact, and the gateway treats it that way: **declare, verify, confine.**

<div align="center">

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/gateway.svg" width="100%" alt="Declared capabilities compared against syscalls observed under strace in a locked-down container, compiled into a per-tool seccomp-BPF filter that denies anything outside the declaration at the kernel boundary." />

</div>

Each server is profiled under `strace` in a `--cap-drop ALL --read-only` container, the observed syscalls are checked against what the server declared, and the verified result is compiled into a per-tool **seccomp-BPF** filter. Anything outside the declaration is denied at the kernel boundary, not by application code that can be talked out of it. Provenance gating on tool-call arguments and per-call manifest re-attestation close CVE-2025-54136.

The part I'd defend in an interview isn't the enforcement, it's the evaluation. A 7-corpus, 583-row harness that separates *detection* from *containment*, because a gateway that notices an attack and doesn't stop it deserves a different number than one that stops it. 84.6% runtime defence, 100% containment, 87.8% on MCPTox.

`python` · `fastapi` · `seccomp-bpf` · `landlock` · `docker` · [PyPI: mcp-ztgateway](https://pypi.org/project/mcp-ztgateway/)

[Repo →](https://github.com/Abhishek86798/MCP_Zero-Trust_Gateway_BTP) · [Evaluation results →](https://drive.google.com/drive/folders/1UxaBiMxdcX8KH6rdeaSiJ0nu2eWcyXNQ?usp=sharing)

---

### CIDRA — CI debugging and repair agent

A **LangGraph** pipeline that reads a failing GitHub Actions run, works out why, and then — the part that matters — reproduces the failure in a sandboxed Docker container and verifies the fix actually passes before proposing it. Model output is Pydantic-validated with bounded retry, so a malformed response is a retry rather than a crash.

100% Tier-1/2 diagnosis accuracy across 53+ tests, with zero false "verified" claims. The second number is the one I care about: an agent that confidently proposes a broken fix is worse than one that says it doesn't know.

`python` · `langgraph` · `claude api` · `docker` · `pydantic`

[Repo →](https://github.com/Abhishek86798/CIDRA)

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/rule.svg" width="100%" alt="" />

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/h-exp.svg" width="100%" alt="Experience" />

**Trionix** · software development intern · *sole developer*

Owned the build end to end — schema through deployment. PostgreSQL data modelling with Row-Level Security, so tenant isolation is a database guarantee rather than a `WHERE` clause somebody has to remember. Being the only developer meant every design decision was also mine to live with two weeks later, which is a faster teacher than any code review.

**Bizzkonnect** · software development intern · *sole developer*

Same shape, different domain. Backend services and data plumbing, and the first time a design mistake of mine had actual users attached to it. That's the part that stuck.

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/rule.svg" width="100%" alt="" />

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/h-path.svg" width="100%" alt="How I got here" />

<table>
<tr><td width="110"><b>2023</b></td><td>Started B.Tech IT + MBA at IIITM Gwalior. Spent the first year in C — pointers, manual allocation, the stuff that makes you careful later.</td></tr>
<tr><td><b>early 2024</b></td><td>Figma and design systems. Prototyped <b>CampusSafe</b>, a campus emergency SOS app. Nothing I've built since has been improved by forgetting that someone has to use it.</td></tr>
<tr><td><b>late 2024</b></td><td>C++ and OOP. Implemented the core data structures myself rather than importing them, which is where most of my instinct for cost per operation came from.</td></tr>
<tr><td><b>early 2025</b></td><td>Moved to Python — PyTorch, NLP, first RAG experiments and transformer pipelines.</td></tr>
<tr><td><b>mid 2025</b></td><td>Built <b>AyuSynapse</b> solo at a healthcare AI hackathon: FHIR EMR parsing into BioBERT NER into ChromaDB, matching patients to clinical trials in a 36-hour sprint.</td></tr>
<tr><td><b>late 2025</b></td><td>Internships at Trionix and Bizzkonnect, sole developer on both. Postgres schemas, Row-Level Security, real users.</td></tr>
<tr><td><b>now</b></td><td>Streaming data and trust boundaries. <b>GridPulse</b> on Kafka and Spark, the <b>MCP gateway</b> on seccomp, <b>CIDRA</b> on LangGraph — and DSA most days.</td></tr>
</table>

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/rule.svg" width="100%" alt="" />

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/h-dsa.svg" width="100%" alt="DSA" />

The most consistent thing I do. 852 problems, most days, for long enough that the C++ years and the "cost per operation" instinct above are the same story.

<div align="center">

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/dsa.svg" width="92%" alt="LeetCode 393 medium and 55 hard at contest rating 1612, GeeksforGeeks 260+, Code360 100+ with 2x monthly topper — 852 total" />

<br/>

<sub><a href="https://leetcode.com/u/abhiii1005_/">LeetCode</a> · <a href="https://www.geeksforgeeks.org/profile/abhi_iiitm">GeeksforGeeks</a> · <a href="https://www.naukri.com/code360/profile/1d0eab26-a66e-4d90-99ed-46328d444eab">Code360</a> · all of it tracked on <a href="https://codolio.com/profile/abhishek_1005">Codolio</a></sub>

</div>

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/rule.svg" width="100%" alt="" />

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/h-oss.svg" width="100%" alt="Open source" />

I'm early here. One merged PR upstream, not twenty, and I'd rather say that than pad the section.

**[kubeflow/trainer #3960](https://github.com/kubeflow/trainer/pull/3960)** — merged into the CNCF Kubeflow project's Kubernetes-native distributed ML training orchestrator.

<!-- TODO: 2-3 sentences on what this PR actually changed and why it wasn't obvious.
     The specific bug is far more interesting than the fact that it merged.
     Reviewers read this line and nothing else in the section. -->

Also contributing through **GSSoC**, and a published inference model on [HuggingFace Hub](https://huggingface.co/abhishek1005). More to come — the goal for this section next year is that it's the longest one on the page.

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/rule.svg" width="100%" alt="" />

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/h-stack.svg" width="100%" alt="Stack" />

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

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/rule.svg" width="100%" alt="" />

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/h-lately.svg" width="100%" alt="Lately" />

<div align="center">

<img height="150" src="https://github-readme-stats.vercel.app/api?username=Abhishek86798&show_icons=true&hide_border=true&bg_color=0d1117&title_color=58a6ff&icon_color=58a6ff&text_color=8b949e&count_private=true" />
<img height="150" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Abhishek86798&layout=compact&hide_border=true&bg_color=0d1117&title_color=58a6ff&text_color=8b949e&hide=html%2Cjupyter%20notebook&langs_count=6" />

<br/><br/>

<img width="98%" src="https://streak-stats.demolab.com?user=Abhishek86798&hide_border=true&background=0d1117&ring=58a6ff&fire=58a6ff&currStreakLabel=58a6ff&sideLabels=8b949e&dates=6e7681" alt="contribution streak" />

<br/><br/>

<img width="98%" src="https://github-readme-activity-graph.vercel.app/graph?username=Abhishek86798&bg_color=0d1117&color=e6edf3&line=58a6ff&point=58a6ff&area=true&area_color=1f6feb&hide_border=true" alt="contribution heatmap" />

<br/><br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/output/github-contribution-grid-snake-dark.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/output/github-contribution-grid-snake.svg" alt="contribution snake" />
</picture>

<br/><br/>

<sub>B.Tech IT + MBA · IIITM Gwalior · graduating 2028</sub>

<br/>

<sub>if something here looks wrong, it probably is. <a href="https://github.com/Abhishek86798/Abhishek86798/issues">tell me</a></sub>

</div>
