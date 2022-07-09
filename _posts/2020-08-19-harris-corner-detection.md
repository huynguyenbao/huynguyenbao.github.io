---
title: 'Harris Corner Detection'
date: 2020-08-19
permalink: /posts/2020/08/blog-post-2/
tags:
  - Image Processing
---

**A Corner** is a point whose local neighborhood stands in two dominant and different edge directions. In other words, a corner can be interpreted as the junction of two edges, where an edge is a sudden change in image brightness. Corners are the important features in the image, and they are generally termed as interest points which are invariant to translation, rotation and illumination.

**The Harris corner detector** use geometry property of corner to detect it. As you see in the first image in figure 2, content of green window does not change when we shift the window in all direction. In the second, when the window lies on edge, its content does not change along edge direction, only change when shifting in other directions. Finally, is the case window lies on corner, the content of window varies when we shifts it in **all directions**. So that, we will find the corner region by placing a window in that place, if window content varies strongly in all directions, that region is corner. The defination **window content varies strongly** is measured by sum of square distance (SSD).

<p align="center">
    <img width="400"  src="figure/corner.png"/>
    <br>
    <i>Figure 2: Intuition of Harris Corner Detector</i>
</p>

The variation can be defined as a sum of square-distance (SSD) as below, $(u, v)$ denotes the shift vector, $W$ is region needed to determine , $w(x,y)$ is a window function, $I(x,y)$ is image function, at coordinate $(x, y)$ image has a certain intensity. The windown function usually chosen is a rectangle or gaussian function.

$$ E(u, v) \approx \sum_{(x, y) \, \in \,W} w(x, y) \, [\,I(x + u, y+ v) - I(x, y)\,] \,^ {2} $$

**The energy function value of $E(u, v)$ in region $W$ should be large for any shift.**

The shifted intensity can be approximated by Taylor expansion:

$$ I (x + u, y + v) \approx I(x, y) + u\,I_{x} (x,y) + v\,I_{y} (x,y) + R_{2}$$

Therefore, the SSD measure is now:

$$ \begin{aligned}
E(u, v) & \approx \sum_{(x, y)\, \in \,W} w(x, y)\,[\,u\,I_{x} (x,y) + v\,I_{y} (x,y)\,]\,^{2} \\
& = \sum_{(x, y)\, \in \,W} w(x, y)\, [u \quad v] 
\left[\begin{array}{cc}
    I_{x}^{\,2}&I_{x}\,I_{y}\\
    I_{x}\,I_{y}&I_{y}^{\,2}
\end{array}\right] 
\left[\begin{array}{c}
    u\\v
\end{array}\right]\\
& =  [u \quad v] \Biggl ( \sum_{(x, y)\, \in \,W} w(x, y)\,
\left[\begin{array}{cc}
    I_{x}^{\,2}&I_{x}\,I_{y}\\
    I_{x}\,I_{y}&I_{y}^{\,2}
\end{array}\right] \Biggr)
\left[\begin{array}{c}
    u\\v
\end{array}\right]\\
    & = \mathbf{u^{T}} \, M \, \mathbf{u}.
\end{aligned}$$

Because $M$ is a real and symmetric matrix, it can be decomposed to be:

$$ M = Q \, \Lambda \, Q^{T}. $$

where $Q$ is orthogonal matrix and $\Lambda$ is diagonal matrix. So the SSD measure can be written again:

$$ \begin{aligned}
    E(\mathbf{u}) & = \mathbf{u^{T}} \, M \, \mathbf{u} = \mathbf{u^{T}} \, Q \, \Lambda \, Q^{T} \, \mathbf{u} = (Q^{\mathbf{T}} \, \mathbf{u})^{\mathbf{T} } \, \Lambda \, (Q^{\mathbf{T}} \, \mathbf{u}) \\
                & = \mathbf{u'^{T}} \, \Lambda \, \mathbf{u'} = \lambda_1 \, ||\mathbf{u'}||_2^{2} + \lambda_2 \, ||\mathbf{u'}||_2^{2}.
\end{aligned} $$

where $\lambda_1$ and $\lambda_2$ is eigen values of $M$. We want $E(\mathbf{u})$ to be big for all directions $\mathbf{u}$ so both $\lambda_1$ and $\lambda_2$ must be large. If both are small, it will be "flat". For "edge", one large eigen value and one small eigen value.

The Harris detector specially designed a response:

$$\begin{aligned}
    R & = det(M) - k \, trace(M)^{2} \\
      & = \lambda_1 \lambda_2 - k \, (\lambda_1 +\lambda_2)^{2}.
\end{aligned}$$

The paramater k is usually set to 0.04 - 0.06. If $R$ is large, it is corner. Otherwise negative $R$, it'll be edge; positive $R$ but small, the flat region.

<!-- <p align = "center">
    <img width="300"  src="figure/harris_region.jpg"/>
    <br>
    <i>Figure 3: Harris Region</i>
</p>
 -->

<p align = "center">
    <img width="500"  src="figure/R_value.png"/>
    <br>
    <i>Figure 3: Harris Region</i>
</p>

Instead, Shi-Tomasi proposed the scoring function as:

$$R = min (\lambda_ 1, \lambda_2)$$
which basically means if $R$ is greater than a threshold, it is classified as a corner.

<p align = "center">
    <img width="400"  src="figure/shitomasi_space.png"/>
    <br>
    <i>Figure 4: Shi-Tomashi Region</i>
</p>

Final, applying non-max suppression.
