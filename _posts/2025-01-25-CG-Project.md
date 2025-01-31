---
title: 'Computer Graphics 2024 - Project'
date: 2025-01-25
permalink: /posts/2025/01/25/CG/
tags:
  - Computer Graphics
---

## Team Members

Bao-Huy Nguyen & Anh Dang Le Tran

## Motivation

When I saw the topic, I quickly recalled to my working place. Messy, unorganized, chaostic sometimes dirty maybe are the words that other people would use to describe it. However, somehow, strangely, to me it's still really "organised" since I know where things are in my desk (or somehow I purposely and unconsciously put them there), and they are there just because of balance and harmony.


In addition, we are really interested in the nostalgia trend recently hence we want to model a scene that reminds everyone (maybe mostly boys) about their childhoods, video games in late night and no homework. Chilling time, peaceful moment in the messy place.

<p align="center">
  <span style="display: inline-block; text-align: center; margin-right: 20px;">
    <img width="500" src="/figure/ComputerGraphics/Scene_layout_structure.png"/>
    <br>
    <i>Layout of the scene</i>
  </span>
  <span style="display: inline-block; text-align: center;">
    <img width="500" src="/figure/ComputerGraphics/instagram.png"/>
    <br>
    <i>Inspired Image</i>
  </span>
</p>

