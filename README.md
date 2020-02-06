# Report Generator

Sample PDF generator with graphs. The graphs are created with matplot lib and saved as PNG image to be later inserted into the pdf file. The data is fetched from world bank and represent population of US, UK and Spain. The pdf file is generated using FPDF. 

### Installation

You might want to create a venv before downloading the dependencies:

```sh
$ pip install virtualenv
$ virtualenv venv 
```
Once you have the venv set up you can activate it and donwload the dependencies:

```sh
$ source venv/bin/activate
```

Now to to download the dependencies:

```sh
$ pip install requirements.txt
```
