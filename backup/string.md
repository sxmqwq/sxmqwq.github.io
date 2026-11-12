首先发现等价于比较 $S,rev(S)$。考虑把反串拼接求 sa，根据 rk 比较。

可以分奇偶性二维数点，且这样只会在 $S=rev(S)$ 时算错，考虑如何减去。

可以发现固定中点后只有 $rk_L<rk_R$ 与 $rk_L>rk_R$ 两种之一，具体是比较两侧首个不同位置。

即可以只考虑中点，manacher 后同样是一个二维数点，于是容易做到 $O(n\log n)$。

```cpp
#include<bits/stdc++.h>
#define rep(i,l,r) for(int qwp=(r),i=(l);i<=qwp;i++)
#define per(i,r,l) for(int qwp=(l),i=(r);i>=qwp;i--)
#define pb push_back
using namespace std;
constexpr int N=2e5+5;
namespace SA{
    int buc[N],tmp[N];
    inline void calc(int n,char *s,int *sa,int *rk){
        int m=max(n,256);rep(i,1,n)rk[i]=s[i]-'a'+1;
        fill(buc+1,buc+m+1,0);rep(i,1,n)buc[rk[i]]++;rep(i,1,m)buc[i]+=buc[i-1];
        per(i,n,1)sa[buc[rk[i]]--]=i;
        for(int k=1;k<=n;k<<=1){
            int idx=0;rep(i,n-k+1,n)tmp[++idx]=i;rep(i,1,n)if(sa[i]>k)tmp[++idx]=sa[i]-k;
            fill(buc+1,buc+m+1,0);rep(i,1,n)buc[rk[i]]++;rep(i,1,m)buc[i]+=buc[i-1];
            per(i,n,1)sa[buc[rk[tmp[i]]]--]=tmp[i];
            m=0;for(int i=1,p=0,q=0;i<=n;i++){
                int x=rk[sa[i]],y=sa[i]+k<=n?rk[sa[i]+k]:0;
                if(p<x||p==x&&q<y)m++;tmp[sa[i]]=m,p=x,q=y;
            }
            copy_n(tmp+1,n,rk+1);if(m==n)break;
        }
    }
}
struct BIT1{
    inline int lb(int x){return x&(-x);}
    int n,tr[N];inline void Init(int nn){fill(tr+1,tr+(n=nn)+1,0);}
    inline void add(int i,int z){for(;i<=n;i+=lb(i))tr[i]+=z;}
    inline int ask(int i){int z=0;for(;i;i-=lb(i))z+=tr[i];return z;}
}T1;
struct BIT2{
    inline int lb(int x){return x&(-x);}
    int n,tr[N];inline void Init(int nn){fill(tr+1,tr+(n=nn)+1,0);}
    inline void add(int i,int z){for(;i;i-=lb(i))tr[i]+=z;}
    inline int ask(int i){int z=0;for(;i<=n;i+=lb(i))z+=tr[i];return z;}
}T2;
int n,q;char s[N];int ql[N],qr[N],qans[N];
char s2[N];int sa[N],rk[N],kr[N];
char so[N];int OL[N],ol[N];
vector<int>t1[N],t2[N],t3[N];
void slv(){
    cin>>n>>q>>(s+1);
    rep(i,1,n)s2[i]=s2[n*2-i+1]=s[i];SA::calc(n*2,s2,sa,rk);
    rep(i,1,n)so[i*2-1]=s[i],so[i*2]='!';so[0]='@',so[n*2]='#';
    for(int i=1,j=1;i<n*2;i++){
        OL[i]=min(j+OL[j]-i,OL[j*2-i]);
        while(so[i-OL[i]]==so[i+OL[i]])OL[i]++;
        if(i+OL[i]>j+OL[j])j=i;
    }
    rep(i,1,n)kr[i]=rk[n*2-i+1],ol[i]=max(i*2-OL[i*2]+3>>1,1);
    rep(i,0,n)t1[i]=t2[i]=t3[i]={};rep(i,1,q){
        cin>>ql[i]>>qr[i],qans[i]=0;
        t1[ql[i]-1].pb(i),t2[ql[i]+qr[i]-1].pb(i),t3[ql[i]+qr[i]*2-1].pb(i);
    }
    T1.Init(n*2);rep(i,1,n){
        if(rk[i]<kr[i+1])T1.add(ol[i],1);
        for(auto j:t1[i])qans[j]+=T1.ask(ql[j]);
        for(auto j:t2[i])qans[j]-=T1.ask(ql[j]);
    }
    rep(_,1,2){
        T2.Init(n*2);for(int i=_;i<=n;i+=2){
            T2.add(kr[i],1);
            for(auto j:t1[i])qans[j]-=T2.ask(rk[ql[j]]+1);
            for(auto j:t3[i])qans[j]+=T2.ask(rk[ql[j]]+1);
        }
    }
    rep(i,1,q)cout<<qans[i]<<'\n';
}
int main(){
    // [[maybe_unused]]auto EVIL=freopen("string.in","r",stdin);
    // [[maybe_unused]]auto LIVE=freopen("string.out","w",stdout);
    cin.tie(0)->sync_with_stdio(0);
    int csi,T;cin>>csi>>T;while(T--)slv();
    return 0;
}
/*
ulimit -s 1048576
g++ -O2 -std=c++14 -fsanitize=address,leak,undefined string.cpp -o %;size %;time ./%;rm %
*/
```