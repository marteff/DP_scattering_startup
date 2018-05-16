#ifndef DMGENERATOR_H
#define DMGENERATOR_H 1

#include "TROOT.h"
#include "FairGenerator.h"
#include "TTree.h"                     
#include "TF1.h"                        
#include "TH1.h"                        
#include "TH2.h"                        
#include "TVector3.h"                        
#include "FairLogger.h"                 // for FairLogger, MESSAGE_ORIGIN
#include "vector"

class FairPrimaryGenerator;

class DMGenerator : public FairGenerator
{
 public:
  
	/** default constructor **/
	DMGenerator();
  
	/** destructor **/
	virtual ~DMGenerator();
  
	/** public method ReadEvent **/
	Bool_t ReadEvent(FairPrimaryGenerator*);  
	void SetPositions(Double_t zTa, Double_t zS=-3352., Double_t zE=-3051.){ //Dimensions according to nuTauTargetDesign=3
 		ztarget     = zTa; //z position of the target
		startZ      = zS;  //z start position of the tau neutrino det
		endZ        = zE;  //z end position of the tau neutrino det
		zRel	    = zS-zTa;	//relative position between the target and the tau neutrino det
	}
	virtual Bool_t Init(const char* fileName, int);
	virtual Bool_t Init(const char*);
  	Double_t MeanMaterialBudget(const Double_t *start, const Double_t *end, Double_t *mparam);
	Int_t GetNevents();


 private:
		
	
 protected:
	Bool_t dis, el, fFirst;
	Int_t parentid, fNevents, fn, dmpdg, pdgl, n_2ry, pdg_2ry[500];
	Double_t weight, ztarget, startZ, endZ, zRel;
	Double_t Edm, pxdm, pydm, pzdm;
	Double_t E_2ry[500], px_2ry[500], py_2ry[500], pz_2ry[500];
	TFile* fInputFile;	 //! pointer to a file
	TTree* fTree;		 //! pointer to a file
	FairLogger*  fLogger; //!   don't make it persistent, magic ROOT command

	ClassDef(DMGenerator,1);
};

#endif /* !DMGENERATOR_H */
