# GloomLog

GloomLog is an unofficial application for logging Gloomhaven campaigns. It is spoiler free, runs from the command line and was build in Python.

GloomLog uses the term Encounter to overarch different things characters can do in the game, such as Scenarios, City events, Donations to the sanctuary, but also unlocking Item designs etc. This makes both the code and the app more modular. With a little creativity and/or tinkering you might be able to use or rebuild this app to log D&D campaigns or other legacy games.

## Design notes

GloomLog was setup with the following principles in mind:

- Spoiler free: There is no unlockable content from the game in the source code.
- As Python native as possible: This to avoid compatibility issues between Windows/Unix. Therefore, it is a simple CLI app.
- Fast logging: Slowly navigating a GUI is the last thing I want to do while playing a boardgame. Most queries from the app have hotkeys. Check them out by selecting "help" or hotkey "h".
- Parallel game worlds: Gloomhaven is well designed to allow multiple parties roaming the same game world. Some players might still prefer to keep their game world separate from other player's parties. GloomLog can keep track of multiple save files. (Bear in mind that save files can contain spoilers for other groups.)

The app now only allows for logging past adventures. The source code contains "# TODO" comments for what I play to implement. Most notably, projecting your options based on your past adventures.

## Personal note

One of my main drivers to build this application is learning Python. I tried to refactor as much stupid decision from the past out of the source code, but well, you probably know how things like these go... As a result, you might encounter some things that clearly indicate my learning curve and some over-engineering here and there.

Anyway, feel free to contribute to this project, log your latest adventures and, most of all, enjoy Gloomhaven!
