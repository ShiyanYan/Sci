# !/usr/bin/perl

# input : vol (as arg[0])
# output: connected components of author graph (from coauths)

# using threshold = 0.0

use strict;

my $cvol= $ARGV[0];

my $lowcutoff= 3; ## redundancy cutoff
my $threshold= 0; ## edge threshold

my $redundancyfile= "../input/names-redundancy_$cvol.txt";

my $infile= "../input/$cvol" . "_in-normalized_stripped.txt";

my $logfile= "../output/$cvol" . "_disambiguation-log.txt";
my $outfile= "../output/$cvol" . "_in-normalized_stripped-disambiguated.txt";

########## redundancy #################################

my %rawredundancy= ();
my %redundancycount= ();  ## histogram
my %redundancy= ();  ### P(x < arg)
my $totalnames= 0;

open(R, "<$redundancyfile");

while(my $l= <R>){
    chomp($l);
    if($l =~ /^(\S+)\s+(\d+)\s*$/){
	$rawredundancy{$1}= $2;
	$redundancycount{$2}++;
	$totalnames++;
    }
}

close(R);

print STDERR "Computing normalized redundancy scores ...\n";

my $cumsum= 0;

foreach my $rc (sort {$a <=> $b} keys %redundancycount){
    $redundancy{$rc}= $cumsum/$totalnames;  ## cumulative probability
    $cumsum+= $redundancycount{$rc};

    #print STDERR "$rc $redundancy{$rc}\n";
}

############ input #####################################

print STDERR "Reading input ...\n";

my $id= "";
my %auths= ();
my %cities= ();
my %refs= ();

my @fullname= ();
my @lastname= ();
my @initial= ();

my $authindex= 0;

my @articleid= ();

my %dupauth; # checking same author name in the same paper

open(IN, "<$infile");

while(my $l= <IN>){
    chomp($l);

    my $fname= "";
    my $lname= "";
    my $iname= ""; # initials

    if($l =~ /^ID\s+(\d+)\s*$/){
	$id= $1;
	
	my @a= ();
	$auths{$id}= \@a;
	
	my %b= ();
	$cities{$id}= \%b;
	
	my @c= ();
	$refs{$id}= \@c;

	%dupauth= ();
    }
    
    elsif($l =~ /^CT\s+(.+)\s*$/){
	${$cities{$id}}{uc($1)}= 1; # just once per paper
    }

    ## refs
    elsif($l =~ /^RF\s+(\d+)$/){
	push(@{$refs{$id}}, $1);
    }

    ## name formats
    elsif($l =~ /^AU\s+(\S+),\s+(\S+)\s*$/){
	$fname= "$1, $2";
	$lname= $1;
	$iname= $2;
    }
    # no initials
    elsif($l =~ /^AU\s+(\S+)\s*$/){
	$fname= $1;
	$lname= $1;
    }
    elsif($l =~ /^\s+(\S+),\s+(\S+)\s*$/){
	$fname= "$1, $2";
	$lname= $1;
	$iname= $2;
    }
    # no initials
    elsif($l =~ /^\s+(\S+)\s*$/){
	$fname= $1;
	$lname= $1;
    }

    if($fname ne ""){
	if(!exists($dupauth{$fname})){
	    
	    push(@fullname, $fname);
	    push(@lastname, $lname);
	    push(@initial, $iname);
	    
	    push(@{$auths{$id}}, $authindex);
	    
	    $authindex++;
	    
	    push(@articleid, $id);

	    $dupauth{$fname}++;
	}
    }
}

close(IN);

########## process #########################################

my $curname= "";
my %disnames= (); ## disname{id:fullname} => lastnameX, initial

open(LOG, ">$logfile");

my @sortedfullname= sort @fullname;

