extern void __VERIFIER_error() __attribute__ ((__noreturn__));
void __VERIFIER_assert(int cond) { if(!(cond)) { ERROR: __VERIFIER_error(); } }
int main( ) {
int M,L;
double x =0 , y = 0; 
int k = 0 ;
while(x<=L)
{   y = 0;
    while(y<=M){ y = y + uniform(-0.1,0.2); }
    x = x + uniform(-0.1,0.2); k = k+1;
}


}








