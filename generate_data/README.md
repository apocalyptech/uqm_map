Getting Map Data From UQM
=========================

This process is rather convoluted, and one that I haven't actually done
back-to-front since I initially started work on this project, back in 2007
or so.  This process could really use some streamlining, but I've not felt
the impulse to rewrite it to be more sensible yet.

Here's the overall steps that were taken:

1. Patch UQM to include extra information in its `dumpUniverseToFile`
   debugging routine.  (`dumpUniverseToFile` already contains much of
   what we're after, including the list of systems and planets)

2. Build a debug build of UQM with `dumpUniverseToFile` enabled, and run
   it.  This creates the file `PlanetInfo`.

3. Use the Perl script `import.pl` to parse the flat-text `PlanetInfo`
   file and import it into a MySQL database (credentials currently
   must be hardcoded into that script).  Early versions of this utility
   actually read the information directly out of a database, hence this
   step.

4. Use the Python script `exportdb.py` to generate a gzipped JSON file
   based on the information in the database.  Database configuration is
   configured more sanely here; just run the script and it'll tell you
   how to do it.  This used to write to a Python Pickle rather than JSON,
   actually, and was only changed to JSON during the PyQt porting process.

Pretty stupid, yes?  The first two steps are pretty unavoidable, since the
planet data is generated pseudorandomly by UQM (with a fixed seed, so it
remains consistent acrosss playthroughs).  Steps 3+4 should really be combined
into a single script which just goes right from `PlanetInfo` -> `uqm.json.gz`.

Patching UQM
------------

I've provided the patch I used as `uqm-0.6.2-mineraldata_and_bio.patch`.

When I did this in 2007, the most recent UQM version was 0.6.2, which is what
this patch is built against, and I have not tried applying it to 0.7.0.  The
internal directory structure has changed betwen those versions, but both files
patched (`uqmdebug.c` and `uqmdebug.h`) exist in the same directory, so I bet
it'll probably still apply if you strip off some directory levels with patch's
`-p`.  Specifically, `sc2/src/sc2code` has become simply `src/uqm`.  Much
nicer!

Anyway, as for the details of what the patch does, it's reasonably
straightforward.  First it enables the `dumpUniverseToFile` hook, and alters
the formatting of the planet labels a bit.  Planet coordinates are left as
numbers ranging from 0-9999 rather than 0.0-999.9.  It adds a loop so that
the mineral details of each planet are explicitly output, instead of just
giving the whole mineral value.

Finally, it does a bit of logic to determine what I consider to be "dangerous"
biologics on the planet.  Basically, to be considered dangerous, the creature
has to actively hunt the player, have a speed level greater than one, and a
danger level of greater than one.  Those values work pretty well for me, though
it might be nice to export all the info to `PlanetInfo` and let the user decide
what to consider dangerous.

As to actually *building* UQM in debug mode, I assume that's not difficult.
See UQM's own docs for building it, and flip whatever seems to need flipping to
turn it into a debug build.  :)
