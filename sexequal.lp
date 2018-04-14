% OPTIMIZATION

% pair rank

m2rank(M, R) :- marry(M, F), mrank(M, F, R).
w2rank(F, R) :- marry(M, F), wrank(F, M, R).

% total rank

mtot(T) :- T = #sum{R, M: m2rank(M, R)}.
wtot(T) :- T = #sum{R, F: w2rank(F, R)}.
ttot(|M-F|) :- mtot(M), wtot(F).

% weak constraint

:~ ttot(T). [T]

% SHOW

#show mtot/1.
#show wtot/1.
#show ttot/1.
