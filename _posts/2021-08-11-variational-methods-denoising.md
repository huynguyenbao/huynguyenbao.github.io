---
title: 'Variational Methods and Image Denoising'
date: 2021-08-11
permalink: /posts/2021/08/variational-methods/
tags:
  - Mathematics
  - Digital Signal Processing
---

Variational methods are really powerful which has a variety of applications such as 2D segmentation and 3D reconstruction. However, today I will present to you one of their interesting applications: Image Denoising.

Nowadays, the popularity and the adaptability power of CNNs are making engineers become depend on more dataset with human labeled ground truth, and the designing of CNNs like playing Lego, adding blocks, feeding an random input and anticipating a desire output. But have you imagined how "our ancestors" can remove noise in image without ground-truth? If you do, let's dive into mathematics :).


## Formulation

Let $f: \Omega \rightarrow \mathbb{R}$ be a gray scaled image on a domain $\Omega \in \mathbb{R}^2$. Assume that we observed a noisy image $u$ and want to recover to free-noise image $f$. However, we do not know noise sources (white noise or poison), additive noise or multiplicate noise but only one noisy image $u$. To solve this inverse problem, we can have two assumptions based on our observation:

* The structure of $f$ should be *similar as possible* to that of $u$.
* $f$ should be *spatially smooth*.

With two above assumptions we can derive an energy function to find $f$:

$$\begin{aligned}
  E(f, u) &= E_{structure}(f, u) + E_{smoothness}(f) \\
\end{aligned}$$

The similarity of two images $f$ and $u$ is computed by:

$$E_{structure}(f, u) = \dfrac{1}{2}\int_{\Omega} (f - u)^2 \text{d}x\,\text{d}y$$

while the smoothness can be evaluated:

$$E_{smoothness}(f) = \dfrac{1}{2}\int_{\Omega} ||\nabla f||^2 \text{d}x \, \text{d}y$$

where $\nabla f = <\partial f/\partial x, \partial f/ \partial y>$.

The optimal $f$ is:

$$\begin{aligned}
  \underset{f}{\operatorname{arg\,min}} \, E(f, u) &= \dfrac{1}{2}\int_{\Omega} (f - u)^2 + \lambda ||\nabla f||^2 \, \text{d}x\,\text{d}y \\
  &= \dfrac{1}{2}\int_{\Omega} (f - u)^2 + \lambda (f_x^2 + f_y^2) \, \text{d}x\,\text{d}y
\end{aligned}$$

where $\lambda$ is weighted number.

## Solution

What we need to find right now is not finite number of parameters but actually the **function $f$** and how we minimize energy function $E$ where $f$ is an argument?

According to Euler - Lagrange equation, the optimal function $f$ must hold the necessary condition. The energy function can be written in the form:

$$E(f, u) = \int_{\Omega}L(f, f_x, f_y,u) \, \text{d}x \, \text{d}y$$

And the necessary condition is:

$$\dfrac{dE}{df} = \dfrac{\partial L}{\partial f} - \dfrac{\partial}{\partial x}\left(\dfrac{\partial L}{\partial f_x}\right) - \dfrac{\partial}{\partial y}\left(\dfrac{\partial L}{\partial f_y}\right) = 0$$

In fact, this necessary condition does not guarantee that the solution is global optimum but only local optimum. However, as least, with a random initialization and gradient decent method, we still can find a solution that is acceptable.

Continue to expand the above equation to get:

$$\begin{aligned}
  \dfrac{dE}{df} &= \dfrac{\partial L}{\partial f} - \dfrac{\partial}{\partial x}\left(\dfrac{\partial L}{\partial f_x}\right) - \dfrac{\partial}{\partial y}\left(\dfrac{\partial L}{\partial f_y}\right) \\
  &= (f - u) - \lambda \dfrac{\partial}{\partial x}f_x - \lambda \dfrac{\partial}{\partial y}f_y \\
  &= (f - u) - \lambda(f_{xx} + f_{yy})
\end{aligned}$$

### Algorithm

The main algorithm is:

* Step 1:
  
  Initialize the first function $f_0$

* Step 2:
  
$$\begin{aligned}
  f_{t+1} &= f_t - \alpha \, \dfrac{dE}{df} \\
          &= f_t - \alpha \, ((f - u) - \lambda (f_{xx} + f_{yy}))
\end{aligned}$$

* Step 3:
  
  If $E(f_{t + 1}, u) < \text{threshold}$, stop the algorithm.

### Code

```py
def denoise(noisy_image, n_iters, weight, step):
    noisy_image = np.copy(noisy_image).astype(np.float32)
    denoised_image = np.copy(noisy_image)
    ddepth = cv2.CV_32F

    kernel_x = np.array([
        [0, 0, 0],
        [-0.5, 0, 0.5],
        [0, 0, 0]
    ])
    kernel_y = np.array([
        [0, -0.5, 0],
        [0, 0, 0],
        [0, 0.5, 0]
    ])
    for _ in range(n_iters):
        grad_x = cv2.filter2D(denoised_image, ddepth, kernel_x)
        grad_y = cv2.filter2D(denoised_image, ddepth, kernel_y)

        grad_xx = cv2.filter2D(grad_x, ddepth, kernel_x)
        grad_yy= cv2.filter2D(grad_y, ddepth, kernel_y)

        grad = (denoised_image - noisy_image) - weight * (grad_xx + grad_yy)
        denoised_image = np.clip(denoised_image - step * grad, 0, 255)

    return denoised_image
```

### Result

<p align = "center">
    <img width="300"  src="/figure/variational_methods_denoising/noisy.jpg"/>
    <br>
    <i>Noisy Image</i>
</p>

<p align = "center">
    <img width="300"  src="/figure/variational_methods_denoising/denoised.jpg"/>
    <br>
    <i>Denoised Image</i>
</p>

## Discussion

In term of smoothness energy, there are several other options and one of them is total variation ($L_1$ norm) [[1]](#1) which is:

$$E_{smoothness}(f) = \int_\Omega ||\nabla f|| \, \text{d}x \, \text{d}y = \int_\Omega \sqrt{f_x^2 + f_y^2} \, \text{d}x \, \text{d}y$$

and:

$$\begin{aligned}
  \dfrac{dE}{df} &= \dfrac{\partial L}{\partial f} - \dfrac{\partial}{\partial x}\left(\dfrac{\partial L}{\partial f_x}\right) - \dfrac{\partial}{\partial y}\left(\dfrac{\partial L}{\partial f_y}\right) \\
  &= (f - u) - \lambda \dfrac{\partial}{\partial x}\left(\dfrac{f_x}{\sqrt{f_x^2 + f_y^2}}\right) - \lambda \dfrac{\partial}{\partial y}\left(\dfrac{f_y}{\sqrt{f_x^2 + f_y^2}}\right) \\
  &= (f - u) - \lambda \operatorname{div}\left(\dfrac{\nabla f}{||\nabla f||}\right)
\end{aligned}$$

## Reference

<a id="1">[1]</a>
Rudin, L. I.; Osher, S.; Fatemi, E. (1992). "Nonlinear total variation based noise removal algorithms". Physica D. 60 (1–4): 259–268