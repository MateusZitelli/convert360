<h1 align="center">
Convert360 🌎
<br/>
<i>360 degree media toolkit (WIP).</i>
<br/>
<img width=150 src="https://raw.githubusercontent.com/MateusZitelli/convert360/master/assets/mercator.jpg" ></img>
</h1>

> GPU accelerated command line tool to convert 360 images and videos between different projections.

### Supported Convertions

- [x] Equirectangular to (connected) cube-map
- [ ] Cube-map to Equirectangular


## Setup

*Convert360* is available as a pip package and **requires FFMpeg**.

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
                        Input projection type.
  -ot TYPE, --output-type TYPE
                        Output projection type.
```


## Example

```sh
$ convert360 -i ~/Pictures/Barcelona/sagrada-familia.jpg -o example.png -s 300 300
```

<img width=900 src="https://raw.githubusercontent.com/MateusZitelli/convert360/master/assets/example.png" ></img>

```sh
$ convert360 -i ~/Pictures/Barcelona/sagrada-familia.jpg -o example.png -s 300 300 -ot connected-cubemap
```

<img width=900 src="https://raw.githubusercontent.com/MateusZitelli/convert360/master/assets/example2.png" ></img>


## Licence

[GPLv3 License](https://opensource.org/licenses/GPL-3.0)


