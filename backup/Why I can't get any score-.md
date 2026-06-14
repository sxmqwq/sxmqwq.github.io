## Statement

对于排列 $\{p_n\}$，给定 $(L_1,R_1),\dots,(L_m,R_m)$，记 $a_i=mex(p_{L_i},\dots,p_{R_i})$。

给定残缺排列 $q$，求将 $q$ 填充完整后得到 $a$ 的本质不同种类数。

## Solution

考虑一个暴力 dp，设 $f_{i,S}$ 表示包含 $0\sim i$ 的区间集合为 $S$ 时的填充方案数。

只需要判断 $S$ 之间能否转移，转移过程直接刻画了每个区间的 mex。

显然不需要记录 $S$，设包含 $0\sim i$ 的极小区间 $[l,r]$，则一个区间是否在 $S$ 中只需考虑其是否包含 $[l,r]$。

有一个问题是不同的 $l,r$ 对应相同的 $S$，令 $[l,r]$ 变为包含其的 $S$ 的交 $[l',r']$ 即可。

这样可以做到 $O(n^4)$ 的复杂度，考虑优化最复杂的一种转移。

枚举转移到的 $[L,R]$，则选取的 $-1$ 一定是最左侧或最右侧的 $-1$。

然后大力对着代码改，变成若干区间内的 $f$ 之和，二维前缀和即可。

好卡常。/dk/dk/dk

```cpp
constexpr int mod=998244353,N=1e3+5;
inline void inc(int &x,int y){x+=y,x-=x>=mod?mod:0;}
inline void dec(int &x,int y){x-=y,x+=x<0?mod:0;}
inline void cmax(int &x,int y){x=x>y?x:y;}
inline void cmin(int &x,int y){x=x<y?x:y;}
int n,m,a[N],pl[N][N],pr[N][N];
int pos[N],uc[N],us[N];
int pre[N],nxt[N],ip[N][N],iq[N][N];
int f[N][N],g[N][N];
void main(){
    cin.tie(0)->sync_with_stdio(0);
    cin>>n>>m;rep(i,1,n){cin>>a[i];if(a[i]==-1)us[i]=1;else pos[a[i]]=i,uc[a[i]]=1;}
    rep(i,1,n)pre[i]=a[i]==-1?i:pre[i-1];per(i,n,1)nxt[i]=a[i]==-1?i:nxt[i+1];
    rep(i,0,n-1)uc[i]^=1;rep(i,1,n)uc[i]+=uc[i-1],us[i]+=us[i-1];rep(l,0,n+1)rep(r,0,n+1)pl[l][r]=1,pr[l][r]=n;
    rep(i,1,m){int l,r;cin>>l>>r;cmax(pl[l][r],l),cmin(pr[l][r],r);}
    rep(l,1,n)per(r,n,l)cmax(pl[l][r],max(pl[l-1][r],pl[l][r+1])),cmin(pr[l][r],min(pr[l-1][r],pr[l][r+1]));
    rep(l,1,n)if(nxt[l])rep(r,nxt[l],n){
        int p=nxt[l],q=pre[r];int &pp=ip[l][r],&qq=iq[l][r];
        pp=r+1;while(pp-1>p&&pl[p][pp-1]==l&&pr[p][pp-1]==r)pp--;
        qq=l-1;while(qq+1<q&&pl[qq+1][q]==l&&pr[qq+1][q]==r)qq++;
    }
    if(pos[0])f[pl[pos[0]][pos[0]]][pr[pos[0]][pos[0]]]=1;else rep(i,1,n)if(a[i]==-1)f[pl[i][i]][pr[i][i]]=1;
    rep(_,1,n-1){
        if(pos[_]){
            rep(l,1,n)rep(r,l,n)if(f[l][r]){
                int L=min(l,pos[_]),R=max(r,pos[_]);
                inc(g[pl[L][R]][pr[L][R]],f[l][r]);
            }
        }
        else{
            per(l,n,1){
                int t=uc[_-1]+us[l-1];rep(r,l,n){
                    if(t<us[r])inc(g[l][r],f[l][r]);
                    inc(f[l][r],f[l][r-1]),inc(f[l][r],f[l+1][r]),dec(f[l][r],f[l+1][r-1]);
                    if(!f[l][r])continue;
                    int p=nxt[l],q=pre[r],pp=ip[l][r],qq=iq[l][r];if(p&&p<=r){
                        inc(g[l][r],f[p+1][r]),inc(g[l][r],f[l][q-1]);
                        if(p<qq)dec(g[l][r],f[p+1][q-1]),dec(g[l][r],f[qq+1][pp-1]);
                        else dec(g[l][r],f[p+1][pp-1]),dec(g[l][r],f[qq+1][q-1]);
                    }
                }
            }
        }
        rep(l,1,n)rep(r,l,n)f[l][r]=g[l][r],g[l][r]=0;
    }
    cout<<f[1][n]<<'\n';
}
```