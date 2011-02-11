var google_rss = document.getElementById("google_rss");
google.load("feeds", "1");
function initFeed() {
  var google_rss_url = 'http://news.google.com/news?hl=en&safe=off&prmdo=1&q=xss&um=1&ie=UTF-8&output=rss';
  var feed = new google.feeds.Feed(google_rss_url);
  feed.load(function(result) {
    if (!result.error) {
      var cnt = result.feed.entries.length;
      if (0 < cnt) {
        var html = '';
        for ( var i = 0; i < cnt; i++) {
          var entry = result.feed.entries[i];
          html += '<li><a href="' + entry.link + '">' + entry.title + '</a></li>';
        }
        google_rss.innerHTML = '<ul>' + html + '</ul>';
      } else {
        google_rss.style.display = 'none';
      }
    } else {
      google_rss.style.display = 'none';
    }
  });
}
google.setOnLoadCallback(initFeed);