#ifndef MuonSystemAging_H
#define MuonSystemAging_H
/*  example of polymorphic condition
 *   *  LUT, function, mixed....
 *    * this is just a prototype: classes do not need to be defined and declared in the same file
 *     * at the moment though all derived classes better sit in the same package together with the base one
 *      */

#include "CondFormats/Serialization/interface/Serializable.h"
#include <cmath>
#include <iostream>
#include <vector>
#include <map>

enum CSCInefficiencyType { 
    EFF_CHAMBER=0, 
    EFF_STRIPS=1,
    EFF_WIRES=2 
};

class MuonSystemAging {
    public:
    MuonSystemAging();
    ~MuonSystemAging(){}
    std::vector<int>  m_RPCchambers;
    std::map<unsigned int, float>  m_DTChambEffs;
    std::map<unsigned int, std::pair<unsigned int, float> >  m_CSCChambEffs;
    double m_CSCineff;
   COND_SERIALIZABLE;
   };


#endif
