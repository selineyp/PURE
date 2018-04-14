% DEFINITIONS

maccept(M,W) :- mpref(M,W,_), W != s.
waccept(W,M) :- wpref(W,M,_), M != s.

msinglepref(M, X) :- mpref(M, s, X), man(M).
wsinglepref(W, X) :- wpref(W, s, X), woman(W).

% GENERATE

accept(M,W) :- manpropose(M,W), womanpropose(M,W).

msingle(M) :- man(M), not accept(M, W) : maccept(M, W).
wsingle(W) :-  woman(W), not accept(M, W) : waccept(W, M).

manpropose(M, W) :- man(M), mpref(M, W, H), msinglepref(M, MM), H < MM,  not accept(M,X) : maccept(M,X), mpref(M,X,L), L <= H, W != X.
manpropose(M, W) :- man(M), mpref(M,W,H),  W!=s,  msinglepref(M, MM), H = MM, not msingle(M), not accept(M,X) : maccept(M,X), mpref(M,X,L), L <= H, W != X.

womanpropose(M, W) :- woman(W), wpref(W, M, H), wsinglepref(W, WW), H < WW, not accept(X, W) : waccept(W, X), wpref(W, X, L), L <= H, M != X.
womanpropose(M, W) :- woman(W), wpref(W, M, H), M!=s, wsinglepref(W, WW), H = WW, not wsingle(W), not accept(X, W) : waccept(W, X), wpref(W, X, L), L <= H, M != X.

% SHOW

#show accept/2.
#show msingle/1.
#show wsingle/1.
