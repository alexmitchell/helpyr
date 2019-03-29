Helpyr is a collection of helpful python scripts for a variety of tasks, from
image processing to file manipulations. Most of these programs should do
concise tasks reasonably well. Or at least that is the goal.

Helpyr currently has:
- crawler.py -- Crawls through a data directory tree to find desired file and
  perform a given task on them. Current implementation creates symbolic links
  in a new links directory for all the desired data files. (To collect
  scattered files in one place without actually moving anything.)
