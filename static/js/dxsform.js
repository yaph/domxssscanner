jQuery(function($) {
  var HTML = '<div id="dxsheaderform" style="position:fixed;top:0;background:#002f00;width:100%;text-align:center;padding:.5em;">'
    + '<a href="/" style="position:absolute;margin:.2em 0 0 12%;width:5%;text-decoration:none;font-weight:bold;">Home</a>'
    + '<form action="/scan" method="GET">'
    + '<input style="width:40%;" name="url" id="url" type="url" value="http://">'
    + '<input style="width:20%;margin-left:.3em;" type="submit" value="Start DOM XSS scan">'
    + '</form></div>';
  $('#container').attr('style','padding-top:2.5em;');
  $('body').prepend(HTML);
});