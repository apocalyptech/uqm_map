TODO
====

* The "idnum" fields we store are basically just there because historically
  the original versions of this utility pulled its information out of a
  database, and used the row's PK to do lookups.  The gtk+ version may have
  made some use of them as well, due to the nature of how that was doing
  its GUI work, but I suspect that they're superfluous in the upcoming
  PyQt rewrite/port.  Look in to that.
