# CupStats

An Application for Understanding the Demographic and Economic Factors that Affect Performance in the FIFA World Cup designed for Yale's CPSC437 Course

[Live Version](http://worldcupstats.herokuapp.com)

[Writeup Link](https://docs.google.com/document/d/1ngWLvT6U1L-217UM_h_rnLq7EhyUDC64bXxgAtj0oC8/edit) (requires Yale email address to access)

### Description
CupStats is an application that allows the user to explore how demographic and economic factors of a country potentially correlate with its ability to be successful in the FIFA World Cup. The application provides several interfaces for analyzing demographic and World Cup competition data including an interactive world map, graphs, and tables. The world map can be colorized based on different variables and comparisons to provide insights into how countries compare. The graphs provide a more in-depth view of the historical trends on a country-specific basis by presenting time series data of different variables, allowing the user to compare trends in country statistics with world cup success. Overall, this application serves as a data exploration tool for users who may be interested in understanding some of the dynamics of World Cup performance and what qualities of a country may influence success.

### Functionality
- **Global View:** View world map colorized by economic characteristics of any country that has ever qualified to the World Cup as well as colorized by ratios of World Cup wins to various economic stats.
- **Country Specific View:** View information on total historical World Cup success as well as current country economic and geopolitical data.
- **Country Specific Historical Graphs:** View graph of every World Cup year along with the number of wins by the country in that year as long as trend lines of population, GDP, and life expectancy.
- **Searchable Tables:** Tables for each of the sets of data we collected that allows you to view all the data and search through it, with autocorrect. 

### Deployment
1. Run necessary scraping scripts in order to collect data and place data into a local Postgres installation.
2. Export the database URL for your local database including username and password with `export DATABASE_URL="<DB_URL>"`.
3. Create a virtual environment with `virutalenv <env_name>`. Make sure your virutalenv is using Python 2.7.
4. Install requirements with `pip install -r requirements.txt`.
5. Run locally with `python app.py`.
6. Navigate to [localhost:5000](http://localhost:5000).
