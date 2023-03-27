---
title: 'Bayesian Occams Razor'
date: 2023-03-20
permalink: /posts/2023/03/20/bayesian-occams-razor/
tags:
  - Bayesian Inference
---

In the 14th century, an English philosopher and theologian, named Willam of Ockham, stated that "Entia non sunt multiplicanda praeter necessitatem", which translates as <span style="color:red"> Entities must not be multiplied beyond necessity </span>. This principle is also known as **Occam's razor**. If there are multiple hypotheses compatible with an observed dataset, Occam's razor then advises us to choose the simplest. Although the conclusion seems hasty, it can be explained and understood as **a consequence of Bayesian inference**, a method of updating beliefs based on evidence.

## Bayesian Inference

According to [Wikipedia](https://en.wikipedia.org/wiki/Bayesian_inference), Bayesian inference is a method of statistical inference in which Bayes' theorem is used to update the probability for a hypothesis as more evidence or information becomes available. Let $\mathcal{H}$ stand as the considered hypothesis and $\mathcal{D}$ be the observed evidence. The probability that evidence $\mathcal{D}$ happens under the hypothesis $\mathcal{H}$ is denoted as $P(\mathcal{D} \mid \mathcal{H})$, which is also called likelihood. $P(\mathcal{D})$ is called evidence which measures how probable $\mathcal{D}$ is, while the prior $P(\mathcal{H})$ evaluates our initial belief that $H$ happens before $\mathcal{D}$. The posterior $P(\mathcal{H}\mid\mathcal{D})$ computes our belief in hypothesis $\mathcal{H}$ after evidence $\mathcal{D}$ happens. Bayes' theorem states that:

$$\begin{equation}
    \begin{split}
        P(\mathcal{H}\mid\mathcal{D}) &= \frac{P(\mathcal{D}\mid\mathcal{H})\times P(\mathcal{H})}{P(\mathcal{D})} \\
        \text{posterior} &= \frac{\text{likelihood}\times \text{prior}}{\text{evidence}} \\
    \end{split}
\end{equation}$$

This equation, although simple, is an extremely useful tool for us to evaluate the plausibility of the believed hypothesis after many observations of the evidence, helping us decide between keeping or replacing the hypothesis. Bayesian inference is found in a great variety of applications including science, engineering, medicine, law, and economics.

## Occam’s razor and Model comparison

Assume that there are hypotheses two $\mathcal{H}_1$ and $\mathcal{H}_2$ compatible with the same observed dataset $\mathcal{D}$. To understand why Occam's razor advises us to choose the simpler hypothesis, we use Bayes' theorem to compare their possibilities over the evidence:

$$\begin{equation}
    \frac{P(\mathcal{H}_1 \mid \mathcal{D})}{P(\mathcal{H}_2 \mid \mathcal{D})} = \frac{P(\mathcal{H}_1)}{P(\mathcal{H}_2)} \frac{P(D \mid \mathcal{H}_1)}{P(D \mid \mathcal{H}_2)}.
\end{equation}$$

The first ratio of two prior terms measures how much the hypothesis $\mathcal{H}_1$ is, initially, more probable than $\mathcal{H}_2$, whereas the second ratio of two likelihood probabilities evaluates how well the hypothesis $\mathcal{H}_1$ fits the dataset $\mathcal{D}$, compared to $\mathcal{H}_2$.

Jeffreys in his book ``Theory of Probability'' (1939) [[1]](#1) implicitly explained the relation between Bayesian inference and Occam's razor, which then later was mentioned in [[2]](#2), that the reason we favor simple hypotheses is that they have higher prior probability values than complex ones. This is true when we consider the **mathematical elegance** aspect of hypotheses that a theory with mathematical beauty is more likely to be correct than an ugly one that fits some experimental data (Paul Dirac). The ratio ($P(\mathcal{H}_1)/P(\mathcal{H}_2)$) allows us to integrate our bias or experience of experts into the inference. However, Jefferys and Berger [[2]](#2), MacKay [[3]](#3) argue that there is no need to have the prior bias in model comparison since the likelihood ratio **automatically embodies Occam's razor**. They explain that simple models tend to produce precise predictions of $\mathcal{D}$ since they usually focus particularly on the given dataset. Complex models, on the other hand, are more flexible in predicting a great variety of datasets, which means they tend to evenly spread the probability $P(\mathcal{D}\mid\mathcal{H})$ over the dataset space. When multiple hypotheses are compatible with the same observed dataset, the simplest model, though having a limited range of predictions, is the most probable since it makes stronger predictions than other more powerful complex ones, without the expression of prior bias. Since the priors of hypotheses do not provide significant contributions to the inference, they are usually assigned the same probability. 

To illustrate this argument, let's consider a toy example that appears in [[2]](#2). Assuming that we have a coin flip game with a friend and whoever loose has to do the chore. If heads appear, he wins, and vice versa. We know that our friend notoriously is a prankster and he could use a two-headed coin to foul us. However, for the sake of our friendship, we let him flip the coin. In our mind at that time, there are two hypotheses: $\mathcal{H}_1$ - that our friend uses a fair coin and a simpler one $\mathcal{H}_2$ - that he uses a two-headed coin. Regarding the two hypotheses, both of them satisfy if heads always appear after $N$ times of flipping. However, if there is one time that tails appear, $\mathcal{H}_2$ is falsified while $\mathcal{H}_1$ is still consistent. 

In the beginning, we are not sure about our friend is trying to foul us or not, so we simply assign $P(\mathcal{H}_1) = P(\mathcal{H}_2) = 0.5$. We know that in the first hypothesis $P(\text{heads}\mid\mathcal{H}_1)=P(\text{tail}\mid\mathcal{H}_1) = 0.5$, while $P(\text{heads}\mid\mathcal{H}_2)= 1$ and $P(\text{tail}\mid\mathcal{H}_2) = 0$ in the second. After the first toss, the coin comes up heads and Bayes' theorem shows that $P(\mathcal{H}_2\mid \text{heads})$ is two times higher than $P(\mathcal{H}_1\mid \text{heads})$. Although, the ratio is not strong enough to conclude that he is playing a trick. However, if heads appear five times consecutively, $P(\mathcal{H}_2\mid \text{heads})$ will be 32 times greater than $P(\mathcal{H}_1\mid \text{heads})$ and we can firmly conclude the coin is not fair. Through the example, we notice that although both hypotheses fit the dataset, the simpler one $\mathcal{H}_2$ is more probable. 

## Bayesian Occam's Razor

In his book [[3]](#3), MacKay provides a great insight into how Bayesian Occam's Razor works. In real problems of data analysis, Bayesian inference is used two times, one in model fitting and one in model comparison. At the first level of inference, assuming that there are multiple models $\{\mathcal{H}_i\}$ compatible with the observed dataset $\mathcal{D}$, Bayes' theorem is used to find the most probable parameters $\textbf{w}$ of each model $\mathcal{H}_i$, given $\mathcal{D}$, by maximizing a posterior distribution:

$$\begin{equation}
    P(\textbf{w} \mid \mathcal{D}, \mathcal{H}_i) = \dfrac{P(\mathcal{D} \mid \textbf{w}, \mathcal{H}_i)P(\textbf{w} \mid \mathcal{H}_i)}{P(\mathcal{D} \mid \mathcal{H}_i)}.
\end{equation}$$

This theorem shows up again when we compare models: 

$$\begin{equation}
    P(\mathcal{H}_i\mid\mathcal{D}) \propto P(\mathcal{D}\mid\mathcal{H}_i) P(\mathcal{H}_i)
\end{equation}$$

where $P(\mathcal{D}\mid\mathcal{H}_i)$ is called as evidence for $\mathcal{H}_i$. It is also considered as marginal likelihood since $P(\mathcal{D}\mid\mathcal{H}_i) = \int P(\mathcal{D}\mid\textbf{w},\mathcal{H}_i)P(\textbf{w}\mid\mathcal{H}_i)\text{d}\textbf{w}$. 

To approximately estimate $P(\mathcal{D}\mid\mathcal{H}_i)$, MacKay uses Laplace's method and achieves a beautiful equation:

$$\begin{equation}
    P(\mathcal{D}\mid\mathcal{H}_i) \simeq \underbrace{P(\mathcal{D}\mid  \textbf{w}_\text{MAP}, \mathcal{H}_i)}_\text{best-fit likelihood} \underbrace{P(\textbf{w}_\text{MAP}\mid\mathcal{H}_i)\sigma_{\textbf{w}\mid\mathcal{D}}}_\text{Occam's factor}
\end{equation}$$

where $\textbf{w}_\text{MAP}$ is achieved by maximizing the posterior $P(\textbf{w} \mid \mathcal{D}, \mathcal{H}_i)$ and $\sigma_{\textbf{w}\mid\mathcal{D}}$  is the posterior uncertainty in $\textbf{w}$, is derived from $-\nabla\nabla\ln P(\textbf{w} \mid \mathcal{D}, \mathcal{H}_i)_{|\textbf{w}_\text{MAP}}$. For the sake of simplicity, MacKay assumes that prior $P(\textbf{w}\mid\mathcal{H}_i)$ is uniform on a large interval $\sigma_\textbf{w}$, which represents the range of possible values of $\textbf{w}$ under $\mathcal{H}_i$. Hence, $P(\textbf{w}_\text{MAP}\mid\mathcal{H}_i) = 1/\sigma_\textbf{w}$ and Occam's factor is:

$$\begin{equation}
    \text{Occam's factor} = \dfrac{\sigma_{\textbf{w}\mid\mathcal{D}}}{\sigma_\textbf{w}}.
\end{equation}$$

Based on the factor, he explains that due to having **many parameters**, and each can vary freely in a large range $\sigma_\textbf{w}$, complex models are penalized by Occam's factor more than simple models which have a smaller range. Occam's factor also strongly penalizes over-parameterized models overfitting the dataset since their standard deviations $\sigma_{\textbf{w}\mid\mathcal{D}}$ are small.

## Conclusion

In conclusion, Occam's razor can be understood as a result of Bayesian inference. Bayes' theorem mathematically explains the term ``simplest'' in Occam's razor based on observed datasets and hypotheses. The reason that Bayesian Occam's razor slashes complex models is that they have lower prior and likelihood probabilities than simple models when both fit the same given dataset. Complex models over-parameterized to over-fit the given dataset are also penalized more than simple models by Occam's factor.


## Reference

<a id="1">[1]</a> Harold Jeffreys. The Theory of Probability. OuP Oxford, 1939.

<a id="2">[2]</a> William H Jefferys and James O Berger. Sharpening occam’s razor on a bayesian strop. In Bulletin of the American Astronomical Society, volume 23, page 1259, 1991.

<a id="3">[3]</a> David JC MacKay. Information theory, inference and learning algorithms, chapter 28. Cambridge university press, 2003.
