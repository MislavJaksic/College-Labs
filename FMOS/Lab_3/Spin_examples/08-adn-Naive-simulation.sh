#! /bin/sh

spin -g -p 08a-adn-Naive.prml | perl -w -a -n -e 'if($_ =~ /i\s\=\s\d+/){print "$_";}'