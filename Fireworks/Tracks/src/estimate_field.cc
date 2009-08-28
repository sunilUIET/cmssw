// -*- C++ -*-
//
// Package:     Tracks
// Class  :     estimate_field
// $Id: estimate_field.cc,v 1.2 2009/01/23 21:35:47 amraktad Exp $
//

#include "Math/Vector3D.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "Fireworks/Tracks/interface/estimate_field.h"

double
fw::estimate_field( const reco::Track& track )
{
   if ( !track.extra().isAvailable() ) return -1;
   // We have 3 states so we can form 3 pairs to check for curvature
   // In practice we want to avoid estimates over lost of material and
   // in regions with small field. Therefore we should look at the pair
   // based on POCA and closest state to it. Than we will estimate the
   // filed inside the solenoid. 
   if ( pow(track.outerPosition().x()-track.vx(),2)+pow(track.outerPosition().y()-track.vy(),2) <
	pow(track.innerPosition().x()-track.vx(),2)+pow(track.innerPosition().y()-track.vy(),2) )
     {
       double estimate = estimate_field( track.outerPosition().x(), 
					 track.outerPosition().y(),
					 track.vx(),
					 track.vy(),
					 track.px(),
					 track.py() );
       /* printf("outer-poca: \tPOCA Pt: %0.2f, \tinner Rho: %0.1f, \touter Rho: %0.1f, \tchange in pt: %0.1f%%, \testimate: %0.2f\n",
	      track.pt(), track.innerPosition().rho(), track.outerPosition().rho(), 
	      fabs( track.outerMomentum().rho()/track.pt()-1 )*100, estimate); */
       return estimate;
     }
   else
     {
       double estimate = estimate_field( track.innerPosition().x(), 
					 track.innerPosition().y(),
					 track.vx(),
					 track.vy(),
					 track.px(),
					 track.py() );
       /* printf("inner-poca: \tPOCA Pt: %0.2f, \tinner Rho: %0.1f, \touter Rho: %0.1f, \tchange in pt: %0.1f%%, \testimate: %0.2f\n",
	  track.pt(), track.innerPosition().rho(), track.outerPosition().rho(), 
	  fabs( track.innerMomentum().rho()/track.pt()-1 )*100, estimate); */
       return estimate;
     }
}

double
fw::estimate_field( double vx1, double vy1, double vx2, double vy2, double px, double py )
{
  math::XYZVector displacement(vx2-vx1, vy2-vy1, 0);
  math::XYZVector transverseMomentum(px, py, 0);
  double cosAlpha = transverseMomentum.Dot(displacement)/transverseMomentum.r()/displacement.r();
  return 200*sqrt(1-cosAlpha*cosAlpha)/0.2998*transverseMomentum.r()/displacement.r();
}
