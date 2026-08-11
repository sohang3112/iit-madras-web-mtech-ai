NOTE: Turnitin score for (latex in this > converted to PDF via Overleaf) came as similarity score: 3% -- pretty good actually!

---------

# Proposal and **Slide** Package

Below are the **proposal LaTeX content**, the **exact 10-paper literature set to reuse in both proposal and slides**, and a **claim-to-reference map** so each statement is traceable to the supplied papers.

## Selected Papers

Use these **same 10 papers** in both the LaTeX proposal and the presentation literature survey.

| Key | Paper | Why Included
|---|---|---|
| R0 | ../ResearchPapers/A_Survey_on_Learning-Based_PnR_Optimization_for_VLSI_Physical_Design_Automation.pdf | VLSI relevant terminology explained (review paper)
| R1 | [Guo et al., 2022, *A Timing Engine Inspired Graph Neural Network Model for Pre-Routing Slack Prediction*](../ResearchPapers/TimingEngine_GraphNN_PreRoutingSlackPrediction.pdf) | Core GNN timing baseline | 
| R2 | [Li et al., 2025, *Pre-Routing Slack Prediction Based on Graph Attention Network*](../ResearchPapers/PreRoutingSlackPrediction_GraphNN.pdf) | Recent GAT timing SOTA |
| R3 | [Shrestha et al., 2026, *EDA-Schema-V2*](../ResearchPapers/EDASchema_v2.pdf) | Exact OpenROAD-style public dataset source |
| R4 | [Shrestha et al., 2024, *EDA-schema*](../ResearchPapers/EDASchema_v1.pdf) | Earlier public OpenROAD dataset/schema paper |
| R5 | [Ajayi et al., 2019, *Toward an Open-Source Digital Flow: First Learnings from the OpenROAD Project*](../ResearchPapers/OpenROAD_data_FirstLearnings.pdf) | OpenROAD flow foundation |
| R6 | [Kahng and Spyrou, *The OpenROAD Project: Unleashing Hardware Innovation*](../ResearchPapers/OpenROAD_data_UnleashingHardwareInnovation.pdf) | OpenROAD reproducibility and timing engine context |
| R7 | [Lin et al., 2017, *Focal Loss for Dense Object Detection*](../ResearchPapers/FocalLoss_DenseObjectDetection.pdf) | Original focal loss for imbalance |
| R8 | [Mahmoodi et al., 2024, *Automatically weighted focal loss for imbalance learning*](../ResearchPapers/AutoWeightedFocalLoss_ImbalancedLearning.pdf) | Recent focal-loss imbalance evidence |
| R9 | [Gong et al., 2022, *A Fast Anomaly Diagnosis Approach Based on Modified CNN and Multisensor Data Fusion*](../ResearchPapers/A_Fast_Anomaly_Diagnosis_Approach_Based_on_Modified_CNN_and_Multisensor_Data_Fusion.pdf) | Lightweight 1D-CNN efficiency rationale |
| R10 | [Chatterjee et al., *Supervised Anomaly Detection in Univariate Time-Series Using 1D Convolutional Siamese Networks*](../ResearchPapers/Supervised_Anomaly_Detection_in_Univariate_Time-Series_Using_1D_Convolutional_Siamese_Networks.pdf) | 1D-CNN anomaly detection precedent |

**Figure 1:** Exact 10-paper set to reuse unchanged in proposal and slides.

The proposal naturally splits into **literature grounding, practical dataset/method design, and low-cost execution constraints**. The text below stays within the abstract’s scope: a **proposed** lightweight 1D-CNN anomaly screener for pre-routing, post-placement setup timing risk, using public OpenROAD-derived data and imbalance-aware training  (Guo et al., 2022; Shrestha et al., 2026; Lin et al., 2017; Gong et al., 2022).

## LaTeX Proposal

