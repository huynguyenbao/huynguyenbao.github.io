---
title: 'Fourier Series Part 1'
date: 2020-09-01
permalink: /posts/2020/09/fourier-series-1/
tags:
  - Mathematics
  - Digital Signal Processing
---

Many students are told that Fourier Transformation are applied almost in everywhere, ranging from digital signal processing to circuit designing, however they found it quite challenging to comprehend the Fourier series and Fourier Transformation since the equations appearing in the methods all involve complex exponential and integral. However, if we break them down into small pieces to deal with, the comprehension would not be impossible. This blog will partly help you to do this. The content of its mainly will cover the mathematical theory of Fourier series and in the next blog, the Fourier transformation will be presented.

## Euler's formula

Before jumping into the Fourier series, let's have a look at Euler's formula:

$$e^{ix} = \cos x + \sin x$$

Do you know why? If not, I recommend that you should prove the equation by yourself before reading next. The proof is quite straightforward and my hint is: *Taylor series*. (You can see the proof on [this](https://en.wikipedia.org/wiki/Euler%27s_formula)).

## Fourier series

Regarding Fourier series, its'idea is pretty similar to that of Taylor series: both of them are used to approximate a complex function by a combination of other functions. In the Taylor series, an arbitrary function $f(.)$ is an infinite sum of its derivatives, while this function is represented by a sum of periodic functions (sine and cosine waves).

The Fourier series form is:

$$\begin{equation}
  f(t) = \sum_{m=0}^{\infty}a_m \, \cos \left( \dfrac{2\pi\,m\,t}{T}\right) + \sum_{n=1}^{\infty}b_n\, \sin \left(\dfrac{2\pi \, n \, t}{T}\right)
\end{equation}$$ 

where $T$ is the period of $f(t)$, and $a_m$, $b_n$ in turn are the magnitudes of periodic function cosines and sines, which determine the relative weight for each of sinusoids. **These weights are things we need to find** when we want to decompose $f(t)$.

In addition, likewise the Taylor series, the more sinusoids we use to describe the $f(t)$, the more description is true (Figure).

Before we go to the next parts, let me ask you some questions:

*Small questions:*

1. Do you know why the $n$ starts from $1$, while $m$ is from $0$?
2. Why both $n$ and $m$ variables in two sum terms set of from no negative points but not $-\infty$?
3. This analysis is for $f(t)$ having period $T$, but what's about the function not having period?

The answers are at the end of the blog.

However, the most common Fourier form is not the equation $(1)$ but actually:

$$\begin{equation}
  f(t) = \sum_{n=-\infty}^{+\infty} c_n \, \exp\{i \, \dfrac{2\pi\,n\,t}{T}\}
\end{equation}$$

*Small question:*

4. Can you prove that both equation $(1)$ and $(2)$ are equal?

The coefficients $c_n$ in equation $(2)$ are found by:

$$\begin{equation}
  c_n = \dfrac{1}{T}\int_0^T f(t) \exp\{-i \, \dfrac{2\pi\,n\,t}{T}\}
\end{equation}
$$

To familiarize yourself with both equations $(2)$ and $(3)$, let's do this small problem:

5. Decompose this square wave to a sum of sinusoids.

$$\begin{equation}
  f =
  \begin{cases}
    1 & \text{if $t \in [0, 10]$} \\
    -1 & \text{if $t \in [-10, 0]$}
  \end{cases}
\end{equation}$$

## Proof

How do we know the equation $(3)$ is true? Let's prove.

**Assume** that the Fourier series $g(t)$ does in fact **converge** to the original periodic function $f(t)$.

$$\begin{equation}
  f(t) = g(t) = \sum_{n=-\infty}^{+\infty} c_n \, \exp\{i \, \dfrac{2\pi\,n\,t}{T}\}
\end{equation}$$

We multiply both sides of the above equation with $\exp\{-i\,\dfrac{2\pi\,m\,t}{T}\}.$

$$\begin{equation}
\begin{aligned}
   f(t) \exp\{-i\,\dfrac{2\pi\,m\,t}{T}\} &= \exp\{-i\,\dfrac{2\pi\,m\,t}{T}\} \sum_{n=-\infty}^{+\infty} c_n \, \exp\{i \, \dfrac{2\pi\,n\,t}{T}\} \\
   &= \sum_{n=-\infty}^{+\infty} c_n \, \exp\{i \, \dfrac{2\pi\,(n - m)\,t}{T}\}
\end{aligned}
\end{equation}$$

Next, integrating both sides with respect to $t$ from $[0, T]$.

$$\begin{equation}
\begin{aligned}
   \int_0^T f(t) \exp\{-i\,\dfrac{2\pi\,m\,t}{T}\} \, dt &= \int_0^T \sum_{n=-\infty}^{+\infty} c_n \, \exp\{i \, \dfrac{2\pi\,(n - m)\,t}{T}\} \, dt \\
    &= \sum_{n=-\infty}^{+\infty} c_n \int_0^T \, \exp\{i \, \dfrac{2\pi\,(n - m)\,t}{T}\} \, dt \\
\end{aligned}
\end{equation}$$

Having a look at:

$$\begin{equation}
   \int_0^T \, \exp\{i \, \dfrac{2\pi\,(n - m)\,t}{T}\} \, dt =
  \begin{cases}
    0 & \text{if $n \neq m$} \\
    1 & \text{if $n = m$}
  \end{cases}
\end{equation}$$

So:

$$\begin{equation}
    \sum_{n=-\infty}^{+\infty} c_n \int_0^T \, \exp\{i \, \dfrac{2\pi\,(n - m)\,t}{T}\} \, dt  = c_m \, T
\end{equation}$$

only once $m = n$

With both equation $(6)$ and $(9)$, we get:

$$\int_0^T f(t) \exp\{-i\,\dfrac{2\pi\,m\,t}{T}\} \, dt = c_m \, T$$

$$\rightarrow c_m = \dfrac{1}{T}\int_0^T f(t) \exp\{-i\,\dfrac{2\pi\,m\,t}{T}\} \, dt$$

## Answers

1. Because when $n = 0$, $\sin(\dfrac{2\pi \, n \, t}{T}) = 0$

2. Because $\cos (.)$ and $\sin (.)$ are periodic functions ($\cos(x) = \cos(-x)$ and $\sin(x) = -\sin(x)$), we can combine the negative with positive by changing the magnitudes $a_m$ and $b_n$.
  
3. If $f(t)$ does not have period (is not a periodic function), we can assume that its period is infinity.

4. Let's have a look at:

$$\begin{aligned}
  \cos (x + \phi) &= \dfrac{1}{2} [\cos(x + \phi) + i \, \sin(x + \phi)] + \dfrac{1}{2}[\cos(x + \phi) - i \, \sin(x + \phi)]\\
                  &= \dfrac{1}{2}e^{i\,\phi} \, e^{ix} + \dfrac{1}{2}e^{-i\,\phi} \, e^{-i\,x}
\end{aligned}$$

So with the above equation, we now can convert from equation $(1)$ to $(2)$ and vice versa.


