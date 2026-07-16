# Use **CircuitNet 2.0** now, and a **CNN-based** project on congestion, DRC, or IR-drop is very feasible.

For a 1-year MTech project, the clearest sub-questions are **which CircuitNet version to use**, **whether CNNs fit the data**, and **which future-work-style topics are still open**. CircuitNet was created to support ML for back-end VLSI cross-stage prediction, with over 10K public samples and both graph-like netlists and image-like layout features, which makes it a strong project base  (Chai et al., 2023; Chai et al., 2022).

## Dataset Choice

CircuitNet **2.0 is the safer thesis dataset** because the CircuitNet family already has broad benchmarking use, while your evidence for “3.0” does not yet contain a usable technical paper with EDA dataset details or downstream benchmarks  (Chai et al., 2023; Li et al., 2024). The current public CircuitNet line already supports congestion, DRC, and IR-drop tasks with reproducible baselines, which matters more for a 1-year academic project than being on the newest release label  (Chai et al., 2022).

- Use **CircuitNet-N28 first** because it has complete support for RC and DRC and a stated train/test split  (Li et al., 2024).
- Prefer **2.0-era benchmarks** because transferability and data imbalance are already identified challenges there, giving you a literature-backed problem statement  (Chai et al., 2023).
- Treat **CircuitNet 3.0 as optional extension** only if you can verify task definitions and format compatibility from its official docs, because the supplied evidence does not yet ground its research maturity.

## CNN Feasibility

Yes, **CNNs fit CircuitNet very naturally** because the layout is commonly tiled into 2D feature maps, and many strong baselines already cast congestion, DRC, and IR-drop as image-to-image prediction  (Chai et al., 2022; Li et al., 2024). Fully convolutional and U-Net-style models are already standard starting points, and several newer papers still improve them with residual blocks, attention, inception modules, or transformers rather than abandoning CNNs entirely  (Chai et al., 2022; Chen & Liu, 2025; Li et al., 2024; Gu et al., 2025).

- A **plain CNN/U-Net baseline** is academically acceptable because it matches established CircuitNet benchmarking practice  (Chai et al., 2022; Li et al., 2024).
- CNNs are strongest when using **image-like placement features**, such as RUDY, PinRUDY, macro region, density, and congestion-related maps  (Li et al., 2024; Holtz et al., 2024).
- The main CNN limitation is **missing netlist topology**, which is why graph or hybrid CNN+GNN models often outperform pure image models  (Wang et al., 2022; Gu et al., 2025)## Evidence Coverage Across CircuitNet Topics

| Sub-Topic | **CNN baselines** | **Graph/topology** | **Multi-task** | **Robustness** | **Design-loop integration** |
|---|---|---|---|---|---|
| Congestion prediction | **10** | **5** | **2** | **2** | **4** |
| DRC prediction | **6** | **1** | **2** | **GAP** | **1** |
| IR-drop prediction | **4** | **GAP** | **1** | **GAP** | **1** |
| Transfer/generalization | **2** | **2** | **GAP** | **1** | **1** |
| Robustness/adversarial | **1** | **1** | **GAP** | **1** | **GAP** |

**Figure 1:** Evidence coverage across CircuitNet project directions

The most obvious gap is **robustness and generalization**, not raw congestion accuracy. CircuitNet 2023 explicitly identifies model transferability as a practical challenge and reports gains from knowledge-distillation transfer learning, while a 2024 robustness study shows both CNN and GNN congestion predictors can fail under imperceptible perturbations and improve with adversarial training  (Chai et al., 2023; Holtz et al., 2024). A second gap is **joint modeling across related tasks**: recent work argues congestion and DRC are correlated, yet most earlier models were task-specific, leaving room for one unified CNN or CNN+Transformer project  (Chen & Liu, 2025; Zuo et al., 2025).

## Project Ideas

A good MTech project should be **incremental but publishable**, with a solid baseline and one clear novelty. The strongest ideas from this literature are the ones that improve transferability, robustness, or joint prediction rather than chasing the very latest architecture  (Chai et al., 2023; Holtz et al., 2024).

- **Project 1: Multi-task CNN for congestion + DRC.** Build a shared U-Net with task-specific heads, following the motivation that existing work often ignores cross-task correlation  (Chen & Liu, 2025).
- **Project 2: Robust CNN for congestion prediction.** Start from FCN/U-Net and add adversarial or perturbation-aware training, because current predictors are vulnerable to small valid layout perturbations  (Holtz et al., 2024).
- **Project 3: Hybrid CNN + netlist branch.** Combine image tiles with graph-derived features, since CNNs capture geometry well but miss topological connections  (Li et al., 2024; Gu et al., 2025; Wang et al., 2022).

For a safer execution path, the best single recommendation is: **use CircuitNet 2.0 / N28, build a CNN or U-Net baseline, and add one novelty in multi-task learning, robustness, or hybrid fusion**. That answers your main question directly: yes, you can absolutely use CNNs, and the most thesis-friendly open problems are the ones after baseline accuracy.
 
_These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at https://consensus.app. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent._
 
## References
 
Chai, Z., Zhao, Y., Liu, W., Lin, Y., Wang, R., & Huang, R. (2023). CircuitNet: An Open-Source Dataset for Machine Learning in VLSI CAD Applications With Improved Domain-Specific Evaluation Metric and Learning Strategies. *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, 42*, 5034-5047. https://doi.org/10.1109/tcad.2023.3287970
 
Chai, Z., Zhao, Y., Lin, Y., Liu, W., Wang, R., & Huang, R. (2022). CircuitNet: an open-source dataset for machine learning applications in electronic design automation (EDA). *Science China Information Sciences, 65*. https://doi.org/10.1007/s11432-022-3571-8
 
Chen, J., & Liu, G. (2025). Multi-Task Learning for Routability Prediction. *2025 IEEE 5th International Conference on Software Engineering and Artificial Intelligence (SEAI)*, 1-5. https://doi.org/10.1109/seai65851.2025.11108727
 
Gu, H., Wang, Y., Zheng, X., Peng, K., Zhu, Z., Chen, J., & Yang, J. (2025). Dual Multimodal Fusions With Convolution and Transformer Layers for VLSI Congestion Prediction. *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, 44*, 2378-2391. https://doi.org/10.1109/tcad.2024.3522199
 
Holtz, C., Wang, Y., Cheng, C.-K., & Lin, B. (2024). On Robustness and Generalization of ML-Based Congestion Predictors to Valid and Imperceptible Perturbations. *ArXiv, abs/2403.00103*. https://doi.org/10.48550/arxiv.2403.00103
 
Li, H., Huo, Y., Wang, Y., Yang, X., Hao, M., & Wang, X. (2024). A Lightweight Inception Boosted U-Net Neural Network for Routability Prediction. *2024 2nd International Symposium of Electronics Design Automation (ISEDA)*, 648-653. https://doi.org/10.1109/iseda62518.2024.10617987
 
Wang, B.-L., Shen, G., Li, D., Hao, J., Liu, W., Huang, Y., Wu, H., Lin, Y., Chen, G., & Heng, P. (2022). LHNN: Lattice Hypergraph Neural Network for VLSI Congestion Prediction. *2022 59th ACM/IEEE Design Automation Conference (DAC)*, 1297-1302. https://doi.org/10.1145/3489517.3530675
 
Zuo, Y., Li, P., Sun, Y., Yan, H., & Shi, L. (2025). Enhanced TransUNet Framework for Predicting Static IR Drop and Chip Routability. *ACM Transactions on Design Automation of Electronic Systems, 31*, 1 - 26. https://doi.org/10.1145/3750726
 
