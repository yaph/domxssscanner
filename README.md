[DOM XSS Scanner](http://domxssscanner.geeksta.net/) is an online tool that
facilitates code review of web pages and JavaScript code for potential
DOM based XSS security vulnerabilities.

## Sample Results Page

![Sample Results Page](/static/img/domxssscanner-results.jpg)

[Check your Web page](http://domxssscanner.geeksta.net/)

Learn more about the tool on the project's [about page](http://domxssscanner.geeksta.net/info/about).

## Install

Clone this repository and download the [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python). Extract the SDK archive and add aliases for the dev server and update programs, for example:

    alias gae_pyserver='python PATH_TO_SDK/google_appengine/dev_appserver.py'
    alias gae_update='python PATH_TO_SDK/google_appengine/appcfg.py update'

Then start the dev server in the domxssscanner directory with the command:

    gae_pyserver .

You can then access the application at `http://localhost:8080/`.