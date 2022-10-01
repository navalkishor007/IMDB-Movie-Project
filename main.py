# Movie Api Project
import psycopg2
import requests


# when we search by Imdb Id or by the movie title at that time movie is available in database
# then it will be shown if it is not available then it will call API and store the data into database.

# i have used PostgreSql as database
conn = psycopg2.connect(database="move_project_db", host="localhost", user="navalkishor", password="welcome@123")
cr = conn.cursor()

def search_movies(search):
    url = "http://www.omdbapi.com/?t="+search+"&apikey=c0dcf7df"
    response = requests.get(url)
    print(response)
    data = response.json()
    print(data)

class MovieDatabase:
    Head_Line = ' ------------------------------------------- Search Your Movies Here! -----------------------------------'
    Movies = '----------------------------------- Movies From IMDB and From Local Database -------------------------------------'
    print(Head_Line + '\n' + Movies)

    def insert_data(self, title, release_year, rating, imdb_id, genres):
        array = [genres]
        query = 'insert into movies(title, release_year, rating, imdb_id, genres) values(%s, %s, %s, %s, ARRAY[%s]);'
        vals = (title, release_year, rating, imdb_id, array)
        try:
            cr.execute(query, vals)
            conn.commit()
        except:
            print("___________Movie might be existing try to search by IMDB Id____________")
            print("_________________Note:- Search is case sensetive___________")

    def operations(self):
        print("Enter 1 for searching movie by Title")
        print("Enter 2 for searching movie by IMDbId")
        print("Enter 3 for searching movie by Released year")
        print("Enter 4 for searching movie by Rating")
        print("Enter 5 searching movie by genres")
        try:
            selection = int(input("Enter Your Selection:"))
            self.selection(selection)
        except:
            print("__________________Enter Valid Input_____________________")
            self.operations()


    def selection(self, selection):
        if selection == 1:
            self.search_by_title()
        elif selection == 2:
            self.search_by_id()
        elif selection == 3:
            self.search_by_released_year()
        elif selection == 4:
            self.search_by_rating()  # include rating more than entered rating
        elif selection == 5:
            self.search_by_genres()

    def search_by_title(self):
        entered_id = str(input("Enter Movie title: "))
        query = 'select * from movies where title ~ %s'
        id = (entered_id, )
        cr.execute(query, id)
        data = cr.fetchall()
        if len(data) < 1:
            url = "http://www.omdbapi.com/?t=" + entered_id + "&apikey=c0dcf7df"
            response = requests.get(url)
            data = response.json()
            title = data['Title']
            year = data['Year']
            rating = data['imdbRating']
            imdb_id = data['imdbID']
            genres = data['Genre']
            self.insert_data(title, year, rating, imdb_id, genres)
        else:
            print(data)

    def search_by_id(self):
        entered_id = str(input("Enter Movie IMDB Id: "))
        query = 'select * from movies where imdb_id = %s'
        id = (entered_id, )
        cr.execute(query, id)
        data = cr.fetchall()
        if len(data) < 1:
            url = "http://www.omdbapi.com/?i=" + entered_id + "&apikey=c0dcf7df"
            response = requests.get(url)
            data = response.json()
            title = data['Title']
            year = data['Year']
            rating = data['imdbRating']
            imdb_id = data['imdbID']
            genres = data['Genre']
            self.insert_data(title, year, rating, imdb_id, genres)
        else:
            print(data)

    def search_by_released_year(self):
        entered_id = str(input("Enter Movie Release Year: "))
        query = 'select * from movies where release_year = %s'
        id = (entered_id,)
        cr.execute(query, id)
        data = cr.fetchall()
        if len(data) < 1:
            print('No data available')
        else:
            print(data)

    @staticmethod
    def search_by_rating():
        entered_id = str(input("Enter Movie Rating: "))
        query = 'select * from movies where rating >= %s'
        id = (entered_id,)
        cr.execute(query, id)
        data = cr.fetchall()
        if len(data) < 1:
            print('No data available')
        for vals in data:
            print(vals)

    def search_by_genres(self):
        entered_id = str(input("Enter Movie Genres: "))
        query = 'select * from movies where %s =ANY(genres)'
        id = (entered_id,)
        cr.execute(query, id)
        data = cr.fetchall()
        if len(data) < 1:
            print('No data available')
        for vals in data:
            print(vals)

    @staticmethod
    def create_tables():
        query = '''CREATE TABLE if not exists movies (
                   id serial PRIMARY KEY,
                   title varchar(200),
                   release_year integer,
                   rating varchar(10),
                   imdb_id varchar(20) UNIQUE,
                   genres TEXT []);'''
        cr.execute(query)
        conn.commit()

if __name__ == '__main__':
    movie = MovieDatabase()
    movie.create_tables()
    movie.operations()
