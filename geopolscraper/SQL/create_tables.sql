create table country_geopol (
Country varchar(50),
Continent varchar(150),
Land_Area real,
Border_Length real);

create table country_year_geopol (
country varchar(50),
Country_Code varchar(5),
year int,
GDP real,
Population real,
Life_Expectancy real,
Urbanization_Percentage real,
Per_Capita_GDP real);

COPY country_geopol(country, continent, land_area, border_length)
from STDIN
delimiter ',' csv header;

COPY country_year_geopol(country, country_code, year, gdp, population, life_expectancy, urbanization_percentage, per_capita_gdp)
from STDIN
delimiter ',' csv header null as 'NA';