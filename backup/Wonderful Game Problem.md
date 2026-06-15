## Statement

有 $n$ 种牌，每种牌有 $c_i$ 张，每获得 $a_i$ 张可以得 $b_i$ 分。

对于一次游戏，Alice 和 Bob 轮流从全可见牌堆中选取一张牌。Alice 希望最大化 Alice 得分，Bob 希望最小化 Alice 得分。

Alice 需要将所有牌分成数量相等的两组进行游戏，第一组 Alice 先手第二组 Bob 先手，求最优策略下 Alice 得分。

$\sum a_i\le 10^4$。

## Solution

先考虑一次游戏，其实赛时大概猜出来了，但是没敢写。/dk

经典模仿上一个人策略即可让两人都选出 $\lceil\frac{c_i}{2}\rceil$ 张牌。

感性理解一下，由于可以模仿，Alice 无法使该策略变优，Bob 也无法使该策略变劣。

那么只需考虑 $c_i\equiv -1\pmod{2a_i}$ 时可能的额外 $b_i$ 贡献，将所有这样的 $b_i$ 拿出来排序。

那么若 Alice 先手则取得奇数位置之和，否则取得偶数位置之和。

对于原问题考虑 dp。按 $b_i$ 排序，设 $f_{i,0/1,0/1}$ 表示考虑前若干种牌，有 $i$ 张牌分到第一次游戏，两次游戏已知的额外贡献次数奇偶性，时的答案。

转移是显然的，时间复杂度 $O((\sum c_i)^2)$。

继续观察一下，可以发现每有 $4a_i$ 张牌时直接给两次游戏各分 $2a_i$ 张牌是最优的，那么时间复杂度变为 $O((\sum a_i)^2)$。

大力卡常即可通过。/hsh

```cpp
constexpr int intinf=2e9,N=2005,A=1e4+5;
void cmax(int &x,int y){x=x>y?x:y;}
int n,a[N],b[N],c[N],ans;
int id[N];bool cmp(int x,int y){return b[x]>b[y];}
int m,f[A*2][2][2],g[A*2][2][2];
void main(){
    cin.tie(0)->sync_with_stdio(0);
    cin>>n;rep(i,1,n){
        cin>>a[i]>>c[i]>>b[i];
        while(c[i]>a[i]*4)ans+=b[i]*2,c[i]-=a[i]*4;
    }
    rep(i,1,n)m+=c[i],id[i]=i;sort(id+1,id+1+n,cmp);
    rep(i,0,m>>1)rep(j,0,1)rep(k,0,1)f[i][j][k]=g[i][j][k]=-intinf;f[0][0][1]=0;
    for(int __=1,ss=0;__<=n;__++){
        int _=id[__],s=a[_]*2;
        rep(w,0,c[_]){
            bool x=!((w+1)%s),y=!((c[_]-w+1)%s);int t=((w/s)+(c[_]-w)/s)*b[_];
            if(x){
                if(y){
                    rep(i,0,min(m>>1,ss))if(i+w<=m>>1){
                        rep(j,0,1)rep(k,0,1)if(f[i][j][k]!=-intinf)
                        cmax(g[i+w][j^1][k^1],f[i][j][k]+t+((j^1)+(k^1))*b[_]);
                    }
                }
                else{
                    rep(i,0,min(m>>1,ss))if(i+w<=m>>1){
                        rep(j,0,1)rep(k,0,1)if(f[i][j][k]!=-intinf)
                        cmax(g[i+w][j^1][k],f[i][j][k]+t+(j^1)*b[_]);
                    }
                }
            }
            else{
                if(y){
                    rep(i,0,min(m>>1,ss))if(i+w<=m>>1){
                        rep(j,0,1)rep(k,0,1)if(f[i][j][k]!=-intinf)
                        cmax(g[i+w][j][k^1],f[i][j][k]+t+(k^1)*b[_]);
                    }
                }
                else{
                    rep(i,0,min(m>>1,ss))if(i+w<=m>>1){
                        rep(j,0,1)rep(k,0,1)if(f[i][j][k]!=-intinf)
                        cmax(g[i+w][j][k],f[i][j][k]+t);
                    }
                }
            }
        }
        rep(i,0,min(m>>1,ss+=c[_]))rep(j,0,1)rep(k,0,1)f[i][j][k]=g[i][j][k],g[i][j][k]=-intinf;
    }
    int res=-intinf;rep(j,0,1)rep(k,0,1)cmax(res,f[m>>1][j][k]);cout<<(ans+=res)<<'\n';
}
```