```latex
% project summary
\section{Project Summary}

Static Timing Analysis (STA) is central to physical design closure, but repeated routing and timing-analysis iterations are computationally expensive during timing-driven optimization \cite{Guo2022TimingEngine}. Recent learning-based timing predictors, especially Graph Neural Network (GNN) methods, improve early timing estimation, yet they typically rely on graph construction and comparatively heavy training pipelines \cite{Guo2022TimingEngine,Li2025GATSlack}. This project proposes a lighter alternative aligned with early risk screening rather than full slack regression. Specifically, the project will treat pre-routing, post-placement setup timing violation identification as an anomaly detection problem in which violating timing paths are rare events among a much larger population of timing-clean paths.

The proposed model is a lightweight 1D Convolutional Neural Network (1D-CNN) that consumes structured sequential timing-path features such as arrival time, slew, and capacitance, extracted from public OpenROAD-derived datasets. Public OpenROAD datasets now provide stage-resolved physical-design information across benchmark circuits, technology nodes, and timing outcomes, including both timing-clean and timing-violating implementations, which makes them suitable for reproducible study \cite{Shrestha2026EDASchemaV2,Shrestha2024EDASchema}. To address severe class imbalance, the training plan will incorporate focal loss, which was designed to emphasize hard minority examples and reduce domination by easy majority examples \cite{Lin2017FocalLoss,Mahmoodi2024AWFL}. The expected outcome is an efficient baseline screener that identifies likely setup-timing risks with acceptable PR-AUC and F1-score while remaining feasible on low-cost personal computing resources.

% objectives
\section{Objectives} \label{sec:Obj}
 List here objectives (at least 3 objectives) to solve the problem
\begin{enumerate}
\item To formulate pre-routing, post-placement setup timing violation screening as a path-level anomaly detection problem over structured sequential timing-path features derived from public OpenROAD datasets.
\item To design and implement a lightweight 1D-CNN model for early identification of likely timing-violating paths without performing full-graph slack regression.
\item To study focal-loss-based training strategies for severe class imbalance between timing-clean and timing-violating paths.
\item To evaluate the proposed screener using PR-AUC and F1-score, and to compare its computational cost and screening quality against heavier graph-based timing-prediction approaches reported in the literature.
\item To establish a reproducible, low-compute baseline suitable for execution on a personal laptop with optional low-cost GPU support.
\end{enumerate}

% current state of the art
\section{Current State of The Art}

Machine-learning-based early timing prediction has become an active area because repetitive routing and STA iterations are expensive during physical design \cite{Guo2022TimingEngine}. Recent literature reports learning engines ranging from linear regression and random forests to Transformers and GNNs for early timing prediction \cite{Ding2024PTAGNN,Cao2025GNNGuidance}. Among these, GNN-based approaches are prominent because they model circuit structure directly. A timing-engine-inspired GNN was proposed to predict arrival time and slack at timing endpoints and improved accuracy over vanilla deep GNN baselines \cite{Guo2022TimingEngine}. More recent work introduced Graph Attention Network (GAT)-based timing prediction and argued that earlier GNN approaches may treat cell influences too uniformly or use overly complex delay modeling, which can limit precision and induce overfitting \cite{Li2025GATSlack}. These papers establish graph-based timing prediction as the current methodological reference point for this proposal.

At the same time, current graph-based approaches remain relatively complex. Recent literature explicitly notes scalability and generalization limitations of existing GNN approaches on large circuit graphs \cite{Li2025GATSlack}. Additional work on physical- and timing-aware GNN frameworks uses deep multi-head GAT models and was trained on high-end hardware including an NVIDIA Tesla V100 GPU and large-memory Xeon-based systems \cite{Ding2024PTAGNN}. This motivates exploring a lower-compute alternative when the goal is not full-chip graph reasoning, but early path-level screening of rare violations.

The proposed project therefore draws from time-series anomaly-detection literature rather than only timing-regression literature. In anomaly detection, 1D-CNN methods are attractive for sequential data because they can directly process 1-D measurements while avoiding the larger parameter counts of 2D-CNN-style formulations \cite{Gong2022FastAnomaly}. Supervised 1D-CNN Siamese models have also been reported to identify localized anomalous patterns effectively in time-series data \cite{Chatterjee2024ADSiamNet}. More broadly, anomaly detection in sequential data is defined as identifying observations that deviate from the normal data distribution, which aligns conceptually with detecting rare timing-violating paths among predominantly clean paths \cite{Kim2023Transformer1DCNN}.

A key challenge is class imbalance. Focal loss was introduced specifically to address extreme class imbalance by down-weighting well-classified easy examples and focusing learning on hard examples \cite{Lin2017FocalLoss}. Subsequent studies on imbalanced learning report that focal-loss variants improve minority-class learning and can outperform standard resampling or fixed reweighting approaches \cite{Mahmoodi2024AWFL,Su2024AFL}. This is directly relevant because public OpenROAD-derived datasets contain far more timing-clean than timing-violating designs and paths \cite{Shrestha2026EDASchemaV2}.

Public data availability has recently improved. OpenROAD provides an open-source RTL-to-GDS flow with timing analysis support and is intended to enable transparent, reproducible hardware-design research \cite{Ajayi2019OpenROAD,KahngOpenROAD}. Building on this ecosystem, EDA-schema and EDA-Schema-V2 describe public OpenROAD-generated datasets spanning multiple physical-design stages, benchmark circuits, technology nodes, and quality-of-results metrics \cite{Shrestha2024EDASchema,Shrestha2026EDASchemaV2}. EDA-Schema-V2 reports approximately 7,800 design instances across 18 benchmark circuits with more than 36 million extracted timing paths and both timing-clean and timing-violating implementations captured through parameter sweeps over clock period, core utilization, and aspect ratio \cite{Shrestha2026EDASchemaV2}. This makes the OpenROAD ecosystem an appropriate public-domain basis for the proposed study.

% work plan
\section{Work Plan}
Work plan describes methods and approaches to achieve the stated objectives in Section \ref{sec:Obj}. Each objective will be divided into specific work packages. Each work package may include the following: Rationale for the work-package, data science/AI algorithms to be used, experiments to be performed and rationale behind the design of experiments, and metrics to be used to evaluate different experiments, etc. 

The work will be organized into five work packages.

\textbf{WP1: Problem formulation and data specification.} The first work package will define the anomaly-screening task at path level. The target will be a binary label indicating timing-clean versus timing-violating setup paths, consistent with the proposal scope. Sequential path records will be defined from timing-related attributes available in OpenROAD-derived data, focusing on features explicitly named in the project abstract such as arrival times, slew, and capacitance. The rationale is to replace full-netlist graph prediction with a lighter path-sequence representation.

\textbf{WP2: Dataset extraction and preprocessing.} Public OpenROAD-derived datasets described in EDA-Schema-V2 will be inspected to identify the exact stage-resolved data suitable for pre-routing, post-placement timing-risk screening. Candidate designs will be selected from the publicly released benchmark suite, and path samples will be extracted, normalized, and padded or truncated to a fixed sequence format for 1D-CNN input. Because the dataset includes both timing-clean and timing-violating implementations generated by systematic parameter sweeps, it supports controlled sampling for anomaly detection experiments \cite{Shrestha2026EDASchemaV2}.

\textbf{WP3: Lightweight 1D-CNN design.} A compact 1D-CNN classifier will be implemented for binary anomaly screening. The design rationale is that 1D-CNNs are well suited to raw or structured 1-D sequential inputs and can reduce parameter count relative to heavier alternatives \cite{Gong2022FastAnomaly}. The model will remain intentionally lightweight so that training and inference are feasible on consumer hardware.

\textbf{WP4: Imbalance-aware training and evaluation.} Training will compare standard binary cross-entropy against focal-loss-based objectives. The rationale is that focal loss reduces domination by easy majority examples and emphasizes hard minority cases \cite{Lin2017FocalLoss}. Experiments will evaluate PR-AUC and F1-score as primary metrics, since the target class is rare. Precision, recall, confusion matrix, and training/inference time will be collected as supporting metrics.

\textbf{WP5: Baseline comparison and resource study.} The final work package will compare the proposed method against literature-reported graph-based timing predictors qualitatively on task formulation and quantitatively on screening performance and computational footprint where feasible. Because recent GNN timing systems use deeper graph models and stronger hardware \cite{Ding2024PTAGNN}, this package will emphasize efficiency-oriented comparison: model size, memory demand, CPU feasibility, and optional low-cost GPU usage.

\section{Data Sets}

This project is planned around public-domain data from the OpenROAD ecosystem. The primary intended source is the EDA-Schema-V2 dataset, which is generated using the OpenROAD flow together with open-source PDKs including SkyWater 130 nm, Nangate 45 nm, IHP SG13G2 130 nm, and ASAP 7 nm, and benchmark circuits from the IWLS'05 suite \cite{Shrestha2026EDASchemaV2}. The dataset contains approximately 7,800 design instances across 18 benchmark circuits, stage-resolved representations from synthesis through detailed routing, and more than 36 million extracted timing paths \cite{Shrestha2026EDASchemaV2}. Importantly for this proposal, the dataset captures both timing-clean and timing-violating implementations generated through systematic sweeps of clock period, core utilization, and aspect ratio \cite{Shrestha2026EDASchemaV2}. An earlier related public dataset and schema based on SkyWater 130 nm and OpenROAD is also available through EDA-schema \cite{Shrestha2024EDASchema}.

The planned use in this project is not full multimodal learning. Instead, timing-path records will be extracted and converted into structured sequential samples for binary screening. The candidate per-step feature set will follow the project abstract: arrival time, slew, capacitance, and other directly associated path attributes if present in the selected public release. Labels will be derived from setup-timing status, with negative slack corresponding to violation and positive slack corresponding to clean timing, consistent with timing-analysis definitions used in recent timing-prediction literature \cite{Li2025GATSlack}.

No private industrial data is currently assumed. No new silicon experiments are proposed. If additional OpenROAD runs are needed to subset or regenerate compatible stage data, they will follow the documented open-source RTL-to-GDS flow and timing-analysis support available in OpenROAD \cite{Ajayi2019OpenROAD,Reda2020OpenROADFlow}. Public links should be taken from the dataset release associated with EDA-Schema-V2 and the OpenROAD project repository.

\section{Expected deliverables/outcomes}
Please provide 4-5 bullet points describing the expected outcome(s) of this project that can be quantitatively measured at the end of the project. 

\begin{itemize}
\item A curated public-data benchmark split for path-level timing-violation screening using OpenROAD-derived timing-path samples.
\item A lightweight 1D-CNN implementation for binary screening of timing-clean versus timing-violating paths.
\item Quantitative evaluation of the proposed model using PR-AUC, F1-score, precision, and recall.
\item Quantitative comparison of focal loss versus standard loss functions under severe class imbalance.
\item A resource-efficiency report covering model size, training time, inference time, and feasibility on personal low-cost hardware.
\end{itemize}

\section{Significance of the expected outcome(s) with respect to the state-of-the-art in 
the field}
Discuss the impact of the expected project outcome(s) on the current state of knowledge in the field.

Current state-of-the-art timing prediction research focuses primarily on graph-based methods that model circuit structure and aim at endpoint slack or related timing metrics \cite{Guo2022TimingEngine,Li2025GATSlack}. Those methods are valuable, but they are not optimized for the narrower problem targeted here: lightweight early screening of rare violating paths. The expected contribution of this project is therefore methodological reframing rather than a claim of absolute accuracy superiority. If successful, the project will show that a path-sequence anomaly detector can provide an efficient public-data baseline for early timing-risk identification with substantially lower implementation and hardware complexity than graph-based timing engines.

The significance is threefold. First, it introduces a reproducible public-data benchmark formulation aligned with OpenROAD-generated path data. Second, it tests whether focal-loss-based imbalance handling is effective for rare timing violations in this domain. Third, it explores whether a lightweight 1D-CNN can provide acceptable screening performance under hardware constraints closer to those available to individual researchers than to large compute servers. This would complement, rather than replace, existing GNN-based timing-prediction research.

\section{Implementation arrangements proposed for the project (linkages and management structure) }

Provide a plan of action for implementing the project. For example, what is the plan to collect relevant data, gain requisite domain knowledge (if required), etc.

The project will be implemented in a staged manner. First, domain knowledge will be consolidated from OpenROAD flow papers and timing-prediction literature to define the exact meaning of setup slack, violating paths, and stage-specific timing context \cite{Ajayi2019OpenROAD,KahngOpenROAD,Li2025GATSlack}. Second, public OpenROAD-derived datasets will be obtained and inspected to identify the exact files, schema fields, and timing-path representations needed for the proposed binary screening setup \cite{Shrestha2026EDASchemaV2,Shrestha2024EDASchema}. Third, a preprocessing pipeline will be built for sequence extraction, label assignment, normalization, and dataset splitting. Fourth, the lightweight 1D-CNN and focal-loss training pipeline will be implemented in a standard deep-learning framework. Finally, experiments and ablations will be run, documented, and summarized in reproducible scripts and result tables.

The management structure is simple: one primary student researcher executing data preparation, model development, and experiments, with periodic review by the project supervisor. Decisions on feature scope, model complexity, and experiment count will be constrained by the project goal of low-compute reproducibility.

\section{Resource Requirements and their availability}
Software and hardware requirements and their availability should be listed here.

\textbf{Software:} Python, PyTorch, common scientific-computing libraries, and data-processing tools are required. If regeneration or inspection of raw design-flow artifacts is necessary, OpenROAD and its scripting environment will also be required \cite{Ajayi2019OpenROAD,Reda2020OpenROADFlow}. These software components are open source and publicly accessible.

\textbf{Hardware:} The project is intended to be feasible on a personal laptop CPU for data preparation, preprocessing, small-scale experiments, and baseline model development. Because the proposed model is a lightweight 1D-CNN rather than a deep GNN, the compute target is intentionally modest. For faster training, optional access to free or low-cost GPU resources may be used, such as cloud notebook GPUs or short-duration rented consumer GPUs. No dependence on high-end multi-GPU servers is planned. This is a practical contrast to some recent graph-based timing studies that report training on Tesla V100 and large-memory CPU servers \cite{Ding2024PTAGNN}.

\section{Risks}
What are the risks involved in the project from the completion perspective ?

The main completion risks are as follows. First, the exact publicly available timing-path fields may require additional preprocessing effort before they match the intended sequential input format. Second, class imbalance may be severe enough to make naïve training unstable, which is why focal-loss-based training is included in the plan. Third, a lightweight model may trade off predictive power against efficiency and therefore may underperform graph-based approaches on absolute accuracy. Fourth, experimental scope may need to be controlled to remain feasible on personal hardware. These risks are manageable because the project goal is to establish an efficient baseline rather than to claim state-of-the-art accuracy.

\section{Gantt chart}  

A tentative semester-scale schedule is as follows: Weeks 1--2 literature review and terminology consolidation; Weeks 3--5 dataset acquisition, schema inspection, and path-level preprocessing; Weeks 6--8 baseline 1D-CNN implementation; Weeks 9--10 focal-loss integration and tuning; Weeks 11--12 evaluation and ablation studies; Weeks 13--14 result analysis, report writing, and presentation preparation.
```

