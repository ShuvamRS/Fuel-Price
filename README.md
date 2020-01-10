# Fuel Price USA

## Features
* Query fuel price by providing fuel type, area, and date. Price for nearest date is displayed if data is unavailable for the date specified.
* Visualize and compare fuel prices on line-graph.
* Scroll through end-of-year fuel prices presented in choropleth map.


## Prerequisites
To get started, ensure you meet the following requirements:
* You are using python-3.7.3.
* You have pip installed in your system.
* You have installed all packages mentioned in requirements.txt using pip.


## Try it out!
* Clone or download the repository to your local machine.
* Run scraper.py to fetch fuel price data which gets stored into SQLite database.
* Run main.py and view this website by visiting localhost:5000 in your browser.


## Limitations
* Input date picker not working on Safari as it does not support input type="date". Users will have to enter date in yyyy-mm-dd format.
* Improvement in CSS implementation needed to make the website more mobile-friendly.


## Acknowledgements
* Web Crawling implemented to extract fuel price data from U.S. Energy Information Administration's website for Independent Statistics & Analysis: https://www.eia.gov.
* Background image downloaded from https://i1.wp.com/glocalkhabar.com/wp-content/uploads/2016/08/fuel-1.jpg?fit=1280%2C850&ssl=1.