## **Table of content:**
 - [Simple Features](#A)
   - [Shading Normals](#A1)
   - [Alpha Masking](#A2)
   - [Halton Sampler](#A3)
   - [Post Processing](#A4)
   - [Image Denoising](#A5)
   - [Rough Dielectric](#A6)
   - [Area Light](#A7)
 - [Intermediate Features](#B)
   - [ThinLens Camera](#B1)
   - [MIS](#B2)
   - [Disney BSDF](#B3)
 - [Other Features](#C)
 - [Final Submission](#D)

<a id="A"></a>
## A. Simple Features

<a id="A1"></a>
### 1. Shading Normals

Shadding Normals/ Normal Mapping is a cheap and easiy way to add more details to a geometry without having to model a complex and detailed mesh. We employ this technique to render the highly detailed and complex objects like a wooden floor. To implement this, we include normal map texture property `ref<Texture> m_normals` in the class `instance.hpp` to get the normal texture if provided. Then we re-compute the `tangent` vector based on the new shading normal in `Instance::transformFrame()`.

Code:

* `include\lightwave\instance.hpp`
* `src\core\instance.cpp`

Below is the result before and after including normal map texture to a simple rectangle shape to increase its realism.

|                          Without                           |                           With                            |
| :--------------------------------------------------------: | :-------------------------------------------------------: |
| ![](/figure/ComputerGraphics/normal_mapping/wo_normal.jpg) | ![](/figure/ComputerGraphics/normal_mapping/w_normal.png) |

<a id="A2"></a>
### 2. Alpha Masking

For our scene, we want to have several transparent sticker notes attached to the CRT television as decorations. These objects is not fully opaque and we can see other objects behind it. To this end, we implement alpha masking similar to shading normals above. The instance class will find the provided alpha texture in a xml file. For `alpha = 0`, the object is fully transparent meaning that `Scene::intersect` method will ignore the ray intersection. When `alpha = 1`, the intersection is always valid. 

Code:

* `include\lightwave\instance.hpp`
* `src\core\instance.cpp`
  
Below is the result with `alpha=0.2`.

<p align = "center">
    <img width="400"  src="/figure/ComputerGraphics/alpha_masking/alpha.jpg"/>
    <br>
</p>

<a id="A3"></a>
### 3. Halton Sampler

The `Independent` sampler sometimes, unluckly, produces many samples in a same region and that leads to high variant results. This may require a large number of sample to cover all the possible incoming light directions to an intersection point to achieve less variance. However, the more samples, the slower renderer is. To get better visual quality with the same amount of samples, we follow the intruction from [PBR](https://www.pbr-book.org/4ed/Sampling_and_Reconstruction/Halton_Sampler) to implement Halton Sampler. The visual quality is significantly enhanced compared to `Independent` sampler with the same amount of samples per pixel.

Code:

* `src\samplers\halton.cpp`
* `src\utils\lowdiscrepancy.hpp`

Below are the results of using Independent Sampler and Halton sampler with 3 different randomizer strategies. All of them use same number of samples, 64.

|                        Indepedent                         |                    OwenScramble                    |
| :-------------------------------------------------------: | :------------------------------------------------: |
|   ![](/figure/ComputerGraphics/halton/independent.png)    |   ![](/figure/ComputerGraphics/halton/owen.png)    |
| ![](/figure/ComputerGraphics/halton/crop_independent.png) | ![](/figure/ComputerGraphics/halton/crop_owen.png) |


|                     PermuteDigit                      |                   RadicalInverse                   |
| :---------------------------------------------------: | :------------------------------------------------: |
|   ![](/figure/ComputerGraphics/halton/permute.png)    |   ![](/figure/ComputerGraphics/halton/none.png)    |
| ![](/figure/ComputerGraphics/halton/crop_permute.png) | ![](/figure/ComputerGraphics/halton/crop_none.png) |


<a id="A4"></a>
### 4. Post Processing

<a id="A4_1"></a>
#### Bloom

In real life, sometimes, the extreme brightness from the light source can overwhelm the human eyes and camera, producing the effects of extending the borders of light area in the scene. Simulating this effect directly in is not an easy task hence we follow the guidline from [LearnOpenGL](https://learnopengl.com/Advanced-Lighting/Bloom) to achieve the bloom effects for the lamp in our scene.

Code:

* `src\postprocess\bloom.cpp`

<iframe src="/figure/ComputerGraphics/html/bloom.html" style="width: 100%; height: 600px;" frameborder="0"></iframe>

Below is the result after applying bloom. We can clearly see the effects of extending edges of two emissive objects.

<a id="A4_2"></a>
#### Reinhard

Although human visual perception has a relatively high dynamic range, most of monitors can only represent RGB color in range [0, 255] or [0, 1]. Output of our renderer is an high dynamic range image without an upper intensity limitation. To map a high dynamic range image to [0, 1] to display it, we refer this [guidline](https://64.github.io/tonemapping/) to implement tonemapping alogrithms.

Code:
* `src\postprocess\tonemapping.cpp`
* `src\utils\imageprocessing.hpp`

|                           Before                            |                           After                            |
| :---------------------------------------------------------: | :--------------------------------------------------------: |
| ![](/figure/ComputerGraphics/tone_mapping/crop_before.jpeg) | ![](/figure/ComputerGraphics/tone_mapping/crop_after.jpeg) |

<a id="A5"></a>
### 5. Image Denoising 

Since our render uses the Monte Carlo method to compute the high-dimensional integral in the rendering equation, a large of number of samples is required to achieve a visally appealing result, which presents a computational burden. Our scene has a considerable number of objects in which using a low number of samples would produce noisy results. To this end, we integrate [Intel®Open Image Denoise](https://www.openimagedenoise.org/) library to our renderer to reduce noise of outputs.

Code:
* `src\postprocess\denoise.cpp`

<iframe src="/figure/ComputerGraphics/html/denoiser.html" style="width: 100%; height: 600px;" frameborder="0"></iframe>


<a id="A6"></a>
### 6. Rough Dielectric 

We want to increase a little bit of realism to our glass material, hence implement rough dielectric bsdf to add a little bit of roughness to our Coca-Cola bottle . We follow the [Microfacet Models for Refraction ](https://www.cs.cornell.edu/~srm/publications/EGSR07-btdf.pdf) to implement that bsdf class.

Code: 
* `src\bsdfs\roughdielectric.cpp`

|                                    Roughness 0.0                                     |                                    Roughness 0.1                                     |                                    Roughness 0.2                                     |
| :----------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/rough-dielectric/emission_roughdielectric_00_test.jpeg) | ![](/figure/ComputerGraphics/rough-dielectric/emission_roughdielectric_01_test.jpeg) | ![](/figure/ComputerGraphics/rough-dielectric/emission_roughdielectric_02_test.jpeg) |

|                                    Roughness 0.3                                     |                                    Roughness 0.4                                     |                                    Roughness 0.5                                     |
| :----------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/rough-dielectric/emission_roughdielectric_03_test.jpeg) | ![](/figure/ComputerGraphics/rough-dielectric/emission_roughdielectric_04_test.jpeg) | ![](/figure/ComputerGraphics/rough-dielectric/emission_roughdielectric_05_test.jpeg) |

<a id="A7"></a>
### 7. Area Light

We implement area light class for the lamp' bulb and the screen of CRT television (which are natuarlly area lights).

Code:
* `src\lights\area.cpp`
* `src\shapes\mesh.cpp`
* `src\shapes\rectangle.cpp`
* `src\shapes\sphere.cpp`
* `include\lightwave\shape.hpp`

<iframe src="/figure/ComputerGraphics/html/arealight.html" style="width: 100%; height: 600px;" frameborder="0"></iframe>

 
### 8. Spot Light

Our scene has the vibe of late game night and sometimes we only want to shine a specific area but not the whole sence. Point light and directional light are not a good choice in this case. To this end, we refer to [PBR](https://pbr-book.org/3ed-2018/Light_Sources/Point_Lights) to implement another light class, spotlight, to handle this task. 

Code:
* `src\lights\spot.cpp`

|                       pointlight                       |                       spotlight                       |
| :----------------------------------------------------: | :---------------------------------------------------: |
| ![](/figure/ComputerGraphics/spotlight/pointlight.jpg) | ![](/figure/ComputerGraphics/spotlight/spotlight.jpg) |

<a id="B"></a>
## B. Intermediate Features

<a id="B1"></a>
### 1. Thinlens Camera

The perspective pin pole camera model in our renderer could not capture the focus effect like real life camera, which may reduce the realism. To simulate the depth of field effect of the real life cameras, we follow [PBR](https://pbr-book.org/3ed-2018/Camera_Models/Projective_Camera_Models) to implement a thin lens camera model.

Code:
* `src\cameras\thinlens.cpp`

**Lens Radius**

|                                 Lens Radius 0.05                                 |                                 Lens Radius 0.10                                 |                                 Lens Radius 0.15                                 |
| :------------------------------------------------------------------------------: | :------------------------------------------------------------------------------: | :------------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_lor_005_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_lor_010_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_lor_015_test.jpeg) |

|                                 Lens Radius 0.20                                 |                                 Lens Radius 0.25                                 |                                 Lens Radius 0.05                                 |
| :------------------------------------------------------------------------------: | :------------------------------------------------------------------------------: | :------------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_lor_020_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_lor_025_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_lor_005_test.jpeg) |

**Plane of Focus Distance**

|                          Plane of Focus Distance 1.0                          |                          Plane of Focus Distance 3.0                          |                          Plane of Focus Distance 5.0                          |
| :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_fd_1_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_fd_3_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_fd_5_test.jpeg) |

|                          Plane of Focus Distance 7.0                          |                          Plane of Focus Distance 9.0                          |                          Plane of Focus Distance 1.0                          |
| :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_fd_7_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_fd_9_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_fd_1_test.jpeg) |

<a id="B2"></a>
### 2. MIS Path Tracer 

Faithfully tracing each ray in BSDF sampling will produce unbias results in rendering but requires a large number of samples and high depth to achieve those results. On the other hand NEE although significantly reduce noise by directly accounting direct illuminace from light source, will fail in case of smooth surfaces which requires idirect illumination. To balance both, we refer the [video lectures of Prof. Ravi Ramamoorthi](https://youtu.be/xrsHo8kcCX0?si=x8o1P760jX_vhJBH) to implement MIS Path Tracer.

Code:
* `src\integrators\mis_pathtracer.cpp`

<iframe src="/figure/ComputerGraphics/html/mis.html" style="width: 100%; height: 500px;" frameborder="0"></iframe>

<a id="B3"></a>
### 3. Disney Bsdf

We want to model plastic material for our NES Console (which is made of plastic) that sometimes reflects light at grazing angles. The reflectance is modeled by coating a layer on the diffuse material. We faithfully follow the instruction from [the UCSD homework](https://cseweb.ucsd.edu/~tzli/cse272/wi2023/homework1.pdf) to implement Disney Bsdf. This bsdf unifies all the material that we have implemented so far. Although not 100% physcially accurate, it still gives good and reasonable results.

Code:
* `src\bsdfs\disney.cpp`

**Subsurface**

|                                  0.0                                  |                                  0.1                                  |                                  0.2                                  |
| :-------------------------------------------------------------------: | :-------------------------------------------------------------------: | :-------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/subsurface/subsurface0_test.jpeg) | ![](/figure/ComputerGraphics/disney/subsurface/subsurface1_test.jpeg) | ![](/figure/ComputerGraphics/disney/subsurface/subsurface2_test.jpeg) |


|                                  0.3                                  |                                  0.4                                  |                                  0.5                                  |
| :-------------------------------------------------------------------: | :-------------------------------------------------------------------: | :-------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/subsurface/subsurface3_test.jpeg) | ![](/figure/ComputerGraphics/disney/subsurface/subsurface4_test.jpeg) | ![](/figure/ComputerGraphics/disney/subsurface/subsurface5_test.jpeg) |


|                                  0.6                                  |                                  0.7                                  |                                  0.8                                  |
| :-------------------------------------------------------------------: | :-------------------------------------------------------------------: | :-------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/subsurface/subsurface6_test.jpeg) | ![](/figure/ComputerGraphics/disney/subsurface/subsurface7_test.jpeg) | ![](/figure/ComputerGraphics/disney/subsurface/subsurface7_test.jpeg) |



|                                  0.9                                  |                                  1.0                                   |                                  0.0                                  |
| :-------------------------------------------------------------------: | :--------------------------------------------------------------------: | :-------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/subsurface/subsurface9_test.jpeg) | ![](/figure/ComputerGraphics/disney/subsurface/subsurface10_test.jpeg) | ![](/figure/ComputerGraphics/disney/subsurface/subsurface0_test.jpeg) |

**Anisotropic**

|                                   0.0                                   |                                   0.1                                   |                                   0.2                                   |
| :---------------------------------------------------------------------: | :---------------------------------------------------------------------: | :---------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/anisotropic/anisotropic0_test.jpeg) | ![](/figure/ComputerGraphics/disney/anisotropic/anisotropic1_test.jpeg) | ![](/figure/ComputerGraphics/disney/anisotropic/anisotropic2_test.jpeg) |


|                                   0.3                                   |                                   0.4                                   |                                   0.5                                   |
| :---------------------------------------------------------------------: | :---------------------------------------------------------------------: | :---------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/anisotropic/anisotropic3_test.jpeg) | ![](/figure/ComputerGraphics/disney/anisotropic/anisotropic4_test.jpeg) | ![](/figure/ComputerGraphics/disney/anisotropic/anisotropic5_test.jpeg) |

|                                   0.6                                   |                                   0.7                                   |                                   0.8                                   |
| :---------------------------------------------------------------------: | :---------------------------------------------------------------------: | :---------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/anisotropic/anisotropic6_test.jpeg) | ![](/figure/ComputerGraphics/disney/anisotropic/anisotropic7_test.jpeg) | ![](/figure/ComputerGraphics/disney/anisotropic/anisotropic8_test.jpeg) |

|                                   0.9                                   |                                   1.0                                    |                                   0.0                                   |
| :---------------------------------------------------------------------: | :----------------------------------------------------------------------: | :---------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/anisotropic/anisotropic9_test.jpeg) | ![](/figure/ComputerGraphics/disney/anisotropic/anisotropic10_test.jpeg) | ![](/figure/ComputerGraphics/disney/anisotropic/anisotropic0_test.jpeg) |

**Clearcoat**

|                                 0.0                                 |                                 0.1                                 |                                 0.2                                 |
| :-----------------------------------------------------------------: | :-----------------------------------------------------------------: | :-----------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/clearcoat/clearcoat0_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoat/clearcoat1_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoat/clearcoat2_test.jpeg) |


|                                 0.3                                 |                                 0.4                                 |                                 0.5                                 |
| :-----------------------------------------------------------------: | :-----------------------------------------------------------------: | :-----------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/clearcoat/clearcoat3_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoat/clearcoat4_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoat/clearcoat5_test.jpeg) |

|                                 0.6                                 |                                 0.7                                 |                                 0.8                                 |
| :-----------------------------------------------------------------: | :-----------------------------------------------------------------: | :-----------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/clearcoat/clearcoat6_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoat/clearcoat7_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoat/clearcoat8_test.jpeg) |


|                                 0.9                                 |                                 1.0                                  |                                 0.0                                 |
| :-----------------------------------------------------------------: | :------------------------------------------------------------------: | :-----------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/clearcoat/clearcoat9_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoat/clearcoat10_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoat/clearcoat0_test.jpeg) |

**ClearcoatGloss**

|                                      0.0                                      |                                      0.1                                      |                                      0.2                                      |
| :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/clearcoatGloss/clearcoatGloss0_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoatGloss/clearcoatGloss1_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoatGloss/clearcoatGloss2_test.jpeg) |


|                                      0.3                                      |                                      0.4                                      |                                      0.5                                      |
| :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/clearcoatGloss/clearcoatGloss3_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoatGloss/clearcoatGloss4_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoatGloss/clearcoatGloss5_test.jpeg) |

|                                      0.6                                      |                                      0.7                                      |                                      0.8                                      |
| :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/clearcoatGloss/clearcoatGloss6_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoatGloss/clearcoatGloss7_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoatGloss/clearcoatGloss8_test.jpeg) |


|                                      0.9                                      |                                      1.0                                       |                                      0.0                                      |
| :---------------------------------------------------------------------------: | :----------------------------------------------------------------------------: | :---------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/clearcoatGloss/clearcoatGloss9_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoatGloss/clearcoatGloss10_test.jpeg) | ![](/figure/ComputerGraphics/disney/clearcoatGloss/clearcoatGloss0_test.jpeg) |

**Metallic**

|                                0.0                                |                                0.1                                |                                0.2                                |
| :---------------------------------------------------------------: | :---------------------------------------------------------------: | :---------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/metallic/metallic0_test.jpeg) | ![](/figure/ComputerGraphics/disney/metallic/metallic1_test.jpeg) | ![](/figure/ComputerGraphics/disney/metallic/metallic2_test.jpeg) |


