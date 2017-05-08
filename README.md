# GPS Figure Drawer

This package implements a generalized processor sharing (GPS) simulator with linear-time complexity. It also provides an interface for demonstrating the results, which is the GPS figure. GPS figure is a simple figure that shows the GPS virtual times (i.e., GPS virtual start/finish time) of all packets per flow. More details you can refer to the paper - [A generalized processor sharing approach to flow control in integrated services networks: the single-node case](http://dl.acm.org/citation.cfm?id=159914). Besides, `example.pdf` gives an example of how GPS figure looks like. 

## Install Dependencies

This package depends on the following packages

* flask
* flask_script

You can simply install them by using,

```shell
sudo pip install -r requirements.txt
```

Note, if you want to install it for `Python 3` 
you might need to change `pip` to `pip3`.

## Usage

Go to directory where `GPSSimctl.py` locates, and open a terminal there, and then type the following shell commands in the terminal:

```shell
python ./GPSSimctl.py make_tex --help
```

It will show ypu how to manage the options like below,

```shell
usage: GPSSimctl.py make_tex [-?] [--input INPUT] [--template TEMPLATE]
                             [--template-dir TEMPLATE_DIR] [--output OUTPUT]
                             [--output-dir OUTPUT_DIR]

Generate GPS figure

optional arguments:
  -?, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Input data (default: packets.txt)
  --template TEMPLATE, -t TEMPLATE
                        OPTIONAL: template file
  --template-dir TEMPLATE_DIR, -D TEMPLATE_DIR
                        OPTIONAL: directory which stores your template
  --output OUTPUT, -o OUTPUT
                        Output filename (default: example.tex)
  --output-dir OUTPUT_DIR, -d OUTPUT_DIR
                        OPTIONAL: directory to store output file
```

Note that, the input format should be as follows.

```shell
[weight:] arrival_time length, arrival_time length, ...
```

Here, each line corresponds to a flow, where `weight` is the weight for the respective flow, which is optional. If you do not input `weight`, the default weight (i.e., **1**) will be used. The following data are the arrival time and length for each packet in the flow. Packets are separated by `,` and arrival time and length are separated by  ` `. Note that, `weight` can be any positive float number, where `arrival time` and `length` can only be integers. 

Note that, you should make sure that no two packets from the same flow have the same arrival time, otherwise, the results will not be unique.

`packets.txt` shows you an example.



