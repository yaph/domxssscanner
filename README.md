[DOM XSS Scanner](http://www.domxssscanner.com/) is an online tool for scanning web pages and JavaScript code for potential DOM based XSS security vulnerabilities.

## Sample Results Page

![Sample Results Page](/static/img/domxssscanner-results.jpg)

[Check your Web page](http://www.domxssscanner.com/)

## TODOs
- Check whether it's possible to have sub directories in templates dir, which worked in Django 0.96 but not in 1.2 (see http://stackoverflow.com/questions/1081949/differences-in-django-template-inheritance-between-0-96-and-1-0) or use a better template engine

## Known Issues
- the regular expression for sources document.write( which is a sink
- cannot access page_url template var created in gae_utils.py in templates

Learn more about the tool on the project's [about page](http://www.domxssscanner.com/info/about)