|                                0.3                                |                                0.4                                |                                0.5                                |
| :---------------------------------------------------------------: | :---------------------------------------------------------------: | :---------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/metallic/metallic3_test.jpeg) | ![](/figure/ComputerGraphics/disney/metallic/metallic4_test.jpeg) | ![](/figure/ComputerGraphics/disney/metallic/metallic5_test.jpeg) |

|                                0.6                                |                                0.7                                |                                0.8                                |
| :---------------------------------------------------------------: | :---------------------------------------------------------------: | :---------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/metallic/metallic6_test.jpeg) | ![](/figure/ComputerGraphics/disney/metallic/metallic7_test.jpeg) | ![](/figure/ComputerGraphics/disney/metallic/metallic8_test.jpeg) |


|                                0.9                                |                                1.0                                 |                                0.0                                |
| :---------------------------------------------------------------: | :----------------------------------------------------------------: | :---------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/metallic/metallic9_test.jpeg) | ![](/figure/ComputerGraphics/disney/metallic/metallic10_test.jpeg) | ![](/figure/ComputerGraphics/disney/metallic/metallic0_test.jpeg) |


**Roughness**

|                                 0.0                                 |                                 0.1                                 |                                 0.2                                 |
| :-----------------------------------------------------------------: | :-----------------------------------------------------------------: | :-----------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/roughness/roughness0_test.jpeg) | ![](/figure/ComputerGraphics/disney/roughness/roughness1_test.jpeg) | ![](/figure/ComputerGraphics/disney/roughness/roughness2_test.jpeg) |


