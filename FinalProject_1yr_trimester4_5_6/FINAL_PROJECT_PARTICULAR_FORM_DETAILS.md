<!-- Hope it doesn't run afoul of AI rule -- will ensure to rewrite abstract also in proposal after doing literature review

"Plagiarism and AI generated report will not be tolerated . AI can be used to improve grammar or sentence structures."
-->

### Project Title

Efficient VLSI Timing Violation Screening: An Anomaly Detection Approach Using Lightweight 1D-CNNs

### Project Abstract - A 150 words brief

In physical design closure, traditional Static Timing Analysis iterations consume significant compute resources and time. While deep learning surrogates can mitigate this, modern Graph Neural Network paradigms demand substantial computational budgets. This project proposes framing pre-routing, post-placement setup timing risk identification as an anomaly detection task to isolate rare timing violations from standard clean paths. We will develop a lightweight 1-Dimensional Convolutional Neural Network (1D-CNN) to process structured sequential timing paths—such as arrival times, slew, and capacitance—extracted from the open-source OpenROAD datasets. Rather than attempting full-graph slack regression, the model will serve as a low-compute sequential anomaly screener. To address severe class imbalance, we plan to optimise training with focal loss and evaluate performance using PR-AUC and F1-score. The goal is to establish an efficient baseline for detecting early hardware timing risks.

### Keywords: Domain, AI/ML models and Approach

Electronic Design Automation (EDA), Very Large Scale Integration (VLSI), Physical Design Closure, Static Timing Analysis (STA), 
1-Dimensional Convolutional Neural Networks (1D-CNN), Anomaly Detection

<!-- AI Explanation:

### Terminology Breakdown

Here is what all the technical terms mean, broken down by domain:

#### VLSI / EDA Domain

* **VLSI (Very Large Scale Integration):** The process of creating an integrated circuit (microchip) by combining millions or billions of transistors onto a single small chip.
* **EDA (Electronic Design Automation):** A category of software tools used to design, simulate, analyze, and manufacture electronic systems and microchips.
* **Physical Design Closure:** The phase in chip design where the physical layout of components is finalized, ensuring it meets all performance, power, and manufacturing constraints.
* **Static Timing Analysis (STA):** A method of validating the timing performance of a circuit by checking all possible paths for timing violations, without simulating the actual logical behavior of the chip.
* **Pre-routing, Post-placement:** A specific stage in chip design. "Placement" means the components (gates) have been positioned on the chip. "Routing" (wiring them together) has not yet occurred.
* **Setup Timing Risk / Violations:** A failure where a digital signal takes too long to travel through a pathway and fails to arrive before the clock ticks. If this happens, the chip fails to function correctly.
* **Arrival Time, Slew, Capacitance:**
* *Arrival Time:* The time it takes a signal to reach a specific point.
* *Slew:* The rate at which a digital signal transitions between 0 and 1 (the speed of the voltage change).
* *Capacitance:* The property of the circuit that resists changes in voltage, which naturally slows down signals.


* **OpenROAD:** An open-source, automated EDA toolchain used to take a chip design from a description language down to the physical layout files.

#### AI / ML Domain

* **Graph Neural Network (GNN):** A type of AI designed to process data structured as graphs (like social networks or chip circuit webs). They are powerful but require massive amounts of computer memory and processing power.
* **1-Dimensional Convolutional Neural Network (1D-CNN):** A highly efficient, lightweight AI model that scans sequential, one-dimensional data (like text sentences, audio waves, or a linear sequence of timing points) to find patterns.
* **Anomaly Detection:** A machine learning strategy focused on identifying rare items, events, or observations that raise suspicions by differing significantly from the majority of the data.
* **Focal Loss:** A mathematical strategy used during AI training that forces the model to focus heavily on hard-to-classify, rare examples (like timing violations) rather than getting lazy by only learning the common, easy examples.
* **Class Imbalance:** A data problem where one category vastly outnumbers the other (e.g., 99.9% of timing paths are perfectly fine, and only 0.1% are broken).
* **PR-AUC & F1-Score:** Specialized metrics used to judge AI accuracy when data is heavily imbalanced. They ensure the AI is actually good at catching the rare errors, rather than just guessing "everything is fine" to get a high generic accuracy score.

---

### The Project Explained in Layman's Terms

Imagine you are building a massive, hyper-complex highway system spanning a tiny area—a microchip. Before you open the highway, you have to ensure that cars (data signals) traveling along every single possible route can reach their destinations before the traffic lights turn red (the clock ticks).

Currently, engineers use massive software simulations (Static Timing Analysis) to check every single route. This takes an enormous amount of time and computing power. Recently, scientists tried using complex AI systems (Graph Neural Networks) to map the entire web of roads, but these AIs are so huge that running them is almost as slow and expensive as the original method.

**This project proposes a clever shortcut.**

Instead of mapping the entire complex web of roads all at once, the project treats a highway route simply as a straight line of connected checkpoints. It looks at basic metrics for each checkpoint: how long it took to get there, how fast the car is moving, and how much traffic resistance it faces.

Because 99% of the routes on a chip work perfectly fine, a timing failure is a rare "anomaly." The project will build a fast, incredibly lightweight AI (a 1D-CNN) that acts like a TSA pre-screener. It will rapidly scan these simple lines of data to spot the rare, suspicious routes that look like they might cause a traffic jam.

By using special training math (Focal Loss) to ensure the AI doesn't ignore the rare failures, this project aims to create a tool that catches design flaws early, saving chip companies massive amounts of time and computing electricity.
-->

<!--

AI suggested Actionable Checklists for the Next Steps

While the abstract is great, the document specifies that your Full Proposal and End Term Report will require strict structural elements. When you expand this abstract into the full proposal, make sure to include:

    The Core Literature Gap (for Term IV Phase 1): You mentioned GNNs are heavy. In your full proposal's literature review (which requires at least 10 papers), highlight why existing ML-for-EDA approaches fail to scale, setting up your 1D-CNN as the lean alternative.

    Resource Requirements (Slide 8): State clearly what compute resources you need. (e.g., "Training requires standard Python/PyTorch environments. Due to the lightweight nature of 1D-CNNs compared to GNNs, standard consumer-grade GPUs or high-end CPUs will suffice, minimizing resource constraints.")

    The Phase 3 Requirements: Keep in mind that by Term VI, you will have to perform an Ablation Study and Error Analysis. (e.g., testing how the model performs without Focal Loss to prove it was necessary).

-->

### Immediate Supervisor

**Name**: Arnavesh Varun Giri
**Contact Details**: arnaveshvarun.giri@hcltech.com

### Mentor Details

**Name**: Arnavesh Varun Giri
**Email**: arnaveshvarun.giri@hcltech.com
**Phone Number**: (+91) 99995 35117
**Company**: HCL Technologies
**Experience (years) in problem domain**: 5
**Experience (years) in AI/ML field**: 5
**Linkedin Profile**: https://www.linkedin.com/in/arnavesh/
**CV Details**: (not filled, either one of linkedin profile or CV of mentor was required)
**Is mentor ready to attend viva?** Yes

<!-- Have filled this in IIT Project Proposal Form at https://samsai.io/ -->