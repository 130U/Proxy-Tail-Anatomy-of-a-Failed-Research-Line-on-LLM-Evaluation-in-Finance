# 130U-FinLLM | Short introduction (translated from the Chinese summary)

130U-FinLLM is a language-model project for personal financial research. It consists of a **2.4B version for personal use** and a **24M public Trial**. This repository presents the model architecture, training system and engineering review in English, and publishes the Trial's code, configurations, notebooks and experiment records.

The project starts from original financial views and human-reviewed text, and organizes supervision around the target, the opinion holder, the evidence scope and the conditions of a judgment. The two core designs are: financial semantic permissions, which distinguish which judgments should change with the semantics and which should stay the same; and objective-preserving scaling, which connects sample families, loss accounting, multi-GPU computation and recovery semantics.

The 24M version is used to run the complete training workflow end to end and to build reusable engineering experience; the 2.4B version is intended for personal research use. Each version manages its own vocabulary, weights and calibration parameters, and experiment results keep a clear version attribution.

[English README](../README.md) · [Project overview](PROJECT_OVERVIEW.md) · [Training system](TRAINING_SYSTEM.md) · [Run the Trial](TRIAL_GUIDE.md)
