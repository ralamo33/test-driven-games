# TestDrivenGames
Checkers is now fully playable! Go to controller and run the file. You can use the env folder for your venv.


### Accomplished & Roadmap
1. Understanding of UV
2. Understanding of Tailwind CSS and HTML

Todo
1. Make tailwind CSS a build step dependecy
2. Refactor main, and index.html to actually display the game properly
3. Refactor into folders


How does tailwind CSS work as a build dependency?

Lets start with how HTML script tags work.
They indicate javascript that needs to be run by the browser. If you say, had a script tailwindcss cdn tag, then the browser would know once it got the HTML, that it needed to retrieve the code at that CDN & run it. In this case it would retrieve tailwind, which would go through the HTML, find out which tailwindcss classes were being used, create css file to match tailwind class to css, and then watch for any updates that would add new classes to the css file. This requires the user to do a lot of hydrating when the browser loads

To do it at build, the user insteads uses a tailwind command to create a minified css file with all the necessary css files. This all happens in the build phase so that file is available to the server when it deploys. Then that file is what is called when 