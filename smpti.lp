% GENERATE

{msingle(M)} :- man(M).
{wsingle(F)} :- woman(F).

{marry(M, F) : woman(F)} = 1 :- man(M), not msingle(M).
:- {marry(M, F) : man(M)} > 1, woman(F).

marriedwoman(F) :- man(M), woman(F), marry(M, F).
:- marriedwoman(F), wsingle(F), woman(F).
:- not wsingle(F), not marriedwoman(F), woman(F).

% DEFINE

% M prefers F to single
m2single(M, F) :- man(M), woman(F), mrank(M, F, X).

% F prefers M to single
w2single(F, M) :- man(M), woman(F), wrank(F, M, X).

% M prefers DF to CF.
mprefer(M, DF, CF) :- mrank(M, CF, CUR), mrank(M, DF, DEV), DEV < CUR.

% F prefers DM to CM.
wprefer(F, DM, CM) :- wrank(F, CM, CUR), wrank(F, DM, DEV),  DEV < CUR.

% TEST

% a pair deviates (4 cases)

% m1-f1, m2-f2 -- m1 and f2 deviate to m1-f2
:- man(M1; M2), woman(F1; F2), marry(M1, F1), marry(M2, F2), mprefer(M1, F2, F1), wprefer(F2, M1, M2).

% m-f1, f2 single -- m and f2 deviate to m-f2
:- man(M), woman(F1; F2), marry(M, F1), wsingle(F2), mprefer(M, F2, F1), wrank(F2, M, X).

% m1-f, m2 single -- m2 and f deviate to m2-f
:- man(M1; M2), woman(F), marry(M1, F), msingle(M2), wprefer(F, M2, M1), mrank(M2, F, X).

% m, f single -- m and f deviate to m-f
:- man(M), woman(F), msingle(M), wsingle(F), mrank(M, F, X), wrank(F, M, Y).

% an individual deviates (2 cases)

% m-f -- m deviates to single
:- man(M), woman(F), marry(M, F), not m2single(M, F).

% m-f -- f deviates to single
:- man(M), woman(F), marry(M, F), not w2single(F, M).

% SHOW

#show marry/2.