for(my $i= 0; $i <= $#sortedfullname; $i++){
    next if $sortedfullname[$i] eq $curname;

    $curname= $sortedfullname[$i];

    print STDERR "Processing $curname ...\n";

    my $lname= $curname;
    if($curname =~ /^(\S+),/){
	$lname= $1;
    }

    my @authset= ();    ## set of indices of authors with same name
    
    for(my $j= 0; $j <= $#fullname; $j++){
	push(@authset, $j) if $fullname[$j] eq $curname;
    }

    my %compnum= (); ## component number
    
    for(my $j= 0; $j <= $#authset; $j++){
	$compnum{$j}= $j; ## one component per paper
    }

    if($rawredundancy{$lname} <= $lowcutoff){
	## merge all
	for(my $j= 0; $j <= $#authset; $j++){
	    $compnum{$j}= 0; ## 1 component
	}
    }
    else{
	### disambiguation

	### (1) co-author overlap graph construction

	my @eu= ();
	my @ev= ();
	my @ew= ();
	
	for(my $j= 0; $j <= $#authset; $j++){
	    my $s= $articleid[$authset[$j]];
	    for(my $k= $j+1; $k <= $#authset; $k++){
		my $t= $articleid[$authset[$k]];
		my $w= edgenonredundancy($s, $t, $curname);
		if($w > 0){
		    push(@eu, $j);
		    push(@ev, $k);
		    push(@ew, $w);
		}
	    }
	}
	
	## sort edges by weight
	my @indices= ();
	for(my $j= 0; $j <= $#ew; $j++){
	    push(@indices, $j);
	}
	
	my @sindices= sort {$ew[$b] <=> $ew[$a]} @indices;
	
	## connected components by set union ########################
	
	for(my $jj= 0; $jj <= $#ew && $ew[$sindices[$jj]] >= $threshold; $jj++){
	    my $j= $sindices[$jj];
	    
	    ## min component label
	    my $mincnum= $compnum{$eu[$j]};
	    $mincnum= $compnum{$ev[$j]} if $mincnum > $compnum{$ev[$j]};
	    
	    ## max label
	    my $maxcnum= $compnum{$eu[$j]};
	    $maxcnum= $compnum{$ev[$j]} if $maxcnum < $compnum{$ev[$j]};
	    
	    ## set the min label to max label component
	    if($maxcnum > $mincnum){
		for(my $k= 0; $k <= $#authset; $k++){
		    $compnum{$k}= $mincnum if $compnum{$k} == $maxcnum;
		}
	    }	    
	}

	### (2) self-citation based merging

	@eu= ();
	@ev= ();

	for(my $j= 0; $j <= $#authset; $j++){
	    my $s= $articleid[$authset[$j]];
	    for(my $k= $j+1; $k <= $#authset; $k++){
		next if $compnum{$j} == $compnum{$k}; ## already merged

		my $t= $articleid[$authset[$k]];

		my $sf= 0;
		foreach my $r (@{$refs{$s}}){
		    $sf++ if $r == $t;
		}
		foreach my $r (@{$refs{$t}}){
		    $sf++ if $r == $s;
		}

		if($sf > 0){
		    push(@eu, $j);
		    push(@ev, $k);    
		}
	    }
	}

	for(my $y= 0; $y <= $#eu; $y++){
	    my $j= $eu[$y];
	    my $k= $ev[$y];

	    next if $compnum{$j} == $compnum{$k}; ## already merged

	    ## min component label
	    my $mincnum= $compnum{$j};
	    $mincnum= $compnum{$k} if $mincnum > $compnum{$k};
	    
	    ## max label
	    my $maxcnum= $compnum{$j};
	    $maxcnum= $compnum{$k} if $maxcnum < $compnum{$k};
	    
	    ## set the min label to max label component
	    if($maxcnum > $mincnum){
		for(my $u= 0; $u <= $#authset; $u++){
		    $compnum{$u}= $mincnum if $compnum{$u} == $maxcnum;
		}
	    }
	}
    }

    print LOG "$curname -> [";

    ## component numbers; also sizes
    my %clist= ();
    for(my $k= 0; $k <= $#authset; $k++){
	$clist{$compnum{$k}}++;
    }

    my $nc= scalar(keys %clist); ## number of components
    
    my $disnum= 0;

    my @gr= ();
    
    foreach my $cnum (keys %clist){
	$disnum++;

	my @alist= ();
	for(my $k= 0; $k <= $#authset; $k++){
	    if($compnum{$k} == $cnum){
		my $j= $authset[$k];
		my $aid= $articleid[$j];
		push(@alist, $aid);

		## just 1 identity, no numbering required
		if($nc == 1){
		    $disnames{"$aid:$fullname[$j]"}= "$fullname[$j]";
		}
		## more than 1 identities
		else{
		    if($initial[$j] ne ""){
			$disnames{"$aid:$fullname[$j]"}= "$lastname[$j]$disnum, $initial[$j]";
		    }
		    else{
			$disnames{"$aid:$fullname[$j]"}= "$lastname[$j]$disnum";
		    }
		}
	    }
	}
	
	$"= ", "; print LOG " {@alist}";

	my %bh= (); ## convert alist to hash
	foreach my $k (@alist){
	    $bh{$k}++;
	}
	
	push(@gr, \%bh);
    }

    print LOG " ]\n";
}

close(LOG);
close(KM);

open(IN, "<$infile");
open(OUT, ">$outfile");

$id= "";

while(my $l= <IN>){
    chomp($l);

    # author
    if(($l =~ /^AU/) || ($l =~ /^\s+/)){
	if($l =~ /^AU\s+(.+)\s*$/){
	    my $nm= $disnames{"$id:$1"};
	    print OUT "AU $nm\n";
	}
	elsif($l =~ /^\s+(.+)\s*$/){
	    my $nm= $disnames{"$id:$1"};
	    print OUT " $nm\n";
	}
    }
    # print everything else
    else{
	print OUT "$l\n";
	
	# save id
	if($l =~ /^ID\s+(\d+)\s*/){
	    $id= $1;
	}
    }
    
}

close(OUT);
close(IN);

######################################################################

### computes the edge non-redundancy
### args : article1 article2 author
sub edgenonredundancy{
    my $a= shift;
    my $b= shift;
    my $c= shift; ## exclude this author from overlap; fullname

    my %ah= ();
    foreach my $auth (@{$auths{$a}}){
	$ah{$fullname[$auth]}++ if $fullname[$auth] ne $c;
    }

    my %bh= ();
    foreach my $auth (@{$auths{$b}}){
	$bh{$fullname[$auth]}++ if $fullname[$auth] ne $c;
    }

    my $p= 1;

    foreach my $coauth (keys %ah){
	if(exists($bh{$coauth})){
	    my $lname= $coauth;
	    if($coauth =~ /^(\S+),/){
		$lname= $1;
	    }
	    
	    $p*= $redundancy{$rawredundancy{$lname}};
	}
    }

    return 1-$p;
}
