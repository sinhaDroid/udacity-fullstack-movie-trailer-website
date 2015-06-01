import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Pooglia's Picks</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            font-size: 12px;
            font-weight: bold;
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 30px;
            padding-top: 30px;
            padding-bottom: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        /* area below the navbar holding the bootstrap well and criterion info */
        #legend {
            margin-top: 10px;
            font-weight:bold;
            padding-left: 20px;
            font-size: 16px;
        }
        /* area below the bootstrap well */
	#instruct {
            padding-left: 20px;
            font-style: italic;
	}
        /* year and title colors */
        h2, h4 {
            color: #084B8A;
        }
        /* makes sure the navbar links float to the right  and stack when the browser is minimized */
        ul.nav.navbar-nav {
            float: right;
            padding-right: 20px;
        }

    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Pooglia's Picks - Cinema by Cats</a>

                <ul class="nav navbar-nav">
        <li><a href="https://twitter.com/p00gz">@p00gz</a></li>
        <li><a href="https://github.com/p00gz">GitHub</a></li>
              </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="well" id="legend">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/The_Criterion_Collection_Logo.svg/63px-The_Criterion_Collection_Logo.svg.png"> = Criterion Collection
    </div>

    <div class ="afterwell" id="instruct">
      Click the movie thumbnails to view the original theatrical trailer!
    </div>

    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>

'''
# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{art}" width="220" height="342">
    <h2>{movie_title}</h2>
    <h4>{release_date} <img src="{criterion_icon}" width="20" height="20"></h4>
    Directed by: {movie_director}
    <p>
    Starring: {movie_actors}
</div>

'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page

    content = ''
    for movie in movies:
        if movie.criterion is False:
            '''
            if conditional will insert tiny 1x1 pixel transparent image as a
            placeholder that will be rendered by the HTML template when there
            is a False boolean present for movie.criterion
            '''
            movie.criterion_icon = "https://upload.wikimedia.org/wikipedia/commons/c/ca/1x1.png"

            # Extract the youtube ID from the url
            youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_url)
            youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_url)
            trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

            # Append the tile for the movie with its content filled in

            content += movie_tile_content.format(
                movie_title=movie.title,
                art=movie.art,
                movie_director=movie.director,
                release_date=movie.release_date,
                movie_actors=movie.actors,
                trailer_youtube_id=trailer_youtube_id,
                criterion_icon=movie.criterion_icon
            )
        else:
            '''
            else conditional will insert the Criterion logo image that will be
            rendered by the HTML template when there is a True boolean present for movie.criterion
            '''
            movie.criterion_icon = ("https://upload.wikimedia.org/"
                                    "wikipedia/commons/thumb/5/5d/"
                                    "The_Criterion_Collection_Logo.svg/"
                                    "63px-The_Criterion_Collection_Logo.svg.png")

            youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_url)
            youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_url)
            trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

            # Append the tile for the movie with its content filled in

            content += movie_tile_content.format(
                movie_title=movie.title,
                art=movie.art,
                movie_director=movie.director,
                release_date=movie.release_date,
                movie_actors=movie.actors,
                trailer_youtube_id=trailer_youtube_id,
                criterion_icon=movie.criterion_icon
            )

    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the placeholder for the movie tiles with the actual dynamically generated content
    rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)  # open in a new tab, if possible
