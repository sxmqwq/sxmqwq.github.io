Sample 1:
```cpp
#include<bits/stdc++.h>
#define TIME chrono::duration_cast<chrono::milliseconds>(chrono::high_resolution_clock::now().time_since_epoch()).count()
#define rep(i,l,r) for(int qwp=(r),i=(l);i<=qwp;i++)
#define per(i,r,l) for(int qwp=(l),i=(r);i>=qwp;i--)
#define pb push_back
#define ins insert
#define SZ(x) (int)((x).size())
#define fir first
#define sec second
using namespace std;
typedef vector<int> arr;typedef pair<int,int> pii;typedef long long ll;
constexpr int N=1e5+5;
int csi,n;arr g[N];
int fa[N],de[N],sz[N],ht[N],lt[N];
int dl[N],dr[N],dfa[N],Tim;
void dfsI(int u){
    dfa[dl[u]=Tim=fa[u]?Tim+1:1]=u,de[u]=de[fa[u]]+1,sz[u]=1,ht[u]=1;
    int t=de[u]+de[lt[lt[u]]]==de[lt[u]]*2?lt[lt[u]]:u;
    for(auto v:g[u])if(v!=fa[u])fa[v]=u,lt[v]=t,
    dfsI(v),sz[u]+=sz[v],ht[u]=max(ht[u],ht[v]+1);
    dr[u]=Tim;
}
int rt;
void Init(){
    fa[1]=0,dfsI(1);int pp=1;rep(i,2,n)if(de[pp]<de[i])pp=i;
    fa[pp]=0,dfsI(pp);int qq=1;rep(i,2,n)if(de[qq]<de[i])qq=i;
    rt=qq;rep(_,1,de[qq]-1>>1)rt=fa[rt];if(sz[rt]*2<n)rt=fa[rt];
    fa[rt]=0,dfsI(rt);
}
int lca(int x,int y){
    if(de[x]>de[y])swap(x,y);while(de[x]<de[y])y=de[x]<=de[lt[y]]?lt[y]:fa[y];
    while(x!=y)lt[x]==lt[y]?(x=fa[x],y=fa[y]):(x=lt[x],y=lt[y]);return x;
}
int idx,rk[N],sfs[N];arr buc[N],sns[N];
bool cmpsns(int x,int y){
    arr &a=sns[x],&b=sns[y];rep(i,0,min(SZ(a),SZ(b))-1)
    if(a[i]!=b[i])return a[i]<b[i];return SZ(a)<SZ(b);
}
void calrk(){
    rep(i,1,n)buc[ht[i]].pb(i);for(auto u:buc[1])rk[u]=1;
    idx=1;rep(i,2,n)if(SZ(buc[i])){
        for(auto u:buc[i]){for(auto v:g[u])if(v!=fa[u])sns[u].pb(rk[v]);
        sort(sns[u].begin(),sns[u].end(),greater<int>());}
        stable_sort(buc[i].begin(),buc[i].end(),cmpsns);
        int lst=0;for(auto u:buc[i])rk[u]=idx+=sns[lst]!=sns[u],lst=u;
    }
    rep(i,1,n)sfs[rk[i]]++;per(i,idx,1)sfs[i-1]+=sfs[i];
}
int F(int x,int y){
    if(dl[y]<=dl[x]&&dl[x]<=dr[y])return de[x]-de[y]+1;int res=sfs[rk[y]+1]+1;
    int xx=x;while(xx&&rk[xx]<=rk[y])xx=lt[xx]&&rk[lt[xx]]<=rk[y]?lt[xx]:fa[xx];
    return res+=de[x]-de[xx];
}
int Q00(int x,int y,int w){return F(x,y)<=w;}
int S01(int x,int y,int g,int w){
    int res=0;if(max(de[x]-w+1,1)<=de[g])res+=de[g]-max(de[x]-w+1,1)+1;
    while(de[y]>de[g]&&F(x,y)>w)y=de[lt[y]]>de[g]&&F(x,lt[y])>w?lt[y]:fa[y];
    return res+=de[y]-de[g];
}
int Q01(int x,int y,int w){int g=lca(x,y);return S01(x,x,x,w)+S01(x,y,g,w)-S01(x,g,g,w)*2+(F(x,g)<=w);}
int S10(int x,int y,int w){
    int res=0;if(dl[y]<=dl[x]&&dl[x]<=dr[y])res+=min(de[x]-de[y]+1,w),x=fa[y];if(!x)return res;
    int xx=x;while(xx&&rk[xx]<=rk[y])xx=lt[xx]&&rk[lt[xx]]<=rk[y]?lt[xx]:fa[xx];
    if(de[xx]+1<=min(w-sfs[rk[y]+1]-1+de[xx],de[x]))res+=min(w-sfs[rk[y]+1]-1+de[xx],de[x])-de[xx];
    if(sfs[rk[y]+1]+1<=w)res+=de[xx];return res;
}
int Q10(int x,int y,int w){int g=lca(x,y);return S10(x,y,w)+S10(y,y,w)-S10(g,y,w)*2+(F(g,y)<=w);}
ll RKS[N];void dfsR(int u){RKS[u]+=sfs[rk[u]+1]+1;for(auto v:g[u])if(v!=fa[u])RKS[v]=RKS[u],dfsR(v);}
int q;ll ans[N];
ll NS(ll l,ll r){return (l+r)*(r-l+1)/2;}
int nt(int u,int g){while(de[u]-1>de[g])u=de[lt[u]]-1>de[g]?lt[u]:fa[u];return u;}
struct qry{int x,y,Y,to;};vector<qry>Q;
void S11(int x,int y,int g,int w,int qid){
    int X=nt(x,g);while(de[y]>de[g]&&F(X,y)>w)y=de[lt[y]]>de[g]&&F(X,lt[y])>w?lt[y]:fa[y];
    if(y==g)return ;int Y=y;while(de[Y]>de[g]&&F(x,Y)>w)Y=de[lt[Y]]>de[g]&&F(x,lt[Y])>w?lt[Y]:fa[Y];
    ans[qid]+=(de[Y]-de[g])*1ll*(de[x]-de[g])+(de[x]-de[g]+w)*1ll*(de[y]-de[Y])-RKS[y]+RKS[Y],Q.pb({x,y,Y,qid});
}
void Q11(int x,int y,int w,int qid){
    int g=lca(x,y);ans[qid]-=F(g,g)<=w;
    if(x!=g&&y!=g)S11(x,y,g,w,qid),S11(y,x,g,w,qid);
    int t=x;while(de[t]>de[g]&&sfs[rk[t]+1]+1>w)t=de[lt[t]]>de[g]&&sfs[rk[lt[t]]+1]+1>w?lt[t]:fa[t];
    int sz=de[x]-de[g]+1;ans[qid]+=NS(sz-min(sz,w)+1,sz)+NS(1,de[t]-de[g]);
    t=y;while(de[t]>de[g]&&sfs[rk[t]+1]+1>w)t=de[lt[t]]>de[g]&&sfs[rk[lt[t]]+1]+1>w?lt[t]:fa[t];
    sz=de[y]-de[g]+1,ans[qid]+=NS(sz-min(sz,w)+1,sz)+NS(1,de[t]-de[g]);
}
vector<pii>A;int ID[2][N];arr D[2];int pc[2][N],S[N*5],P[2][N];
int I(int x,int y){return x*(SZ(D[1])+1)+y;}
void work(){
    rep(i,1,idx)buc[i]={};rep(i,1,n)buc[rk[i]].pb(i);
    rep(i,1,idx)rep(j,0,1)for(auto u:buc[i])A.pb({u,j});rep(i,0,SZ(A)-1)ID[A[i].sec][A[i].fir]=i;
    for(int blen=sqrt(n)*2,cl=0,cr;cr=min(cl+blen-1,SZ(A)-1),cl<SZ(A);cl=cr+1){
        rep(i,1,n){int u=dfa[i];pc[0][u]=pc[0][fa[u]]+(ID[0][u]<cl);pc[1][u]=pc[1][fa[u]]+(cl<=ID[1][u]&&ID[1][u]<=cr);}
        for(auto it:Q)ans[it.to]-=pc[0][it.x]*1ll*(pc[1][it.y]-pc[1][it.Y]);
        D[0]=D[1]={};rep(i,cl,cr)D[A[i].sec].pb(dl[A[i].fir]),D[A[i].sec].pb(dr[A[i].fir]+1);
        if(!SZ(D[0])||!SZ(D[1]))continue;rep(_,0,1){
            sort(D[_].begin(),D[_].end()),D[_].erase(unique(D[_].begin(),D[_].end()),D[_].end());
            rep(i,0,SZ(D[_])-2)rep(j,D[_][i],D[_][i+1]-1)P[_][j]=i+1;
            rep(j,0,D[_][0]-1)P[_][j]=0;rep(j,D[_].back(),n+1)P[_][j]=SZ(D[_]);
        }
        rep(i,0,SZ(D[0]))rep(j,0,SZ(D[1]))S[I(i,j)]=0;
        rep(i,cl,cr)if(!A[i].sec){
            int x=A[i].fir,lx=P[0][dl[x]],rx=P[0][dr[x]+1];rep(j,cl,cr)if(A[j].sec){
                int y=A[j].fir;if(rk[x]>rk[y])continue;int ly=P[1][dl[y]],ry=P[1][dr[y]+1];
                S[I(lx,ly)]--,S[I(lx,ry)]++,S[I(rx,ly)]++,S[I(rx,ry)]--;
            }
        }
        rep(i,1,SZ(D[0]))rep(j,0,SZ(D[1]))S[I(i,j)]+=S[I(i-1,j)];rep(i,0,SZ(D[0]))rep(j,1,SZ(D[1]))S[I(i,j)]+=S[I(i,j-1)];
        for(auto it:Q)if(pc[1][it.y]>pc[1][it.Y]){int xx=P[0][dl[it.x]];ans[it.to]+=S[I(xx,P[1][dl[it.y]])]-S[I(xx,P[1][dl[it.Y]])];}
    }
}
signed main(){
    cin.tie(0)->sync_with_stdio(0);
    cin>>csi>>n;rep(i,1,n-1){int x,y;cin>>x>>y;g[x].pb(y),g[y].pb(x);}
    Init(),calrk(),dfsR(rt);cin>>q;rep(i,1,q){
        int x,y,ox,oy,w;cin>>x>>y>>ox>>oy>>w;
        if(!ox&&!oy)ans[i]=Q00(x,y,w);if(!ox&&oy)ans[i]=Q01(x,y,w);if(ox&&!oy)ans[i]=Q10(x,y,w);if(ox&&oy)Q11(x,y,w,i);
    }
    work();rep(i,1,q)cout<<ans[i]<<'\n';
}
```