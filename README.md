This repo contains all of the scripts and references to other github repos that are used for the St Catherine website.

**Calendar Events**

**Incognito Mode**

We embed events, calendars, and other objects from One Church, but the embeds break in incognito mode. This script will do its best to detect that the user is in an incognito or private window and will notify them that the site may not work correctly.

Detect Incognito mode repo:
https://github.com/Joe12387/detectIncognito

CDN-based script

    <script src="https://cdn.jsdelivr.net/gh/Joe12387/detectIncognito@v1.3.0/dist/es5/detectIncognito.min.js"></script>

Test with https://detectincognito.com/