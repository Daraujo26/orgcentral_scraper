## OrgCentral Web Scrapper

Link to OrgCentral home: https://orgcentral.psu.edu/organizations

This script pulls data from each club listed in the link above. If you're interested in playing with the script I included steps below for setting up the environment and running it:

To start you can clone this repo locally:

```
git clone https://github.com/Daraujo26/orgcentral_scraper.git
cd orgcentral_scraper/
```

Next set up your environment:

#### If you have experience with this, you can set up your own enviroment then it should work by just installing selenium:
```
pip install selenium
```
or
```
pip install -r requirements.txt
```

#### Env setup:

I recommend using conda, theres instructions to install it here: https://docs.anaconda.com/miniconda/ 

Once you've installed this create and activate an environment:
```
conda create -n ibm -y
conda activate ibm
```

Then install dependancies
``` 
pip install -r requirements.txt
```

#### To run the script:
```
python main.py
```
