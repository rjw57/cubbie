# cubbie: real time ticket sales for theatre productions

[![Build Status](https://travis-ci.org/rjw57/cubbie.svg?branch=master)](https://travis-ci.org/rjw57/cubbie)

**IMPORTANT: the fetch-deps.sh script *must* be run first.**

## Launching the UI

The UI webapp is in a separate module from the main cubbie API app. To run a
full UI:

```console
$ cubbieui -c $PWD/dev.cfg runserver
```

## Tips

Running manager with the in-development configuration. E.g. to upgrade the development database.

```console
$ cubbie -c $PWD/dev.cfg db upgrade
```
