our $data = do 'data.pl' || require XML::Simple && new XML::Simple(ForceArray => 1)->XMLin("LicenseWizard.xml");
print keys(%{ $data->{Questions}->[0]->{Question} });
