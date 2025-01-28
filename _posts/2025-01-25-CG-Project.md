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

When I saw the topic, I quickly recalled my working place. Messy, unorganized, chaostic sometimes dirty maybe are the words that other people would use to describe it. However, somehow, strangely, to me it's still really "organised" since I know where things are in my desk (or somehow I purposely and unconsciously put them there), and they are there just because of balance and harmony.

<!-- <p align = "center">
    <img width="500"  src="/figure/Snakes/failure_case.gif"/>
    <br>
    <i>My Working Place</i>
</p> -->


In addition, we are really interested in the nostalgia trend recently hence we want to make a scene that reminds everyone (maybe mostly boys) about their childhoods, video games in late night and no homework. Chilling time, peaceful moment in the messy place.

<p align = "center">
    <img width="500"  src="/figure/ComputerGraphics/Scene_layout_structure.png"/>
    <br>
    <i>Layout of the scene </i>
</p>



## Simple Features

### Shading Normals

Shadding Normals/ Normal Mapping is a cheap and easiy way to add more details to a geometry without having to model a complex and detailed mesh. We employ this technique to render the highly detailed and complex objects like a wooden floor. To implement this, we include normal map texture property `ref<Texture> m_normals` in the class `instance.hpp` to get the normal texture if provided. Then we re-compute the `tangent` vector based on the new shading normal in `Instance::transformFrame()`.

Code:

* `include\lightwave\instance.hpp`
* `src\core\instance.cpp`

Below is the result before and after including normal map texture to a simple rectangle shape to increase its realism.

|                          Without                           |                           With                            |
| :--------------------------------------------------------: | :-------------------------------------------------------: |
| ![](/figure/ComputerGraphics/normal_mapping/wo_normal.jpg) | ![](/figure/ComputerGraphics/normal_mapping/w_normal.png) |

### Alpha Masking

For our scene, we want to have several transparent sticker notes attached to the CRT television as decorations. These objects is not fully opaque and we can see other objects behind it. To this end, we implement alpha masking similar to shading normals above. The instance class will find the provided alpha texture in a xml file. For `alpha = 0`, the object is fully transparent meaning that `Scene::intersect` method will ignore the ray intersection. When `alpha = 1`, the intersection is always valid. 

Code:

* `include\lightwave\instance.hpp`
* `src\core\instance.cpp`
  
Below is the result with `alpha=0.2`.

<p align = "center">
    <img width="500"  src="/figure/ComputerGraphics/alpha_masking/alpha.jpg"/>
    <br>
</p>
### Halton Sampler

