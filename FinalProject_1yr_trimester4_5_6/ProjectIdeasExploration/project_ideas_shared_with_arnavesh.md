Track	VLSI Physical Design Problem Statement	Proposed ML Solution

RECOMMENDED
	
Routing Congestion Stability Flaw: Modern placement tools modify layouts iteratively. 
When engineers apply minor design changes (e.g., cell padding or tiny macro shifts), global routing demand changes insignificantly. 
However, conventional ML congestion proxies lack physical spatial constraints; they treat these minute, valid adjustments as high-frequency noise, leading to highly volatile predictions that miss critical routing hotspots.
	
Perturbation-Aware U-Net: Build a robust image-to-image proxy model utilizing an adversarial training framework. 
By dynamically injecting localized mathematical pixel perturbations (using algorithms like PGD) into input feature maps 
(e.g., RUDY routing demand) during training loops, the network is forced to learn stable physical layouts rather than memorizing volatile pixel boundaries.


OPTION-2
	
Decoupled Congestion & DRC Evaluation: Standard EDA suites execute global routing congestion estimation and detailed Design Rule Checking (DRC) spot-checks in separate, sequential software cycles. 
Running distinct ML models for each metric creates redundant compute pipelines and ignores the physical reality that global wire congestion hotspots directly trigger localized geometric DRC failures.
	
Unified Multi-Task Network: Design a single CNN architecture with a shared encoder that branches into parallel, distinct decoder heads. 
The shared backbone maps placement layout densities, while the split decoders concurrently output continuous global congestion estimates and local DRC violation probabilities, balancing the dual objectives with a joint loss function.


OPTION-3
(Hybrid CNN+Netlist)
	
Connectivity Blindness in Image Proxies: Traditional vision-based EDA models rasterize chip components into flat 2D spatial density grids to achieve fast proxy simulation. 
However, two layout windows can appear identical on an image grid while having radically different underlying circuit netlist connectivity graphs, blinding the CNN to actual routing path requirements and electrical current paths.
	
Cross-Modal Fusion Network: Implement a dual-branch framework that captures both geometry and topology. 
A spatial 2D CNN processes the placement grid images, while a Graph Neural Network (GNN) processes the logical netlist graph. 
The resulting structural graph embeddings are flattened and mathematically fused into the CNN layers before final estimation.

-----------------------

I have to do a 1 year project for my MTech AI/ML.
I am unfamiliar with VLSI domain and with CNN I have some knowledge but not expertise. 
So I have difficulty in judging feasability of AI suggested project ideas (these were suggested by Consensus AI).
But my project mentor has expertise in both AI/ML and VLSI/embedded.

Project Mentor Feedback when I shared these project ideas:

These problem statements are quite tough, since the images here are very dense so your problem statement becomes that much more complicated.
So they would require big networks and also increase training time and otherwise.
Which might become a bottleneck for you
Are there more options that are present ? where dense image characterization is not required ?
 