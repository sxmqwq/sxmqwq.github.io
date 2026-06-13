[problem link](https://www.luogu.com.cn/problem/P16910)

从前往后进行 dp，难点在于不能直接记录栈的状态。

考虑对于栈中的每个元素，在其加入时直接钦定是否弹出并产生贡献，即可使信息量减少。

具体设 $f_{i,j,0/1}=(x,y)$ 表示，考虑了前若干个操作，取了 $A$ 中前 $i$ 个元素，栈顶有 $j$ 个元素钦定弹出，是否有元素钦定不弹出，时的方案数和答案和。

转移 $1$ 是简单的。转移 $2$ 需讨论，要求栈顶钦定弹出时必须钦定弹出。转移 $3$ 需注意栈顶钦定不弹出时无法转移。特别注意 $A/B$ 被取完的情况。

答案就是最后的 $\sum_{0\le i\le n}f_{i,0,0/1}$，时间复杂度 $O(n^2m)$，滚动数组则空间复杂度 $O(n^2)$。

```cpp
#include<bits/stdc++.h>
#define TIME chrono::duration_cast<chrono::milliseconds>(chrono::high_resolution_clock::now().time_since_epoch()).count()
#define rep(i,l,r) for(int qwp=(r),i=(l);i<=qwp;i++)
#define per(i,r,l) for(int qwp=(l),i=(r);i>=qwp;i--)
#define fir first
#define sec second
using namespace std;
namespace c0dE1ng{
typedef pair<int,int> pii;
constexpr int mod=998244353,N=205,M=N*2;
void inc(int &x,int y){x+=y,x-=x>=mod?mod:0;}
void trs(pii &x,pii y,int z){inc(x.fir,y.fir),inc(x.sec,y.fir*1ll*z%mod),inc(x.sec,y.sec);}
int n,m,a[N],b[M];
pii f[N][N][2],g[N][N][2];
void slv(){
    cin>>n>>m;rep(i,1,n)cin>>a[i];rep(i,1,m)cin>>b[i];
    rep(i,0,n)rep(j,0,n)rep(k,0,1)f[i][j][k]={0,0};f[0][0][0]={1,0};
    rep(_,1,m){
        if(b[_]>>0&1){
            rep(i,0,n)rep(j,0,n)rep(k,0,1)if(f[i][j][k].fir){
                if(i==n)trs(g[i][j][k],f[i][j][k],0);
                else trs(g[i+1][j][k],f[i][j][k],a[i+1]);
            }
        }
        if(b[_]>>1&1){
            rep(i,0,n)rep(j,0,n)rep(k,0,1)if(f[i][j][k].fir){
                if(i==n)trs(g[i][j][k],f[i][j][k],0);
                else{
                    trs(g[i+1][j+1][k],f[i][j][k],a[i+1]);
                    if(!j)trs(g[i+1][j][1],f[i][j][k],0);
                }
            }
        }
        if(b[_]>>2&1){
            rep(i,0,n)rep(j,0,n)rep(k,0,1)if(f[i][j][k].fir){
                if(j)trs(g[i][j-1][k],f[i][j][k],0);
                else if(!k)trs(g[i][j][k],f[i][j][k],0);
            }
        }
        rep(i,0,n)rep(j,0,n)rep(k,0,1)f[i][j][k]=g[i][j][k],g[i][j][k]={0,0};
    }
    int ans=0;rep(i,0,n)rep(k,0,1)inc(ans,f[i][0][k].sec);
    cout<<ans<<'\n';
}
void main(){
    cin.tie(0)->sync_with_stdio(0);
    int T,csi;cin>>T>>csi;while(T--)slv();
}
}
int main(){
    auto _Tbe=TIME;c0dE1ng::main();auto _Ted=TIME;
    return cerr<<"\nTIME:"<<_Ted-_Tbe<<"ms\n",0;
}
/*
ulimit -s 1048576
g++ -O2 -std=c++14 -static A.cpp -o %;size %;./% < A.in > A.out
*/
```

所以为啥不是乘积而是求和啊。