|                                 0.3                                 |                                 0.4                                 |                                 0.5                                 |
| :-----------------------------------------------------------------: | :-----------------------------------------------------------------: | :-----------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/roughness/roughness3_test.jpeg) | ![](/figure/ComputerGraphics/disney/roughness/roughness4_test.jpeg) | ![](/figure/ComputerGraphics/disney/roughness/roughness5_test.jpeg) |

|                                 0.6                                 |                                 0.7                                 |                                 0.8                                 |
| :-----------------------------------------------------------------: | :-----------------------------------------------------------------: | :-----------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/roughness/roughness6_test.jpeg) | ![](/figure/ComputerGraphics/disney/roughness/roughness7_test.jpeg) | ![](/figure/ComputerGraphics/disney/roughness/roughness8_test.jpeg) |


|                                 0.9                                 |                                 1.0                                  |                                 0.0                                 |
| :-----------------------------------------------------------------: | :------------------------------------------------------------------: | :-----------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/roughness/roughness9_test.jpeg) | ![](/figure/ComputerGraphics/disney/roughness/roughness10_test.jpeg) | ![](/figure/ComputerGraphics/disney/roughness/roughness0_test.jpeg) |



**SpecularTransmittance 1.0, and Roughness**

|                                       0.0                                       |                                       0.1                                       |                                       0.2                                       |
| :-----------------------------------------------------------------------------: | :-----------------------------------------------------------------------------: | :-----------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/disney/transmittance/transmittance_roughness0.jpg) | ![](/figure/ComputerGraphics/disney/transmittance/transmittance_roughness1.jpg) | ![](/figure/ComputerGraphics/disney/transmittance/transmittance_roughness2.jpg) |

