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
Sample 2:
```cpp
typedef unsigned long long ll;typedef vector<ll> Poly;typedef pair<ll,ll> pll;
constexpr ll mod=998244353;
namespace POLY{
constexpr ll I2=mod+1>>1,G=3,IG=332748118;constexpr int brutemul=256;
Poly frmod(Poly mods,ll lim){Poly res(SZ(mods));char c=getchar();while(c<'0'||'9'<c)c=getchar();while('0'<=c&&c<='9'){rep(i,0,SZ(mods)-1){res[i]=res[i]*10+c-48;while(res[i]>=lim)res[i]-=mods[i];}c=getchar();}return res;}
void inc(ll &x,ll y){x=x+y<mod?x+y:x+y-mod;}void dec(ll &x,ll y){x=x<y?x+mod-y:x-y;}ll ksm(ll a,ll b,ll p){a%=p;ll r=1;while(b){if(b&1)r=r*a%p;a=a*a%p;b>>=1;}return r%p;}ll inv0(ll x){return ksm(x,mod-2,mod);}Poly invs={1,1};ll inv1(ll x){if(SZ(invs)<=x){ll y=SZ(invs);invs.RSZ(x+1);while(y<=x)invs[y]=(mod-mod/y)*invs[mod%y]%mod,y++;}return invs[x];}
Poly operator * (Poly a,ll b){rep(i,0,SZ(a)-1)a[i]=a[i]*b%mod;return a;}void operator *= (Poly &a,ll b){a=a*b;}Poly operator / (Poly a,ll b){return a*inv0(b);}void operator /= (Poly &a,ll b){a=a/b;}
Poly operator + (Poly a,Poly b){Poly c(max(SZ(a),SZ(b)));rep(i,0,SZ(a)-1)inc(c[i],a[i]);rep(i,0,SZ(b)-1)inc(c[i],b[i]);return c;}void operator += (Poly &a,Poly b){a=a+b;}Poly operator - (Poly a,Poly b){Poly c(max(SZ(a),SZ(b)));rep(i,0,SZ(a)-1)inc(c[i],a[i]);rep(i,0,SZ(b)-1)dec(c[i],b[i]);return c;}void operator -= (Poly &a,Poly b){a=a-b;}
Poly Ntt(Poly a,int e){int n=SZ(a);vector<int>to(n);rep(i,0,n-1)to[i]=(to[i>>1]>>1)|((n>>1)*(i&1));rep(i,0,n-1)if(i<to[i])swap(a[i],a[to[i]]);for(int k=2;k<=n;k<<=1){ll g=ksm(e==1?G:IG,(mod-1)/k,mod);for(int i=0;i<n;i+=k){ll w=1;rep(j,0,(k>>1)-1){ll p=a[i|j],q=a[i|j|k>>1]*w%mod;a[i|j]=(p+q)%mod;a[i|j|k>>1]=(p+mod-q)%mod;w=w*g%mod;}}}if(e==-1){ll w=inv1(n);rep(i,0,n-1)a[i]=a[i]*w%mod;}return a;}
Poly operator * (Poly a,Poly b){if(SZ(a)+SZ(b)<=brutemul){Poly c(SZ(a)+SZ(b)-1);rep(i,0,SZ(a)-1)rep(j,0,SZ(b)-1)inc(c[i+j],a[i]*b[j]%mod);return c;}Poly c(SZ(a)+SZ(b)-1);int k=1;while(k<=SZ(c))k<<=1;a.RSZ(k);a=Ntt(a,1);b.RSZ(k);b=Ntt(b,1);rep(i,0,k-1)a[i]=a[i]*b[i];a=Ntt(a,-1);rep(i,0,SZ(c)-1)c[i]=a[i];return c;}void operator *= (Poly &a,Poly b){a=a*b;}
Poly Inv(Poly a){if(SZ(a)==1)return (Poly){inv0(a[0])};Poly a_=a;a_.RSZ(SZ(a)+1>>1);a_=Inv(a_);a_=((Poly){2}-a*a_)*a_;a_.RSZ(SZ(a));return a_;}Poly operator / (Poly a,Poly b){int n=max(SZ(a),SZ(b));a.RSZ(n);b.RSZ(n);a=a*Inv(b);a.RSZ(n);return a;}void operator /= (Poly &a,Poly b){a=a/b;}Poly Der(Poly a){rep(i,0,SZ(a)-2)a[i]=a[i+1]*(i+1)%mod;a[SZ(a)-1]=0;return a;}Poly Int(Poly a){per(i,SZ(a)-1,1)a[i]=a[i-1]*inv1(i)%mod;a[0]=0;return a;}
Poly Ln(Poly a){return Int(Der(a)/a);}Poly Exp(Poly a){if(SZ(a)==1)return (Poly){1};Poly a_=a;a_.RSZ(SZ(a)+1>>1);a_=Exp(a_);a_.RSZ(SZ(a));a_=a_*(a-Ln(a_)+(Poly){1});a_.RSZ(SZ(a));return a_;}
Poly Pow(Poly a,ll b1,ll b2){rep(i,0,SZ(a)-1)if(a[i]){Poly a_(SZ(a)-i);rep(j,i,SZ(a)-1)a_[j-i]=a[j];a_=Exp(Ln(a_/a_[0])*b1)*ksm(a_[0],b2,mod);rep(j,0,SZ(a)-1)a[j]=0;for(ll qwp=SZ(a)-1,j=i*b1;j<=qwp;j++)a[j]=a_[j-i*b1];return a;}rep(i,0,SZ(a)-1)a[i]=0;a[0]=1;return a;}
namespace Cipolla{constexpr ll W2=(mod-1)/2;mt19937 rng(TIME);ll II;pll operator * (pll a,pll b){return {(a.first*b.first+a.second*b.second%mod*II)%mod,(a.first*b.second+a.second*b.first)%mod};}void operator *= (pll& a,pll b){a=a*b;}pll fpw(pll a,ll b){pll r={1,0};while(b){if(b&1)r*=a;a*=a;b>>=1;}return r;}ll cal(ll n){if(!n)return 0;if(ksm(n,W2,mod)!=1)return -1;ll a=rng()%mod;while(ksm((a*a-n+mod)%mod,W2,mod)==1)a=rng()%mod;II=(a*a-n+mod)%mod;ll res=fpw({a,1},I2).first;return min(res,(mod-res)%mod);}}
Poly Sqrt(Poly a){if(SZ(a)==1){ll w=Cipolla::cal(a[0]);assert(w!=-1);return {w};}Poly a_=a;a_.RSZ(SZ(a)+1>>1);a_=Sqrt(a_);a_=(a_+a/a_)*I2;a_.RSZ(SZ(a));return a_;}
}
```