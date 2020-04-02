# if-covid19-keeps-accelerating
putting projections in historical context

created for the [CoViD-19 Global Hackathon](https://covid-global-hackathon.devpost.com/)

[check it out](if-covid19-keeps-accelerating.com)


### get it running

first need to set up a virtual environment

`virtualenv .env`

`source .env/bin/activate`

then, make sure to install requirements

`sudo python3 -m pip install -r requirements.txt`

you may need to also add aws configuration details

`aws configure`

then you can intialize zappa and then deploy

`zappa init`

`zappa deploy dev`