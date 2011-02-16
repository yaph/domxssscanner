jQuery(function($) {
  DOMXSS.scanResponse($);
  if ("undefined" != typeof script_urls) {
    var urls = $.parseJSON(script_urls)
    for (url in urls) {
      var request_url = "/scan?url=" + encodeURIComponent(urls[url]);
      $.get(request_url, function(data) {
        $('#responses').append(data);
        DOMXSS.scanResponse($);
      });
    }
  }
});

var DOMXSS = {
  // regular expressions from https://code.google.com/p/domxsswiki/wiki/FindingDOMXSS
  re_sources: new RegExp(/(location\s*[\[.])|([.\[]\s*["']?\s*(arguments|dialogArguments|innerHTML|write(ln)?|open(Dialog)?|showModalDialog|cookie|URL|documentURI|baseURI|referrer|name|opener|parent|top|content|self|frames)\W)|(localStorage|sessionStorage|Database)/g),
  re_sinks: new RegExp(/((src|href|data|location|code|value|action)\s*["'\]]*\s*\+?\s*=)|((replace|assign|navigate|getResponseHeader|open(Dialog)?|showModalDialog|eval|evaluate|execCommand|execScript|setTimeout|setInterval)\s*["']]*\s*\()/g),

  source_count: 0,
  sink_count: 0,

  highlight: function(text) {
    text = text.replace(DOMXSS.re_sinks, function(m){
      DOMXSS.sink_count++;
      return 'DOMXSS_SINK_START' + m + 'DOMXSS_END';
    });
    text = text.replace(DOMXSS.re_sources, function(m){
      DOMXSS.source_count++;
      return 'DOMXSS_SOURCE_START' + m + 'DOMXSS_END';
    });
    return text;
  },
  markUp: function(text) {
    text = text.replace(/DOMXSS_SINK_START/g, '<span class="domxss_sink">');
    text = text.replace(/DOMXSS_SOURCE_START/g, '<span class="domxss_source">');
    text = text.replace(/DOMXSS_END/g, '</span>');
    return text;
  },
  scanResponse: function($) {
    DOMXSS.source_count = 0;
    DOMXSS.sink_count = 0;
    $('.response_text').each(function(idx, elt) {
      //http://debuggable.com/posts/encode-html-entities-with-jquery:480f4dd6-13cc-4ce9-8071-4710cbdd56cb
      //var text = $(elt).text(DOMXSS.highlight(elt.innerHTML)).html();
      var text = DOMXSS.markUp(DOMXSS.highlight(elt.innerHTML));
      var p = $(elt).parent();
      var t = p.parent();
      p.remove();
      t.append('<h3>Number of sources found: <span class="domxss_source">' + DOMXSS.source_count + '</span></h3>');
      t.append('<h3>Number of sinks found: <span class="domxss_sink">' + DOMXSS.sink_count + '</span></h3>');
      t.append('<pre class="domxss_highlighted">' + text + '</pre>');
    });
  }
};