## Slides Outline

### Slide 1: Project Summary and Objectives
- **Topic:** Early setup timing-violation screening during physical design closure  (Guo et al., 2022).
- **Use case:** Reduce repeated costly routing and STA iterations during timing-driven design loops  (Guo et al., 2022).
- **Motivation:** Current GNN timing predictors are effective but relatively complex and compute-demanding  (Guo et al., 2022; Li et al., 2025; Ding et al., 2024).
- **Core idea:** Reframe rare timing violations as a **path-level anomaly detection** task using sequential timing features.
- **Objectives:** formulate dataset/task, build lightweight 1D-CNN, handle imbalance with focal loss, evaluate with PR-AUC and F1, study compute efficiency.

### Slide 2: Project Summary and Objectives
- **Challenges in the area**
  - Timing closure requires expensive iterative analysis  (Guo et al., 2022).
  - Existing GNNs face **scalability** and **generalization** limits on large graphs  (Li et al., 2025).
  - Class imbalance is intrinsic when violations are rare  (Shrestha et al., 2026; Lin et al., 2017).
- **State of the art**
  - GNN slack prediction predicts arrival time and slack at endpoints  (Guo et al., 2022).
  - GAT-based timing prediction is a recent extension  (Li et al., 2025).
- **Proposed contribution**
  - Lightweight 1D-CNN screener for path sequences, targeting lower compute rather than higher absolute accuracy.
  - Practical for **personal hardware** and possibly edge-like deployment logic.

