#include<assert.h>
#include "CompareVersion.h"

using namespace std;

int main(int argc, char* argv[]) {

    
    Sol sol;
    // -1
    assert(sol.compareVersion("1.2", "1.3") == -1);
    
    assert(sol.compareVersion("1.2.3.4.5.6.7.8.9", "1.2.3.4.5.6.7.8.10") == -1);
    assert(sol.compareVersion("1", "2") == -1);
    assert(sol.compareVersion("0", "1") == -1);
    assert(sol.compareVersion("0.1", "0.2") == -1);

    // 0 
    assert(sol.compareVersion("0", "0") == 0);
    assert(sol.compareVersion("1.2.3.4.5.6.7.8.9", "1.2.3.4.5.6.7.8.9") == 0);
    assert(sol.compareVersion("1", "1") == 0);
    assert(sol.compareVersion("1.1", "1.1") == 0);
    assert(sol.compareVersion("0.9", "0.9") == 0);
    assert(sol.compareVersion("0.0", "0.0") == 0);
    assert(sol.compareVersion("0", "0") == 0);

    // 1
    assert(sol.compareVersion("0.1", "0.0") == 1);
    assert(sol.compareVersion("10.9", "7.3") == 1);
    assert(sol.compareVersion("1.2.3.4.5.6.7.8.9", "1.2.3.4.5.6.7.8") == 1);
    
    
    return 0;
}


