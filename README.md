## Mandelbrot Web

This app is very simple.

It's a Fractal zoomer using URL to map the zoom path of a fractal. It
subdivides the image in 16 parts, and each of them is a hex number in the URL,
representing, the various zooming steps one can take.

The zoom interface is created by links in a image map over the fractal's image.

### How it works

It uses the fantastic python bottle, the micro-framework, PIL (python imaging),
and the Mandelbrot Set fractal's formulas.

### TODO

* Use smarter client caching
* Implement memory cache (memcached)
* Implement image flipping to make use of fractal's simetry
* Use analytics
* Show a border in zooming rectangles

