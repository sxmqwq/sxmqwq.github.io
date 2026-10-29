做法之后再补，先挂一个首次通过的代码，可读性不高。

```cpp
#include<bits/stdc++.h>
#define rep(i,l,r) for(int qwp=(r),i=(l);i<=qwp;i++)
#define per(i,r,l) for(int qwp=(l),i=(r);i>=qwp;i--)
#define pb push_back
#define fir first
#define sec second
using namespace std;
typedef pair<int,int> pii;
constexpr int mod=998244353,N=1e5+5;
inline int red(int x){return x>=mod?x-mod:x;}
inline void inc(int &x,int y){x=red(x+y);}
inline void dec(int &x,int y){x=red(x+mod-y);}
struct BIT{
    inline int lb(int x){return x&(-x);}
    int n,tr[N];inline void Init(int nn){rep(i,1,n=nn)tr[i]=0;}
    inline void add(int i,int z){for(;i<=n;i+=lb(i))inc(tr[i],z);}
    inline int ask(int i){int z=0;for(;i;i-=lb(i))inc(z,tr[i]);return z;}
}tr;
int n;vector<int>g[N];int fa[N],de[N],dl[N],dr[N],h[N];
int lt[N],ltmn[N];inline int jmpde(int u,int k){while(k<de[u])u=k<=de[lt[u]]?lt[u]:fa[u];return u;}
int Tim,Tl[N],Tr[N];void dfs(int u){Tl[u]=++Tim;for(auto v:g[u])dfs(v);Tr[u]=Tim;}
int p1[N],p2[N];vector<int>b1[N],b2[N];
int nx[N];vector<int>bs[N];
vector<pii>bc[N];int wc[N],ac[N];
int DE[N],LT[N];
int f[N],fs[N];
void slv(){
    cin>>n;rep(i,1,n)g[i]=b1[i]=b2[i]=bs[i]={},bc[i]={},f[i]=wc[i]=ac[i]=0;
    rep(i,2,n)cin>>fa[i]>>dl[i]>>dr[i]>>h[i],g[fa[i]].pb(i);
    de[1]=1;rep(i,2,n){
        de[i]=de[fa[i]]+1;
        dl[i]=de[i]-dl[i],dr[i]=de[i]-dr[i],h[i]=de[i]-h[i]-1;
        swap(dl[i],dr[i]),dr[i]=min(dr[i],h[i]);
        if(de[fa[i]]+de[lt[lt[fa[i]]]]==de[lt[fa[i]]]<<1)
        lt[i]=lt[lt[fa[i]]],ltmn[i]=min({h[fa[i]],ltmn[fa[i]],ltmn[lt[fa[i]]]});
        else lt[i]=fa[i],ltmn[i]=h[fa[i]];
        p2[i]=-1;
        if(dl[i]<=dr[i]){
            for(p1[i]=i;fa[p1[i]]&&dr[i]<=h[fa[p1[i]]];)
            p1[i]=lt[p1[i]]&&dr[i]<=ltmn[p1[i]]?lt[p1[i]]:fa[p1[i]];
            b1[p1[i]].pb(i);
            if(dl[i]<=h[fa[p1[i]]]){
                for(p2[i]=fa[p1[i]];fa[p2[i]]&&dl[i]<=h[fa[p2[i]]];)
                p2[i]=lt[p2[i]]&&dl[i]<=ltmn[p2[i]]?lt[p2[i]]:fa[p2[i]];
                b2[p2[i]].pb(i),bs[p1[i]].pb(p2[i]);
            }
        }
        for(nx[i]=i;fa[nx[i]]&&h[fa[nx[i]]]>=h[i];)
        nx[i]=lt[nx[i]]&&ltmn[nx[i]]>=h[i]?lt[nx[i]]:fa[nx[i]];
    }
    DE[1]=1;rep(i,2,n){
        int x=fa[nx[i]],y=LT[x],z=LT[y];
        DE[i]=DE[x]+1,LT[i]=DE[x]+DE[z]==DE[y]<<1?z:x;
    }
    rep(i,1,n)for(auto y:bs[i]){
        ac[i]++;int x=i;while(de[nx[x]]>de[y])
        x=LT[x]&&de[nx[LT[x]]]>de[y]?LT[x]:fa[nx[x]];
        ac[x]--,bc[y].pb({x,1});
    }
    per(i,n,1)bc[nx[i]].pb({i,ac[i]}),wc[fa[nx[i]]]+=ac[i],ac[fa[nx[i]]]+=ac[i];
    Tim=0,dfs(1),tr.Init(n),f[1]=fs[1]=1;
    rep(i,2,n){
        for(auto u:b1[i])tr.add(Tl[u],red(fs[jmpde(u,dr[u])]+mod-fs[jmpde(u,dl[u]-1)]));
        for(auto u:b2[i])tr.add(Tl[fa[p1[u]]],mod-fs[jmpde(u,dl[u]-1)]);
        for(auto u:bc[i])tr.add(Tl[fa[u.fir]],1ll*fs[jmpde(u.fir,h[u.fir])]*u.sec%mod);
        inc(f[i],1ll*wc[i]*fs[jmpde(i,h[i])]%mod);
        inc(f[i],red(tr.ask(Tr[i])+mod-tr.ask(Tl[i]-1)));
        fs[i]=red(f[i]+fs[fa[i]]);
    }
    rep(i,2,n)cout<<f[i]<<' ';cout<<'\n';
}
int main(){
    cin.tie(0)->sync_with_stdio(0);
    int csi,T;cin>>csi>>T;while(T--)slv();
    return 0;
}
/*
ulimit -v 1048576;ulimit -s 1048576
g++ -O2 -std=c++14 -static mountain.cpp -o %;size %;time ./% < mountain.in > mountain.out
ulimit -s 1048576
g++ -O2 -std=c++14 -fsanitize=address,leak,undefined mountain.cpp -o %;size %;time ./% < mountain.in > mountain.out
*/
```