**Comparison of Disney Coatting and Principle Specular for Plastic Material**

|                     Dinesy                      |                    Principle                    |
| :---------------------------------------------: | :---------------------------------------------: |
| ![](/figure/ComputerGraphics/plastic/coat.jpeg) | ![](/figure/ComputerGraphics/plastic/spec.jpeg) |

Disney Coatting gives a little bit more realism than Principle Specular since the coatting layer of the Bsdf (not physcially accurate) reflects sufficient amount of light but not too much compared to Principle bsdf.

<a id="C"></a>
## C. Other Features

### CRT TV Effect

The old CRT TVs in 80s have an interesting effect, CRT effect, which if we look closely to the screen, we can easily notice with our naked eyes that there are many separate red, green and blue pixels. And because the screen is curved, we can see some curved line strips in the screen. Although we can implement a texture class to simulate that effect, for the sake of simplicty, we modify the texture of screen byt multiplying it with a CRT pattern.

|                    Pattern                    |                   After                    |
| :-------------------------------------------: | :----------------------------------------: |
| ![](/figure/ComputerGraphics/crt/pattern.jpg) | ![](/figure/ComputerGraphics/crt/crop.jpg) |



<a id="D"></a>
## D. Final Submission

![](/figure/ComputerGraphics/final/final-submission.jpeg)

