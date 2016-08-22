#!/usr/bin/perl
use strict;
use CGI;
use Data::Dumper;
use utf8;

#print ("Content-Type: text/html;\n\n");

sub processAnswers
{
	my ($data, $joinedAnswers) = @_;
	my $questions = $data->{Questions}->[0]->{Question}; #getQuestions
	
	my @ans = grep { $_ } split(/_/, $joinedAnswers);
	my @licensesLeft = keys %{ $data->{Licenses}->[0]->{License} };
	my $q = $data->{Questions}->[0]->{initialQuestion};
	foreach my $a (@ans)
	{
		my $ans = (grep { $_->{value} eq $a } @{ $questions->{$q}->{Answers}->[0]->{Answer} })[0];
		my @licenses = keys(%{ $ans->{Licenses}->[0]->{License} });
		{ my $x; @licensesLeft = grep { $x = $_, grep { $x eq $_ } @licenses } @licensesLeft }
		$q = $ans->{nextQuestion};
	}
	return ($q, $questions->{$q}, sort @licensesLeft);
}
sub txt 
{
        return $_[0] if not $_[0];
        return "" if ref($_[0]->[0]) eq 'HASH';
#        return replaceNewLine($_[0]->[0]);
        return $_[0]->[0];
}

our $data = do 'data.pl';
if (not $data)
{
	require XML::Simple;
	open FH, "<:utf8", "LicenseWizard.xml";
	undef $/;
	my $x = <FH>;
	close FH;
	$data = new XML::Simple(ForceArray => 1)->XMLin($x);
}
our $oldAns = new CGI()->param('ans');
#our ($oldAns) = $ENV{QUERY_STRING} =~ m/&?ans=(.*?)&?/;
our ($questionId, $question, @licenses) = processAnswers($data, $oldAns);
our ($formURL) = ($0 =~ m#.*/(.*)#);

$questionId = "NoLicenses" if not @licenses;
print (do "$questionId.html" || do "DefaultPage.html");

#perl -MXML::Simple -MData::Dumper -e 'print Dumper(new XML::Simple(ForceArray => 1)->XMLin("LicenseWizard.xml"))' > data.pl

