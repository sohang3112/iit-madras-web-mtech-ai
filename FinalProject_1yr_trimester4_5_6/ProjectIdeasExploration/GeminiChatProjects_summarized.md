Here is a brief summary of the project options tailored for your mentor's VLSI and AI/ML expertise, strictly ordered by problem statement, proposed ML solution, and exact public datasets:

### Option 1: Hardware-Aware Neural Architecture Search (HW-NAS)

* **VLSI Domain Problem:** Manually optimizing and pruning deep neural network layers to fit the rigid hardware constraints (RAM/MACC limits) of target edge microcontrollers is slow and highly inefficient.


* **Proposed ML Solution:** An automated Reinforcement Learning (RL) or evolutionary algorithm framework that searches for the optimal neural network architecture alongside a layer-wise mixed-precision quantization policy.


* **Feasible Public Datasets:** *NAS-Bench-201*, *HW-NAS-Bench* (pre-computed hardware metrics mapping architectures to edge devices), *ImageNet-mini*, *PlantVillage*, or *Food-101*.



### Option 2: Machine Learning-Driven Routing Congestion Prediction

* **VLSI Domain Problem:** Physical design placement and routing take massive compute times in traditional Electronic Design Automation (EDA) loops before layout hot spots are identified.


* **Proposed ML Solution:** An Image-to-Image translation framework using Fully Convolutional Networks (FCN) or U-Nets to predict routing congestion heatmaps directly from early macro placement spatial grids, bypassing slow routing simulations.


* **Feasible Public Datasets:** *CircuitNet* (specifically *CircuitNet-N14/N28/N45*, containing over 10,000 layout samples from open-source RISC-V designs) and *ISPD 2015 / 2024 Placement Benchmarks*.



### Option 3: Cross-Device Knowledge Distillation (KD) for Edge Accelerators

* **VLSI Domain Problem:** Deploying massive, high-accuracy vision or multimodal models onto heterogeneous edge hardware topologies requires highly customized, lightweight student architectures that fit the physical device.


* **Proposed ML Solution:** A systematic optimization framework evaluating multi-teacher and progressive feature-based Knowledge Distillation techniques, using custom loss functions (KL divergence) to transfer logic from heavy cloud models to edge-friendly student variants.


* **Feasible Public Datasets:** *MS-COCO* (Full or Person subset), *Pascal VOC*, and the *MobileNet baseline zoos*.

--------------

Gemini suggested project ideas -- not yet shared with project mentor.