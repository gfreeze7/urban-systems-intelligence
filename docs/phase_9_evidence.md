\# Phase 9 â€” Production, Cloud, BI and AI Evidence



\## Orchestration and Scheduling



The Project 3 pipeline has a single Python orchestration entry point:



`python -m src.orchestration.pipeline`



The orchestrator runs the Census ingestion, BNIA ingestion, and geography stages and records operational pipeline status.



A PowerShell launcher (`run\_pipeline.ps1`) uses the project's virtual-environment interpreter. Windows Task Scheduler successfully executed the pipeline unattended on a daily schedule.



\## Containerization



The application is packaged with Docker using a reproducible `requirements.txt`.



The containerized database-mode pipeline successfully executed against the local PostgreSQL database using runtime environment configuration.



Secrets, the virtual environment, Git metadata, tests, documentation, and development artifacts are excluded from the Docker image through `.dockerignore`.



\## Azure Cloud Execution



The Docker image was pushed to a private Azure Container Registry.



An Azure Container Apps Job successfully pulled the private image using managed identity with the `AcrPull` role and executed the project's cloud-validation mode on the Consumption workload profile.



Cloud validation used the live Census API plus packaged BNIA and geographic crosswalk sources.



The Census API key was supplied through a runtime secret reference rather than embedded in the image.



The successful cloud execution validated:



\- 199 Census records

\- 104,272 BNIA observations

\- 784 BNIA geography-year records

\- 199 geography crosswalk records



No Azure-hosted PostgreSQL database was deployed. The cloud execution therefore demonstrates containerized ingestion and validation rather than a cloud database write.



\## Business Intelligence



A dedicated BI reporting layer produces:



`data/processed/bi/baltimore\_csa\_year.csv`



The dataset contains 770 CSA-year records covering 55 Baltimore Community Statistical Areas across 2010â€“2023.



A Power BI Desktop report implements:



\- Power Query ingestion and data typing

\- DAX measures

\- year-based interactive filtering

\- KPI cards

\- poverty versus violent-crime analysis

\- poverty versus chronic-absence analysis

\- longitudinal system indicators



The report is saved as:



`docs/Urban\_Systems\_Intelligence.pbix`



A Microsoft Fabric Free account was established and Power BI Service publication was attempted. PBIX publication was not completed because the Desktop authentication handoff did not complete. Cloud Power BI deployment is therefore not claimed as demonstrated.



\## AI-Assisted Analytics



Project 3 includes a local AI analytical briefing capability using Ollama and `llama3.2:3b`.



The LLM receives the project's structured hypothesis evidence matrix rather than independently generating analytical evidence.



The prompt constrains the model to:



\- use only supplied Project 3 evidence

\- preserve evidence states

\- avoid unsupported causal claims

\- state analytical limitations

\- distinguish findings from interpretation

\- explicitly identify questions the available evidence cannot answer



The analytical pipeline remains the evidence engine; the LLM is used for evidence-aware synthesis and communication.



The local model requires no paid API and introduces no recurring model cost.



\## Verification



Phase 9 verification completed successfully:



\- local orchestrated pipeline: PASS

\- unattended Windows scheduled execution: PASS

\- Docker database-mode execution: PASS

\- Azure Container Apps cloud-validation execution: PASS

\- Power BI Desktop implementation: PASS

\- Power BI Service publication: attempted, not demonstrated

\- local Ollama analytical briefing: PASS

\- full automated regression suite: 46/46 PASS



Phase 9 claims are limited to capabilities actually demonstrated.
