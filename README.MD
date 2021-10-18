## Exploring second-hand house transaction in Shanghai

### Project goals
This interactive data science application aims to explore a second-hand house transaction dataset. The dataset is comprised of 34355 second-hand house transaction records in Shanghai between 2012-2017.

The goal of all the visualizations is to enable users to answer the below question:

> **What determines the unit price of house transcations in Shanghai?**

A series of visualizations are implemented to help better understand the dataset and explore the potential factors. 


### Design decisions
#### 1. Scatter plot in Map: Unit Price By Location
While thinking about house transactions, the first and most important factor that comes to my mind is location.

Therefore, I decided to explore the relation between house and location first and use map to depict the location distributions.

Each small circle is a transaction with radius representing the total amount of transaction price.

The color density indicates the unit price of the house. If the the unit transaction price is below 80k per/square meter, its color is white. If the unit transaction price is higher than 120k per/square meter, then the color is red. So the color density reflects different levels of unit price.


#### 2. Bar charts: Unit Price By District
Because business, education resources, and hospital resources in different districts is different, so district is another factor that will influence house transaction price. Therefore, I calculated the average unit transaction price for each district and decided to present it with bar chart.

Users could choose to add or delete districts from the bar chart to make the comparisions more straightforward and intuitive.


#### 3. Scatter plot by area and year: Change Of Unit Price From 2012-2017
- It's interesting to explore the correlation between total price and unit price of a second-house. In early years, because few people can afford expensive houses, so the average unit price for large houses is actually cheaper. But as time goes by, when large houses become scare resources, the average unit price of large house actually grows. Therefore, I calculated the average unit price of different area at an interval of 5. Originally, I plan to plot with a line chart. However, because there are some missing point for some areas, line chart will be imcomplete. Therefore, I decided to use scatter plot to show such correlation.

- Year is definetly an important factor that will influence house price. House prices grows as time goes by. Therefore, users could explore such change by selecting different years. 


### Development process
Because this is a solo project, so I implemented all the process by myself. It tooke me around two days to develop this visualization application (around 5 hours + 5 hours).

Actually the visualization is not the most time-consuming part for me. It took me a lot of time to think about which dataset to use and what kind of research question would be meaningful to explore.

As for the difficulty of realizing different components, the first one is definitely harder than the rest. First, because it's the first one to impelemet, so I spent a lot of time on familiarizing myself with the API. After completing the first plot, rest of the work becomes much easier.