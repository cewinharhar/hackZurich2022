# RenAG - Responsability Energy AG
## Responsibility platform for the reduction of energy usage of swiss companies

# HackZürich2022 

Installation

Download the code, install required Python packages with

```
pip install -r requirements.txt
```

Deploy the backend on your localhost with

```
export FLASK_APP=app
flask run
```
## About the webpage:

The front page is a is a leaderboard consisting of different companies. They are rated relative to every other company participating and the score is weighted on electricity consumed and, to a lesser extent, the water consumed. The value on the right is the total electricity consumed over the course of the month. The green or red value under it is the difference of electricity consumed based on the current month and the previous month.

When you click the company you landed on the company page. Here we can see their electricity consumption over the course of the year. And gauge on the right is their overall score based on a per company basis and is based purely on water or electricity consumed. The badge seen on the top right of the company page is based on the companies electricity performance over the year.


## About the data:

The data was randomly generated and that is why some of the values may seem strange. The data we are after is not publicly availble but does exist. so the plan would be to get companies to willingly participate and share their data for various incentives we could provide. Check our creator_space for more information: https://app.creatorspace.dev/kevinyar/projects/IX8dmNVmIttlHCKI

## About the goal

The goal of the project was to develope a platform for companies to evaluate and compare their electricity usage and compete with other companies for the RenAG badge which shows the monthly effort (reduced electricity consumption relative to the rest of month). The main interest for companies to participate on this platform is the annual energy reduction certificate which is issued in  
