% OPTIMIZATION

% pair rank

m2rank(M, R) :- marry(M, F), mrank(M, F, R).
w2rank(F, R) :- marry(M, F), wrank(F, M, R).

% total rank

regret(man, T) :- T = #max{R, M: m2rank(M, R)}.
regret(woman, T) :- T = #max{R, F: w2rank(F, R)}.

maxregret(T) :- T = #max{R: regret(_, R)}.

% weak constraint

:~ maxregret(R), R > #inf. [R]

% SHOW

#show regret/2.
#show maxregret/1.
