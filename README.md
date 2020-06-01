# lyrics-app-djangorestframework

**To see the full live application, visit:<br/>
https://lyrics-app-bf3d0.web.app/**

The full application consists of two apps - a frontend one and a backend one. This is the backend API part.<br/>
You can see the live API application here:<br/>
https://lyrics-app-api.herokuapp.com/api/

Here you can see the code of the frontend (React) part:<br/>
https://github.com/dominiika/lyrics-app-react

**Python** version 3.8.0<br/>
**Django** version: 3.0.2<br/>
**Django Rest Framework** version: 3.11.0<br/>

### Functionality overview

This is a website which enables the user to add lyrics, songs, artists, genres, listen to music and watch videos.
It uses both a custom API and an external API for requests. 

##### General functionality

- fetching data (songs, album images, etc.) from Spotify API
- fetching videos from YouTube API
- fetching lyrics from Genius API
- signing up and logging in
- adding, viewing and editing artists, genres, songs 
- leaving rates 
- leaving comments and likes (not implemented in the frontend app, yet)
- searching for records<br/> 


### Installing and Prerequisites

If you'd like to clone this app and use it locally, then you need to do the following steps.<br/><br/>
First, you need to provide your Spotify, YouTube and Genius tokens and IDs to make fetching data from external APIs possible.<br/>
Do it in the development settings file:

```
SPOTIFY_CLIENT_ID = 'your Spotify client ID'
SPOTIFY_CLIENT_SECRET = 'your Spotify client secret'
YOUTUBE_API_KEY = 'your YT client key'
GENIUS_ACCESS_TOKEN = 'your Genius access token
```

Here are the guides which explain how to get IDs and tokens:
https://developer.spotify.com/documentation/general/guides/app-settings/ <br/>
https://developers.google.com/youtube/v3/getting-started <br/>
https://docs.genius.com/ <br/>


To run the app locally:

1. Clone this repository.

2. Create virtual environment and run it:

```
virtualenv venv

source venv/bin/activate
```

3. Go into the app directory and install dependencies:

```
pip install -r requirements.txt
```

4. Make migrations:

```
python manage.py makemigrations
```

5. Migrate:

```
python manage.py migrate
```

6. Create a superuser:

```
python manage.py createsuperuser
```

7. Finally run the server:

```
python manage.py runserver
```

8. You can visit the app at http://127.0.0.1:8000 or http://localhost:8000

### Usage

1. To see the admin site, go to /admin/ 

2. To see all the users or to register a new one, go to /api/auth/users/

3. Go to /api/auth/token/ to get a token which needs to be passed in the HTML header in order to make the usage of the API available.

4. Go to /api/ to see all available links connected with songs, genres, artists, ratings, comments and likes.

5. To see all the genres or to add a new one, go to /api/genres/

6. To see all the artists or to add a new one, go to /api/artists/

7. To see all the songs or to add a new one, go to /api/songs/

8. To see all the ratings, go to /api/ratings/ 

9. To see all the comments or to add a new one, go to /api/comments/

10. To see all the comment likes, go to /api/comment_likes/

11. To see, edit or delete a particular item, add its ID at the end of the link, e.g. /api/songs/1/

12. To rate a particular song, go to /api/songs/[song-id]/rate/

13. To fetch lyrics, go to /api/songs/fetch/

14.  To like a particular comment, go to /api/comments/[comment-id]/like/ <br/>
If you visit this url again, you'll dislike the comment.

15. To search for a particular value, go to /api/search/all/?value=[your-value]&page_number=1 

<br/>
Bare in mind that some of the requests require json data in the body, POST methods and headers.<br/>
See the views for the reference.
<br/>
<br/>

You can clone the frontend part as well (the link is provided at the beginning of this file), so that you can have a full overview of the application.
