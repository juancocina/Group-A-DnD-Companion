* This is for implementing the background music player *

You MUST include the following files:

    - musicplayerstyles.css
    - musicplayer-popup.js

In order for the HTML inside of

    - youtubetest.html

to work

How to implement into a another page...

1) Make sure the top links include the proper .css and .js

Specifically these:
    <!-- external links -->
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
      <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans+Condensed:300">
    <!-- scripts to open up the pop up window -->

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script src="/static/bgm/musicplayer-popup.js"></script>

    <link rel="stylesheet" href="{{ url_for('static', filename='/bgm/musicplayerstyles.css') }}" />


2) Find the section of the HTML code labeled, <!-- pop-up tab information -->
and copy that until you reach, <!-- end of pop-up tab -->

Paste this inside the file you want, in the location that you want the pop-up tab to inhabit

3) Find the section of HTML code labeled, <!-- pop up window -->
and copy until you reach,  <!-- end of pop up window -->

This is to be pasted, preferably, right after the pop up tab code, but whatever works best for you.

4) Done

Just make sure file locations are properly sorted inside the HTML file. Other than that, should be good
Ask me if you have any questions...
