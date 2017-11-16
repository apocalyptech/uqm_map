#!/usr/bin/perl -w
# vim: set expandtab tabstop=4 shiftwidth=4:

use strict;
use DBI qw( :sql_types );

# DB info
my $dbhost = 'hostname';
my $dbuser = 'username';
my $dbpass = 'password';
my $dbname = 'database';

# File info
my $filename = 'PlanetInfo';

# Open the file
my $DF;
open DF, $filename or die "can't open $filename";

# Connect to DB and set up stored procs
my $dbh = DBI->connect("dbi:mysql:hostname=$dbhost;database=$dbname", $dbuser, $dbpass);
if (!$dbh)
{
    die "Couldn't connect to DB";
}
my $sth_sys = $dbh->prepare('insert into system (name, position, x, y, stype, extra) values (?, ?, ?, ?, ?, ?)');
my $sth_pln = $dbh->prepare('insert into planet (sid, pname, ptype, tectonics, weather, temp, gravity, bio, bio_danger, ' .
    'mineral, min_common, min_corrosive, min_base, min_noble, min_rare, min_precious, min_radio, min_exotic) ' .
    'values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');

# Clear out existing data
print "Clearing existing tables\n";
$dbh->do('truncate planet');
$dbh->do('truncate system');

# A bunch of vars
my $line;
my $i;
my $sysname;
my $syspos;
my $systype;
my $sysextra;
my $sysid;
my $x;
my $y;
my $plancat;
my $planname;
my $plannamesave;
my $plantype;
my $num_systems = 0;
my $num_planets = 0;

# More planet data
my $tectonics;
my $weather;
my $temp;
my $gravity;
my $bio;
my $bio_danger;
my $mineral;
my $min_common;
my $min_corrosive;
my $min_base;
my $min_noble;
my $min_rare;
my $min_precious;
my $min_radio;
my $min_exotic;

