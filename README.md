<div align="center">

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/header.svg" width="100%" alt="abhishek kokadwar. data pipelines, backend, the boundaries between systems" />

<br/>

[![Portfolio](https://img.shields.io/badge/portfolio-0d1117?style=flat-square&logo=vercel&logoColor=white&labelColor=0d1117)](https://abhikokadwar.vercel.app/)
[![LinkedIn](https://img.shields.io/badge/linkedin-0d1117?style=flat-square&logo=linkedin&logoColor=white&labelColor=0d1117)](https://www.linkedin.com/in/abhishek-kokadwar/)
[![Email](https://img.shields.io/badge/email-0d1117?style=flat-square&logo=maildotru&logoColor=white&labelColor=0d1117)](mailto:abhikokadwar2@gmail.com)
[![PyPI](https://img.shields.io/badge/pypi-0d1117?style=flat-square&logo=pypi&logoColor=white&labelColor=0d1117)](https://pypi.org/project/mcp-ztgateway/)
[![Medium](https://img.shields.io/badge/medium-0d1117?style=flat-square&logo=medium&logoColor=white&labelColor=0d1117)](https://medium.com/@abhikokadwar2)

<br/>

[![Resume](https://img.shields.io/badge/download%20résumé-1f6feb?style=for-the-badge&logo=readdotcv&logoColor=white&labelColor=0d1117)](https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/abhishek-kokadwar-resume.pdf)

</div>

<br/>

Hi, I'm Abhishek.

I started with web apps, because that's where you can see what you built. Two internships in, the interesting part had quietly moved somewhere else: not the page, but the schema underneath it, and the question of how many round-trips it took to fill.

So now I spend most of my time on **data in motion** and on **trust boundaries** — the two places where a system is most likely to be confidently wrong. A dashboard that renders perfectly off a stale aggregate. A tool server that says it only needs to read one file.

The habit I'm trying to build is measuring the thing rather than assuming it. It's easy to write "real-time" in a README. It's harder to say what the watermark is, what happens to the packet that arrives four minutes late, and what the number looks like when you go back and check it.

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/rule.svg" width="100%" alt="" />

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/h-exp.svg" width="100%" alt="Experience" />

Two internships, remote, sole developer on both. Both shipped to a live domain — which is a different kind of pressure than a repo nobody deploys.

<table>
<tr>
<td width="32%" valign="top">

**HiGigAi**
<br/><sub>Software Developer Intern</sub>
<br/><sub>Jul 2026 – Aug 2026 · remote</sub>

<sub>`next.js` · `sanity cms`</sub>
<br/><sub>`cloudinary` · `vercel`</sub>

<sub>↗ <a href="https://www.tridentpublicschool.com/">tridentpublicschool.com</a></sub>
<br/><sub>↗ <a href="https://saaro-creations.vercel.app/">saaro-creations</a></sub>

</td>
<td valign="top">

A one-month engagement that had to outlive me. **Five branch sites on five subdomains from a single Next.js codebase**, so onboarding a sixth branch is content entry rather than a deploy.

25+ Sanity schemas with the Studio scoped through Structure Builder — the part that actually mattered: five branch admins manage 15+ page types with zero developer involvement, including mine.

Recurring infra came to **$0/month**. A planned Supabase tier replaced with Sanity-native forms and Cloudinary media, ISR plus webhooks for redeploy-free publishing. The cheapest thing to operate is the thing you didn't provision.

</td>
</tr>
<tr>
<td valign="top">

**Trionix Technologies**
<br/><sub>Software Developer Intern</sub>
<br/><sub>Jul 2025 – Sep 2025 · remote</sub>

<sub>`next.js` · `postgresql`</sub>
<br/><sub>`firebase` · `row-level security`</sub>

</td>
<td valign="top">

Architected the **Vyapar Pragati** admin platform: 6 backend modules, 500+ users, real-time Firestore messaging in place of manual polling.

Normalized the PostgreSQL schema with **Row-Level Security**, so tenant isolation is a database guarantee rather than a `WHERE` clause somebody has to remember. Eliminated the N+1 queries that were doubling DB round-trips on SSR routes.

First time a design decision of mine had users attached to it. That's the part that stuck.

</td>
</tr>
</table>

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/rule.svg" width="100%" alt="" />

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/h-active.svg" width="100%" alt="Currently building" />

### GridPulse — real-time IoT energy streaming

<sub>`kafka` · `spark structured streaming` · `pyspark` · `postgres` · `parquet` · `docker` · `streamlit` · <a href="https://github.com/Abhishek86798/GridPulse">repo →</a></sub>

Live electrical telemetry from **42 smart sub-meters** across **19 campus buildings**, ingested, aggregated and served.

The pipeline is deliberately boring in shape and specific in its choices. A Python simulator produces per-meter readings into a containerized **Kafka** cluster in KRaft mode, partitioned by meter ID so a single meter's events stay strictly ordered while different meters process in parallel. A **Spark Structured Streaming** job consumes the raw topic under a 5-minute sliding window with a 1-minute slide and a 2-minute event-time watermark — because sensor packets do not arrive in the order they were measured, and pretending otherwise gives you clean-looking numbers that are wrong.

<div align="center">

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/pipeline.svg" width="100%" alt="Meters into Kafka into Spark Structured Streaming, then forking into a hot path to Postgres and a cold path to date-partitioned Parquet, with a Streamlit dashboard reading the hot path." />

</div>

Storage splits two ways, and the split is the design. Hot path: aggregates land in **PostgreSQL** through tuned JDBC micro-batches — batch size 5,000, 15-second trigger — a deliberate trade of connection overhead against freshness that holds sub-minute latency from meter to queryable table. Cold path: raw telemetry writes to **Parquet partitioned by year/month/day**, so the full history stays cheap to scan later instead of bloating the operational store. A **Streamlit** dashboard reads the hot path with fragment-scoped polling, refreshing live aggregates every 3 seconds without re-rendering the layout around them.

---

### CIDRA — CI debugging and repair agent

<sub>`python` · `langgraph` · `claude api` · `docker` · `pydantic` · <a href="https://github.com/Abhishek86798/CIDRA">repo →</a></sub>

A **LangGraph** pipeline that reads a failing GitHub Actions run, works out why, and then — the part that matters — reproduces the failure in a sandboxed Docker container and verifies the fix actually passes before proposing it. Model output is Pydantic-validated with bounded retry, so a malformed response is a retry rather than a crash.

100% Tier-1/2 diagnosis accuracy across 53+ tests, with **zero false "verified" claims**. The second number is the one I care about: an agent that confidently proposes a broken fix is worse than one that says it doesn't know.

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/rule.svg" width="100%" alt="" />

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/h-done.svg" width="100%" alt="Shipped" />

### MCP Zero-Trust Gateway — kernel confinement for agent tools

<sub>`python` · `fastapi` · `seccomp-bpf` · `landlock` · `docker` · <a href="https://pypi.org/project/mcp-ztgateway/">PyPI →</a> · <a href="https://github.com/Abhishek86798/MCP_Zero-Trust_Gateway_BTP">repo →</a> · <a href="https://drive.google.com/drive/folders/1UxaBiMxdcX8KH6rdeaSiJ0nu2eWcyXNQ?usp=sharing">evaluation →</a></sub>

An MCP tool server describes its own capabilities. That description is a claim, not a fact, and the gateway treats it that way: **declare, verify, confine.**

<div align="center">

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/gateway.svg" width="100%" alt="Declared capabilities compared against syscalls observed under strace in a locked-down container, compiled into a per-tool seccomp-BPF filter that denies anything outside the declaration at the kernel boundary." />

</div>

Each server is profiled under `strace` in a `--cap-drop ALL --read-only` container, the observed syscalls are checked against what the server declared, and the verified result is compiled into a per-tool **seccomp-BPF** filter. Anything outside the declaration is denied at the kernel boundary, not by application code that can be talked out of it. Provenance gating on tool-call arguments and per-call manifest re-attestation close CVE-2025-54136.

The part I'd defend in an interview isn't the enforcement, it's the evaluation. A 7-corpus, 583-row harness that separates *detection* from *containment*, because a gateway that notices an attack and doesn't stop it deserves a different number than one that stops it. 84.6% runtime defence, 100% containment, 87.8% on MCPTox.

---

### Trinetra — parking violation prediction

<sub>`python` · `scikit-learn` · `fastapi` · `next.js` · `vercel` · <a href="https://gridlockl-fugg.vercel.app">live demo →</a></sub>

Built for the Flipkart Gridlock hackathon, aimed at Bangalore Traffic Police: given where and when violations have happened before, predict where enforcement should go next. **Top 5%.**

The modelling problem was more about the join than the model. Violation records, geospatial zones and time-of-day buckets have to line up before anything downstream means much, and most of the work was getting that feature table honest — deduplicating locations that appear under three spellings, and resisting the urge to read a hotspot into what is really just a place with more reporting. Served as a REST inference API with a Next.js dashboard on top, so the prediction lands somewhere a non-technical user can act on it.

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/rule.svg" width="100%" alt="" />

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/h-dsa.svg" width="100%" alt="DSA" />

The most consistent thing I do — 306 active days, and the reason a cost-per-operation instinct shows up in everything above.

<div align="center">

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/dsa.svg" width="92%" alt="859 solved, LeetCode contest rating 1640, 29 contests, 273 easy / 399 medium / 55 hard" />

<br/>

<sub>across <a href="https://leetcode.com/u/abhiii1005_/">LeetCode</a> (top 17%), <a href="https://www.geeksforgeeks.org/profile/abhi_iiitm">GeeksforGeeks</a>, <a href="https://www.naukri.com/code360/profile/1d0eab26-a66e-4d90-99ed-46328d444eab">Code360</a> (4x monthly topper) and CodeChef · rating and difficulty split fetched live · totals tracked on <a href="https://codolio.com/profile/abhishek_1005">Codolio</a></sub>

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

![Next.js](https://img.shields.io/badge/Next.js-0d1117?style=flat-square&logo=nextdotjs&logoColor=white&labelColor=0d1117)
![FastAPI](https://img.shields.io/badge/FastAPI-0d1117?style=flat-square&logo=fastapi&logoColor=white&labelColor=0d1117)
![Sanity](https://img.shields.io/badge/Sanity-0d1117?style=flat-square&logo=sanity&logoColor=white&labelColor=0d1117)
![Firebase](https://img.shields.io/badge/Firebase-0d1117?style=flat-square&logo=firebase&logoColor=white&labelColor=0d1117)
![LangChain](https://img.shields.io/badge/LangChain-0d1117?style=flat-square&logo=langchain&logoColor=white&labelColor=0d1117)
![HuggingFace](https://img.shields.io/badge/HuggingFace-0d1117?style=flat-square&logo=huggingface&logoColor=white&labelColor=0d1117)

</div>

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/rule.svg" width="100%" alt="" />

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/h-lately.svg" width="100%" alt="Lately" />

<div align="center">

<img src="https://raw.githubusercontent.com/Abhishek86798/Abhishek86798/main/assets/github.svg" width="92%" alt="GitHub contributions, commits, merged PRs, public repos and stars, with a language share bar" />

<br/><br/>

<img width="92%" src="https://streak-stats.demolab.com?user=Abhishek86798&hide_border=true&background=0d1117&ring=58a6ff&fire=58a6ff&currStreakLabel=58a6ff&sideLabels=8b949e&dates=6e7681" alt="contribution streak" />

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
