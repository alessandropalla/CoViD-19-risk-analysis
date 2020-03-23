
# CoVid-19 Outbreak Analysis

## Introduction

This project goal is to build an epidemic prediction model from the public available infection data using machine learning techniques.

***A technical discussion abut the methodology is coming soon***

## Discaimer

I'm not an expert epidemiologist but an engineer/data scientist. This means that I've no medical authority on this topic and therefore I take no responsability for any forecast/misuse of this model.

***Extrapolate at your own risk***

Also, in places with few patients the dataset is not big enough to have statistical relevance

Any suggestion/critic is therefore highly appreciated . If you want to contribute, please open an issue in github.

## Installation

Install python and pip3

```(bash)
sudo apt-get install python3.6
sudo apt-get install python3-pip
```

Create a python virtual environment

```(bash)
virtualenv -p /usr/bin/python3.6 venv
source venv/bin/activate
```

Install dependencies

```(bash)
make install
```

## How to run

Start a jupyter notebook server with

```(bash)
jupyter notebook
```

Open the `Training.ipynb` notebook to train and test the machine learning model and predict the epidemic in different countries

## Acknowledgements

Many thanks to Johns Hopkins University for the amazing dashboard and the daily update github [dataset](https://github.com/CSSEGISandData/2019-nCoV)