# Now loop
print "Importing new data\n";
while ($line = <DF>)
{
    chomp $line;
    if ($line =~ /^System\t(.*?)\t\((\d+), (\d+)\)\t(.*?)\t(.*?)$/)
    {
        $syspos = '';
        $sysname = $1;
        $x = $2;
        $y = $3;
        $systype = $4;
        $sysextra = $5;
        if ($sysname =~ /(\w+) (\w+)/)
        {
            $syspos = $1;
            $sysname = $2;
        }
        if ($sysextra =~ /(.*)\#(\d+)/)
        {
            $sysextra = $1 . '#' . ($2+1);
        }
        $sysname =~ s/(\w+) (\w+)/$2 $1/;   # Flip so Alpha/Beta/etc is at the end

        $i=1;
        $sth_sys->bind_param($i++, $sysname, SQL_CHAR);
        $sth_sys->bind_param($i++, $syspos, SQL_CHAR);
        $sth_sys->bind_param($i++, $x, SQL_INTEGER);
        $sth_sys->bind_param($i++, $y, SQL_INTEGER);
        $sth_sys->bind_param($i++, $systype, SQL_CHAR);
        $sth_sys->bind_param($i++, $sysextra, SQL_CHAR);
        if ($sth_sys->execute())
        {
            $sysid = $dbh->{'mysql_insertid'};
            $num_systems++;
        }
        else
        {
            print STDERR "Warning: couldn't insert system $sysname\n";
        }

    }
    elsif ($line =~ /^(Planet|Moon)\t(.*?)\t(.*?)$/)
    {
        $plancat = $1;
        $planname = $2;
        $plantype = $3;

        # Normalize the name
        if ($plancat eq 'Planet')
        {
            $plannamesave = $planname;
        }
        else
        {
            $planname = $plannamesave . ' ' . $planname;
        }

        # Initialize vars
        $tectonics=0;
        $weather=0;
        $temp=0;
        $gravity=0;
        $bio=0;
        $bio_danger=0;
        $mineral=0;
        $min_common=0;
        $min_corrosive=0;
        $min_base=0;
        $min_noble=0;
        $min_rare=0;
        $min_precious=0;
        $min_radio=0;
        $min_exotic=0;

        # Loop through attrs
        while ($line = <DF>)
        {
            chomp $line;
            $line =~ s/^\s*//;

            # No more data to get, here
            if ($line eq 'NoScan' or $line eq 'NoAttr')
            {
                last;
            }

            # Load in whatever data we've gotten
            if ($line =~ /Tectonics:\s+(\S+)/)
            {
                $tectonics = $1;
                $tectonics++;
            }
            elsif ($line =~ /Weather:\s+(\S+)/)
            {
                $weather = $1;
                if ($weather > 0)
                {
                    $weather++;
                }
            }
            elsif ($line =~ /Gravity:\s+(\S+)/)
            {
                $gravity = $1;
            }
            elsif ($line =~ /Temp:\s+(\S+)/)
            {
                $temp = $1;
            }
            elsif ($line =~ /Bio: (\S+)\s+Min: (\S+)/)
            {
                $bio = $1;
                $mineral = $2;
            }
            elsif ($line =~ /Dangerous Bio: (\d+)/)
            {
                $bio_danger = $1;
            }
            elsif ($line =~ /Common Minerals:\s+(\S+)/)
            {
                $min_common = $1;
            }
            elsif ($line =~ /Corrosive Minerals:\s+(\S+)/)
            {
                $min_corrosive = $1;
            }
            elsif ($line =~ /Base Metal Minerals:\s+(\S+)/)
            {
                $min_base = $1;
            }
            elsif ($line =~ /Noble Gas Minerals:\s+(\S+)/)
            {
                $min_noble = $1;
            }
            elsif ($line =~ /Rare Earth Minerals:\s+(\S+)/)
            {
                $min_rare = $1;
            }
            elsif ($line =~ /Precious Minerals:\s+(\S+)/)
            {
                $min_precious = $1;
            }
            elsif ($line =~ /Radioactive Minerals:\s+(\S+)/)
            {
                $min_radio = $1;
            }
            elsif ($line =~ /Exotic Minerals:\s+(\S+)/)
            {
                $min_exotic = $1;
            }

            # Break out if we're at the last line
            if ($line =~ /Exotic/)
            {
                last;
            }
        }

        # ... and now insert 'em
        $i = 1;
        $sth_pln->bind_param($i++, $sysid, SQL_INTEGER);
        $sth_pln->bind_param($i++, $planname, SQL_CHAR);
        $sth_pln->bind_param($i++, $plantype, SQL_CHAR);
        $sth_pln->bind_param($i++, $tectonics, SQL_INTEGER);
        $sth_pln->bind_param($i++, $weather, SQL_INTEGER);
        $sth_pln->bind_param($i++, $temp, SQL_INTEGER);
        $sth_pln->bind_param($i++, $gravity, SQL_INTEGER);
        $sth_pln->bind_param($i++, $bio, SQL_INTEGER);
        $sth_pln->bind_param($i++, $bio_danger, SQL_INTEGER);
        $sth_pln->bind_param($i++, $mineral, SQL_INTEGER);
        $sth_pln->bind_param($i++, $min_common, SQL_INTEGER);
        $sth_pln->bind_param($i++, $min_corrosive, SQL_INTEGER);
        $sth_pln->bind_param($i++, $min_base, SQL_INTEGER);
        $sth_pln->bind_param($i++, $min_noble, SQL_INTEGER);
        $sth_pln->bind_param($i++, $min_rare, SQL_INTEGER);
        $sth_pln->bind_param($i++, $min_precious, SQL_INTEGER);
        $sth_pln->bind_param($i++, $min_radio, SQL_INTEGER);
        $sth_pln->bind_param($i++, $min_exotic, SQL_INTEGER);
        if ($sth_pln->execute())
        {
            $num_planets++;
        }
        else
        {
            print STDERR "WARNING: Couldn't insert planet $planname\n";
        }
    }
}

# Clean up
print "Done!\n";
print "$num_systems systems imported.\n";
print "$num_planets planets imported.\n";
close DF;
$dbh->disconnect();