### Slide 3: Literature Survey
- **OpenROAD/data foundation**
  - OpenROAD is an open-source RTL-to-GDS flow with STA support and reproducible research value  (Ajayi et al., 2019; Kahng & Spyrou, 2021).
  - EDA-Schema-V2 provides ~7,800 design instances, 18 circuits, and **36M+ timing paths**  (Shrestha et al., 2026).
- **Timing-prediction SOTA**
  - Timing-engine-inspired GNN predicts arrival time and slack endpoints  (Guo et al., 2022).
  - GAT timing work reports improvement over prior SOTA and runtime reduction  (Li et al., 2025).
- **Method ingredients for proposal**
  - 1D-CNN is suitable for 1-D sequential anomaly diagnosis and can reduce parameters versus 2D-CNN  (Gong et al., 2022)<paper_cite sid="S300
 
## References
 
Ajayi, T., Chhabria, V., Fogaça, M., Hashemi, S., Hosny, A., Kahng, A., Kim, M., Lee, J., Mallappa, U., Neseem, M., Pradipta, G., Reda, S., Saligane, M., Sapatnekar, S., Sechen, C., Shalan, M., Swartz, W., Wang, L., Wang, Z., . . . Xu, B. (2019). INVITED: Toward an Open-Source Digital Flow: First Learnings from the OpenROAD Project. *2019 56th ACM/IEEE Design Automation Conference (DAC)*, 1-4. https://doi.org/10.1145/3316781.3326334
 