The `Independent` sampler sometimes, unluckly, produces many samples in a region and that leads to high variant results. This may require a large number of sample to cover all the possible incoming light directions to an intersection point to achieve less variance. However, the more samples, the slower renderer is. To get better visual quality with the same amount of samples, we follow the intruction from [PBR](https://www.pbr-book.org/4ed/Sampling_and_Reconstruction/Halton_Sampler) to implement Halton Sampler. The visual quality is significantly enhanced compared to `Independent` sampler with the same amount of samples per pixel.

Code:

* `src\samplers\halton.cpp`
* `src\utils\lowdiscrepancy.hpp`

Below are the results of using two different samplers, independent and halton with the same 64 samples.

|                        Indepedent                         |                     HaltonOwen                     |
| :-------------------------------------------------------: | :------------------------------------------------: |
|   ![](/figure/ComputerGraphics/halton/independent.png)    |   ![](/figure/ComputerGraphics/halton/owen.png)    |
| ![](/figure/ComputerGraphics/halton/crop_independent.png) | ![](/figure/ComputerGraphics/halton/crop_owen.png) |

### Post Processing

#### Bloom

In real life, sometimes, the extreme brightness from the light source can overwhelm the human eyes and camera, producing the effects of extending the borders of light area in the scene. Simulating this effect is not an easy task hence we follow the guidline from [LearnOpenGL](https://learnopengl.com/Advanced-Lighting/Bloom) to achieve the bloom effects for the lamp in our scene.

Code:

* `src\postprocess\bloom.cpp`


Below is the result after apply bloom. We can clearly see the effects of extending edges of two emissive objects.


#### Reinhard

Although human visual perception has a relatively high dynamic range, most of monitors can only represent RGB color in range [0, 255] or [0, 1]. Output of our renderer is an high dynamic range image without an upper intensity limitation. To map a high dynamic range image to [0, 1] to display it, we refer this [guidline](https://64.github.io/tonemapping/) to implement tonemapping alogrithms.

Code:
* `src\postprocess\tonemapping.cpp`
* `src\utils\imageprocessing.hpp`

### Image Denoising 

Since our render uses the Monte Carlo method to compute the high-dimensional integral in the rendering equation, a large of number of samples is required to achieve a visally appealing result which is maybe a computational burden. Our scene includes a lots of different objects in which using a low number of samples would produce noisy results. To this end, we integrate [Intel®Open Image Denoise](https://www.openimagedenoise.org/) library to our renderer to reduce noise of outputs.

Code:
* `src\postprocess\denoise.cpp`



### Rough Dielectric 

We want to increase a little bit of realism to our glass material, hence implement rough dielectric bsdf to add a little bit of roughness to our Coca-Cola bottle . We follow the [Microfacet Models for Refraction ](https://www.cs.cornell.edu/~srm/publications/EGSR07-btdf.pdf) to implement that bsdf class.

Code: 
* `src\bsdfs\roughdielectric.cpp`

|                                    Roughness 0.0                                     |                                    Roughness 0.1                                     |                                    Roughness 0.2                                     |
| :----------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/rough-dielectric/emission_roughdielectric_00_test.jpeg) | ![](/figure/ComputerGraphics/rough-dielectric/emission_roughdielectric_01_test.jpeg) | ![](/figure/ComputerGraphics/rough-dielectric/emission_roughdielectric_02_test.jpeg) |

|                                    Roughness 0.3                                     |                                    Roughness 0.4                                     |                                    Roughness 0.5                                     |
| :----------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/rough-dielectric/emission_roughdielectric_03_test.jpeg) | ![](/figure/ComputerGraphics/rough-dielectric/emission_roughdielectric_04_test.jpeg) | ![](/figure/ComputerGraphics/rough-dielectric/emission_roughdielectric_05_test.jpeg) |

### Area Light

We implement area light class to attach to the lamp' bulb and the screen of CRT television (which are natuarlly area lights).

Code:
* `src\lights\area.cpp`
* `src\shapes\mesh.cpp`
* `src\shapes\rectangle.cpp`
* `src\shapes\sphere.cpp`
* `include\lightwave\shape.hpp`

<div class="slideshow-container" id="slides1">
  <div class="slides fade">
    <div class="text">Caption for Image 1</div>
    <img src="/figure/ComputerGraphics/area_light/without.jpg" style="width:100%">
  </div>
  <div class="slides fade">
    <div class="text">Caption for Image 2</div>
    <img src="/figure/ComputerGraphics/area_light/with.jpg" style="width:100%">
  </div>
  <a class="prev" onclick="plusSlides(-1, 1)">&#10094;</a>
  <a class="next" onclick="plusSlides(1, 1)">&#10095;</a>
</div>
<br>
<div style="text-align:center">
  <span class="dot" onclick="currentSlide(1, 1)"></span>
  <span class="dot" onclick="currentSlide(2, 1)"></span>
</div>


### Spot Light

Our scene has the vibe of late game night and sometimes we only want to shine a specific area but not the whole sence. Point light and directional light are not a good choice in this case. To this end, we refer to [PBR](https://pbr-book.org/3ed-2018/Light_Sources/Point_Lights) to implement another light class, spotlight, to handle this task. 

Code:
* `src\lights\spot.cpp`

|                       pointlight                       |                       spotlight                       |
| :----------------------------------------------------: | :---------------------------------------------------: |
| ![](/figure/ComputerGraphics/spotlight/pointlight.jpg) | ![](/figure/ComputerGraphics/spotlight/spotlight.jpg) |

## Intermediate Features

### Thinlens Camera

The perspective pin pole camera model in our renderer could not capture the focus effect like real life camera, which may reduce the realism. To simulate the depth of field effect of the real life cameras, we follow [PBR](https://pbr-book.org/3ed-2018/Camera_Models/Projective_Camera_Models) to implement a thin lens camera model.

Code:
* `src\cameras\thinlens.cpp`

|                                 Lens Radius 0.05                                 |                                 Lens Radius 0.10                                 |                                 Lens Radius 0.15                                 |                                 Lens Radius 0.20                                 |                                 Lens Radius 0.25                                 |
| :------------------------------------------------------------------------------: | :------------------------------------------------------------------------------: | :------------------------------------------------------------------------------: | :------------------------------------------------------------------------------: | :------------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_lor_005_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_lor_010_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_lor_015_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_lor_020_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_lor_025_test.jpeg) |


|                          Plane of Focus Distance 1.0                          |                          Plane of Focus Distance 3.0                          |                          Plane of Focus Distance 5.0                          |                          Plane of Focus Distance 7.0                          |                          Plane of Focus Distance 9.0                          |
| :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------: |
| ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_fd_1_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_fd_3_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_fd_5_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_fd_7_test.jpeg) | ![](/figure/ComputerGraphics/thinlens/sphere_snowman_thinlens_fd_9_test.jpeg) |


### MIS Path Tracer 

Faithfully tracing each ray in BSDF sampling will produce unbias results in rendering but requires a large number of samples and high depth to achieve those results. On the other hand NEE although significantly reduce noise by directly accounting direct illuminace from light source, will fail in case of smooth surfaces which requires idirect illumination. To balance both, we refer the [video lectures of Prof. Ravi Ramamoorthi](https://youtu.be/xrsHo8kcCX0?si=x8o1P760jX_vhJBH) to implement MIS Path Tracer.

Code:
* `src\integrators\mis_pathtracer.cpp`

<div class="slideshow-container" id="slides2">
  <div class="slides fade">
    <div class="text">Caption for Image 4</div>
    <img src="/figure/ComputerGraphics/mis/bsdf.jpg" style="width:100%">
  </div>
  <div class="slides fade">
    <div class="text">Caption for Image 5</div>
    <img src="/figure/ComputerGraphics/mis/nee.jpg" style="width:100%">
  </div>
  <div class="slides fade">
    <div class="text">Caption for Image 6</div>
    <img src="/figure/ComputerGraphics/mis/mis.jpg" style="width:100%">
  </div>
  <a class="prev" onclick="plusSlides(-1, 2)">&#10094;</a>
  <a class="next" onclick="plusSlides(1, 2)">&#10095;</a>
</div>
<br>
<div style="text-align:center">
  <span class="dot" onclick="currentSlide(1, 2)"></span>
  <span class="dot" onclick="currentSlide(2, 2)"></span>
  <span class="dot" onclick="currentSlide(3, 2)"></span>
</div>


### Disney Bsdf

We want to model plastic material for our NES Console (which is made of plastic) that sometimes reflects light at grazing angles. The reflectance is modeled by coating a layer on the diffuse material. We faithfully follow the instruction from [the UCSD homework](https://cseweb.ucsd.edu/~tzli/cse272/wi2023/homework1.pdf) to implement Disney Bsdf. This bsdf unifies all the material that we have implemented so far. Although not 100% physcially accurate, it still gives good and reasonable results.

Code:
* `src\bsdfs\disney.cpp`

## Other Features

### CRT TV Effect

The old CRT TVs in 80s have an interesting effect, CRT effect, which if we look closely to the screen, we can easily notice with our naked eyes that there are many separate red, green and blue pixels. And because the screen is curved, we can see some curved line strips in the screen. Although we can implement a texture class to simulate that effect, for the sake of simplicty, we modify the texture of screen byt multiplying it with a CRT pattern.

| Before |                                After                                 |
| :----: | :------------------------------------------------------------------: |
| ![]()  | ![](/figure/ComputerGraphics/normal_mapping/normal_mapping_test.png) |


## Final Submission

## References
<!-- 
<a id="1">[1]</a> Prisacariu, Victor Adrian, et al. "Real-time 3d tracking and reconstruction on mobile phones." IEEE transactions on visualization and computer graphics 21.5 (2014): 557-570.

<a id="2">[2]</a> Kolev, Kalin, Thomas Brox, and Daniel Cremers. "Fast joint estimation of silhouettes and dense 3D geometry from multiple images." IEEE transactions on pattern analysis and machine intelligence 34.3 (2012): 493-505.

<a id="3">[3]</a> Yuan, Jing, Egil Bae, and Xue-Cheng Tai. "A study on continuous max-flow and min-cut approaches." 2010 ieee computer society conference on computer vision and pattern recognition. IEEE, 2010.

<a id="4">[4]</a> Chambolle, Antonin. "An algorithm for total variation minimization and applications." Journal of Mathematical imaging and vision 20.1 (2004): 89-97. -->

<style>
  .slideshow-container {
    max-width: 500px;
    position: relative;
    margin: auto;
  }

  .slides {
    display: none;
  }

  .prev, .next {
    cursor: pointer;
    position: absolute;
    top: 50%;
    width: auto;
    padding: 16px;
    margin-top: -22px;
    color: white;
    font-weight: bold;
    font-size: 18px;
    transition: 0.6s ease;
    border-radius: 0 3px 3px 0;
    user-select: none;
  }

  .next {
    right: 0;
    border-radius: 3px 0 0 3px;
  }

  .prev:hover, .next:hover {
    background-color: rgba(0,0,0,0.8);
  }

  .text {
    color: #f2f2f2;
    font-size: 15px;
    padding: 8px 12px;
    position: absolute;
    bottom: 8px;
    width: 100%;
    text-align: center;
  }

  .dot {
    cursor: pointer;
    height: 15px;
    width: 15px;
    margin: 0 2px;
    background-color: #bbb;
    border-radius: 50%;
    display: inline-block;
    transition: background-color 0.6s ease;
  }

  .active, .dot:hover {
    background-color: #717171;
  }

  .fade {
    -webkit-animation-name: fade;
    -webkit-animation-duration: 0.5s; /* Adjust this value to make the transition faster */
    animation-name: fade;
    animation-duration: 0.5s; /* Adjust this value to make the transition faster */
  }

  @-webkit-keyframes fade {
    from {opacity: .4}
    to {opacity: 1}
  }

  @keyframes fade {
    from {opacity: .4}
    to {opacity: 1}
  }
</style>

<script>
  var slideIndex = [1, 1];
  var slideId = ["slides1", "slides2"]
  showSlides(1, 0);
  showSlides(1, 1);

  function plusSlides(n, no) {
    showSlides(slideIndex[no] += n, no);
  }

  function currentSlide(n, no) {
    showSlides(slideIndex[no] = n, no);
  }

  function showSlides(n, no) {
    var i;
    var x = document.getElementsByClassName(slideId[no]);
    var dots = document.getElementsByClassName("dot");
    if (n > x.length) {slideIndex[no] = 1}    
    if (n < 1) {slideIndex[no] = x.length}
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";  
    }
    for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
    }
    x[slideIndex[no]-1].style.display = "block";  
    dots[slideIndex[no]-1].className += " active";
  }
</script>
