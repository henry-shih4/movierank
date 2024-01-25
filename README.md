# movierank


Using Python, I was able to webscrape IMDB for the top 250 movies and their information into a CSV file.
After obtaining the data, I created a PostgresQL database along with a Django webapp to allow for interaction with movies and their data.
I styled the frontend using Tailwind css and used HTMX to add for more user intraction; users can add and remove favorites and also arrange the order to allow other users to see their top favorite movies and what they want to watch next. 

Hosted on digital ocean droplet, using Gunicorn and Nginx. 

http://159.223.188.83/movie-list
