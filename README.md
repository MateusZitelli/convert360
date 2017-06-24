<h1 align="center">
Convert360 🌎
<br/>
<i>360 degree media toolkit.</i>
<br/>
<img width=150 src="https://cdn.rawgit.com/MateusZitelli/convert360/master/mercator.jpg" ></img>
</h1>

GPU accelerated command line tool to convert 360 images and videos between different projections.

### Supported Convertions

- [x] Equirectangular to Cube-map
- [ ] Cube-map to Equirectangular


## Setup

Convert360 is available as a pip package.

```sh
pip install convert360
```

## Usage

```
convert360 -h
usage: convert360 [-h] -i FILE -o FILE [-s WIDTH HEIGHT] [-it TYPE] [-ot TYPE]

Cube-map to equiretangular conversor.

optional arguments:
  -h, --help            show this help message and exit
  -i FILE, --input FILE
                        Equiretangular video to be converted.
  -o FILE, --output FILE
                        Output cube-map video.
  -s WIDTH HEIGHT, --size WIDTH HEIGHT
                        Cube faces size in pixels.
  -it TYPE, --input-type TYPE
                        Cube faces size in pixels.
  -ot TYPE, --output-type TYPE
                        Cube faces size in pixels.
```


## Licence

[GPLv3 License](https://opensource.org/licenses/GPL-3.0)