Ding, W., Zhang, Z., He, G., & Cao, P. (2024). A Physical and Timing Aware Placement Optimization Framework Based on Graph Neural Network. *2024 ACM/IEEE International Conference On Computer Aided Design (ICCAD)*, 1-9. https://doi.org/10.1145/3676536.3676772
 
Gong, W., Wang, Y., Zhang, M., Mihankhah, E., Chen, H., & Wang, D. W. (2022). A Fast Anomaly Diagnosis Approach Based on Modified CNN and Multisensor Data Fusion. *IEEE Transactions on Industrial Electronics, 69*, 13636-13646. https://doi.org/10.1109/tie.2021.3135520
 
Guo, Z., Liu, M., Gu, J., Zhang, S., Pan, D., & Lin, Y. (2022). A Timing Engine Inspired Graph Neural Network Model for Pre-Routing Slack Prediction. *2022 59th ACM/IEEE Design Automation Conference (DAC)*, 1207-1212. https://doi.org/10.1145/3489517.3530597
 
Kahng, A., & Spyrou, T. (2021). The OpenROAD Project: Unleashing Hardware Innovation.
 
Li, J., Hu, J., Wu, Y., & Yang, X. (2025). Pre-Routing Slack Prediction Based on Graph Attention Network. *Automation*. https://doi.org/10.3390/automation6020020
 
