#ifndef _COMPARE_VERSION_
#define _COMPARE_VERSION_

#include<iostream>
#include<vector>

using namespace std;

class Sol { 

public:
int compareVersion(string v1, string v2) {
    size_t mx_sz = max(v1.size(), v2.size());

    for(size_t i = 0, j = 0; i < v1.size() or j < v2.size(); ) {
        
        string s1, s2;
        size_t index_dot_1, index_dot_2;
        if(i < v1.size()) {
            index_dot_1 = v1.find_first_of(".", i);
            if(index_dot_1 != std::string::npos) {
                s1 = v1.substr(i, index_dot_1 - i);
                i = index_dot_1 + 1;
            }
            else {
                s1 = v1.substr(i, v1.size() - i);
                i = v1.size();
            }
        }

        if(j < v2.size()) {
            index_dot_2 = v2.find_first_of(".", j);
            if(index_dot_2 != std::string::npos) {
                s2 = v2.substr(j, index_dot_2 - j);
                j = index_dot_2 + 1;
            }
            else {
                s2 = v2.substr(j, v2.size() - j);
                j = v2.size();
            }
        }
    int n1 = s1.empty() ? 0 : stoi(s1);
    int n2 = s2.empty() ? 0 : stoi(s2);
        if(n1 > n2) {
            return 1;
        }
        else if(n1 < n2) {
            return -1;
        }
        else if(i == mx_sz or j == mx_sz) {
            return 0;
        }
    }
    return -1;
}
};

#endif


