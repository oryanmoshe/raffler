# Raffler

An Azure based raffle system, made of two pages, and two cloud function.

One page (`entry.html`) consists of an email input and submit button that sends the email to a cloud function (`EntryTrigger`) that adds it to a redis SET.

The other page (`raffle.html`) consists of one button that calls the second cloud function (`GetRandom`) which picks a random member in the set (using SRANDMEMBER) and returns it. The page then displays it.
