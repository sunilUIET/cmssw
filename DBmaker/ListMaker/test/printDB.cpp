void PrintDB(){
   std::cout <<std::endl<< "---- Test Program for CondCachedIter ----"<<std::endl;
 
    std::string NameDB;
    NameDB ="sqlite_file:///afs/cern.ch/user/s/subansal/CMS/MuonAging/CMSSW_8_1_0_pre5/src/DBmaker/ListMaker/test/MuonSystemAging.db";
 
    std::string TagData;
    TagData = "MuonSystemAging_test";

    CondCachedIter <MuonSystemAging> *Iterator = new CondCachedIter<MuonSystemAging>;
    Iterator->create (NameDB,TagData);
    
 
    std::string NameFile = "DataA.txt";
    ofstream myfile;
     myfile.open (NameFile.c_str());
     const MuonSystemAging* reference;
     reference = Iterator->next();
     std::stringstream Inside;
     reference->print(Inside);
     myfile<<Inside.str();  
     myfile.close();      
               
}

