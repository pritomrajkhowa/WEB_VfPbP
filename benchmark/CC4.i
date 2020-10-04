extern void __VERIFIER_error() __attribute__ ((__noreturn__));
void __VERIFIER_assert(int cond) { if(!(cond)) { ERROR: __VERIFIER_error(); } }
int main( ) {
    int M;
    double f = 0;
    double g = 0;
    double a = 0;
    double b = 0;
    double c = 0;
    double d = 0;
    while(d<M){

         @f = 1 [1/2] 0;
         @g = 1 [1/2] 0;
         a = a + (1-a)*f*g;
         b = b + (1-b)*f*(1-g);
         c = c + (1-c)*(1-f)*g;
         d = d + (1-d)*(1-f)*(1-g);

   }

}