Lin, T.-Y., Goyal, P., Girshick, R. B., He, K., & Dollár, P. (2017). Focal Loss for Dense Object Detection. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 42*, 318-327. https://doi.org/10.1109/tpami.2018.2858826
 
Shrestha, P., Aversa, A., & Savidis, I. (2026). EDA-Schema-V2: A Multimodal Schema, Open Datasets, and Benchmarks for Machine Learning in Digital Physical Design. *ArXiv, abs/2605.06952*. https://doi.org/10.48550/arxiv.2605.06952
 
 ---------------

 ADDITIONAL SECTION I REQUESTED ON VLSI DOMAIN TERMINOLOGY EXPLAINED USING A SINGLE REVIEW PAPER

 # **VLSI** and Timing Terms

**VLSI physical design** refers to the stage of integrated-circuit implementation where the logical design is turned into a layout through **placement and routing (PnR)**, and this stage is driven by **performance, power, and area (PPA)** requirements  (Jenila & Member, 2025). **Physical Design Closure** means reaching an implementation that satisfies these layout-stage requirements well enough for the design flow to complete, which is why the review describes PnR as a complicated process and notes that traditional heuristic approaches can be time consuming as design complexity grows  (Jenila & Member, 2025).

**Static timing analysis (STA)** is the timing-checking step used during this physical-design process, so when the proposal mentions repeated STA iterations, it is referring to repeated timing verification while placement and routing are being optimized. The related phrase **setup timing violation** therefore means a path that fails the required timing target during these checks, while a **timing-clean path** is one that meets it; in your proposal, these paths are the objects to be screened early before expensive iterative optimization continues. The review does not define STA in detail, so this explanation should be kept at exactly this level and not expanded further beyond the PnR optimization context it covers  (Jenila & Member, 2025).
 
## References
 
Jenila, R., & Member, I. J. N. S. K. (2025). A Survey on Learning-Based PnR Optimization for VLSI Physical Design Automation. *IEEE Access, 13*, 195953-195974. https://doi.org/10.1109/access.2025.3631956
 

