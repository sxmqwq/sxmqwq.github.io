爆搜决策树，记录当前是第几次询问，可能的答案集合，以及已经花费的代价。若是第四次询问或可以直接问整个集合则直接结束。

对于第一次询问，定义一个数的权值为其 $2,3,5,7$ 因子的指数和。取权值 $\ge6$ 的所有数为元素池，直接随机若干次 $5$ 个数，取最大后续集合最小的方案。可以得到 `{4320,1620,432,2268,840}`。

对于第二次询问，直接在刚才的元素池里面不断随机 $10$ 个数，直到后继集合 $\le40$。对于第三次询问，在可能答案集合值域内随机可接受元素个数和元素。

然后就可以稳定在五秒内跑出决策树了，直接用 stl 记录决策进行交互即可。

```cpp
#include<bits/stdc++.h>
// #include"pudding.h"
#define rep(i,l,r) for(int qwp=(r),i=(l);i<=qwp;i++)
#define per(i,r,l) for(int qwp=(l),i=(r);i>=qwp;i--)
#define TIME chrono::duration_cast<chrono::milliseconds>(chrono::high_resolution_clock::now().time_since_epoch()).count()
#define pb push_back
#define SZ(x) (int)((x).size())
#define fir first
#define sec second
using namespace std;
typedef vector<int> arr;
constexpr int inf=1e9;
mt19937_64 rng(TIME);
int RND(int l,int r){return l+rng()%(r-l+1);}
int calc(arr a,int b){
    a.pb(b);sort(a.begin(),a.end());
    int s=0;rep(i,0,SZ(a)-2)s+=__gcd(a[i],a[i+1]);
    return s;
}
int sc1(int x){
    int w=0;for(auto p:{2,3,5,7})
    while(!(x%p))x/=p,w++;return w;
}
int maxsz(arr a,arr A){
    map<int,int>cnt;for(auto x:a)cnt[calc(A,x)]++;
    int m=0;for(auto x:cnt)m=max(m,x.sec);return m;
}
arr all,pl1,q1={4320,1620,432,2268,840};
arr gen2(arr a,int w){
    int be=inf;arr BE;
    while(be>40){
        arr q;rep(i,1,10)q.pb(pl1[rng()%SZ(pl1)]);
        int t=maxsz(a,q);if(t<be)be=t,BE=q;
    }
    return BE;
}
arr gen3(arr a,int w){
    int wl=*min_element(a.begin(),a.end());
    int wr=*max_element(a.begin(),a.end());
    int be=inf,cnt=1024;arr BE;
    while(be>35&&cnt--){
        arr q;rep(i,1,RND(1,35-w))q.pb(RND(wl,wr));
        int t=w+SZ(q)+maxsz(a,q);if(t<be)be=t,BE=q;
    }
    return BE;
}
map<arr,pair<arr,int> >mem[10];
int dfs(arr a,int u,int w){
    if(u==4||w+SZ(a)<=35)return w+SZ(a);
    int res=inf;
    if(u==1){
        arr q=q1;map<int,arr>mp;for(auto x:a)mp[calc(q,x)].pb(x);
        int mx=0;for(auto it:mp)mx=max(mx,dfs(it.sec,u+1,w+SZ(q)));
        return mx;
    }
    rep(_,1,1){
        arr q=u==2?gen2(a,w):gen3(a,w);
        map<int,arr>mp;for(auto x:a)mp[calc(q,x)].pb(x);
        int mx=0;for(auto it:mp)mx=max(mx,dfs(it.sec,u+1,w+SZ(q)));
        if(!mem[u].count(a)||mem[u][a].sec>mx)mem[u][a]={q,mx};
        res=min(res,mx);
    }
    return res;
}
void init(int,int){
    rep(i,1,3000)all.pb(i);rep(i,1,4500)if(sc1(i)>=6)pl1.pb(i);
    // int be=inf,cnt=0;arr BE;
    // while(be>=185||cnt<=1000){
    //     arr q;rep(i,1,5)q.pb(pl1[rng()%SZ(pl1)]);
    //     int t=maxsz(all,q);
    //     if(t<be)be=t,BE=q,cnt=1,cerr<<be<<'\n';
    //     else cnt++;
    // }
    // for(auto x:BE)cerr<<x<<',';
    while(dfs(all,1,0)>35);
}
int query_tastiness(arr);
int find_tastiness(int,int){
    arr qwq=all,awa;int usd=0;
    arr ask1=q1;int ret1=query_tastiness(ask1);
    awa={};for(auto x:qwq)if(calc(ask1,x)==ret1)awa.pb(x);qwq=awa;
    if((usd+=SZ(ask1))+SZ(qwq)<=35){
        arr ask4=qwq;int ret4=query_tastiness(ask4);
        awa={};for(auto x:qwq)if(calc(ask4,x)==ret4)awa.pb(x);qwq=awa;
        return qwq[0];
    }
    arr ask2=mem[2][qwq].fir;int ret2=query_tastiness(ask2);
    awa={};for(auto x:qwq)if(calc(ask2,x)==ret2)awa.pb(x);qwq=awa;
    if((usd+=SZ(ask2))+SZ(qwq)<=35){
        arr ask4=qwq;int ret4=query_tastiness(ask4);
        awa={};for(auto x:qwq)if(calc(ask4,x)==ret4)awa.pb(x);qwq=awa;
        return qwq[0];
    }
    arr ask3=mem[3][qwq].fir;int ret3=query_tastiness(ask3);
    awa={};for(auto x:qwq)if(calc(ask3,x)==ret3)awa.pb(x);qwq=awa;
    arr ask4=qwq;int ret4=query_tastiness(ask4);
    awa={};for(auto x:qwq)if(calc(ask4,x)==ret4)awa.pb(x);qwq=awa;
    return qwq[0];
}
/*
ulimit -s 1048576
g++ -O2 -std=c++14 -static grader.cpp pudding.cpp -o %;size %;time ./% < pudding.in > pudding.out
*/
```