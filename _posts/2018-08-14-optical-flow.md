---
title: 'Optical Flow'
date: 2018-08-14
permalink: /posts/2018/08/optical-flow/
tags:
  - Image Processing
---

Optical flow is the pattern of appearance objects motion in image, between two successive frames caused by the movement of objects or camera. It is a 2D vector field, where each vector represents a displacement or movement of feature from first frame to second frame.

![alt text](/figure/definition.png "Title")

Our problem:

Given 2 successive frame $I_1$ and $I_2$, find the motion vector $(dx, dy)$ for each pixel.

To solve this problem, [Horn & Schunck](https://www.caam.rice.edu/~zhang/caam699/opt-flow/horn81.pdf) had made some assumptions:

1. Images are captured in ambient light: This means that the intensity of pixels do not depend on position of the camera.

2. Spatial Motion: Pixels do not move fast.

3. Spatial Correlation: All neighbors of one pixel also move same motion.

After having some assumptions, we can solve this easily.

The first assumption let we have: $I(x, y, t) = I(x + dx, y + dy, t + dt)$

The second assumption means that: $dx$, $dy$, $dt$ are very small, so that we can approximate $I(x + dx, y + dy, t + dt)$ with the first order of Taylor series:

$I(x + dx, y + dy, t + dt) \approx I(x, y, t) + \nabla I_x dx + \nabla I_y dy + \nabla I_t dt.$

Because of 2 successive frames, that mean $dt = 1$, then we have:

$I(x, y, t) = I(x + dx, y + dy, t + dt) \approx I(x, y, t) + \nabla I_x dx + \nabla I_y dy + \nabla I_t.$

$\rightarrow \nabla I_x dx + \nabla I_y dy + \nabla I_t \approx 0.$ (1)

Where $\nabla I_x$, $\nabla I_y$, $\nabla I_t$ are gradient of image respect to x-axis, y-axis, and time.

$\nabla I_x (x, y)= I_t (x + 1, y) - I_t (x - 1, y)$.

$\nabla I_y (x, y)= I_t (x, y + 1) - I_t (x, y - 1)$.

$\nabla I_t (x, y)= I_{t + 1} (x, y) - I_t(x, y)$.

To find $dx$, $dy$ in equation (1), we need at least 2 equations, and the assumption will help us that.

In third assumption, all neighbor of pixel will have the same motion. So that, we can assumpe that $3\times3$ region around pixel will have the same motion. We have 9 equations, so that we can solve equation (1).

$$\left[\begin{array}{cc}
    I_{x1} & I_{y1} \\
    I_{x2} & I_{y2} \\
     ...   &   ...  \\
    I_{x9} & I_{y9} \\
\end{array}\right]

\left[\begin{array}{c}
    dx \\
    dy \\
\end{array}\right] =

\left[\begin{array}{cc}
    -I_{t1} \\
    -I_{t2} \\
    ...     \\
    -I_{tn}
\end{array}\right]
$$

$$Ax = b$$

There ara a lot of methods used to solve this equation: Close form, Pseudo Inverse, [Least squares](https://en.wikipedia.org/wiki/Least_squares), [Gaussian elimination](https://en.wikipedia.org/wiki/Gaussian_elimination), [Jacobi method](https://en.wikipedia.org/wiki/Jacobi_method) and [Gauss–Seidel method](https://en.wikipedia.org/wiki/Gauss%E2%80%93Seidel_method#:~:text=In%20numerical%20linear%20algebra%2C%20the,a%20system%20of%20linear%20equations.). Or even, you can utilize [SVD](https://www.youtube.com/watch?v=PjeOmOz9jSY) to solve.
