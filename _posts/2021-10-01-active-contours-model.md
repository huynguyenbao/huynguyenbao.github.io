<!-- ---
title: 'Active Contours Model'
date: 2021-10-01
permalink: /posts/2021/10/variational-methods/
tags:
  - Mathematics
  - Digital Signal Processing
---

One of applications of **variational methods** is used to compute segmentations of a given image $I: \Omega \rightarrow \mathbb{R}$ by evolving the contours in the directions of negative gradient, using partial derivative of energy function. This model is also known as **Active Contours Model** or **Snake**.

Assume that a curve $C$ is explicitly parametrized by $s$ which $C: \, \left[0, 1\right] \rightarrow \Omega$ or in other words, $C = (x(s), y(s))$ where $s \in \left[0, 1\right]$

The energy function can be defined:
$$E(C) = \int_0^1 E_{int}(C) + E_{ext}(C) \operatorname{d}s$$

*Note: This is line integral, parameterized by $s$.*

**Internal energy** penalizes the non - continuity and non - smoothness of a curve:

$$E_{int} (C) = \int_0^1 \alpha(s) \, ||C_s||^2 + \beta(s) \, ||C_{ss}||^2 \operatorname{d}s$$

**External energy** represents on . We wa -->