<a id="E"></a>
## E. Features in Detail
![](/figure/ComputerGraphics/final/features.jpg)

<!-- <iframe src="/figure/ComputerGraphics/html/pipeline.html" style="width: 100%; height: 1920;" frameborder="0"></iframe> -->

## References

### Assets

<a id="1">[1]</a> [Wooden Floor](https://sketchfab.com/3d-models/wooden-planks-9c1bc003f9e245bf823a3a60b7437299) 

<a id="2">[2]</a> [CRT TV](https://sketchfab.com/3d-models/nintendo-entertainment-system-85-scene-cfd6dcb544fa4401b3dac20061d7fefb) 

<a id="3"> [3] </a> [NES](https://sketchfab.com/3d-models/nes-console-and-controller-ffd427134d5e44b4850628030aa66236)

<a id="4"> [4] </a> [Pixar Lamp](https://www.cgtrader.com/free-3d-models/furniture/lamp/pixar-lamp-518a1299-ae8f-4847-ba1a-110d4f68d172)

<a id="5"> [5] </a> [Comics Book](https://sketchfab.com/3d-models/opened-comics-book-6931e14a96f64b158ac4cebcf7ae8763)

<a id="6"> [6] </a> [NES Controller](https://sketchfab.com/3d-models/nintendo-nes-controller-4da098673d4d44cba268e058bc1f195e)
