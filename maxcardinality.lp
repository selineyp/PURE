% OPTIMIZATION

singlecount(man, T) :- T = #count{M: msingle(M)}.
singlecount(woman, T) :- T = #count{F: wsingle(F)}.

singlecount(total, M+F) :- singlecount(man, M), singlecount(woman, F).

% weak constraint

:~ singlecount(total, T). [T]

% SHOW

#show singlecount/2.