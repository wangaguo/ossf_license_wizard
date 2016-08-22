#!/bin/sh
perl -MXML::Simple -MData::Dumper -e 'print Dumper(new XML::Simple(ForceArray => 1)->XMLin("LicenseWizard.xml"))' > data.pl
