############################TESTS ON POTENTIALS################################
from __future__ import print_function, division
import os
import sys
import pytest
import numpy
import pynbody
from galpy import potential
from galpy.util import bovy_coords
_TRAVIS= bool(os.getenv('TRAVIS'))

#Test whether the normalization of the potential works
def test_normalize_potential():
    #Grab all of the potentials
    pots= [p for p in dir(potential) 
           if ('Potential' in p and not 'plot' in p and not 'RZTo' in p 
               and not 'FullTo' in p and not 'toPlanar' in p
               and not 'evaluate' in p)]
    pots.append('mockTwoPowerIntegerSphericalPotential')
    pots.append('specialTwoPowerSphericalPotential')
    pots.append('HernquistTwoPowerIntegerSphericalPotential')
    pots.append('JaffeTwoPowerIntegerSphericalPotential')
    pots.append('NFWTwoPowerIntegerSphericalPotential')
    pots.append('specialMiyamotoNagaiPotential')
    pots.append('specialPowerSphericalPotential')
    pots.append('specialFlattenedPowerPotential')
    pots.append('specialMN3ExponentialDiskPotentialPD')
    pots.append('specialMN3ExponentialDiskPotentialSECH')
    rmpots= ['Potential','MWPotential','MWPotential2014',
             'MovingObjectPotential',
             'interpRZPotential', 'linearPotential', 'planarAxiPotential',
             'planarPotential', 'verticalPotential','PotentialError',
             'SnapshotRZPotential','InterpSnapshotRZPotential']
    if False: #_TRAVIS: #travis CI
        rmpots.append('DoubleExponentialDiskPotential')
        rmpots.append('RazorThinExponentialDiskPotential')
    for p in rmpots:
        pots.remove(p)
    for p in pots:
        #if not 'NFW' in p: continue #For testing the test
        #Setup instance of potential
        try:
            tclass= getattr(potential,p)
        except AttributeError:
            tclass= getattr(sys.modules[__name__],p)
        tp= tclass()
        if hasattr(tp,'isNonAxi') and tp.isNonAxi:
            continue # skip, bc vcirc not well defined
        if not hasattr(tp,'normalize'): continue
        tp.normalize(1.)
        assert (tp.Rforce(1.,0.)+1.)**2. < 10.**-16., \
            "Normalization of %s potential fails" % p
        assert (tp.vcirc(1.)**2.-1.)**2. < 10.**-16., \
            "Normalization of %s potential fails" % p
        tp.normalize(.5)
        if hasattr(tp,'toPlanar'):
            ptp= tp.toPlanar()
        else:
            ptp= tp
        assert (ptp.Rforce(1.,0.)+.5)**2. < 10.**-16., \
            "Normalization of %s potential fails" % p
        assert (ptp.vcirc(1.)**2.-0.5)**2. < 10.**-16., \
            "Normalization of %s potential fails" % p

#Test whether the derivative of the potential is minus the force
def test_forceAsDeriv_potential():
    #Grab all of the potentials
    pots= [p for p in dir(potential) 
           if ('Potential' in p and not 'plot' in p and not 'RZTo' in p 
               and not 'FullTo' in p and not 'toPlanar' in p
               and not 'evaluate' in p)]
    pots.append('mockTwoPowerIntegerSphericalPotential')
    pots.append('specialTwoPowerSphericalPotential')
    pots.append('HernquistTwoPowerIntegerSphericalPotential')
    pots.append('JaffeTwoPowerIntegerSphericalPotential')
    pots.append('NFWTwoPowerIntegerSphericalPotential')
    pots.append('specialMiyamotoNagaiPotential')
    pots.append('specialMN3ExponentialDiskPotentialPD')
    pots.append('specialMN3ExponentialDiskPotentialSECH')
    pots.append('specialPowerSphericalPotential')
    pots.append('specialFlattenedPowerPotential')
    pots.append('testMWPotential')
    pots.append('testplanarMWPotential')
    pots.append('testlinearMWPotential')
    pots.append('mockInterpRZPotential')
    pots.append('mockSnapshotRZPotential')
    pots.append('mockInterpSnapshotRZPotential')
    pots.append('mockCosmphiDiskPotentialT1')
    pots.append('mockCosmphiDiskPotentialTm1')
    pots.append('mockCosmphiDiskPotentialTm5')
    pots.append('mockDehnenBarPotentialT1')
    pots.append('mockDehnenBarPotentialTm1')
    pots.append('mockDehnenBarPotentialTm5')
    pots.append('mockEllipticalDiskPotentialT1')
    pots.append('mockEllipticalDiskPotentialTm1')
    pots.append('mockEllipticalDiskPotentialTm5')
    pots.append('mockSteadyLogSpiralPotentialT1')
    pots.append('mockSteadyLogSpiralPotentialTm1')
    pots.append('mockSteadyLogSpiralPotentialTm5')
    pots.append('mockTransientLogSpiralPotential')
    pots.append('mockFlatEllipticalDiskPotential') #for evaluate w/ nonaxi lists
    pots.append('mockMovingObjectPotential')
    pots.append('mockMovingObjectExplSoftPotential')
    pots.append('oblateHernquistPotential')
    pots.append('oblateNFWPotential')
    pots.append('oblatenoGLNFWPotential')
    pots.append('oblateJaffePotential')
    pots.append('prolateHernquistPotential')
    pots.append('prolateNFWPotential')
    pots.append('prolateJaffePotential')
    pots.append('triaxialHernquistPotential')
    pots.append('triaxialNFWPotential')
    pots.append('triaxialJaffePotential')
    pots.append('zRotatedTriaxialNFWPotential')
    pots.append('yRotatedTriaxialNFWPotential')
    pots.append('fullyRotatedTriaxialNFWPotential')
    pots.append('fullyRotatednoGLTriaxialNFWPotential')
    pots.append('HernquistTwoPowerTriaxialPotential')
    pots.append('NFWTwoPowerTriaxialPotential')
    pots.append('JaffeTwoPowerTriaxialPotential')
    pots.append('mockSCFZeeuwPotential')
    pots.append('mockSCFNFWPotential')
    pots.append('mockSCFAxiDensity1Potential')
    pots.append('mockSCFAxiDensity2Potential')
    pots.append('mockSCFDensityPotential')
    pots.append('mockAxisymmetricFerrersPotential')
    pots.append('sech2DiskSCFPotential')
    pots.append('expwholeDiskSCFPotential')
    pots.append('nonaxiDiskSCFPotential')
    rmpots= ['Potential','MWPotential','MWPotential2014',
             'MovingObjectPotential',
             'interpRZPotential', 'linearPotential', 'planarAxiPotential',
             'planarPotential', 'verticalPotential','PotentialError',
             'SnapshotRZPotential','InterpSnapshotRZPotential']
    if False: #_TRAVIS: #travis CI
        rmpots.append('DoubleExponentialDiskPotential')
        rmpots.append('RazorThinExponentialDiskPotential')
    for p in rmpots:
        pots.remove(p)
    Rs= numpy.array([0.5,1.,2.])
    Zs= numpy.array([0.,.125,-.125,0.25,-0.25])
    phis= numpy.array([0.,0.5,-0.5,1.,-1.,
                       numpy.pi,0.5+numpy.pi,
                       1.+numpy.pi])
    #tolerances in log10
    tol= {}
    tol['default']= -8.
    tol['DoubleExponentialDiskPotential']= -6. #these are more difficult
    tol['RazorThinExponentialDiskPotential']= -6.
    tol['mockInterpRZPotential']= -4.
    for p in pots:
        #if not 'NFW' in p: continue #For testing the test
        #Setup instance of potential
        try:
            tclass= getattr(potential,p)
        except AttributeError:
            tclass= getattr(sys.modules[__name__],p)
        tp= tclass()
        if hasattr(tp,'normalize'): tp.normalize(1.)
        #Set tolerance
        if p in list(tol.keys()): ttol= tol[p]
        else: ttol= tol['default']
        #Radial force
        for ii in range(len(Rs)):
            for jj in range(len(Zs)):
                dr= 10.**-8.
                newR= Rs[ii]+dr
                dr= newR-Rs[ii] #Representable number
                if isinstance(tp,potential.linearPotential): 
                    mpotderivR= (potential.evaluatelinearPotentials(tp,Rs[ii])
                                 -potential.evaluatelinearPotentials(tp,Rs[ii]+dr))/dr
                    tRforce= potential.evaluatelinearForces(tp,Rs[ii])
                elif isinstance(tp,potential.planarPotential):
                    mpotderivR= (potential.evaluateplanarPotentials(tp,Rs[ii],phi=Zs[jj])-potential.evaluateplanarPotentials(tp,Rs[ii]+dr,phi=Zs[jj]))/dr
                    tRforce= potential.evaluateplanarRforces(tp,Rs[ii],
                                                             phi=Zs[jj])
                else:
                    mpotderivR= (potential.evaluatePotentials(tp,Rs[ii],Zs[jj],phi=0.)
                                 -potential.evaluatePotentials(tp,Rs[ii]+dr,Zs[jj],phi=0.))/dr
                    tRforce= potential.evaluateRforces(tp,Rs[ii],Zs[jj],phi=0.)
                if tRforce**2. < 10.**ttol:
                    assert mpotderivR**2. < 10.**ttol, \
                        "Calculation of the Radial force as the Radial derivative of the %s potential fails at (R,Z) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],Zs[jj],numpy.fabs(tRforce-mpotderivR), numpy.fabs((tRforce-mpotderivR)/tRforce))
                else:
                    assert (tRforce-mpotderivR)**2./tRforce**2. < 10.**ttol, \
                        "Calculation of the Radial force as the Radial derivative of the %s potential fails at (R,Z) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],Zs[jj],numpy.fabs(tRforce-mpotderivR), numpy.fabs((tRforce-mpotderivR)/tRforce))
        #Azimuthal force, if it exists
        if isinstance(tp,potential.linearPotential): continue
        for ii in range(len(Rs)):
            for jj in range(len(phis)):
                dphi= 10.**-8.
                newphi= phis[jj]+dphi
                dphi= newphi-phis[jj] #Representable number
                if isinstance(tp,potential.planarPotential):
                    mpotderivphi= (tp(Rs[ii],phi=phis[jj])-tp(Rs[ii],phi=phis[jj]+dphi))/dphi
                    tphiforce= potential.evaluateplanarphiforces(tp,Rs[ii],
                                                                 phi=phis[jj])
                else:
                    mpotderivphi= (tp(Rs[ii],0.05,phi=phis[jj])-tp(Rs[ii],0.05,phi=phis[jj]+dphi))/dphi
                    tphiforce= potential.evaluatephiforces(tp,Rs[ii],0.05,
                                                           phi=phis[jj])
                try:
                    if tphiforce**2. < 10.**ttol:
                        assert(mpotderivphi**2. < 10.**ttol)
                    else:
                        assert((tphiforce-mpotderivphi)**2./tphiforce**2. < 10.**ttol)
                except AssertionError:
                    if isinstance(tp,potential.planarPotential):
                        raise AssertionError("Calculation of the azimuthal force as the azimuthal derivative of the %s potential fails at (R,phi) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],phis[jj],numpy.fabs(tphiforce-mpotderivphi),numpy.fabs((tphiforce-mpotderivphi)/tphiforce)))
                    else:
                        raise AssertionError("Calculation of the azimuthal force as the azimuthal derivative of the %s potential fails at (R,Z,phi) = (%.3f,0.05,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],phis[jj],numpy.fabs(tphiforce-mpotderivphi),numpy.fabs((tphiforce-mpotderivphi)/tphiforce)))
        #Vertical force, if it exists
        if isinstance(tp,potential.planarPotential) \
                or isinstance(tp,potential.linearPotential): continue

        for ii in range(len(Rs)):
            for jj in range(len(Zs)):
                ##Excluding KuzminDiskPotential when z = 0
                if Zs[jj]==0 and isinstance(tp,potential.KuzminDiskPotential):
                    continue
                dz= 10.**-8.
                newZ= Zs[jj]+dz
                dz= newZ-Zs[jj] #Representable number
                mpotderivz= (tp(Rs[ii],Zs[jj])-tp(Rs[ii],Zs[jj]+dz,phi=0.))/dz
                tzforce= potential.evaluatezforces(tp,Rs[ii],Zs[jj],phi=0.)
                if tzforce**2. < 10.**ttol:
                    assert mpotderivz**2. < 10.**ttol, \
                        "Calculation of the vertical force as the vertical derivative of the %s potential fails at (R,Z) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],Zs[jj],numpy.fabs(mpotderivz),numpy.fabs((tzforce-mpotderivz)/tzforce))
                else:
                    assert (tzforce-mpotderivz)**2./tzforce**2. < 10.**ttol, \
"Calculation of the vertical force as the vertical derivative of the %s potential fails at (R,Z) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],Zs[jj],numpy.fabs(mpotderivz),numpy.fabs((tzforce-mpotderivz)/tzforce))

#Test whether the second derivative of the potential is minus the derivative of the force
def test_2ndDeriv_potential():
    #Grab all of the potentials
    pots= [p for p in dir(potential) 
           if ('Potential' in p and not 'plot' in p and not 'RZTo' in p 
               and not 'FullTo' in p and not 'toPlanar' in p
               and not 'evaluate' in p)]
    pots.append('mockTwoPowerIntegerSphericalPotential')
    pots.append('specialTwoPowerSphericalPotential')
    pots.append('HernquistTwoPowerIntegerSphericalPotential')
    pots.append('JaffeTwoPowerIntegerSphericalPotential')
    pots.append('NFWTwoPowerIntegerSphericalPotential')
    pots.append('specialMiyamotoNagaiPotential')
    pots.append('specialMN3ExponentialDiskPotentialPD')
    pots.append('specialMN3ExponentialDiskPotentialSECH')
    pots.append('specialPowerSphericalPotential')
    pots.append('specialFlattenedPowerPotential')
    pots.append('testMWPotential')
    pots.append('testplanarMWPotential')
    pots.append('testlinearMWPotential')
    pots.append('mockInterpRZPotential')
    pots.append('mockCosmphiDiskPotentialT1')
    pots.append('mockCosmphiDiskPotentialTm1')
    pots.append('mockCosmphiDiskPotentialTm5')
    pots.append('mockDehnenBarPotentialT1')
    pots.append('mockDehnenBarPotentialTm1')
    pots.append('mockDehnenBarPotentialTm5')
    pots.append('mockEllipticalDiskPotentialT1')
    pots.append('mockEllipticalDiskPotentialTm1')
    pots.append('mockEllipticalDiskPotentialTm5')
    pots.append('mockSteadyLogSpiralPotentialT1')
    pots.append('mockSteadyLogSpiralPotentialTm1')
    pots.append('mockSteadyLogSpiralPotentialTm5')
    pots.append('mockTransientLogSpiralPotential')
    pots.append('mockFlatEllipticalDiskPotential') #for evaluate w/ nonaxi lists
    pots.append('oblateHernquistPotential') # in case these are ever implemented
    pots.append('oblateNFWPotential')
    pots.append('oblatenoGLNFWPotential')
    pots.append('oblateJaffePotential')
    pots.append('prolateHernquistPotential')
    pots.append('prolateNFWPotential')
    pots.append('prolateJaffePotential')
    pots.append('triaxialHernquistPotential')
    pots.append('triaxialNFWPotential')
    pots.append('triaxialJaffePotential')
    pots.append('HernquistTwoPowerTriaxialPotential')
    pots.append('NFWTwoPowerTriaxialPotential')
    pots.append('JaffeTwoPowerTriaxialPotential')
    pots.append('mockAxisymmetricFerrersPotential')
    rmpots= ['Potential','MWPotential','MWPotential2014',
             'MovingObjectPotential',
             'interpRZPotential', 'linearPotential', 'planarAxiPotential',
             'planarPotential', 'verticalPotential','PotentialError',
             'SnapshotRZPotential','InterpSnapshotRZPotential']
    if False: #_TRAVIS: #travis CI
        rmpots.append('DoubleExponentialDiskPotential')
        rmpots.append('RazorThinExponentialDiskPotential')
    rmpots.append('DiskSCFPotential') # 2nd derivs not implemented yet, but placeholders exist
    for p in rmpots:
        pots.remove(p)
    Rs= numpy.array([0.5,1.,2.])
    Zs= numpy.array([0.,.125,-.125,0.25,-0.25])
    phis= numpy.array([0.,0.5,-0.5,1.,-1.,
                       numpy.pi,0.5+numpy.pi,
                       1.+numpy.pi])
    #tolerances in log10
    tol= {}
    tol['default']= -8.
    tol['DoubleExponentialDiskPotential']= -3. #these are more difficult
    tol['RazorThinExponentialDiskPotential']= -6.
    tol['mockInterpRZPotential']= -4.
    tol['DehnenBarPotential']= -7.
    for p in pots:
        #if not 'NFW' in p: continue #For testing the test
        #Setup instance of potential
        try:
            tclass= getattr(potential,p)
        except AttributeError:
            tclass= getattr(sys.modules[__name__],p)
        tp= tclass()
        if hasattr(tp,'normalize'): tp.normalize(1.)
        #Set tolerance
        if p in list(tol.keys()): ttol= tol[p]
        else: ttol= tol['default']
        #2nd radial
        if hasattr(tp,'_R2deriv'):
            for ii in range(len(Rs)):
                for jj in range(len(Zs)):
                    if p == 'RazorThinExponentialDiskPotential' and numpy.fabs(Zs[jj]) > 0.: continue #Not implemented
                    dr= 10.**-8.
                    newR= Rs[ii]+dr
                    dr= newR-Rs[ii] #Representable number
                    if isinstance(tp,potential.linearPotential): 
                        mRforcederivR= (tp.Rforce(Rs[ii])-tp.Rforce(Rs[ii]+dr))/dr
                        tR2deriv= tp.R2deriv(Rs[ii])
                    elif isinstance(tp,potential.planarPotential): 
                        mRforcederivR= (tp.Rforce(Rs[ii],Zs[jj])-tp.Rforce(Rs[ii]+dr,Zs[jj]))/dr
                        tR2deriv= potential.evaluateplanarR2derivs(tp,Rs[ii],
                                                                   phi=Zs[jj])
                    else:
                        mRforcederivR= (tp.Rforce(Rs[ii],Zs[jj])-tp.Rforce(Rs[ii]+dr,Zs[jj]))/dr
                        tR2deriv= potential.evaluateR2derivs(tp,Rs[ii],Zs[jj],phi=0.)
                    if tR2deriv**2. < 10.**ttol:
                        assert mRforcederivR**2. < 10.**ttol, \
                            "Calculation of the second Radial derivative of the potential as the Radial derivative of the %s Radial force fails at (R,Z) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],Zs[jj],numpy.fabs(tR2deriv-mRforcederivR), numpy.fabs((tR2deriv-mRforcederivR)/tR2deriv))
                    else:
                        assert (tR2deriv-mRforcederivR)**2./tR2deriv**2. < 10.**ttol, \
                            "Calculation of the second Radial derivative of the potential as the Radial derivative of the %s Radial force fails at (R,Z) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],Zs[jj],numpy.fabs(tR2deriv-mRforcederivR), numpy.fabs((tR2deriv-mRforcederivR)/tR2deriv))
        #2nd azimuthal
        if not isinstance(tp,potential.linearPotential) \
                and hasattr(tp,'_phi2deriv'):
            for ii in range(len(Rs)):
                for jj in range(len(phis)):
                    dphi= 10.**-8.
                    newphi= phis[jj]+dphi
                    dphi= newphi-phis[jj] #Representable number
                    if isinstance(tp,potential.planarPotential):
                        mphiforcederivphi= (tp.phiforce(Rs[ii],phi=phis[jj])-tp.phiforce(Rs[ii],phi=phis[jj]+dphi))/dphi
                        tphi2deriv= tp.phi2deriv(Rs[ii],phi=phis[jj])
                    else:
                        mphiforcederivphi= (tp.phiforce(Rs[ii],0.05,phi=phis[jj])-tp.phiforce(Rs[ii],0.05,phi=phis[jj]+dphi))/dphi
                        tphi2deriv= tp.phi2deriv(Rs[ii],0.05,phi=phis[jj])
                    try:
                        if tphi2deriv**2. < 10.**ttol:
                            assert(mphiforcederivphi**2. < 10.**ttol)
                        else:
                            assert((tphi2deriv-mphiforcederivphi)**2./tphi2deriv**2. < 10.**ttol)
                    except AssertionError:
                        if isinstance(tp,potential.planarPotential):
                            raise AssertionError("Calculation of the second azimuthal derivative of the potential as the azimuthal derivative of the %s azimuthal force fails at (R,phi) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],phis[jj],numpy.fabs(tphi2deriv-mphiforcederivphi), numpy.fabs((tphi2deriv-mphiforcederivphi)/tphi2deriv)))
                        else:
                            raise AssertionError("Calculation of the second azimuthal derivative of the potential as the azimuthal derivative of the %s azimuthal force fails at (R,Z,phi) = (%.3f,0.05,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],phis[jj],numpy.fabs(tphi2deriv-mphiforcederivphi), numpy.fabs((tphi2deriv-mphiforcederivphi)/tphi2deriv)))
        #mixed radial azimuthal: Isn't this the same as what's below??
        if not isinstance(tp,potential.linearPotential) \
                and hasattr(tp,'_Rphideriv'):
            for ii in range(len(Rs)):
                for jj in range(len(phis)):
                    dphi= 10.**-8.
                    newphi= phis[jj]+dphi
                    dphi= newphi-phis[jj] #Representable number
                    if isinstance(tp,potential.planarPotential):
                        mRforcederivphi= (tp.Rforce(Rs[ii],phi=phis[jj])-tp.Rforce(Rs[ii],phi=phis[jj]+dphi))/dphi
                        tRphideriv= tp.Rphideriv(Rs[ii],phi=phis[jj])
                    else:
                        mRforcederivphi= (tp.Rforce(Rs[ii],0.05,phi=phis[jj])-tp.Rforce(Rs[ii],0.05,phi=phis[jj]+dphi))/dphi
                        tRphideriv= tp.Rphideriv(Rs[ii],0.05,phi=phis[jj])
                    try:
                        if tRphideriv**2. < 10.**ttol:
                            assert(mRforcederivphi**2. < 10.**ttol)
                        else:
                            assert((tRphideriv-mRforcederivphi)**2./tRphideriv**2. < 10.**ttol)
                    except AssertionError:
                        if isinstance(tp,potential.planarPotential):
                            raise AssertionError("Calculation of the mixed radial, azimuthal derivative of the potential as the azimuthal derivative of the %s Radial force fails at (R,phi) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],phis[jj],numpy.fabs(tRphideriv-mRforcederivphi), numpy.fabs((tRphideriv-mRforcederivphi)/tRphideriv)))
                        else:
                            raise AssertionError("Calculation of the mixed radial, azimuthal derivative of the potential as the azimuthal derivative of the %s azimuthal force fails at (R,Z,phi) = (%.3f,0.05,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],phis[jj],numpy.fabs(tphi2deriv-mphiforcederivphi), numpy.fabs((tphi2deriv-mphiforcederivphi)/tphi2deriv)))
        #2nd vertical
        if not isinstance(tp,potential.planarPotential) \
                and not isinstance(tp,potential.linearPotential) \
                and hasattr(tp,'_z2deriv'):
            for ii in range(len(Rs)):
                for jj in range(len(Zs)):
                    if p == 'RazorThinExponentialDiskPotential': continue #Not implemented, or badly defined
                    if p == 'TwoPowerSphericalPotential': continue #Not implemented, or badly defined
                    if p == 'mockTwoPowerIntegerSphericalPotential': continue #Not implemented, or badly defined
                    if p == 'specialTwoPowerSphericalPotential': continue #Not implemented, or badly defined
                    if p == 'HernquistTwoPowerIntegerSphericalPotential': continue #Not implemented, or badly defined
                    if p == 'JaffeTwoPowerIntegerSphericalPotential': continue #Not implemented, or badly defined
                    if p == 'NFWTwoPowerIntegerSphericalPotential': continue #Not implemented, or badly defined
                    #Excluding KuzminDiskPotential at z = 0
                    if p == 'KuzminDiskPotential' and Zs[jj] == 0: continue  
                    dz= 10.**-8.
                    newz= Zs[jj]+dz
                    dz= newz-Zs[jj] #Representable number
                    mzforcederivz= (tp.zforce(Rs[ii],Zs[jj])-tp.zforce(Rs[ii],Zs[jj]+dz))/dz
                    tz2deriv= potential.evaluatez2derivs(tp,Rs[ii],Zs[jj],phi=0.)
                    if tz2deriv**2. < 10.**ttol:
                        assert mzforcederivz**2. < 10.**ttol, \
                            "Calculation of the second vertical derivative of the potential as the vertical derivative of the %s vertical force fails at (R,Z) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],Zs[jj],numpy.fabs(tz2deriv-mzforcederivz), numpy.fabs((tz2deriv-mzforcederivz)/tz2deriv))
                    else:
                        assert (tz2deriv-mzforcederivz)**2./tz2deriv**2. < 10.**ttol, \
                            "Calculation of the second vertical derivative of the potential as the vertical derivative of the %s vertical force fails at (R,Z) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],Zs[jj],numpy.fabs(tz2deriv-mzforcederivz), numpy.fabs((tz2deriv-mzforcederivz)/tz2deriv))
        #mixed radial vertical
        if not isinstance(tp,potential.planarPotential) \
                and not isinstance(tp,potential.linearPotential) \
                and hasattr(tp,'_Rzderiv'):             
            for ii in range(len(Rs)):
                for jj in range(len(Zs)):
                    #Excluding KuzminDiskPotential at z = 0
                    if p == 'KuzminDiskPotential' and Zs[jj] == 0: continue 
#                    if p == 'RazorThinExponentialDiskPotential': continue #Not implemented, or badly defined
                    dz= 10.**-8.
                    newz= Zs[jj]+dz
                    dz= newz-Zs[jj] #Representable number
                    mRforcederivz= (tp.Rforce(Rs[ii],Zs[jj])-tp.Rforce(Rs[ii],Zs[jj]+dz))/dz
                    tRzderiv= potential.evaluateRzderivs(tp,Rs[ii],Zs[jj],phi=0.)
                    if tRzderiv**2. < 10.**ttol:
                        assert mRforcederivz**2. < 10.**ttol, \
                            "Calculation of the mixed radial vertical derivative of the potential as the vertical derivative of the %s radial force fails at (R,Z) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],Zs[jj],numpy.fabs(tRzderiv-mRforcederivz), numpy.fabs((tRzderiv-mRforcederivz)/tRzderiv))
                    else:
                        assert (tRzderiv-mRforcederivz)**2./tRzderiv**2. < 10.**ttol, \
"Calculation of the mixed radial vertical derivative of the potential as the vertical derivative of the %s radial force fails at (R,Z) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],Zs[jj],numpy.fabs(tRzderiv-mRforcederivz), numpy.fabs((tRzderiv-mRforcederivz)/tRzderiv))                        
        #mixed radial, azimuthal
        if not isinstance(tp,potential.linearPotential) \
                and hasattr(tp,'_Rphideriv'):
            for ii in range(len(Rs)):
                for jj in range(len(phis)):
#                    if p == 'RazorThinExponentialDiskPotential': continue #Not implemented, or badly defined
                    dphi= 10.**-8.
                    newphi= phis[jj]+dphi
                    dphi= newphi-phis[jj] #Representable number
                    if isinstance(tp,potential.planarPotential):
                        mRforcederivphi= (tp.Rforce(Rs[ii],phi=phis[jj])\
                                              -tp.Rforce(Rs[ii],phi=phis[jj]+dphi))/dphi
                        tRphideriv= potential.evaluateplanarPotentials(tp,Rs[ii],
                                                                       phi=phis[jj],dR=1,dphi=1)
                    else:
                        mRforcederivphi= (tp.Rforce(Rs[ii],0.1,phi=phis[jj])\
                                              -tp.Rforce(Rs[ii],0.1,phi=phis[jj]+dphi))/dphi
                        tRphideriv= potential.evaluatePotentials(tp,Rs[ii],0.1,
                                                                 phi=phis[jj],dR=1,dphi=1)
                    if tRphideriv**2. < 10.**ttol:
                        assert mRforcederivphi**2. < 10.**ttol, \
                            "Calculation of the mixed radial azimuthal derivative of the potential as the azimuthal derivative of the %s radial force fails at (R,phi) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],phis[jj],numpy.fabs(tRphideriv-mRforcederivphi), numpy.fabs((tRphideriv-mRforcederivphi)/tRphideriv))
                    else:
                        assert (tRphideriv-mRforcederivphi)**2./tRphideriv**2. < 10.**ttol, \
"Calculation of the mixed radial azimuthal derivative of the potential as the azimuthal derivative of the %s radial force fails at (R,phi) = (%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],phis[jj],numpy.fabs(tRphideriv-mRforcederivphi), numpy.fabs((tRphideriv-mRforcederivphi)/tRphideriv))

#Test whether the Poisson equation is satisfied if _dens and the relevant second derivatives are implemented
def test_poisson_potential():
    #Grab all of the potentials
    pots= [p for p in dir(potential) 
           if ('Potential' in p and not 'plot' in p and not 'RZTo' in p 
               and not 'FullTo' in p and not 'toPlanar' in p
               and not 'evaluate' in p)]
    pots.append('mockTwoPowerIntegerSphericalPotential')
    pots.append('specialTwoPowerSphericalPotential')
    pots.append('HernquistTwoPowerIntegerSphericalPotential')
    pots.append('JaffeTwoPowerIntegerSphericalPotential')
    pots.append('NFWTwoPowerIntegerSphericalPotential')
    pots.append('specialMiyamotoNagaiPotential')
    pots.append('specialMN3ExponentialDiskPotentialPD')
    pots.append('specialMN3ExponentialDiskPotentialSECH')
    pots.append('specialFlattenedPowerPotential')
    pots.append('specialPowerSphericalPotential')
    pots.append('testMWPotential')
    pots.append('testplanarMWPotential')
    pots.append('testlinearMWPotential')
    pots.append('oblateHernquistPotential') # in cae these are ever implemented
    pots.append('oblateNFWPotential')
    pots.append('oblateJaffePotential')
    pots.append('prolateHernquistPotential')
    pots.append('prolateNFWPotential')
    pots.append('prolateJaffePotential')
    pots.append('triaxialHernquistPotential')
    pots.append('triaxialNFWPotential')
    pots.append('triaxialJaffePotential')
    pots.append('HernquistTwoPowerTriaxialPotential')
    pots.append('NFWTwoPowerTriaxialPotential')
    pots.append('JaffeTwoPowerTriaxialPotential')
    rmpots= ['Potential','MWPotential','MWPotential2014',
             'MovingObjectPotential',
             'interpRZPotential', 'linearPotential', 'planarAxiPotential',
             'planarPotential', 'verticalPotential','PotentialError',
             'SnapshotRZPotential','InterpSnapshotRZPotential']
    if False: #_TRAVIS: #travis CI
        rmpots.append('DoubleExponentialDiskPotential')
        rmpots.append('RazorThinExponentialDiskPotential')
    rmpots.append('DiskSCFPotential') # 2nd derivs not implemented yet, but placeholders exist
    for p in rmpots:
        pots.remove(p)
    Rs= numpy.array([0.5,1.,2.])
    Zs= numpy.array([0.,.125,-.125,0.25,-0.25])
    phis= numpy.array([0.,0.5,-0.5,1.,-1.,
                       numpy.pi,0.5+numpy.pi,
                       1.+numpy.pi])
    #tolerances in log10
    tol= {}
    tol['default']= -8.
    tol['DoubleExponentialDiskPotential']= -3. #these are more difficult
    #tol['RazorThinExponentialDiskPotential']= -6.
    for p in pots:
        #if not 'NFW' in p: continue #For testing the test
        #if 'Isochrone' in p: continue #For testing the test
        #Setup instance of potential
        try:
            tclass= getattr(potential,p)
        except AttributeError:
            tclass= getattr(sys.modules[__name__],p)
        tp= tclass()
        if hasattr(tp,'normalize'): tp.normalize(1.)
        #Set tolerance
        if p in list(tol.keys()): ttol= tol[p]
        else: ttol= tol['default']
        #2nd radial
        if not hasattr(tp,'_dens') or not hasattr(tp,'_R2deriv') \
                or not hasattr(tp,'_Rforce') or not hasattr(tp,'phi2deriv') \
                or not hasattr(tp,'_z2deriv'):
            continue
        for ii in range(len(Rs)):
            for jj in range(len(Zs)):
                for kk in range(len(phis)):
                    tpoissondens= tp.dens(Rs[ii],Zs[jj],phi=phis[kk],
                                         forcepoisson=True)
                    tdens= potential.evaluateDensities(tp,Rs[ii],Zs[jj],
                                                       phi=phis[kk],
                                                       forcepoisson=False)
                    if tdens**2. < 10.**ttol:
                        assert tpoissondens**2. < 10.**ttol, \
                            "Poisson equation relation between the derivatives of the potential and the implemented density is not satisfied for the %s potential at (R,Z,phi) = (%.3f,%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],Zs[jj],phis[kk],numpy.fabs(tdens-tpoissondens), numpy.fabs((tdens-tpoissondens)/tdens))
                    else:
                        assert (tpoissondens-tdens)**2./tdens**2. < 10.**ttol, \
                            "Poisson equation relation between the derivatives of the potential and the implemented density is not satisfied for the %s potential at (R,Z,phi) = (%.3f,%.3f,%.3f); diff = %e, rel. diff = %e" % (p,Rs[ii],Zs[jj],phis[kk],numpy.fabs(tdens-tpoissondens), numpy.fabs((tdens-tpoissondens)/tdens))
    return None
                        
#Test whether the _evaluate function is correctly implemented in specifying derivatives
def test_evaluateAndDerivs_potential():
    #Grab all of the potentials
    pots= [p for p in dir(potential) 
           if ('Potential' in p and not 'plot' in p and not 'RZTo' in p 
               and not 'FullTo' in p and not 'toPlanar' in p
               and not 'evaluate' in p)]
    pots.append('mockTwoPowerIntegerSphericalPotential')
    pots.append('specialTwoPowerSphericalPotential')
    pots.append('HernquistTwoPowerIntegerSphericalPotential')
    pots.append('JaffeTwoPowerIntegerSphericalPotential')
    pots.append('NFWTwoPowerIntegerSphericalPotential')
    pots.append('specialMiyamotoNagaiPotential')
    pots.append('specialMN3ExponentialDiskPotentialPD')
    pots.append('specialMN3ExponentialDiskPotentialSECH')
    pots.append('specialFlattenedPowerPotential')
    pots.append('specialPowerSphericalPotential')
    pots.append('mockCosmphiDiskPotentialT1')
    pots.append('mockCosmphiDiskPotentialTm1')
    pots.append('mockCosmphiDiskPotentialTm5')
    pots.append('mockDehnenBarPotentialT1')
    pots.append('mockDehnenBarPotentialTm1')
    pots.append('mockDehnenBarPotentialTm5')
    pots.append('mockEllipticalDiskPotentialT1')
    pots.append('mockEllipticalDiskPotentialTm1')
    pots.append('mockEllipticalDiskPotentialTm5')
    pots.append('mockSteadyLogSpiralPotentialT1')
    pots.append('mockSteadyLogSpiralPotentialTm1')
    pots.append('mockSteadyLogSpiralPotentialTm5')
    pots.append('mockTransientLogSpiralPotential')
    pots.append('mockMovingObjectPotential')
    pots.append('oblateHernquistPotential') # in cae these are ever implemented
    pots.append('oblateNFWPotential')
    pots.append('oblateJaffePotential')
    pots.append('prolateHernquistPotential')
    pots.append('prolateNFWPotential')
    pots.append('prolateJaffePotential')
    pots.append('triaxialHernquistPotential')
    pots.append('triaxialNFWPotential')
    pots.append('triaxialJaffePotential')
    pots.append('mockSCFZeeuwPotential')
    pots.append('mockSCFNFWPotential')
    pots.append('mockSCFAxiDensity1Potential')
    pots.append('mockSCFAxiDensity2Potential')
    pots.append('mockSCFDensityPotential')
    pots.append('sech2DiskSCFPotential')
    pots.append('expwholeDiskSCFPotential')
    pots.append('nonaxiDiskSCFPotential')
    rmpots= ['Potential','MWPotential','MWPotential2014',
             'MovingObjectPotential',
             'interpRZPotential', 'linearPotential', 'planarAxiPotential',
             'planarPotential', 'verticalPotential','PotentialError',
             'SnapshotRZPotential','InterpSnapshotRZPotential']
    if False: #_TRAVIS: #travis CI
        rmpots.append('DoubleExponentialDiskPotential')
        rmpots.append('RazorThinExponentialDiskPotential')
    for p in rmpots:
        pots.remove(p)
    #tolerances in log10
    tol= {}
    tol['default']= -12.
    #tol['DoubleExponentialDiskPotential']= -3. #these are more difficult
    #tol['RazorThinExponentialDiskPotential']= -6.
    for p in pots:
        #if 'Isochrone' in p: continue #For testing the test
        #Setup instance of potential
        try:
            tclass= getattr(potential,p)
        except AttributeError:
            tclass= getattr(sys.modules[__name__],p)
        tp= tclass()
        if hasattr(tp,'normalize'): tp.normalize(1.)
        #Set tolerance
        if p in list(tol.keys()): ttol= tol[p]
        else: ttol= tol['default']
        #1st radial
        if isinstance(tp,potential.linearPotential): 
            continue
        elif isinstance(tp,potential.planarPotential): 
            tevaldr= tp(1.2,phi=0.1,dR=1)
            trforce= tp.Rforce(1.2,phi=0.1)
        else:
            tevaldr= tp(1.2,0.1,phi=0.1,dR=1)
            trforce= tp.Rforce(1.2,0.1,phi=0.1)
        if not tevaldr is None:
            if tevaldr**2. < 10.**ttol:
                assert trforce**2. < 10.**ttol, \
"Calculation of radial derivative through _evaluate and Rforce inconsistent for the %s potential" % p
            else:
                assert (tevaldr+trforce)**2./tevaldr**2. < 10.**ttol, \
                    "Calculation of radial derivative through _evaluate and Rforce inconsistent for the %s potential" % p                
        #2nd radial
        hasR2= True
        from galpy.potential import PotentialError
        if 'RazorThin' in p: R2z= 0.
        else: R2z= 0.1
        try:
            if isinstance(tp,potential.planarPotential): 
                tp.R2deriv(1.2)
            else:
                tp.R2deriv(1.2,R2z)
        except PotentialError:
            hasR2= False
        if hasR2:
            if isinstance(tp,potential.planarPotential): 
                tevaldr2= tp(1.2,phi=0.1,dR=2)
                tr2deriv= tp.R2deriv(1.2,phi=0.1)
            else:
                tevaldr2= tp(1.2,R2z,phi=0.1,dR=2)
                tr2deriv= tp.R2deriv(1.2,R2z,phi=0.1)
            if not tevaldr2 is None:
                if tevaldr2**2. < 10.**ttol:
                    assert tr2deriv*2. < 10.**ttol, \
                        "Calculation of 2nd radial derivative through _evaluate and R2deriv inconsistent for the %s potential" % p
                else:
                    assert (tevaldr2-tr2deriv)**2./tevaldr2**2. < 10.**ttol, \
                        "Calculation of 2nd radial derivative through _evaluate and R2deriv inconsistent for the %s potential" % p                    
        #1st phi
        if isinstance(tp,potential.planarPotential): 
            tevaldphi= tp(1.2,phi=0.1,dphi=1)
            tphiforce= tp.phiforce(1.2,phi=0.1)
        else:
            tevaldphi= tp(1.2,0.1,phi=0.1,dphi=1)
            tphiforce= tp.phiforce(1.2,0.1,phi=0.1)
        if not tevaldphi is None:
            if tevaldphi**2. < 10.**ttol:
                assert tphiforce**2. < 10.**ttol, \
                    "Calculation of azimuthal derivative through _evaluate and phiforce inconsistent for the %s potential" % p
            else:
                assert (tevaldphi+tphiforce)**2./tevaldphi**2. < 10.**ttol, \
                    "Calculation of azimuthal derivative through _evaluate and phiforce inconsistent for the %s potential" % p
        #2nd phi
        hasphi2= True
        try:
            if isinstance(tp,potential.planarPotential): 
                tp.phi2deriv(1.2,phi=0.1)
            else:
                tp.phi2deriv(1.2,0.1,phi=0.1)
        except (PotentialError,AttributeError):
            hasphi2= False
        if hasphi2 and hasattr(tp,'_phi2deriv'):
            if isinstance(tp,potential.planarPotential): 
                tevaldphi2= tp(1.2,phi=0.1,dphi=2)
                tphi2deriv= tp.phi2deriv(1.2,phi=0.1)
            else:
                tevaldphi2= tp(1.2,0.1,phi=0.1,dphi=2)
                tphi2deriv= tp.phi2deriv(1.2,0.1,phi=0.1)
            if not tevaldphi2 is None:
                if tevaldphi2**2. < 10.**ttol:
                    assert tphi2deriv*2. < 10.**ttol, \
                        "Calculation of 2nd azimuthal derivative through _evaluate and phi2deriv inconsistent for the %s potential" % p
                else:
                    assert (tevaldphi2-tphi2deriv)**2./tevaldphi2**2. < 10.**ttol, \
                        "Calculation of 2nd azimuthal derivative through _evaluate and phi2deriv inconsistent for the %s potential" % p
        continue
        #mixed radial,vertical
        if isinstance(tp,potential.planarPotential): 
            tevaldrz= tp(1.2,0.1,phi=0.1,dR=1,dz=1)
            trzderiv= tp.Rzderiv(1.2,0.1,phi=0.1)
        else:
            tevaldrz= tp(1.2,0.1,phi=0.1,dR=1,dz=1)
            trzderiv= tp.Rzderiv(1.2,0.1,phi=0.1)
        if not tevaldrz is None:
            if tevaldrz**2. < 10.**ttol:
                assert trzderiv*2. < 10.**ttol, \
                    "Calculation of mixed radial,vertical derivative through _evaluate and z2deriv inconsistent for the %s potential" % p
            else:
                assert (tevaldrz-trzderiv)**2./tevaldrz**2. < 10.**ttol, \
"Calculation of mixed radial,vertical derivative through _evaluate and z2deriv inconsistent for the %s potential" % p
    #Finally test that much higher derivatives are not implemented
    try: tp(1.2,0.1,dR=4,dphi=10)
    except NotImplementedError: pass
    else: raise AssertionError('Higher-order derivative request in potential __call__ does not raise NotImplementedError')
    return None

# Test that the spherically radial force is correct
def test_rforce():
    # Spherical potentials: Rforce = rforce x R / r; zforce = rforce x z /r
    pp= potential.PlummerPotential(amp=2.,b=2.)
    R,z= 1.3, 0.4
    r= numpy.sqrt(R*R+z*z)
    assert numpy.fabs(pp.Rforce(R,z)*r/R-pp.rforce(R,z)) < 10.**-10., 'rforce does not behave as expected for spherical potentials'
    assert numpy.fabs(potential.evaluateRforces(pp,R,z)*r/R-potential.evaluaterforces(pp,R,z)) < 10.**-10., 'evaluaterforces does not behave as expected for spherical potentials'
    return None
    

# Check that the masses are calculated correctly for spherical potentials
def test_mass_spher():
    #PowerPotential close to Kepler should be very steep
    pp= potential.PowerSphericalPotential(amp=2.,alpha=2.999)
    kp= potential.KeplerPotential(amp=2.)
    assert numpy.fabs((((3.-2.999)/(4.*numpy.pi)*pp.mass(10.)-kp.mass(10.)))/kp.mass(10.)) < 10.**-2., "Mass for PowerSphericalPotential close to KeplerPotential is not close to KeplerPotential's mass"
    pp= potential.PowerSphericalPotential(amp=2.)
    #mass = amp x r^(3-alpha)
    tR= 1.
    assert numpy.fabs(pp.mass(tR,forceint=True)-pp._amp*tR**(3.-pp.alpha)) < 10.**-10., 'Mass for PowerSphericalPotential not as expected'
    tR= 2.
    assert numpy.fabs(pp.mass(tR,forceint=True)-pp._amp*tR**(3.-pp.alpha)) < 10.**-10., 'Mass for PowerSphericalPotential not as expected'
    tR= 20.
    assert numpy.fabs(pp.mass(tR,forceint=True)-pp._amp*tR**(3.-pp.alpha)) < 10.**-10., 'Mass for PowerSphericalPotential not as expected'
    #Test that for a cut-off potential, the mass far beyond the cut-off is 
    # 2pi rc^(3-alpha) gamma(1.5-alpha/2)
    pp= potential.PowerSphericalPotentialwCutoff(amp=2.)
    from scipy import special
    expecMass= 2.*pp._amp*numpy.pi*pp.rc**(3.-pp.alpha)*special.gamma(1.5-pp.alpha/2.)
    tR= 5.
    assert numpy.fabs((pp.mass(tR,forceint=True)-expecMass)/expecMass) < 10.**-6., 'Mass of PowerSphericalPotentialwCutoff far beyond the cut-off not as expected'
    tR= 15.
    assert numpy.fabs((pp.mass(tR,forceint=True)-expecMass)/expecMass) < 10.**-6., 'Mass of PowerSphericalPotentialwCutoff far beyond the cut-off not as expected'
    tR= 50.
    assert numpy.fabs((pp.mass(tR,forceint=True)-expecMass)/expecMass) < 10.**-6., 'Mass of PowerSphericalPotentialwCutoff far beyond the cut-off not as expected'
    #Jaffe and Hernquist both have finite masses, NFW diverges logarithmically
    jp= potential.JaffePotential(amp=2.,a=0.1)
    hp= potential.HernquistPotential(amp=2.,a=0.1)
    np= potential.NFWPotential(amp=2.,a=0.1)
    tR= 10.
    # Limiting behavior
    jaffemass= jp._amp*(1.-jp.a/tR)
    hernmass= hp._amp/2.*(1.-2.*hp.a/tR)
    nfwmass= np._amp*(numpy.log(tR/np.a)-1.+np.a/tR)
    assert numpy.fabs((jp.mass(tR,forceint=True)-jaffemass)/jaffemass) < 10.**-3., 'Limit mass for Jaffe potential not as expected'
    assert numpy.fabs((hp.mass(tR,forceint=True)-hernmass)/hernmass) < 10.**-3., 'Limit mass for Jaffe potential not as expected'
    assert numpy.fabs((np.mass(tR,forceint=True)-nfwmass)/nfwmass) < 10.**-2., 'Limit mass for NFW potential not as expected'
    tR= 200.
    # Limiting behavior, add z, to test that too
    jaffemass= jp._amp*(1.-jp.a/tR)
    hernmass= hp._amp/2.*(1.-2.*hp.a/tR)
    nfwmass= np._amp*(numpy.log(tR/np.a)-1.+np.a/tR)
    assert numpy.fabs((jp.mass(tR,forceint=True)-jaffemass)/jaffemass) < 10.**-6., 'Limit mass for Jaffe potential not as expected'
    assert numpy.fabs((hp.mass(tR,forceint=True)-hernmass)/hernmass) < 10.**-6., 'Limit mass for Jaffe potential not as expected'
    assert numpy.fabs((np.mass(tR,forceint=True)-nfwmass)/nfwmass) < 10.**-4., 'Limit mass for NFW potential not as expected'
    tR, tz= 200., 10.
    tr= numpy.sqrt(tR**2.+tz**2.)
    # Limiting behavior, add z, to test that too
    jaffemass= jp._amp*(1.-jp.a/tr)
    hernmass= hp._amp/2.*(1.-2.*hp.a/tr)
    nfwmass= np._amp*(numpy.log(tr/np.a)-1.+np.a/tr)
    assert numpy.fabs((jp.mass(tR,z=tz,forceint=False)-jaffemass)/jaffemass) < 10.**-6., 'Limit mass for Jaffe potential not as expected'
    assert numpy.fabs((hp.mass(tR,z=tz,forceint=False)-hernmass)/hernmass) < 10.**-6., 'Limit mass for Jaffe potential not as expected'
    assert numpy.fabs((np.mass(tR,z=tz,forceint=False)-nfwmass)/nfwmass) < 10.**-4., 'Limit mass for NFW potential not as expected'
    return None

# Check that the masses are implemented correctly for spherical potentials
def test_mass_spher_analytic():
    #TwoPowerSphericalPotentials all have explicitly implemented masses
    jp= potential.JaffePotential(amp=2.)
    hp= potential.HernquistPotential(amp=2.)
    np= potential.NFWPotential(amp=2.)
    tp= potential.TwoPowerSphericalPotential(amp=2.)
    tR= 2.
    assert numpy.fabs(jp.mass(tR,forceint=True)-jp.mass(tR)) < 10.**-10., 'Explicit mass does not agree with integral of the density for Jaffe potential'
    assert numpy.fabs(hp.mass(tR,forceint=True)-hp.mass(tR)) < 10.**-10., 'Explicit mass does not agree with integral of the density for Hernquist potential'
    assert numpy.fabs(np.mass(tR,forceint=True)-np.mass(tR)) < 10.**-10., 'Explicit mass does not agree with integral of the density for NFW potential'
    assert numpy.fabs(tp.mass(tR,forceint=True)-tp.mass(tR)) < 10.**-10., 'Explicit mass does not agree with integral of the density for TwoPowerSpherical potential'
    assert numpy.fabs(tp.mass(tR,forceint=True)-tp.mass(numpy.sqrt(tR**2.-1**2.),z=1.)) < 10.**-10., 'Explicit mass does not agree with integral of the density for TwoPowerSpherical potential, for not z is None'
    return None

# Check that the masses are calculated correctly for axisymmetric potentials
def test_mass_axi():
    #For Miyamoto-Nagai, we know that mass integrated over everything should be equal to amp, so
    mp= potential.MiyamotoNagaiPotential(amp=1.)
    assert numpy.fabs(mp.mass(200.,20.)-1.) < 0.01, 'Total mass of Miyamoto-Nagai potential w/ amp=1 is not equal to 1'
    #For a double-exponential disk potential, the 
    # mass(R,z) = amp x hR^2 x hz x (1-(1+R/hR)xe^(-R/hR)) x (1-e^(-Z/hz)
    dp= potential.DoubleExponentialDiskPotential(amp=2.)
    def dblexpmass(r,z,dp):
        return 4.*numpy.pi*dp._amp*dp._hr**2.*dp._hz*(1.-(1.+r/dp._hr)*numpy.exp(-r/dp._hr))*(1.-numpy.exp(-z/dp._hz))
    tR,tz= 0.01,0.01
    assert numpy.fabs((dp.mass(tR,tz,forceint=True)-dblexpmass(tR,tz,dp))/dblexpmass(tR,tz,dp)) < 10.**-10., 'Mass for DoubleExponentialDiskPotential incorrect'
    tR,tz= 0.1,0.05
    assert numpy.fabs((dp.mass(tR,tz,forceint=True)-dblexpmass(tR,tz,dp))/dblexpmass(tR,tz,dp)) < 10.**-10., 'Mass for DoubleExponentialDiskPotential incorrect'
    tR,tz= 1.,0.1
    assert numpy.fabs((dp.mass(tR,tz,forceint=True)-dblexpmass(tR,tz,dp))/dblexpmass(tR,tz,dp)) < 10.**-10., 'Mass for DoubleExponentialDiskPotential incorrect'
    tR,tz= 5.,0.1
    assert numpy.fabs((dp.mass(tR,tz,forceint=True)-dblexpmass(tR,tz,dp))/dblexpmass(tR,tz,dp)) < 10.**-10., 'Mass for DoubleExponentialDiskPotential incorrect'
    tR,tz= 5.,1.
    assert numpy.fabs((dp.mass(tR,tz,forceint=True)-dblexpmass(tR,tz,dp))/dblexpmass(tR,tz,dp)) < 10.**-10., 'Mass for DoubleExponentialDiskPotential incorrect'
    tR,tz= 100.,100.
    assert numpy.fabs((dp.mass(tR,tz,forceint=True)-dblexpmass(tR,tz,dp))/dblexpmass(tR,tz,dp)) < 10.**-6., 'Mass for DoubleExponentialDiskPotential incorrect'
    #Test that nonAxi raises error
    from galpy.orbit import Orbit
    mop= potential.MovingObjectPotential(Orbit([1.,0.1,1.1,0.1,0.,0.]))
    try: mop.mass(1.,0.)
    except NotImplementedError: pass
    else: raise AssertionError('mass for non-axisymmetric potential should have raised NotImplementedError, but did not')
    return None

# Check that toVertical and toPlanar work
def test_toVertical_toPlanar():
    #Grab all of the potentials
    pots= [p for p in dir(potential) 
           if ('Potential' in p and not 'plot' in p and not 'RZTo' in p 
               and not 'FullTo' in p and not 'toPlanar' in p
               and not 'evaluate' in p)]
    rmpots= ['Potential','MWPotential','MWPotential2014',
             'MovingObjectPotential',
             'interpRZPotential', 'linearPotential', 'planarAxiPotential',
             'planarPotential', 'verticalPotential','PotentialError',
             'SnapshotRZPotential','InterpSnapshotRZPotential']
    if False: #_TRAVIS: #travis CI
        rmpots.append('DoubleExponentialDiskPotential')
        rmpots.append('RazorThinExponentialDiskPotential')
    for p in rmpots:
        pots.remove(p)
    for p in pots:
        #Setup instance of potential
        try:
            tclass= getattr(potential,p)
        except AttributeError:
            tclass= getattr(sys.modules[__name__],p)
        tp= tclass()
        if not hasattr(tp,'normalize'): continue #skip these
        tp.normalize(1.)
        if isinstance(tp,potential.linearPotential) or \
                isinstance(tp,potential.planarPotential):
            continue
        tpp= tp.toPlanar()
        assert isinstance(tpp,potential.planarPotential), \
            "Conversion into planar potential of potential %s fails" % p
        tlp= tp.toVertical(1.)
        assert isinstance(tlp,potential.linearPotential), \
            "Conversion into linear potential of potential %s fails" % p

def test_RZToplanarPotential():
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    plp= potential.RZToplanarPotential(lp)
    assert isinstance(plp,potential.planarPotential), 'Running an RZPotential through RZToplanarPotential does not produce a planarPotential'
    #Check that a planarPotential through RZToplanarPotential is still planar
    pplp= potential.RZToplanarPotential(lp)
    assert isinstance(pplp,potential.planarPotential), 'Running a planarPotential through RZToplanarPotential does not produce a planarPotential'
    try:
        plp= potential.RZToplanarPotential('something else')
    except potential.PotentialError:
        pass
    else:
        raise AssertionError('Using RZToplanarPotential with a string rather than an RZPotential or a planarPotential did not raise PotentialError')
    return None

def test_toPlanarPotential():
    tnp= potential.TriaxialNFWPotential(normalize=1.,b=0.5)
    ptnp= potential.toPlanarPotential(tnp)
    assert isinstance(ptnp,potential.planarPotential), 'Running a non-axisymmetric Potential through toPlanarPotential does not produce a planarPotential'
    # Also for list
    ptnp= potential.toPlanarPotential([tnp])
    assert isinstance(ptnp[0],potential.planarPotential), 'Running a non-axisymmetric Potential through toPlanarPotential does not produce a planarPotential'
    #Check that a planarPotential through toPlanarPotential is still planar
    pptnp= potential.toPlanarPotential(tnp)
    assert isinstance(pptnp,potential.planarPotential), 'Running a planarPotential through toPlanarPotential does not produce a planarPotential'
    try:
        ptnp= potential.toPlanarPotential('something else')
    except potential.PotentialError:
        pass
    else:
        raise AssertionError('Using toPlanarPotential with a string rather than an Potential or a planarPotential did not raise PotentialError')
    return None

# Sanity check the derivative of the rotation curve and the frequencies in the plane
def test_dvcircdR_omegac_epifreq_rl_vesc():
    #Derivative of rotation curve
    #LogarithmicHaloPotential: rotation everywhere flat
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    assert lp.dvcircdR(1.)**2. < 10.**-16., \
        "LogarithmicHaloPotential's rotation curve is not flat at R=1"
    assert lp.dvcircdR(0.5)**2. < 10.**-16., \
        "LogarithmicHaloPotential's rotation curve is not flat at R=0.5"
    assert lp.dvcircdR(2.)**2. < 10.**-16., \
        "LogarithmicHaloPotential's rotation curve is not flat at R=2"
    #Kepler potential, vc = vc_0(R/R0)^-0.5 -> dvcdR= -0.5 vc_0 (R/R0)**-1.5
    kp= potential.KeplerPotential(normalize=1.)
    assert (kp.dvcircdR(1.)+0.5)**2. < 10.**-16., \
        "KeplerPotential's rotation curve is not what it should be at R=1"
    assert (kp.dvcircdR(0.5)+0.5**-0.5)**2. < 10.**-16., \
        "KeplerPotential's rotation curve is not what it should be at R=0.5"
    assert (kp.dvcircdR(2.)+0.5**2.5)**2. < 10.**-16., \
        "KeplerPotential's rotation curve is not what it should be at R=2"
    #Rotational frequency
    assert (lp.omegac(1.)-1.)**2. < 10.**-16., \
        "LogarithmicHalo's rotational frequency is off at R=1"
    assert (lp.omegac(0.5)-2.)**2. < 10.**-16., \
        "LogarithmicHalo's rotational frequency is off at R=0.5"
    assert (lp.omegac(2.)-0.5)**2. < 10.**-16., \
        "LogarithmicHalo's rotational frequency is off at R=2"
    assert (lp.toPlanar().omegac(2.)-0.5)**2. < 10.**-16., \
        "LogarithmicHalo's rotational frequency is off at R=2 through planarPotential"
    #Epicycle frequency, flat rotation curve
    assert (lp.epifreq(1.)-numpy.sqrt(2.)*lp.omegac(1.))**2. < 10.**-16., \
        "LogarithmicHalo's epicycle and rotational frequency are inconsistent with kappa = sqrt(2) Omega at R=1"
    assert (lp.epifreq(0.5)-numpy.sqrt(2.)*lp.omegac(0.5))**2. < 10.**-16., \
        "LogarithmicHalo's epicycle and rotational frequency are inconsistent with kappa = sqrt(2) Omega at R=0.5"
    assert (lp.epifreq(2.0)-numpy.sqrt(2.)*lp.omegac(2.0))**2. < 10.**-16., \
        "LogarithmicHalo's epicycle and rotational frequency are inconsistent with kappa = sqrt(2) Omega at R=2"
    assert (lp.toPlanar().epifreq(2.0)-numpy.sqrt(2.)*lp.omegac(2.0))**2. < 10.**-16., \
        "LogarithmicHalo's epicycle and rotational frequency are inconsistent with kappa = sqrt(2) Omega at R=, through planar2"
    #Epicycle frequency, Kepler
    assert (kp.epifreq(1.)-kp.omegac(1.))**2. < 10.**-16., \
        "KeplerPotential's epicycle and rotational frequency are inconsistent with kappa = Omega at R=1"
    assert (kp.epifreq(0.5)-kp.omegac(0.5))**2. < 10.**-16., \
        "KeplerPotential's epicycle and rotational frequency are inconsistent with kappa = Omega at R=0.5"
    assert (kp.epifreq(2.)-kp.omegac(2.))**2. < 10.**-16., \
        "KeplerPotential's epicycle and rotational frequency are inconsistent with kappa = Omega at R=2"
    #Check radius of circular orbit, Kepler
    assert (kp.rl(1.)-1.)**2. < 10.**-16., \
        "KeplerPotential's radius of a circular orbit is wrong at Lz=1."
    assert (kp.rl(0.5)-1./4.)**2. < 10.**-16., \
        "KeplerPotential's radius of a circular orbit is wrong at Lz=0.5"
    assert (kp.rl(2.)-4.)**2. < 10.**-16., \
        "KeplerPotential's radius of a circular orbit is wrong at Lz=2."
    #Check radius of circular orbit, PowerSphericalPotential with close-to-flat rotation curve
    pp= potential.PowerSphericalPotential(alpha=1.8,normalize=1.)
    assert (pp.rl(1.)-1.)**2. < 10.**-16., \
        "PowerSphericalPotential's radius of a circular orbit is wrong at Lz=1."
    assert (pp.rl(0.5)-0.5**(10./11.))**2. < 10.**-16., \
        "PowerSphericalPotential's radius of a circular orbit is wrong at Lz=0.5"
    assert (pp.rl(2.)-2.**(10./11.))**2. < 10.**-16., \
        "PowerSphericalPotential's radius of a circular orbit is wrong at Lz=2."
    #Check radius of circular orbit, PowerSphericalPotential with steeper rotation curve
    pp= potential.PowerSphericalPotential(alpha=0.5,normalize=1.)
    assert (pp.rl(1.)-1.)**2. < 10.**-16., \
        "PowerSphericalPotential's radius of a circular orbit is wrong at Lz=1."
    assert (pp.rl(0.0625)-0.0625**(4./7.))**2. < 10.**-16., \
        "PowerSphericalPotential's radius of a circular orbit is wrong at Lz=0.0625"
    assert (pp.rl(16.)-16.**(4./7.))**2. < 10.**-16., \
        "PowerSphericalPotential's radius of a circular orbit is wrong at Lz=16."
    #Escape velocity of Kepler potential
    assert (kp.vesc(1.)**2.-2.)**2. < 10.**-16., \
        "KeplerPotential's escape velocity is wrong at R=1"
    assert (kp.vesc(0.5)**2.-2.*kp.vcirc(0.5)**2.)**2. < 10.**-16., \
        "KeplerPotential's escape velocity is wrong at R=0.5"
    assert (kp.vesc(2.)**2.-2.*kp.vcirc(2.)**2.)**2. < 10.**-16., \
        "KeplerPotential's escape velocity is wrong at R=2"
    assert (kp.toPlanar().vesc(2.)**2.-2.*kp.vcirc(2.)**2.)**2. < 10.**-16., \
        "KeplerPotential's escape velocity is wrong at R=2, through planar"
    # W/ different interface
    assert (kp.vcirc(1.)-potential.vcirc(kp,1.))**2. < 10.**-16., \
        "KeplerPotential's circular velocity does not agree between kp.vcirc and vcirc(kp)"
    assert (kp.vcirc(1.)-potential.vcirc(kp.toPlanar(),1.))**2. < 10.**-16., \
        "KeplerPotential's circular velocity does not agree between kp.vcirc and vcirc(kp.toPlanar)"
    assert (kp.vesc(1.)-potential.vesc(kp,1.))**2. < 10.**-16., \
        "KeplerPotential's escape velocity does not agree between kp.vesc and vesc(kp)"
    assert (kp.vesc(1.)-potential.vesc(kp.toPlanar(),1.))**2. < 10.**-16., \
        "KeplerPotential's escape velocity does not agree between kp.vesc and vesc(kp.toPlanar)"
    return None

def test_vcirc_phi_axi():
    # Test that giving phi to vcirc for an axisymmetric potential doesn't
    # affect the answer
    kp= potential.KeplerPotential(normalize=1.)
    phis= numpy.linspace(0.,numpy.pi,101)
    vcs= numpy.array([kp.vcirc(1.,phi) for phi in phis])
    assert numpy.all(numpy.fabs(vcs-1.) < 10.**-8.), 'Setting phi= in vcirc for axisymmetric potential gives different answers for different phi'
    # One at a different radius
    R= 0.5
    vcs= numpy.array([kp.vcirc(R,phi) for phi in phis])
    assert numpy.all(numpy.fabs(vcs-kp.vcirc(R)) < 10.**-8.), 'Setting phi= in vcirc for axisymmetric potential gives different answers for different phi'
    return None

def test_vcirc_phi_nonaxi():
    # Test that giving phi to vcirc for a non-axisymmetric potential does
    # affect the answer
    tnp= potential.TriaxialNFWPotential(b=0.4,normalize=1.)
    # limited phi range
    phis= numpy.linspace(numpy.pi/5.,numpy.pi/2.,5)
    vcs= numpy.array([tnp.vcirc(1.,phi) for phi in phis])
    assert numpy.all(numpy.fabs(vcs-1.) > 0.01), 'Setting phi= in vcirc for axisymmetric potential does not give different answers for different phi'
    # One at a different radius
    R= 0.5
    vcs= numpy.array([tnp.vcirc(R,phi) for phi in phis])
    assert numpy.all(numpy.fabs(vcs-tnp.vcirc(R,phi=0.)) > 0.01), 'Setting phi= in vcirc for axisymmetric potential does not give different answers for different phi'
    return None

def test_vcirc_vesc_special():
    #Test some special cases of vcirc and vesc
    dp= potential.EllipticalDiskPotential()
    try:
        potential.plotRotcurve([dp])
    except (AttributeError,potential.PotentialError): #should be raised
        pass
    else:
        raise AssertionError("plotRotcurve for non-axisymmetric potential should have raised AttributeError, but didn't")
    try:
        potential.plotEscapecurve([dp])
    except AttributeError: #should be raised
        pass
    else:
        raise AssertionError("plotEscapecurve for non-axisymmetric potential should have raised AttributeError, but didn't")
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    assert numpy.fabs(potential.calcRotcurve(lp,0.8)-lp.vcirc(0.8)) < 10.**-16., 'Circular velocity calculated with calcRotcurve not the same as that calculated with vcirc'
    assert numpy.fabs(potential.calcEscapecurve(lp,0.8)-lp.vesc(0.8)) < 10.**-16., 'Escape velocity calculated with calcEscapecurve not the same as that calculated with vcirc'
    return None        

def test_lindbladR():
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    assert numpy.fabs(lp.lindbladR(0.5,'corotation')-2.) < 10.**-10., 'Location of co-rotation resonance is wrong for LogarithmicHaloPotential'
    assert numpy.fabs(lp.omegac(lp.lindbladR(0.5,2))-2./(2.-numpy.sqrt(2.))*0.5) < 10.**-14., 'Location of m=2 resonance is wrong for LogarithmicHaloPotential'
    assert numpy.fabs(lp.omegac(lp.lindbladR(0.5,-2))+2./(-2.-numpy.sqrt(2.))*0.5) < 10.**-14., 'Location of m=-2 resonance is wrong for LogarithmicHaloPotential'
    #Also through general interface
    assert numpy.fabs(lp.omegac(potential.lindbladR(lp,0.5,-2))+2./(-2.-numpy.sqrt(2.))*0.5) < 10.**-14., 'Location of m=-2 resonance is wrong for LogarithmicHaloPotential'
    #Also for planar
    assert numpy.fabs(lp.omegac(lp.toPlanar().lindbladR(0.5,-2))+2./(-2.-numpy.sqrt(2.))*0.5) < 10.**-14., 'Location of m=-2 resonance is wrong for LogarithmicHaloPotential'
    #Test non-existent ones
    mp= potential.MiyamotoNagaiPotential(normalize=1.,a=0.3)
    assert mp.lindbladR(3.,2) is None, 'MiyamotoNagai w/ OmegaP=3 should not have a inner m=2 LindbladR'
    assert mp.lindbladR(6.,'corotation') is None, 'MiyamotoNagai w/ OmegaP=6 should not have a inner m=2 LindbladR'
    #Test error
    try:
        lp.lindbladR(0.5,'wrong resonance')
    except IOError:
        pass
    else:
        raise AssertionError("lindbladR w/ wrong m input should have raised IOError, but didn't")
    return None

def test_vterm():
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    assert numpy.fabs(lp.vterm(30.,deg=True)-0.5*(lp.omegac(0.5)-1.)) < 10.**-10., 'vterm for LogarithmicHaloPotential at l=30 is incorrect'
    assert numpy.fabs(lp.vterm(numpy.pi/3.,deg=False)-numpy.sqrt(3.)/2.*(lp.omegac(numpy.sqrt(3.)/2.)-1.)) < 10.**-10., 'vterm for LogarithmicHaloPotential at l=60 in rad is incorrect'
    #Also using general interface
    assert numpy.fabs(potential.vterm(lp,30.,deg=True)-0.5*(lp.omegac(0.5)-1.)) < 10.**-10., 'vterm for LogarithmicHaloPotential at l=30 is incorrect'
    assert numpy.fabs(potential.vterm(lp,numpy.pi/3.,deg=False)-numpy.sqrt(3.)/2.*(lp.omegac(numpy.sqrt(3.)/2.)-1.)) < 10.**-10., 'vterm for LogarithmicHaloPotential at l=60 in rad is incorrect'
    return None

def test_flattening():
    #Simple tests: LogarithmicHalo
    qs= [0.75,1.,1.25]
    for q in qs:
        lp= potential.LogarithmicHaloPotential(normalize=1.,q=q)
        assert (lp.flattening(1.,0.001)-q)**2. < 10.**-16., \
            "Flattening of LogarithmicHaloPotential w/ q= %f is not equal to q  at (R,z) = (1.,0.001)" % q
        assert (lp.flattening(1.,0.1)-q)**2. < 10.**-16., \
            "Flattening of LogarithmicHaloPotential w/ q= %f is not equal to q  at (R,z) = (1.,0.1)" % q
        assert (lp.flattening(0.5,0.001)-q)**2. < 10.**-16., \
            "Flattening of LogarithmicHaloPotential w/ q= %f is not equal to q  at (R,z) = (0.5,0.001)" % q
        assert (lp.flattening(0.5,0.1)-q)**2. < 10.**-16., \
            "Flattening of LogarithmicHaloPotential w/ q= %f is not equal to q  at (R,z) = (0.5,0.1)" % q
        #One test with the general interface
        assert (potential.flattening(lp,0.5,0.1)-q)**2. < 10.**-16., \
            "Flattening of LogarithmicHaloPotential w/ q= %f is not equal to q  at (R,z) = (0.5,0.1), through potential.flattening" % q
    #Check some spherical potentials
    kp= potential.KeplerPotential(normalize=1.)
    assert (kp.flattening(1.,0.02)-1.)**2. < 10.**-16., \
        "Flattening of KeplerPotential is not equal to 1 at (R,z) = (1.,0.02)"
    np= potential.NFWPotential(normalize=1.,a=5.)
    assert (np.flattening(1.,0.02)-1.)**2. < 10.**-16., \
        "Flattening of NFWPotential is not equal to 1 at (R,z) = (1.,0.02)"
    hp= potential.HernquistPotential(normalize=1.,a=5.)
    assert (hp.flattening(1.,0.02)-1.)**2. < 10.**-16., \
        "Flattening of HernquistPotential is not equal to 1 at (R,z) = (1.,0.02)"
    #Disk potentials should be oblate everywhere
    mp= potential.MiyamotoNagaiPotential(normalize=1.,a=0.5,b=0.05)
    assert mp.flattening(1.,0.1) <= 1., \
        "Flattening of MiyamotoNagaiPotential w/ a=0.5, b=0.05 is > 1 at (R,z) = (1.,0.1)"
    assert mp.flattening(1.,2.) <= 1., \
        "Flattening of MiyamotoNagaiPotential w/ a=0.5, b=0.05 is > 1 at (R,z) = (1.,2.)"
    assert mp.flattening(3.,3.) <= 1., \
        "Flattening of MiyamotoNagaiPotential w/ a=0.5, b=0.05 is > 1 at (R,z) = (3.,3.)"
    return None

def test_verticalfreq():
    #For spherical potentials, vertical freq should be equal to rotational freq
    lp= potential.LogarithmicHaloPotential(normalize=1.,q=1.)
    kp= potential.KeplerPotential(normalize=1.)
    np= potential.NFWPotential(normalize=1.)
    bp= potential.BurkertPotential(normalize=1.)
    rs= numpy.linspace(0.2,2.,21)
    for r in rs:
        assert numpy.fabs(lp.verticalfreq(r)-lp.omegac(r)) < 10.**-10., \
            'Verticalfreq for spherical potential does not equal rotational freq'
        assert numpy.fabs(kp.verticalfreq(r)-kp.omegac(r)) < 10.**-10., \
            'Verticalfreq for spherical potential does not equal rotational freq'
        #Through general interface
        assert numpy.fabs(potential.verticalfreq(np,r)-np.omegac(r)) < 10.**-10., \
            'Verticalfreq for spherical potential does not equal rotational freq'
        assert numpy.fabs(potential.verticalfreq([bp],r)-bp.omegac(r)) < 10.**-10., \
            'Verticalfreq for spherical potential does not equal rotational freq'
    #For Double-exponential disk potential, epi^2+vert^2-2*rot^2 =~ 0 (explicitly, because we use a Kepler potential)
    if True: #not _TRAVIS:
        dp= potential.DoubleExponentialDiskPotential(normalize=1.,hr=0.05,hz=0.01)
        assert numpy.fabs(dp.epifreq(1.)**2.+dp.verticalfreq(1.)**2.-2.*dp.omegac(1.)**2.) < 10.**-6., 'epi^2+vert^2-2*rot^2 !=~ 0 for dblexp potential, very far from center'
        #Closer to the center, this becomes the Poisson eqn.
        assert numpy.fabs(dp.epifreq(.125)**2.+dp.verticalfreq(.125)**2.-2.*dp.omegac(.125)**2.-4.*numpy.pi*dp.dens(0.125,0.))/4./numpy.pi/dp.dens(0.125,0.) < 10.**-3., 'epi^2+vert^2-2*rot^2 !=~ dens for dblexp potential'
    return None

def test_planar_nonaxi():
    dp= potential.EllipticalDiskPotential()
    try:
        potential.evaluateplanarPotentials(dp,1.)
    except potential.PotentialError:
        pass
    else:
        raise AssertionError('evaluateplanarPotentials for non-axisymmetric potential w/o specifying phi did not raise PotentialError')
    try:
        potential.evaluateplanarRforces(dp,1.)
    except potential.PotentialError:
        pass
    else:
        raise AssertionError('evaluateplanarRforces for non-axisymmetric potential w/o specifying phi did not raise PotentialError')
    try:
        potential.evaluateplanarphiforces(dp,1.)
    except potential.PotentialError:
        pass
    else:
        raise AssertionError('evaluateplanarphiforces for non-axisymmetric potential w/o specifying phi did not raise PotentialError')
    try:
        potential.evaluateplanarR2derivs(dp,1.)
    except potential.PotentialError:
        pass
    else:
        raise AssertionError('evaluateplanarR2derivs for non-axisymmetric potential w/o specifying phi did not raise PotentialError')
    return None

def test_ExpDisk_special():
    #Test some special cases for the ExponentialDisk potentials
    #if _TRAVIS: return None
    #Test that array input works
    dp= potential.DoubleExponentialDiskPotential(normalize=1.)
    rs= numpy.linspace(0.1,2.11)
    zs= numpy.ones_like(rs)*0.1
    #Potential itself
    dpevals= numpy.array([dp(r,z) for (r,z) in zip(rs,zs)])
    assert numpy.all(numpy.fabs(dp(rs,zs)-dpevals) < 10.**-10.), \
        'DoubleExppnentialDiskPotential evaluation does not work as expected for array inputs'
    #Rforce
    dpevals= numpy.array([dp.Rforce(r,z) for (r,z) in zip(rs,zs)])
    assert numpy.all(numpy.fabs(dp.Rforce(rs,zs)-dpevals) < 10.**-10.), \
        'DoubleExppnentialDiskPotential Rforce evaluation does not work as expected for array inputs'
    #zforce
    dpevals= numpy.array([dp.zforce(r,z) for (r,z) in zip(rs,zs)])
    assert numpy.all(numpy.fabs(dp.zforce(rs,zs)-dpevals) < 10.**-10.), \
        'DoubleExppnentialDiskPotential zforce evaluation does not work as expected for array inputs'
    #R2deriv
    dpevals= numpy.array([dp.R2deriv(r,z) for (r,z) in zip(rs,zs)])
    assert numpy.all(numpy.fabs(dp.R2deriv(rs,zs)-dpevals) < 10.**-10.), \
        'DoubleExppnentialDiskPotential R2deriv evaluation does not work as expected for array inputs'
    #z2deriv
    dpevals= numpy.array([dp.z2deriv(r,z) for (r,z) in zip(rs,zs)])
    assert numpy.all(numpy.fabs(dp.z2deriv(rs,zs)-dpevals) < 10.**-10.), \
        'DoubleExppnentialDiskPotential z2deriv evaluation does not work as expected for array inputs'
    #Rzderiv
    dpevals= numpy.array([dp.Rzderiv(r,z) for (r,z) in zip(rs,zs)])
    assert numpy.all(numpy.fabs(dp.Rzderiv(rs,zs)-dpevals) < 10.**-10.), \
        'DoubleExppnentialDiskPotential Rzderiv evaluation does not work as expected for array inputs'
    #Check the PotentialError for z=/=0 evaluation of R2deriv of RazorThinDiskPotential
    rp= potential.RazorThinExponentialDiskPotential(normalize=1.)
    try: rp.R2deriv(1.,0.1)
    except potential.PotentialError: pass
    else: raise AssertionError("RazorThinExponentialDiskPotential's R2deriv did not raise AttributeError for z=/= 0 input")
    return None

def test_MovingObject_density():
    mp= mockMovingObjectPotential()
    #Just test that the density far away from the object is close to zero
    assert numpy.fabs(mp.dens(5.,0.)) < 10.**-8., 'Density far away from MovingObject is not close to zero'
    return None

# Test that MWPotential is what it's supposed to be
def test_MWPotential2014():
    pot= potential.MWPotential2014
    V0, R0= 220., 8.
    #Check the parameters of the bulge
    assert pot[0].rc == 1.9/R0, "MWPotential2014's bulge cut-off radius is incorrect"
    assert pot[0].alpha == 1.8, "MWPotential2014's bulge power-law exponent is incorrect"
    assert numpy.fabs(pot[0].Rforce(1.,0.)+0.05) < 10.**-14., "MWPotential2014's bulge amplitude is incorrect"
    #Check the parameters of the disk
    assert numpy.fabs(pot[1]._a-3./R0) < 10.**-14., "MWPotential2014's disk scale length is incorrect"
    assert numpy.fabs(pot[1]._b-0.28/R0) < 10.**-14., "MWPotential2014's disk scale heigth is incorrect"
    assert numpy.fabs(pot[1].Rforce(1.,0.)+0.60) < 10.**-14., "MWPotential2014's disk amplitude is incorrect"
    #Check the parameters of the halo
    assert numpy.fabs(pot[2].a-16./R0) < 10.**-14., "MWPotential2014's halo scale radius is incorrect"
    assert numpy.fabs(pot[2].Rforce(1.,0.)+0.35) < 10.**-14., "MWPotential2014's halo amplitude is incorrect"
    return None

# Test that the virial setup of NFW works
def test_NFW_virialsetup_wrtmeanmatter():
    H, Om, overdens, wrtcrit= 71., 0.32, 201., False
    ro, vo= 220., 8.
    conc, mvir= 12., 1.1
    np= potential.NFWPotential(conc=conc,mvir=mvir,vo=vo,ro=ro,
                               H=H,Om=Om,overdens=overdens,
                               wrtcrit=wrtcrit)
    assert numpy.fabs(conc-np.conc(H=H,Om=Om,overdens=overdens,
                                   wrtcrit=wrtcrit)) < 10.**-6., "NFWPotential virial setup's concentration does not work"
    assert numpy.fabs(mvir-np.mvir(H=H,Om=Om,overdens=overdens,
                                   wrtcrit=wrtcrit)/10.**12.) < 10.**-6., "NFWPotential virial setup's virial mass does not work"
    return None

def test_NFW_virialsetup_wrtcrit():
    H, Om, overdens, wrtcrit= 71., 0.32, 201., True
    ro, vo= 220., 8.
    conc, mvir= 12., 1.1
    np= potential.NFWPotential(conc=conc,mvir=mvir,vo=vo,ro=ro,
                               H=H,Om=Om,overdens=overdens,
                               wrtcrit=wrtcrit)
    assert numpy.fabs(conc-np.conc(H=H,Om=Om,overdens=overdens,
                                   wrtcrit=wrtcrit)) < 10.**-6., "NFWPotential virial setup's concentration does not work"
    assert numpy.fabs(mvir-np.mvir(H=H,Om=Om,overdens=overdens,
                                   wrtcrit=wrtcrit)/10.**12.) < 10.**-6., "NFWPotential virial setup's virial mass does not work"
    return None

def test_TriaxialNFW_virialsetup_wrtmeanmatter():
    H, Om, overdens, wrtcrit= 71., 0.32, 201., False
    ro, vo= 220., 8.
    conc, mvir= 12., 1.1
    np= potential.NFWPotential(conc=conc,mvir=mvir,vo=vo,ro=ro,
                               H=H,Om=Om,overdens=overdens,
                               wrtcrit=wrtcrit)
    tnp= potential.TriaxialNFWPotential(b=0.3,c=0.7,
                                        conc=conc,mvir=mvir,vo=vo,ro=ro,
                                        H=H,Om=Om,overdens=overdens,
                                        wrtcrit=wrtcrit)
    assert numpy.fabs(np.a-tnp.a) < 10.**-10., "TriaxialNFWPotential virial setup's concentration does not work"
    assert numpy.fabs(np._amp-tnp._amp) < 10.**-6., "TriaxialNFWPotential virial setup's virial mass does not work"
    return None

def test_TriaxialNFW_virialsetup_wrtcrit():
    H, Om, overdens, wrtcrit= 71., 0.32, 201., True
    ro, vo= 220., 8.
    conc, mvir= 12., 1.1
    np= potential.NFWPotential(conc=conc,mvir=mvir,vo=vo,ro=ro,
                               H=H,Om=Om,overdens=overdens,
                               wrtcrit=wrtcrit)
    tnp= potential.TriaxialNFWPotential(b=0.3,c=0.7,
                                        conc=conc,mvir=mvir,vo=vo,ro=ro,
                                        H=H,Om=Om,overdens=overdens,
                                        wrtcrit=wrtcrit)
    assert numpy.fabs(np.a-tnp.a) < 10.**-10., "TriaxialNFWPotential virial setup's concentration does not work"
    assert numpy.fabs(np._amp-tnp._amp) < 10.**-6., "TriaxialNFWPotential virial setup's virial mass does not work"
    return None

def test_conc_attributeerror():
    pp= potential.PowerSphericalPotential(normalize=1.)
    #This potential doesn't have a scale, so we cannot calculate the concentration
    try: pp.conc(220.,8.)
    except AttributeError: pass
    else: raise AssertionError('conc function for potential w/o scale did not raise AttributeError')
    return None

def test_mvir_attributeerror():
    mp= potential.MiyamotoNagaiPotential(normalize=1.)
    #Don't think I will ever implement the virial radius for this
    try: mp.mvir(220.,8.)
    except AttributeError: pass
    else: raise AssertionError('mvir function for potential w/o rvir did not raise AttributeError')
    return None

# Test that virial quantities are correctly computed when specifying a different (ro,vo) pair from Potential setup (see issue #290)
def test_NFW_virialquantities_diffrovo():
    from galpy.util import bovy_conversion
    H, Om, overdens, wrtcrit= 71., 0.32, 201., False
    ro_setup, vo_setup= 220., 8.
    ros= [7.,8.,9.]
    vos= [220.,230.,240.]
    for ro,vo in zip(ros,vos):
        np= potential.NFWPotential(amp=2.,a=3.,
                                   ro=ro_setup,vo=vo_setup)
        # Computing the overdensity in physical units
        od= (np.mvir(ro=ro,vo=vo,H=H,Om=Om,overdens=overdens,wrtcrit=wrtcrit)\
                 /4./numpy.pi*3.\
                 /np.rvir(ro=ro,vo=vo,H=H,Om=Om,overdens=overdens,wrtcrit=wrtcrit)**3.)\
            *(10.**6./H**2.*8.*numpy.pi/3./Om*(4.302*10.**-6.))
        assert numpy.fabs(od-overdens) < 0.01, "NFWPotential's virial quantities computed in physical units with different (ro,vo) from setup are incorrect"
        od= (np.mvir(ro=ro,vo=vo,H=H,Om=Om,overdens=overdens,wrtcrit=wrtcrit,use_physical=False)\
                 /4./numpy.pi*3.\
                 /np.rvir(ro=ro,vo=vo,H=H,Om=Om,overdens=overdens,wrtcrit=wrtcrit,use_physical=False)**3.)\
            *bovy_conversion.dens_in_meanmatterdens(vo,ro,H=H,Om=Om)
        assert numpy.fabs(od-overdens) < 0.01, "NFWPotential's virial quantities computed in internal units with different (ro,vo) from setup are incorrect"
        # Also test concentration
        assert numpy.fabs(np.conc(ro=ro,vo=vo,H=H,Om=Om,overdens=overdens,wrtcrit=wrtcrit)\
                              -np.rvir(ro=ro,vo=vo,H=H,Om=Om,overdens=overdens,wrtcrit=wrtcrit)/np._scale/ro) < 0.01, "NFWPotential's concentration computed for different (ro,vo) from setup is incorrect"
    return None

def test_LinShuReductionFactor():
    #Test that the LinShuReductionFactor is implemented correctly, by comparing to figure 1 in Lin & Shu (1966)
    from galpy.potential import LinShuReductionFactor, \
        LogarithmicHaloPotential, omegac, epifreq
    lp= LogarithmicHaloPotential(normalize=1.) #work in flat rotation curve
    #nu^2 = 0.2, x=4 for m=2,sigmar=0.1 
    # w/ nu = m(OmegaP-omegac)/epifreq, x=sr^2*k^2/epifreq^2
    R,m,sr = 0.9,2.,0.1
    tepi, tomegac= epifreq(lp,R), omegac(lp,R)
    OmegaP= tepi*numpy.sqrt(0.2)/m+tomegac #leads to nu^2 = 0.2
    k= numpy.sqrt(4.)*tepi/sr
    assert numpy.fabs(LinShuReductionFactor(lp,R,sr,m=m,k=k,OmegaP=OmegaP)-0.18) < 0.01, 'LinShuReductionFactor does not agree w/ Figure 1 from Lin & Shu (1966)'
    #nu^2 = 0.8, x=10
    OmegaP= tepi*numpy.sqrt(0.8)/m+tomegac #leads to nu^2 = 0.8
    k= numpy.sqrt(10.)*tepi/sr
    assert numpy.fabs(LinShuReductionFactor(lp,R,sr,m=m,k=k,OmegaP=OmegaP)-0.04) < 0.01, 'LinShuReductionFactor does not agree w/ Figure 1 from Lin & Shu (1966)'   
    #Similar test, but using a nonaxiPot= input
    from galpy.potential import SteadyLogSpiralPotential
    sp= SteadyLogSpiralPotential(m=2.,omegas=OmegaP,alpha=k*R)
    assert numpy.fabs(LinShuReductionFactor(lp,R,sr,nonaxiPot=sp)-0.04) < 0.01, 'LinShuReductionFactor does not agree w/ Figure 1 from Lin & Shu (1966)'   
    #Test exception
    try:
        LinShuReductionFactor(lp,R,sr)
    except IOError: pass
    else: raise AssertionError("LinShuReductionFactor w/o nonaxiPot set or k=,m=,OmegaP= set did not raise IOError")
    return None

def test_nemoaccname():
    #There is no real good way to test this (I think), so I'm just testing to
    #what I think is the correct output now to make sure this isn't 
    #accidentally changed
    # Log
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    assert lp.nemo_accname() == 'LogPot', "Logarithmic potential's NEMO name incorrect"
    # NFW
    np= potential.NFWPotential(normalize=1.)
    assert np.nemo_accname() == 'NFW', "NFW's NEMO name incorrect"
    # Miyamoto-Nagai
    mp= potential.MiyamotoNagaiPotential(normalize=1.)
    assert mp.nemo_accname() == 'MiyamotoNagai', "MiyamotoNagai's NEMO name incorrect"
    # Power-spherical w/ cut-off
    pp= potential.PowerSphericalPotentialwCutoff(normalize=1.)
    assert pp.nemo_accname() == 'PowSphwCut', "Power-spherical potential w/ cuto-ff's NEMO name incorrect"
    # MN3ExponentialDiskPotential
    mp= potential.MN3ExponentialDiskPotential(normalize=1.)
    assert mp.nemo_accname() == 'MiyamotoNagai+MiyamotoNagai+MiyamotoNagai', "MN3ExponentialDiskPotential's NEMO name incorrect"
    # Plummer
    pp= potential.PlummerPotential(normalize=1.)
    assert pp.nemo_accname() == 'Plummer', "PlummerPotential's NEMO name incorrect"
    return None

def test_nemoaccnamepars_attributeerror():
    # Use BurkertPotential (unlikely that I would implement that one in NEMO soon)
    bp= potential.BurkertPotential(normalize=1.)
    try: bp.nemo_accname()
    except AttributeError: pass
    else:
        raise AssertionError('nemo_accname for potential w/o accname does not raise AttributeError')
    try: bp.nemo_accpars(220.,8.)
    except AttributeError: pass
    else:
        raise AssertionError('nemo_accpars for potential w/o accname does not raise AttributeError')
    return None

def test_nemoaccnames():
    # Just test MWPotential2014 and a single potential
    # MWPotential2014
    assert potential.nemo_accname(potential.MWPotential2014) == 'PowSphwCut+MiyamotoNagai+NFW', "MWPotential2014's NEMO name is incorrect"
    # Power-spherical w/ cut-off
    pp= potential.PowerSphericalPotentialwCutoff(normalize=1.)
    assert potential.nemo_accname(pp) == 'PowSphwCut', "Power-spherical potential w/ cut-off's NEMO name incorrect"
    return None

def test_nemoaccpars():
    # Log
    lp= potential.LogarithmicHaloPotential(amp=2.,core=3.,q=27.) #completely ridiculous, but tests scalings
    vo, ro= 2., 3.
    vo/= 1.0227121655399913
    ap= lp.nemo_accpars(vo,ro).split(',')
    assert numpy.fabs(float(ap[0])-0) < 10.**-8., "Logarithmic potential's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[1])-8.0) < 10.**-8., "Logarithmic potential's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[2])-729.0) < 10.**-8., "Logarithmic potential's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[3])-1.0) < 10.**-8., "Logarithmic potential's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[4])-27.0) < 10.**-8., "Logarithmic potential's NEMO accpars incorrect"
    # Miyamoto-Nagai
    mp= potential.MiyamotoNagaiPotential(amp=3.,a=2.,b=5.)
    vo, ro= 7., 9.
    vo/= 1.0227121655399913
    ap= mp.nemo_accpars(vo,ro).split(',')
    assert numpy.fabs(float(ap[0])-0) < 10.**-8., "MiyamotoNagai's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[1])-1323.0) < 10.**-5., "MiyamotoNagai's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[2])-18.0) < 10.**-8., "MiyamotoNagai's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[3])-45.0) < 10.**-8., "MiyamotoNagai's NEMO accpars incorrect"
    # Power-spherical w/ cut-off
    pp= potential.PowerSphericalPotentialwCutoff(amp=3.,alpha=4.,rc=5.)
    vo, ro= 7., 9.
    vo/= 1.0227121655399913
    ap= pp.nemo_accpars(vo,ro).split(',')
    assert numpy.fabs(float(ap[0])-0) < 10.**-8., "Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[1])-11907.0) < 10.**-4., "Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[2])-4.0) < 10.**-8., "Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[3])-45.0) < 10.**-8., "Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    # NFW
    np= potential.NFWPotential(amp=1./0.2162165954,a=1./16)
    vo, ro= 3., 4.
    vo/= 1.0227121655399913
    ap= np.nemo_accpars(vo,ro).split(',')
    assert numpy.fabs(float(ap[0])-0) < 10.**-8., "NFW's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[1])-0.25) < 10.**-8., "NFW's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[2])-12.0) < 10.**-8., "NFW's NEMO accpars incorrect"
    # MN3ExponentialDiskPotential
    mn= potential.MN3ExponentialDiskPotential(normalize=1.,hr=2.,hz=0.5)
    vo, ro= 3., 4.
    ap= mn.nemo_accpars(vo,ro).replace('#',',').split(',')
    assert numpy.fabs(float(ap[0])-0) < 10.**-8., "MN3ExponentialDiskPotential 's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[4])-0) < 10.**-8., "MN3ExponentialDiskPotential 's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[8])-0) < 10.**-8., "MN3ExponentialDiskPotential 's NEMO accpars incorrect"
    # Test ratios
    assert numpy.fabs(float(ap[1])/float(ap[5])-mn._mn3[0]._amp/mn._mn3[1]._amp) < 10.**-8., "MN3ExponentialDiskPotential 's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[1])/float(ap[9])-mn._mn3[0]._amp/mn._mn3[2]._amp) < 10.**-8., "MN3ExponentialDiskPotential 's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[2])/float(ap[6])-mn._mn3[0]._a/mn._mn3[1]._a) < 10.**-8., "MN3ExponentialDiskPotential 's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[2])/float(ap[10])-mn._mn3[0]._a/mn._mn3[2]._a) < 10.**-8., "MN3ExponentialDiskPotential 's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[3])/float(ap[7])-1.) < 10.**-8., "MN3ExponentialDiskPotential 's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[3])/float(ap[11])-1.) < 10.**-8., "MN3ExponentialDiskPotential 's NEMO accpars incorrect"
    # Plummer
    pp= potential.PlummerPotential(amp=3.,b=5.)
    vo, ro= 7., 9.
    vo/= 1.0227121655399913
    ap= pp.nemo_accpars(vo,ro).split(',')
    assert numpy.fabs(float(ap[0])-0) < 10.**-8., "Plummer's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[1])-1323.0) < 10.**-5., "Plummer's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[2])-45.0) < 10.**-8., "Plummer's NEMO accpars incorrect"
    return None

def test_nemoaccparss():
    # Just combine a few of the above ones
    # Miyamoto + PowerSpherwCut
    mp= potential.MiyamotoNagaiPotential(amp=3.,a=2.,b=5.)
    pp= potential.PowerSphericalPotentialwCutoff(amp=3.,alpha=4.,rc=5.)
    vo, ro= 7., 9.
    vo/= 1.0227121655399913
    ap= potential.nemo_accpars(mp,vo,ro).split(',')
    assert numpy.fabs(float(ap[0])-0) < 10.**-8., "MiyamotoNagai's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[1])-1323.0) < 10.**-5., "MiyamotoNagai's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[2])-18.0) < 10.**-8., "MiyamotoNagai's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[3])-45.0) < 10.**-8., "MiyamotoNagai's NEMO accpars incorrect"
    # PowSpherwCut
    ap= potential.nemo_accpars(pp,vo,ro).split(',')
    assert numpy.fabs(float(ap[0])-0) < 10.**-8., "Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[1])-11907.0) < 10.**-4., "Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[2])-4.0) < 10.**-8., "Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[3])-45.0) < 10.**-8., "Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    # Combined
    apc= potential.nemo_accpars([mp,pp],vo,ro).split('#')
    ap= apc[0].split(',') # should be MN
    assert numpy.fabs(float(ap[0])-0) < 10.**-8., "Miyamoto+Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[1])-1323.0) < 10.**-5., "Miyamoto+Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[2])-18.0) < 10.**-8., "Miyamoto+Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[3])-45.0) < 10.**-8., "Miyamoto+Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    ap= apc[1].split(',') # should be PP
    assert numpy.fabs(float(ap[0])-0) < 10.**-8., "Miyamoto+Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[1])-11907.0) < 10.**-4., "Miyamoto+Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[2])-4.0) < 10.**-8., "Miyamoto+Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    assert numpy.fabs(float(ap[3])-45.0) < 10.**-8., "Miyamoto+Power-spherical potential w/ cut-off's NEMO accpars incorrect"
    return None

def test_MN3ExponentialDiskPotential_inputs():
    #Test the inputs of the MN3ExponentialDiskPotential
    # IOError for hz so large that b is negative
    try:
        mn= potential.MN3ExponentialDiskPotential(amp=1.,hz=50.)
    except IOError: pass
    else:
        raise AssertionError("MN3ExponentialDiskPotential with ridiculous hz should have given IOError, but didn't")
    # Warning when b/Rd > 3 or (b/Rd > 1.35 and posdens)
    #Turn warnings into errors to test for them
    import warnings
    from galpy.util import galpyWarning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always",galpyWarning)
        mn= MN3ExponentialDiskPotential(normalize=1.,hz=1.438,hr=1.)
        # Should raise warning bc of MN3ExponentialDiskPotential, 
        # might raise others
        raisedWarning= False
        for wa in w:
            raisedWarning= ('MN3ExponentialDiskPotential' in str(wa.message))
            if raisedWarning: break
        assert raisedWarning, "MN3ExponentialDiskPotential w/o posdens, but with b/Rd > 3 did not raise galpyWarning"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always",galpyWarning)
        mn= MN3ExponentialDiskPotential(normalize=1.,hr=1.,hz=0.7727,
                                        posdens=True)
        raisedWarning= False
        for wa in w:
            raisedWarning= ('MN3ExponentialDiskPotential' in str(wa.message))
            if raisedWarning: break
        assert raisedWarning, "MN3ExponentialDiskPotential w/o posdens, but with b/Rd > 1.35 did not raise galpyWarning"
    return None

def test_MN3ExponentialDiskPotential_hz():
    #Test that we correctly convert from hz/Rd to b/Rd
    # exp
    mn= potential.MN3ExponentialDiskPotential(amp=1.,hr=1.,hz=1.,sech=False)
    assert numpy.fabs(mn._brd-1.875) < 0.05, "b/Rd not computed correctly for exponential profile"
    mn= potential.MN3ExponentialDiskPotential(amp=1.,hr=2.,hz=1.,sech=False)
    assert numpy.fabs(mn._brd-0.75) < 0.05, "b/Rd not computed correctly for exponential profile"
    # sech
    mn= potential.MN3ExponentialDiskPotential(amp=1.,hr=1.,hz=2.,sech=True)
    assert numpy.fabs(mn._brd-2.1) < 0.05, "b/Rd not computed correctly for sech^2 profile"
    mn= potential.MN3ExponentialDiskPotential(amp=1.,hr=2.,hz=2.,sech=True)
    assert numpy.fabs(mn._brd-0.9) < 0.05, "b/Rd not computed correctly for sech^2 profile"
    return None

def test_MN3ExponentialDiskPotential_approx():
    # Test that the 3MN approximation works to the advertised level
    # Zero thickness
    mn= potential.MN3ExponentialDiskPotential(amp=1.,hr=1.,hz=0.001,sech=False)
    dp= potential.DoubleExponentialDiskPotential(amp=1.,hr=1.,hz=0.001)
    dpmass= dp.mass(4.,5.*.001)
    assert numpy.fabs(mn.mass(4.,5.*.001)-dpmass)/dpmass < 0.005, "MN3ExponentialDiskPotential does not approximate the enclosed mass as advertised"
    # Finite thickness
    mn= potential.MN3ExponentialDiskPotential(amp=1.,hr=1.,hz=0.62,sech=False)
    dp= potential.DoubleExponentialDiskPotential(amp=1.,hr=1.,hz=0.62)
    dpmass= dp.mass(4.,5.*0.6)
    assert numpy.fabs(mn.mass(4.,10.*0.6)-dpmass)/dpmass < 0.01, "MN3ExponentialDiskPotential does not approximate the enclosed mass as advertised"
    # Finite thickness w/ sech
    mn= potential.MN3ExponentialDiskPotential(amp=.5,hr=1.,hz=1.24,sech=True)
    dp= potential.DoubleExponentialDiskPotential(amp=1.,hr=1.,hz=0.62)
    dpmass= dp.mass(4.,5.*0.6)
    assert numpy.fabs(mn.mass(4.,20.*0.6)-dpmass)/dpmass < 0.01, "MN3ExponentialDiskPotential does not approximate the enclosed mass as advertised"
    # At 10 Rd
    # Zero thickness
    mn= potential.MN3ExponentialDiskPotential(amp=1.,hr=1.,hz=0.001,sech=False)
    dp= potential.DoubleExponentialDiskPotential(amp=1.,hr=1.,hz=0.001)
    dpmass= dp.mass(10.,5.*.001)
    assert numpy.fabs(mn.mass(10.,5.*.001)-dpmass)/dpmass < 0.04, "MN3ExponentialDiskPotential does not approximate the enclosed mass as advertised"
    # Finite thickness
    mn= potential.MN3ExponentialDiskPotential(amp=1.,hr=1.,hz=0.62,sech=False)
    dp= potential.DoubleExponentialDiskPotential(amp=1.,hr=1.,hz=0.62)
    dpmass= dp.mass(10.,5.*0.6)
    assert numpy.fabs(mn.mass(10.,10.*0.6)-dpmass)/dpmass < 0.04, "MN3ExponentialDiskPotential does not approximate the enclosed mass as advertised"
    # Finite thickness w/ sech
    mn= potential.MN3ExponentialDiskPotential(amp=0.5,hr=1.,hz=1.24,sech=True)
    dp= potential.DoubleExponentialDiskPotential(amp=1.,hr=1.,hz=0.62)
    dpmass= dp.mass(10.,5.*0.6)
    assert numpy.fabs(mn.mass(10.,20.*0.6)-dpmass)/dpmass < 0.04, "MN3ExponentialDiskPotential does not approximate the enclosed mass as advertised"
    # For posdens the deviations are larger
    # Zero thickness
    mn= potential.MN3ExponentialDiskPotential(amp=1.,hr=1.,hz=0.001,sech=False,
                                              posdens=True)
    dp= potential.DoubleExponentialDiskPotential(amp=1.,hr=1.,hz=0.001)
    dpmass= dp.mass(4.,5.*.001)
    assert numpy.fabs(mn.mass(4.,5.*.001)-dpmass)/dpmass < 0.015, "MN3ExponentialDiskPotential does not approximate the enclosed mass as advertised"
    # Finite thickness
    mn= potential.MN3ExponentialDiskPotential(amp=1.,hr=1.,hz=0.62,sech=False,
                                              posdens=True)
    dp= potential.DoubleExponentialDiskPotential(amp=1.,hr=1.,hz=0.62)
    dpmass= dp.mass(4.,5.*0.6)
    assert numpy.fabs(mn.mass(4.,10.*0.6)-dpmass)/dpmass < 0.015, "MN3ExponentialDiskPotential does not approximate the enclosed mass as advertised"
    # At 10 Rd
    # Zero thickness
    mn= potential.MN3ExponentialDiskPotential(amp=1.,hr=1.,hz=0.001,sech=False,
                                              posdens=True)
    dp= potential.DoubleExponentialDiskPotential(amp=1.,hr=1.,hz=0.001)
    dpmass= dp.mass(10.,5.*.001)
    assert numpy.fabs(mn.mass(10.,5.*.001)-dpmass)/dpmass > 0.04, "MN3ExponentialDiskPotential does not approximate the enclosed mass as advertised"
    assert numpy.fabs(mn.mass(10.,5.*.001)-dpmass)/dpmass < 0.07, "MN3ExponentialDiskPotential does not approximate the enclosed mass as advertised"
    # Finite thickness
    mn= potential.MN3ExponentialDiskPotential(amp=1.,hr=1.,hz=0.62,sech=False,
                                              posdens=True)
    dp= potential.DoubleExponentialDiskPotential(amp=1.,hr=1.,hz=0.62)
    dpmass= dp.mass(10.,5.*0.6)
    assert numpy.fabs(mn.mass(10.,10.*0.6)-dpmass)/dpmass < 0.08, "MN3ExponentialDiskPotential does not approximate the enclosed mass as advertised"
    assert numpy.fabs(mn.mass(10.,10.*0.6)-dpmass)/dpmass > 0.03, "MN3ExponentialDiskPotential does not approximate the enclosed mass as advertised"
    return None

def test_TwoPowerTriaxialPotential_vs_TwoPowerSphericalPotential():
    # Test that TwoPowerTriaxialPotential with spherical parameters is the same
    # as TwoPowerSphericalPotential
    tol= -4. # tough general case
    rs= numpy.linspace(0.001,25.,1001)
    tnp= potential.TwoPowerTriaxialPotential(normalize=1.,b=1.,c=1.,a=1.5,
                                             alpha=1.5,beta=3.5)
    np= potential.TwoPowerSphericalPotential(normalize=1.,a=1.5,
                                             alpha=1.5,beta=3.5)
    assert numpy.all(numpy.fabs(numpy.array(\
                [numpy.sqrt(tnp.Rforce(r,0.)/np.Rforce(r,0.)) for r in rs])-1.) < 10.**tol), 'Vcirc not the same for TwoPowerSphericalPotential and spherical version of TwoPowerTriaxialPotential'
    # Also do specific cases
    tol= -8. # much better
    # Hernquist
    tnp= potential.TriaxialHernquistPotential(normalize=1.,b=1.,c=1.,a=1.5)
    np= potential.HernquistPotential(normalize=1.,a=1.5)
    assert numpy.all(numpy.fabs(numpy.array(\
                [numpy.sqrt(tnp.Rforce(r,0.)/np.Rforce(r,0.)) for r in rs])-1.) < 10.**tol), 'Vcirc not the same for Hernquist and spherical version of TriaxialHernquist'
    # NFW
    tnp= potential.TriaxialNFWPotential(normalize=1.,b=1.,c=1.,a=1.5)
    np= potential.NFWPotential(normalize=1.,a=1.5)
    assert numpy.all(numpy.fabs(numpy.array(\
                [numpy.sqrt(tnp.Rforce(r,0.)/np.Rforce(r,0.)) for r in rs])-1.) < 10.**tol), 'Vcirc not the same for NFW and spherical version of TriaxialNFW'
    # Jaffe
    tnp= potential.TriaxialJaffePotential(normalize=1.,b=1.,c=1.,a=1.5)
    np= potential.JaffePotential(normalize=1.,a=1.5)
    assert numpy.all(numpy.fabs(numpy.array(\
                [numpy.sqrt(tnp.Rforce(r,0.)/np.Rforce(r,0.)) for r in rs])-1.) < 10.**tol), 'Vcirc not the same for Jaffe and spherical version of TriaxialJaffe'
    return None

# Test that TwoPowerTriaxial setup raises an error for bad values of alpha
# and beta
def test_TwoPowerTriaxialPotential_alphalowerror():
    with pytest.raises(IOError) as excinfo:
        dummy= potential.TwoPowerTriaxialPotential(alpha=-1.)
    return None
def test_TwoPowerTriaxialPotential_alphahigherror():
    with pytest.raises(IOError) as excinfo:
        dummy= potential.TwoPowerTriaxialPotential(alpha=3.5)
    return None
def test_TwoPowerTriaxialPotential_betalowerror():
    with pytest.raises(IOError) as excinfo:
        dummy= potential.TwoPowerTriaxialPotential(beta=1.)
    return None

# Test that FerrersPotential raises a value error for n < 0
def test_FerrersPotential_nNegative():
    with pytest.raises(ValueError) as excinfo:
        dummy= potential.FerrersPotential(n=-1.)
    return None

def test_planeRotatedNFWPotential():
    # Test that the rotation according to pa works as expected
    tnp= potential.TriaxialNFWPotential(normalize=1.,a=1.5,b=0.5,
                                        pa=30./180.*numpy.pi)
    # Compute the potential at a fixed radius, minimum should be at pa!
    Rs= 0.8
    phis= numpy.linspace(0.,numpy.pi,1001)
    pot= numpy.array([tnp(Rs,0.,phi=phi) for phi in phis])
    minphi= numpy.argmin(pot)
    minphi_pred= numpy.argmin(numpy.fabs(phis-30./180.*numpy.pi))
    assert minphi == minphi_pred, 'Flattened NFW potential rotated around the z axis does not behave as expected'
    # Same for density, but max instead
    dens= numpy.array([tnp.dens(Rs,0.,phi=phi) for phi in phis])
    minphi= numpy.argmax(dens)
    minphi_pred= numpy.argmin(numpy.fabs(phis-30./180.*numpy.pi))
    assert minphi == minphi_pred, 'Flattened NFW potential rotated around the z axis does not behave as expected'
    # Also do a negative angle
    tnp= potential.TriaxialNFWPotential(normalize=1.,a=1.5,b=0.5,
                                        pa=-60./180.*numpy.pi)
    # Compute the potential at a fixed radius, minimum should be at pa!
    Rs= 0.8
    phis= numpy.linspace(0.,numpy.pi,1001)
    pot= numpy.array([tnp(Rs,0.,phi=phi) for phi in phis])
    minphi= numpy.argmin(pot)
    minphi_pred= numpy.argmin(numpy.fabs(phis-120./180.*numpy.pi))
    assert minphi == minphi_pred, 'Flattened NFW potential rotated around the z axis does not behave as expected'
    # Same for density, but max instead
    dens= numpy.array([tnp.dens(Rs,0.,phi=phi) for phi in phis])
    minphi= numpy.argmax(dens)
    minphi_pred= numpy.argmin(numpy.fabs(phis-120./180.*numpy.pi))
    assert minphi == minphi_pred, 'Flattened NFW potential rotated around the z axis does not behave as expected'
    return None

def test_zaxisRotatedNFWPotential():
    from galpy.util import bovy_coords
    # Test that the rotation according to zvec works as expected
    pa= 30./180.*numpy.pi
    tnp= potential.TriaxialNFWPotential(normalize=1.,a=1.5,c=0.5,
                                        zvec=[0.,-numpy.sin(pa),numpy.cos(pa)])
    # Compute the potential at a fixed radius in the y/z plane,
    # minimum should be at pa!
    Rs= 0.8
    phis= numpy.linspace(0.,numpy.pi,1001)
    xs= numpy.zeros_like(phis)
    ys= Rs*numpy.cos(phis)
    zs= Rs*numpy.sin(phis)
    tR,tphi,tz= bovy_coords.rect_to_cyl(xs,ys,zs)
    pot= numpy.array([tnp(r,z,phi=phi) for r,z,phi in zip(tR,tz,tphi)])
    minphi= numpy.argmin(pot)
    minphi_pred= numpy.argmin(numpy.fabs(phis-30./180.*numpy.pi))
    assert minphi == minphi_pred, 'Flattened NFW potential with rotated z axis does not behave as expected'
    # Same for density, but max instead
    dens= numpy.array([tnp.dens(r,z,phi=phi) for r,z,phi in zip(tR,tz,tphi)])
    minphi= numpy.argmax(dens)
    minphi_pred= numpy.argmin(numpy.fabs(phis-30./180.*numpy.pi))
    assert minphi == minphi_pred, 'Flattened NFW potential with rotated z axis does not behave as expected'
    # Another one
    pa= -60./180.*numpy.pi
    tnp= potential.TriaxialNFWPotential(normalize=1.,a=1.5,c=0.5,
                                        zvec=[-numpy.sin(pa),0.,numpy.cos(pa)])
    # Compute the potential at a fixed radius in the z/z plane,
    # minimum should be at pa!
    Rs= 0.8
    phis= numpy.linspace(0.,numpy.pi,1001)
    xs= Rs*numpy.cos(phis)
    ys= numpy.zeros_like(phis)
    zs= Rs*numpy.sin(phis)
    tR,tphi,tz= bovy_coords.rect_to_cyl(xs,ys,zs)
    pot= numpy.array([tnp(r,z,phi=phi) for r,z,phi in zip(tR,tz,tphi)])
    minphi= numpy.argmin(pot)
    minphi_pred= numpy.argmin(numpy.fabs(phis-120./180.*numpy.pi))
    assert minphi == minphi_pred, 'Flattened NFW potential with rotated z axis does not behave as expected'
    # Same for density, but max instead
    dens= numpy.array([tnp.dens(r,z,phi=phi) for r,z,phi in zip(tR,tz,tphi)])
    minphi= numpy.argmax(dens)
    minphi_pred= numpy.argmin(numpy.fabs(phis-120./180.*numpy.pi))
    assert minphi == minphi_pred, 'Flattened NFW potential with rotated z axis does not behave as expected'
    return None

def test_nonaxierror_function():
    # Test that the code throws an exception when calling a non-axisymmetric 
    # potential without phi
    tnp= potential.TriaxialNFWPotential(amp=1.,b=0.7,c=0.9)
    with pytest.raises(potential.PotentialError) as excinfo:
        potential.evaluatePotentials(tnp,1.,0.)
    with pytest.raises(potential.PotentialError) as excinfo:
        potential.evaluateDensities(tnp,1.,0.)
    with pytest.raises(potential.PotentialError) as excinfo:
        potential.evaluateRforces(tnp,1.,0.)
    with pytest.raises(potential.PotentialError) as excinfo:
        potential.evaluatezforces(tnp,1.,0.)
    with pytest.raises(potential.PotentialError) as excinfo:
        potential.evaluatephiforces(tnp,1.,0.)
    with pytest.raises(potential.PotentialError) as excinfo:
        potential.evaluateR2derivs(tnp,1.,0.)
    with pytest.raises(potential.PotentialError) as excinfo:
        potential.evaluatez2derivs(tnp,1.,0.)
    with pytest.raises(potential.PotentialError) as excinfo:
        potential.evaluateRzderivs(tnp,1.,0.)
    return None


def test_SoftenedNeedleBarPotential_density():
    # Some simple tests of the density of the SoftenedNeedleBarPotential
    # For a spherical softening kernel, density should be symmetric to y/z
    sbp= potential.SoftenedNeedleBarPotential(normalize=1.,a=1.,c=.1,b=0.,
                                              pa=0.)
    assert numpy.fabs(sbp.dens(2.,0.,phi=numpy.pi/4.)-sbp.dens(numpy.sqrt(2.),numpy.sqrt(2.),phi=0.)) < 10.**-13., 'SoftenedNeedleBarPotential with spherical softening kernel does not appear to have a spherically symmetric density'
    # Another one
    assert numpy.fabs(sbp.dens(4.,0.,phi=numpy.pi/4.)-sbp.dens(2.*numpy.sqrt(2.),2.*numpy.sqrt(2.),phi=0.)) < 10.**-13., 'SoftenedNeedleBarPotential with spherical softening kernel does not appear to have a spherically symmetric density'
    # For a flattened softening kernel, the density at (y,z) should be higher than at (z,y)
    sbp= potential.SoftenedNeedleBarPotential(normalize=1.,a=1.,c=.1,b=0.3,
                                              pa=0.)
    assert sbp.dens(2.,0.,phi=numpy.pi/4.) > sbp.dens(numpy.sqrt(2.),numpy.sqrt(2.),phi=0.), 'SoftenedNeedleBarPotential with flattened softening kernel does not appear to have a consistent'
    # Another one
    assert sbp.dens(4.,0.,phi=numpy.pi/4.) > sbp.dens(2.*numpy.sqrt(2.),2.*numpy.sqrt(2.),phi=0.), 'SoftenedNeedleBarPotential with flattened softening kernel does not appear to have a consistent'
    return None
    
def test_DiskSCFPotential_SigmaDerivs():
    # Test that the derivatives of Sigma are correctly implemented in DiskSCF
    # Very rough finite difference checks
    dscfp= potential.DiskSCFPotential(dens=lambda R,z: 1.,# doesn't matter
                                      Sigma=[{'type':'exp','h':1./3.,'amp':1.},
                                             {'type':'expwhole','h':1./3.,
                                              'amp':1.,'Rhole':0.5}],
                                      hz=[{'type':'exp','h':1./27.},
                                          {'type':'sech2','h':1./27.}],
                                      a=1.,N=2,L=2)
    # Sigma exp
    testRs= numpy.linspace(0.3,1.5,101)
    dR= 10.**-8.
    assert numpy.all(numpy.fabs(((dscfp._Sigma[0](testRs+dR)-dscfp._Sigma[0](testRs))/dR-dscfp._dSigmadR[0](testRs))/dscfp._dSigmadR[0](testRs)) < 10.**-7.), "Derivative dSigmadR does not agree with finite-difference derivative of Sigma for exponential profile in DiskSCFPotential"
    assert numpy.all(numpy.fabs(((dscfp._dSigmadR[0](testRs+dR)-dscfp._dSigmadR[0](testRs))/dR-dscfp._d2SigmadR2[0](testRs))/dscfp._d2SigmadR2[0](testRs)) < 10.**-7.), "Derivative d2SigmadR2 does not agree with finite-difference derivative of dSigmadR for exponential profile in DiskSCFPotential"
    # Sigma expwhole
    dR= 10.**-8.
    assert numpy.all(numpy.fabs(((dscfp._Sigma[1](testRs+dR)-dscfp._Sigma[1](testRs))/dR-dscfp._dSigmadR[1](testRs))/dscfp._dSigmadR[1](testRs)) < 10.**-4.), "Derivative dSigmadR does not agree with finite-difference derivative of Sigma for exponential-with-hole profile in DiskSCFPotential"
    assert numpy.all(numpy.fabs(((dscfp._dSigmadR[1](testRs+dR)-dscfp._dSigmadR[1](testRs))/dR-dscfp._d2SigmadR2[1](testRs))/dscfp._d2SigmadR2[1](testRs)) < 10.**-4.), "Derivative d2SigmadR2 does not agree with finite-difference derivative of dSigmadR for exponential-with-hole profile in DiskSCFPotential"
    return None

def test_DiskSCFPotential_verticalDerivs():
    # Test that the derivatives of Sigma are correctly implemented in DiskSCF
    # Very rough finite difference checks
    dscfp= potential.DiskSCFPotential(dens=lambda R,z: 1.,# doesn't matter
                                      Sigma=[{'type':'exp','h':1./3.,'amp':1.},
                                             {'type':'expwhole','h':1./3.,
                                              'amp':1.,'Rhole':0.5}],
                                      hz=[{'type':'exp','h':1./27.},
                                          {'type':'sech2','h':1./27.}],
                                      a=1.,N=2,L=2)
    # Vertical exp
    testzs= numpy.linspace(0.1/27.,3./27,101)
    dz= 10.**-8.
    assert numpy.all(numpy.fabs(((dscfp._Hz[0](testzs+dz)-dscfp._Hz[0](testzs))/dz-dscfp._dHzdz[0](testzs))/dscfp._dHzdz[0](testzs)) < 10.**-5.5), "Derivative dHzdz does not agree with finite-difference derivative of Hz for exponential profile in DiskSCFPotential"
    assert numpy.all(numpy.fabs(((dscfp._dHzdz[0](testzs+dz)-dscfp._dHzdz[0](testzs))/dz-dscfp._hz[0](testzs))/dscfp._hz[0](testzs)) < 10.**-6.), "Derivative hz does not agree with finite-difference derivative of dHzdz for exponential profile in DiskSCFPotential"
    # Vertical sech^2
    dz= 10.**-8.
    assert numpy.all(numpy.fabs(((dscfp._Hz[1](testzs+dz)-dscfp._Hz[1](testzs))/dz-dscfp._dHzdz[1](testzs))/dscfp._dHzdz[1](testzs)) < 10.**-5.5), "Derivative dSigmadz does not agree with finite-difference derivative of Sigma for sech2 profile in DiskSCFPotential"
    assert numpy.all(numpy.fabs(((dscfp._dHzdz[1](testzs+dz)-dscfp._dHzdz[1](testzs))/dz-dscfp._hz[1](testzs))/dscfp._hz[1](testzs)) < 10.**-6.), "Derivative hz does not agree with finite-difference derivative of dHzdz for sech2 profile in DiskSCFPotential"
    return None

def test_DiskSCFPotential_nhzNeqnsigmaError():
    with pytest.raises(ValueError) as excinfo:
        dummy= potential.DiskSCFPotential(\
            dens=lambda R,z: numpy.exp(-3.*R)\
                *1./numpy.cosh(z/2.*27.)**2./4.*27.,
            Sigma={'h': 1./3.,
                   'type': 'exp', 'amp': 1.0},
            hz=[{'type':'sech2','h':1./27.},{'type':'sech2','h':1./27.}],
            a=1.,N=5,L=5)
    return None

def test_DiskSCFPotential_againstDoubleExp():
    # Test that the DiskSCFPotential approx. of a dbl-exp disk agrees with
    # DoubleExponentialDiskPotential
    dp= potential.DoubleExponentialDiskPotential(amp=13.5,hr=1./3.,hz=1./27.)
    dscfp= potential.DiskSCFPotential(dens=lambda R,z: dp.dens(R,z),
                                      Sigma_amp=1.,
                                      Sigma=lambda R: numpy.exp(-3.*R),
                                      dSigmadR=lambda R: -3.*numpy.exp(-3.*R),
                                      d2SigmadR2=lambda R: 9.*numpy.exp(-3.*R),
                                      hz={'type':'exp','h':1./27.},
                                      a=1.,N=10,L=10)
    testRs= numpy.linspace(0.3,1.5,101)
    testzs= numpy.linspace(0.1/27.,3./27,101)
    testR= 0.9*numpy.ones_like(testzs)
    testz= 1.5/27.*numpy.ones_like(testRs)
    # Test potential
    assert numpy.all(numpy.fabs((dp(testRs,testz)-dscfp(testRs,testz))/dscfp(testRs,testz)) < 10.**-2.5), "DiskSCFPotential for double-exponential disk does not agree with DoubleExponentialDiskPotential"
    assert numpy.all(numpy.fabs((dp(testR,testzs)-dscfp(testR,testzs))/dscfp(testRs,testz)) < 10.**-2.5), "DiskSCFPotential for double-exponential disk does not agree with DoubleExponentialDiskPotential"
    # Rforce
    assert numpy.all(numpy.fabs((dp.Rforce(testRs,testz)-dscfp.Rforce(testRs,testz))/dscfp.Rforce(testRs,testz)) < 10.**-2.), "DiskSCFPotential for double-exponential disk does not agree with DoubleExponentialDiskPotential"
    assert numpy.all(numpy.fabs((dp.Rforce(testR,testzs)-dscfp.Rforce(testR,testzs))/dscfp.Rforce(testRs,testz)) < 10.**-2.), "DiskSCFPotential for double-exponential disk does not agree with DoubleExponentialDiskPotential"
    # zforce
    assert numpy.all(numpy.fabs((dp.zforce(testRs,testz)-dscfp.zforce(testRs,testz))/dscfp.zforce(testRs,testz)) < 10.**-1.5), "DiskSCFPotential for double-exponential disk does not agree with DoubleExponentialDiskPotential"
    # Following has rel. large difference at high z
    assert numpy.all(numpy.fabs((dp.zforce(testR,testzs)-dscfp.zforce(testR,testzs))/dscfp.zforce(testRs,testz)) < 10.**-1.), "DiskSCFPotential for double-exponential disk does not agree with DoubleExponentialDiskPotential"
    return None

def test_DiskSCFPotential_againstDoubleExp_dens():
    # Test that the DiskSCFPotential approx. of a dbl-exp disk agrees with
    # DoubleExponentialDiskPotential
    dp= potential.DoubleExponentialDiskPotential(amp=13.5,hr=1./3.,hz=1./27.)
    dscfp= potential.DiskSCFPotential(dens=lambda R,z: dp.dens(R,z),
                                      Sigma={'type':'exp','h':1./3.,'amp':1.},
                                      hz={'type':'exp','h':1./27.},
                                      a=1.,N=10,L=10)
    testRs= numpy.linspace(0.3,1.5,101)
    testzs= numpy.linspace(0.1/27.,3./27,101)
    testR= 0.9*numpy.ones_like(testzs)
    testz= 1.5/27.*numpy.ones_like(testRs)
    # Test density
    assert numpy.all(numpy.fabs((dp.dens(testRs,testz)-dscfp.dens(testRs,testz))/dscfp.dens(testRs,testz)) < 10.**-1.25), "DiskSCFPotential for double-exponential disk does not agree with DoubleExponentialDiskPotential"
    # difficult at high z
    assert numpy.all(numpy.fabs((dp.dens(testR,testzs)-dscfp.dens(testR,testzs))/dscfp.dens(testRs,testz)) < 10.**-1.), "DiskSCFPotential for double-exponential disk does not agree with DoubleExponentialDiskPotential"
    return None

def test_plotting():
    import tempfile
    #Some tests of the plotting routines, to make sure they don't fail
    kp= potential.KeplerPotential(normalize=1.)
    #Plot the rotation curve
    kp.plotRotcurve()
    kp.toPlanar().plotRotcurve() #through planar interface
    kp.plotRotcurve(Rrange=[0.01,10.],
                    grid=101,
                    savefilename=None)
    potential.plotRotcurve([kp])
    potential.plotRotcurve([kp],Rrange=[0.01,10.],
                           grid=101,
                           savefilename=None)
    #Also while saving the result
    savefile, tmp_savefilename= tempfile.mkstemp()
    try:
        os.close(savefile) #Easier this way 
        os.remove(tmp_savefilename)
        #First save
        kp.plotRotcurve(Rrange=[0.01,10.],
                        grid=101,
                        savefilename=tmp_savefilename)
        #Then plot using the saved file
        kp.plotRotcurve(Rrange=[0.01,10.],
                        grid=101,
                        savefilename=tmp_savefilename)
    finally:
        os.remove(tmp_savefilename)
    #Plot the escape-velocity curve
    kp.plotEscapecurve()
    kp.toPlanar().plotEscapecurve() #Through planar interface
    kp.plotEscapecurve(Rrange=[0.01,10.],
                       grid=101,
                       savefilename=None)
    potential.plotEscapecurve([kp])
    potential.plotEscapecurve([kp],Rrange=[0.01,10.],
                              grid=101,
                              savefilename=None)
    #Also while saving the result
    savefile, tmp_savefilename= tempfile.mkstemp()
    try:
        os.close(savefile) #Easier this way 
        os.remove(tmp_savefilename)
        #First save
        kp.plotEscapecurve(Rrange=[0.01,10.],
                           grid=101,
                           savefilename=tmp_savefilename)
        #Then plot using the saved file
        kp.plotEscapecurve(Rrange=[0.01,10.],
                           grid=101,
                           savefilename=tmp_savefilename)
    finally:
        os.remove(tmp_savefilename)
    #Plot the potential itself
    kp.plot()
    kp.plot(t=1.,rmin=0.01,rmax=1.8,nrs=11,zmin=-0.55,zmax=0.55,nzs=11, 
            effective=False,Lz=None,xy=True,
            xrange=[0.01,1.8],yrange=[-0.55,0.55],justcontours=True,
            ncontours=11,savefilename=None)
    #Also while saving the result
    savefile, tmp_savefilename= tempfile.mkstemp()
    try:
        os.close(savefile) #Easier this way 
        os.remove(tmp_savefilename)
        #First save
        kp.plot(t=1.,rmin=0.01,rmax=1.8,nrs=11,zmin=-0.55,zmax=0.55,nzs=11, 
                effective=False,Lz=None, 
                xrange=[0.01,1.8],yrange=[-0.55,0.55], 
                ncontours=11,savefilename=tmp_savefilename)
        #Then plot using the saved file
        kp.plot(t=1.,rmin=0.01,rmax=1.8,nrs=11,zmin=-0.55,zmax=0.55,nzs=11, 
                effective=False,Lz=None, 
                xrange=[0.01,1.8],yrange=[-0.55,0.55], 
                ncontours=11,savefilename=tmp_savefilename)
    finally:
        os.remove(tmp_savefilename)
    potential.plotPotentials([kp])
    #Also while saving the result
    savefile, tmp_savefilename= tempfile.mkstemp()
    try:
        os.close(savefile) #Easier this way 
        os.remove(tmp_savefilename)
        #First save
        potential.plotPotentials([kp],
                                 rmin=0.01,rmax=1.8,nrs=11,
                                 zmin=-0.55,zmax=0.55,nzs=11, 
                                 justcontours=True,xy=True,
                                 ncontours=11,savefilename=tmp_savefilename)
        #Then plot using the saved file
        potential.plotPotentials([kp],
                                 rmin=0.01,rmax=1.8,nrs=11,
                                 zmin=-0.55,zmax=0.55,nzs=11, 
                                 ncontours=11,savefilename=tmp_savefilename)
    finally:
        os.remove(tmp_savefilename)
    #Plot the effective potential
    kp.plot()
    kp.plot(effective=True,Lz=1.)
    try:
        kp.plot(effective=True,Lz=None)
    except RuntimeError:
        pass
    else:
        raise AssertionError("Potential.plot with effective=True, but Lz=None did not return a RuntimeError")
    #Plot the density of a LogarithmicHaloPotential
    lp= potential.LogarithmicHaloPotential(normalize=1.)
    lp.plotDensity()
    lp.plotDensity(rmin=0.05,rmax=1.8,nrs=11,zmin=-0.55,zmax=0.55,nzs=11, 
                   aspect=1.,log=True,justcontours=True,xy=True,
                   ncontours=11,savefilename=None)
    #Also while saving the result
    savefile, tmp_savefilename= tempfile.mkstemp()
    try:
        os.close(savefile) #Easier this way 
        os.remove(tmp_savefilename)
        #First save
        lp.plotDensity(savefilename=tmp_savefilename)
        #Then plot using the saved file
        lp.plotDensity(savefilename=tmp_savefilename)
    finally:
        os.remove(tmp_savefilename)
    potential.plotDensities([lp])
    potential.plotDensities([lp],
                            rmin=0.05,rmax=1.8,nrs=11,
                            zmin=-0.55,zmax=0.55,nzs=11, 
                            aspect=1.,log=True,xy=True,
                            justcontours=True,
                            ncontours=11,savefilename=None)
    #Plot the potential itself for a 2D potential
    kp.toPlanar().plot()
    savefile, tmp_savefilename= tempfile.mkstemp()
    try:
        os.close(savefile) #Easier this way 
        os.remove(tmp_savefilename)
        #First save
        kp.toPlanar().plot(Rrange=[0.01,1.8],grid=11,
                           savefilename=tmp_savefilename)
        #Then plot using the saved file
        kp.toPlanar().plot(Rrange=[0.01,1.8],grid=11,
                           savefilename=tmp_savefilename)
    finally:
        os.remove(tmp_savefilename)
    dp= potential.EllipticalDiskPotential()
    savefile, tmp_savefilename= tempfile.mkstemp()
    try:
        os.close(savefile) #Easier this way 
        os.remove(tmp_savefilename)
        #First save
        dp.plot(xrange=[0.01,1.8],yrange=[0.01,1.8],gridx=11,gridy=11,
                ncontours=11,savefilename=tmp_savefilename)
        #Then plot using the saved file
        dp.plot(xrange=[0.01,1.8],yrange=[0.01,1.8],gridx=11,gridy=11,
                ncontours=11,savefilename=tmp_savefilename)
    finally:
        os.remove(tmp_savefilename)
    potential.plotplanarPotentials([dp],gridx=11,gridy=11)
    #Tests of linearPotential plotting
    lip= potential.RZToverticalPotential(potential.MiyamotoNagaiPotential(normalize=1.),1.)
    lip.plot()
    savefile, tmp_savefilename= tempfile.mkstemp()
    try:
        os.close(savefile) #Easier this way 
        os.remove(tmp_savefilename)
        #First save
        lip.plot(t=0.,min=-15.,max=15,ns=21,savefilename=tmp_savefilename)
        #Then plot using the saved file
        lip.plot(t=0.,min=-15.,max=15,ns=21,savefilename=tmp_savefilename)
    finally:
        os.remove(tmp_savefilename)
    savefile, tmp_savefilename= tempfile.mkstemp()
    try:
        os.close(savefile) #Easier this way 
        os.remove(tmp_savefilename)
        #First save
        potential.plotlinearPotentials(lip,t=0.,min=-15.,max=15,ns=21,
                                       savefilename=tmp_savefilename)
        #Then plot using the saved file
        potential.plotlinearPotentials(lip,t=0.,min=-15.,max=15,ns=21,
                                       savefilename=tmp_savefilename)
    finally:
        os.remove(tmp_savefilename)
    return None

#Classes for testing Integer TwoSphericalPotential and for testing special
# cases of some other potentials
from galpy.potential import TwoPowerSphericalPotential, \
    MiyamotoNagaiPotential, PowerSphericalPotential, interpRZPotential, \
    MWPotential, FlattenedPowerPotential,MN3ExponentialDiskPotential, \
    TriaxialHernquistPotential, TriaxialNFWPotential, TriaxialJaffePotential, \
    TwoPowerTriaxialPotential, BurkertPotential, SoftenedNeedleBarPotential, \
    FerrersPotential, DiskSCFPotential
class mockSphericalSoftenedNeedleBarPotential(SoftenedNeedleBarPotential):
    def __init__(self):
        SoftenedNeedleBarPotential.__init__(self,amp=1.,a=0.000001,b=0.,
                                            c=10.,omegab=0.,pa=0.)
        self.normalize(1.)
        self.isNonAxi= False
        return None
    def _evaluate(self,R,z,phi=0.,t=0.):
        if phi is None: phi= 0.
        x,y,z= self._compute_xyz(R,phi,z,t)
        Tp, Tm= self._compute_TpTm(x,y,z)
        return numpy.log((x-self._a+Tm)/(x+self._a+Tp))/2./self._a
class mockTwoPowerIntegerSphericalPotential(TwoPowerSphericalPotential):
    def __init__(self):
        TwoPowerSphericalPotential.__init__(self,amp=1.,a=5.,alpha=2.,beta=5.)
        return None
class specialTwoPowerSphericalPotential(TwoPowerSphericalPotential):
    def __init__(self):
        TwoPowerSphericalPotential.__init__(self,amp=1.,a=5.,alpha=1.5,beta=3.)
        return None
class HernquistTwoPowerIntegerSphericalPotential(TwoPowerSphericalPotential):
    def __init__(self):
        TwoPowerSphericalPotential.__init__(self,amp=1.,a=5.,alpha=1.,beta=4.)
        return None
class JaffeTwoPowerIntegerSphericalPotential(TwoPowerSphericalPotential):
    def __init__(self):
        TwoPowerSphericalPotential.__init__(self,amp=1.,a=5.,alpha=2.,beta=4.)
        return None
class NFWTwoPowerIntegerSphericalPotential(TwoPowerSphericalPotential):
    def __init__(self):
        TwoPowerSphericalPotential.__init__(self,amp=1.,a=5.,alpha=1.,beta=3.)
        return None
class specialPowerSphericalPotential(PowerSphericalPotential):
    def __init__(self):
        PowerSphericalPotential.__init__(self,amp=1.,alpha=2.)
        return None
class specialMiyamotoNagaiPotential(MiyamotoNagaiPotential):
    def __init__(self):
        MiyamotoNagaiPotential.__init__(self,amp=1.,a=0.,b=0.1)
        return None
class specialFlattenedPowerPotential(FlattenedPowerPotential):
    def __init__(self):
        FlattenedPowerPotential.__init__(self,alpha=0.)
        return None
class specialMN3ExponentialDiskPotentialPD(MN3ExponentialDiskPotential):
    def __init__(self):
        MN3ExponentialDiskPotential.__init__(self,normalize=1.,posdens=True)
        return None
class specialMN3ExponentialDiskPotentialSECH(MN3ExponentialDiskPotential):
    def __init__(self):
        MN3ExponentialDiskPotential.__init__(self,normalize=1.,sech=True)
        return None
class BurkertPotentialNoC(BurkertPotential):
    def __init__(self):
        # Just to force not using C
        BurkertPotential.__init__(self)
        self.hasC= False
        self.hasC_dxdv= False
        return None
class oblateHernquistPotential(TriaxialHernquistPotential):
    def __init__(self):
        TriaxialHernquistPotential.__init__(self,normalize=1.,b=1.,c=.2)
        return None
class oblateNFWPotential(TriaxialNFWPotential):
    def __init__(self):
        TriaxialNFWPotential.__init__(self,normalize=1.,b=1.,c=.2)
        return None
class oblatenoGLNFWPotential(TriaxialNFWPotential):
    def __init__(self):
        TriaxialNFWPotential.__init__(self,normalize=1.,b=1.,c=.2,glorder=None)
        return None
class oblateJaffePotential(TriaxialJaffePotential):
    def __init__(self):
        TriaxialJaffePotential.__init__(self,normalize=1.,b=1.,c=.2)
        return None
class prolateHernquistPotential(TriaxialHernquistPotential):
    def __init__(self):
        TriaxialHernquistPotential.__init__(self,normalize=1.,b=1.,c=1.8)
        return None
class prolateNFWPotential(TriaxialNFWPotential):
    def __init__(self):
        TriaxialNFWPotential.__init__(self,normalize=1.,b=1.,c=1.8)
        return None
class prolateJaffePotential(TriaxialJaffePotential):
    def __init__(self):
        TriaxialJaffePotential.__init__(self,normalize=1.,b=1.,c=1.8)
        return None
class triaxialHernquistPotential(TriaxialHernquistPotential):
    def __init__(self):
        TriaxialHernquistPotential.__init__(self,normalize=1.,b=1.4,c=0.6)
        return None
class triaxialNFWPotential(TriaxialNFWPotential):
    def __init__(self):
        TriaxialNFWPotential.__init__(self,normalize=1.,b=.2,c=1.8)
        return None
class triaxialJaffePotential(TriaxialJaffePotential):
    def __init__(self):
        TriaxialJaffePotential.__init__(self,normalize=1.,b=0.4,c=0.7)
        return None
class zRotatedTriaxialNFWPotential(TriaxialNFWPotential):
    def __init__(self):
        TriaxialNFWPotential.__init__(self,normalize=1.,b=1.5,c=.2,
                                      zvec=[numpy.sin(0.5),0.,numpy.cos(0.5)])
        return None
class yRotatedTriaxialNFWPotential(TriaxialNFWPotential):
    def __init__(self):
        TriaxialNFWPotential.__init__(self,normalize=1.,b=1.5,c=.2,
                                      pa=0.2)
        return None
class fullyRotatedTriaxialNFWPotential(TriaxialNFWPotential):
    def __init__(self):
        TriaxialNFWPotential.__init__(self,normalize=1.,b=1.5,c=.2,
                                      zvec=[numpy.sin(0.5),0.,numpy.cos(0.5)],
                                      pa=0.2)
        return None
class fullyRotatednoGLTriaxialNFWPotential(TriaxialNFWPotential):
    def __init__(self):
        TriaxialNFWPotential.__init__(self,normalize=1.,b=1.5,c=.2,
                                      zvec=[numpy.sin(0.5),0.,numpy.cos(0.5)],
                                      pa=0.2,glorder=None)
        return None
# Implementations through TwoPowerTriaxialPotential
class HernquistTwoPowerTriaxialPotential(TwoPowerTriaxialPotential):
    def __init__(self):
        TwoPowerTriaxialPotential.__init__(self,amp=1.,a=5.,alpha=1.,beta=4.,
                                           b=0.3,c=1.8)
        return None
class NFWTwoPowerTriaxialPotential(TwoPowerTriaxialPotential):
    def __init__(self):
        TwoPowerTriaxialPotential.__init__(self,amp=1.,a=2.,alpha=1.,beta=3.,
                                           b=1.3,c=0.8)
        self.isNonAxi= True # to test planar-from-full
        return None
class JaffeTwoPowerTriaxialPotential(TwoPowerTriaxialPotential):
    def __init__(self):
        TwoPowerTriaxialPotential.__init__(self,amp=1.,a=5.,alpha=2.,beta=4.,
                                           b=1.3,c=1.8)
        return None
# Other DiskSCFPotentials
class sech2DiskSCFPotential(DiskSCFPotential):
    def __init__(self):
        DiskSCFPotential.__init__(self,
                                  dens=lambda R,z: numpy.exp(-3.*R)\
                                      *1./numpy.cosh(z/2.*27.)**2./4.*27.,
                                  Sigma={'h': 1./3.,
                                         'type': 'exp', 'amp': 1.0},
                                  hz={'type':'sech2','h':1./27.},
                                  a=1.,N=5,L=5)
        return None
class expwholeDiskSCFPotential(DiskSCFPotential):
    def __init__(self):
        # Add a Hernquist potential because otherwise the density near the 
        # center is zero
        from galpy.potential import HernquistPotential
        hp= HernquistPotential(normalize=0.5)
        DiskSCFPotential.__init__(self,\
            dens=lambda R,z: 13.5*numpy.exp(-0.5/(R+10.**-10.)
                                             -3.*R-numpy.fabs(z)*27.)
                                  +hp.dens(R,z),
                                  Sigma={'h': 1./3.,
                                         'type': 'expwhole','amp': 1.0,
                                         'Rhole':0.5},
                                  hz={'type':'exp','h':1./27.},
                                  a=1.,N=5,L=5)
        return None
class nonaxiDiskSCFPotential(DiskSCFPotential):
    def __init__(self):
        thp= triaxialHernquistPotential()
        DiskSCFPotential.__init__(self,\
            dens= lambda R,z,phi: 13.5*numpy.exp(-3.*R)\
                                      *numpy.exp(-27.*numpy.fabs(z))
                                  +thp.dens(R,z,phi=phi),
                                  Sigma_amp=[0.5,0.5],
                                  Sigma=[lambda R: numpy.exp(-3.*R),
                                         lambda R: numpy.exp(-3.*R)],
                                  dSigmadR=[lambda R: -3.*numpy.exp(-3.*R),
                                            lambda R: -3.*numpy.exp(-3.*R)],
                                  d2SigmadR2=[lambda R: 9.*numpy.exp(-3.*R),
                                              lambda R: 9.*numpy.exp(-3.*R)],
                                  hz=lambda z: 13.5*numpy.exp(-27.
                                                               *numpy.fabs(z)),
                                  Hz=lambda z: (numpy.exp(-27.*numpy.fabs(z))-1.
                                                +27.*numpy.fabs(z))/54.,
                                  dHzdz=lambda z: 0.5*numpy.sign(z)*\
                                      (1.-numpy.exp(-27.*numpy.fabs(z))),
                                  N=5,L=5)
        return None
# An axisymmetric FerrersPotential
class mockAxisymmetricFerrersPotential(FerrersPotential):
    def __init__(self):
        FerrersPotential.__init__(self,normalize=1.,b=1.,c=.2)
        return None
class mockInterpRZPotential(interpRZPotential):
    def __init__(self):
        interpRZPotential.__init__(self,RZPot=MWPotential,
                                   rgrid=(0.01,2.1,101),zgrid=(0.,0.26,101),
                                   logR=True,
                                   interpPot=True,interpRforce=True,
                                   interpzforce=True,interpDens=True)
class mockSnapshotRZPotential(potential.SnapshotRZPotential):
    def __init__(self):
        # Test w/ equivalent of KeplerPotential: one mass
        kp= potential.KeplerPotential(amp=1.)
        s= pynbody.new(star=1)
        s['mass']= 1./numpy.fabs(kp.Rforce(1.,0.)) #forces vc(1,0)=1
        s['eps']= 0.
        potential.SnapshotRZPotential.__init__(self,s)
class mockInterpSnapshotRZPotential(potential.InterpSnapshotRZPotential):
    def __init__(self):
        # Test w/ equivalent of KeplerPotential: one mass
        kp= potential.KeplerPotential(amp=1.)
        s= pynbody.new(star=1)
        s['mass']= 1./numpy.fabs(kp.Rforce(1.,0.)) #forces vc(1,0)=1
        s['eps']= 0.
        potential.InterpSnapshotRZPotential.__init__(self,s,
                                                   rgrid=(0.01,2.,101),
                                                   zgrid=(0.,0.3,101),
                                                   logR=False,
                                                   interpPot=True,
                                                   zsym=True)
# Some special cases of 2D, non-axisymmetric potentials, to make sure they
# are covered; need 3 to capture all of the transient behavior
from galpy.potential import CosmphiDiskPotential, DehnenBarPotential, \
    EllipticalDiskPotential, SteadyLogSpiralPotential, \
    TransientLogSpiralPotential
class mockCosmphiDiskPotentialT1(CosmphiDiskPotential):
    def __init__(self):
        CosmphiDiskPotential.__init__(self,amp=1.,phib=25.*numpy.pi/180.,
                                      p=1.,phio=0.01,m=1., 
                                      tform=0.5,tsteady=1.,
                                      cp=0.05,sp=0.05)
class mockCosmphiDiskPotentialTm1(CosmphiDiskPotential):
    def __init__(self):
        CosmphiDiskPotential.__init__(self,amp=1.,phib=25.*numpy.pi/180.,
                                      p=1.,phio=0.01,m=1., 
                                      tform=-1.,tsteady=None,
                                      cp=-0.05,sp=0.05)
class mockCosmphiDiskPotentialTm5(CosmphiDiskPotential):
    def __init__(self):
        CosmphiDiskPotential.__init__(self,amp=1.,phib=25.*numpy.pi/180.,
                                      p=1.,phio=0.01,m=1., 
                                      tform=-5.,tsteady=-1.,
                                      cp=-0.05,sp=0.05)
class mockDehnenBarPotentialT1(DehnenBarPotential):
    def __init__(self):
        DehnenBarPotential.__init__(self,omegab=1.9,rb=0.4,
                                    barphi=25.*numpy.pi/180.,beta=0.,
                                    tform=0.5,tsteady=0.5,
                                    alpha=0.01,Af=0.04)
class mockDehnenBarPotentialTm1(DehnenBarPotential):
    def __init__(self):
        DehnenBarPotential.__init__(self,omegab=1.9,rb=0.6,
                                    barphi=25.*numpy.pi/180.,beta=0.,
                                    tform=-1.,tsteady=1.01,
                                    alpha=0.01,Af=0.04)
class mockDehnenBarPotentialTm5(DehnenBarPotential):
    def __init__(self):
        DehnenBarPotential.__init__(self,omegab=1.9,rb=0.4,
                                    barphi=25.*numpy.pi/180.,beta=0.,
                                    tform=-5.,tsteady=2.,
                                    alpha=0.01,Af=0.04)
class mockEllipticalDiskPotentialT1(EllipticalDiskPotential):
    def __init__(self):
        EllipticalDiskPotential.__init__(self,amp=1.,phib=25.*numpy.pi/180.,
                                         p=1.,twophio=0.02, 
                                         tform=0.5,tsteady=1.,
                                         cp=0.05,sp=0.05)
class mockEllipticalDiskPotentialTm1(EllipticalDiskPotential):
    def __init__(self):
        EllipticalDiskPotential.__init__(self,amp=1.,phib=25.*numpy.pi/180.,
                                         p=1.,twophio=0.02,
                                         tform=-1.,tsteady=None,
                                         cp=-0.05,sp=0.05)
class mockEllipticalDiskPotentialTm5(EllipticalDiskPotential):
    def __init__(self):
        EllipticalDiskPotential.__init__(self,amp=1.,phib=25.*numpy.pi/180.,
                                         p=1.,twophio=0.02,
                                         tform=-5.,tsteady=-1.,
                                         cp=-0.05,sp=0.05)
class mockSteadyLogSpiralPotentialT1(SteadyLogSpiralPotential):
    def __init__(self):
        SteadyLogSpiralPotential.__init__(self,amp=1.,omegas=0.65,A=-0.035, 
                                          m=2,gamma=numpy.pi/4.,
                                          p=-0.3, 
                                          tform=0.5,tsteady=1.)
class mockSteadyLogSpiralPotentialTm1(SteadyLogSpiralPotential):
    def __init__(self):
        SteadyLogSpiralPotential.__init__(self,amp=1.,omegas=0.65,A=-0.035, 
                                          m=2,gamma=numpy.pi/4.,
                                          p=-0.3, 
                                          tform=-1.,tsteady=None)
class mockSteadyLogSpiralPotentialTm5(SteadyLogSpiralPotential):
    def __init__(self):
        SteadyLogSpiralPotential.__init__(self,amp=1.,omegas=0.65,A=-0.035, 
                                          m=2,gamma=numpy.pi/4.,
                                          p=-0.3, 
                                          tform=-1.,tsteady=-5.)
class mockTransientLogSpiralPotential(TransientLogSpiralPotential):
    def __init__(self):
        TransientLogSpiralPotential.__init__(self,amp=1.,omegas=0.65,A=-0.035, 
                                             m=2,gamma=numpy.pi/4.,
                                             p=-0.3)

##Potentials used for mock SCF
def rho_Zeeuw(R, z=0., phi=0., a=1.):
    r, theta, phi = bovy_coords.cyl_to_spher(R,z, phi)
    return 3./(4*numpy.pi) * numpy.power((a + r),-4.) * a
   
    
def axi_density1(R, z=0, phi=0.):
    r, theta, phi = bovy_coords.cyl_to_spher(R,z, phi)
    h = potential.HernquistPotential()
    return h.dens(R, z, phi)*(1 + numpy.cos(theta) + numpy.cos(theta)**2.)
    
def axi_density2(R, z=0, phi=0.):
    r, theta, phi = bovy_coords.cyl_to_spher(R,z, phi)
    return rho_Zeeuw(R,z,phi)*(1 +numpy.cos(theta) + numpy.cos(theta)**2)
    
def scf_density(R, z=0, phi=0.):
    eps = .1
    return axi_density2(R,z,phi)*(1 + eps*(numpy.cos(phi) + numpy.sin(phi)))

##Mock SCF class                                                         
class mockSCFZeeuwPotential(potential.SCFPotential):
    def __init__(self):
        Acos, Asin = potential.scf_compute_coeffs_spherical(rho_Zeeuw,2)
        potential.SCFPotential.__init__(self,amp=1.,Acos=Acos, Asin=Asin)
        

class mockSCFNFWPotential(potential.SCFPotential):
    def __init__(self):
        nfw = potential.NFWPotential()
        Acos, Asin = potential.scf_compute_coeffs_spherical(nfw.dens,10)
        potential.SCFPotential.__init__(self,amp=1.,Acos=Acos, Asin=Asin)
        
class mockSCFAxiDensity1Potential(potential.SCFPotential):
    def __init__(self):
        Acos, Asin = potential.scf_compute_coeffs_axi(axi_density1,10,2)
        potential.SCFPotential.__init__(self,amp=1.,Acos=Acos, Asin=Asin)
              
              
class mockSCFAxiDensity2Potential(potential.SCFPotential):
    def __init__(self):
        Acos, Asin = potential.scf_compute_coeffs_axi(axi_density2,10,2)
        potential.SCFPotential.__init__(self,amp=1.,Acos=Acos, Asin=Asin)
        
class mockSCFDensityPotential(potential.SCFPotential):
    def __init__(self):
        Acos, Asin = potential.scf_compute_coeffs(scf_density,10,10,phi_order=30)
        potential.SCFPotential.__init__(self,amp=1.,Acos=Acos, Asin=Asin)
        
#Class to test potentials given as lists, st we can use their methods as class.
from galpy.potential import Potential, \
    evaluatePotentials, evaluateRforces, evaluatezforces, evaluatephiforces, \
    evaluateR2derivs, evaluatez2derivs, evaluateRzderivs, \
    evaluateDensities
from galpy.potential import planarPotential, \
    evaluateplanarPotentials, evaluateplanarRforces, evaluateplanarphiforces, \
    evaluateplanarR2derivs
class testMWPotential(Potential):
    """Initialize with potential in natural units"""
    def __init__(self,potlist=MWPotential):
        self._potlist= potlist
        Potential.__init__(self,amp=1.)
        self.isNonAxi= True^numpy.prod([True^p.isNonAxi for p in self._potlist])
        return None
    def _evaluate(self,R,z,phi=0,t=0,dR=0,dphi=0):
        return evaluatePotentials(self._potlist,R,z,phi=phi,t=t,
                                  dR=dR,dphi=dphi)
    def _Rforce(self,R,z,phi=0.,t=0.):
        return evaluateRforces(self._potlist,R,z,phi=phi,t=t)
    def _phiforce(self,R,z,phi=0.,t=0.):
        return evaluatephiforces(self._potlist,R,z,phi=phi,t=t)
    def _zforce(self,R,z,phi=0.,t=0.):
        return evaluatezforces(self._potlist,R,z,phi=phi,t=t)
    def _R2deriv(self,R,z,phi=0.,t=0.):
        return evaluateR2derivs(self._potlist,R,z,phi=phi,t=t)
    def _z2deriv(self,R,z,phi=0.,t=0.):
        return evaluatez2derivs(self._potlist,R,z,phi=phi,t=t)
    def _Rzderiv(self,R,z,phi=0.,t=0.):
        return evaluateRzderivs(self._potlist,R,z,phi=phi,t=t)
    def _phi2deriv(self,R,z,phi=0.,t=0.):
        return evaluatePotentials(self._potlist,R,z,phi=phi,t=t,dphi=2)
    def _Rphideriv(self,R,z,phi=0.,t=0.):
        return evaluatePotentials(self._potlist,R,z,phi=phi,t=t,dR=1,
                                  dphi=1)
    def _dens(self,R,z,phi=0.,t=0.,forcepoisson=False):
        return evaluateDensities(self._potlist,R,z,phi=phi,t=t,
                                 forcepoisson=forcepoisson)
    def vcirc(self,R):
        return potential.vcirc(self._potlist,R)
    def normalize(self,norm,t=0.):
        self._amp= norm
    def OmegaP(self):
        return 1.
#Class to test lists of planarPotentials
class testplanarMWPotential(planarPotential):
    """Initialize with potential in natural units"""
    def __init__(self,potlist=MWPotential):
        self._potlist= [p.toPlanar() for p in potlist if isinstance(p,Potential)]
        self._potlist.extend([p for p in potlist if isinstance(p,planarPotential)])
        planarPotential.__init__(self,amp=1.)
        self.isNonAxi= True^numpy.prod([True^p.isNonAxi for p in self._potlist])
        return None
    def _evaluate(self,R,phi=0,t=0,dR=0,dphi=0):
        return evaluateplanarPotentials(self._potlist,R,phi=phi,t=t)
    def _Rforce(self,R,phi=0.,t=0.):
        return evaluateplanarRforces(self._potlist,R,phi=phi,t=t)
    def _phiforce(self,R,phi=0.,t=0.):
        return evaluateplanarphiforces(self._potlist,R,phi=phi,t=t)
    def _R2deriv(self,R,phi=0.,t=0.):
        return evaluateplanarR2derivs(self._potlist,R,phi=phi,t=t)
    def _phi2deriv(self,R,phi=0.,t=0.):
        return evaluateplanarPotentials(self._potlist,R,phi=phi,t=t,dphi=2)
    def _Rphideriv(self,R,phi=0.,t=0.):
        return evaluateplanarPotentials(self._potlist,R,phi=phi,t=t,dR=1,
                                        dphi=1)
    def vcirc(self,R):
        return potential.vcirc(self._potlist,R)
    def normalize(self,norm,t=0.):
        self._amp= norm
    def OmegaP(self):
        return 1.

class mockFlatEllipticalDiskPotential(testplanarMWPotential):
    def __init__(self):
        testplanarMWPotential.__init__(self,
                                       potlist=[potential.LogarithmicHaloPotential(normalize=1.),
                                                potential.EllipticalDiskPotential(phib=numpy.pi/2.,p=0.,tform=None,tsteady=None,twophio=14./220.)])
    def OmegaP(self):
        return 0.
class mockSlowFlatEllipticalDiskPotential(testplanarMWPotential):
    def __init__(self):
        testplanarMWPotential.__init__(self,
                                       potlist=[potential.LogarithmicHaloPotential(normalize=1.),
                                                potential.EllipticalDiskPotential(phib=numpy.pi/2.,p=0.,twophio=14./220.,tform=1.,tsteady=250.)])
    def OmegaP(self):
        return 0.
class mockFlatLopsidedDiskPotential(testplanarMWPotential):
    def __init__(self):
        testplanarMWPotential.__init__(self,
                                       potlist=[potential.LogarithmicHaloPotential(normalize=1.),
                                                potential.LopsidedDiskPotential(phib=numpy.pi/2.,p=0.,tform=None,tsteady=None,phio=10./220.)])
    def OmegaP(self):
        return 0.
class mockSlowFlatLopsidedDiskPotential(testplanarMWPotential):
    def __init__(self):
        testplanarMWPotential.__init__(self,
                                       potlist=[potential.LogarithmicHaloPotential(normalize=1.),
                                                potential.LopsidedDiskPotential(phib=numpy.pi/2.,p=0.,tform=1.,tsteady=250.,phio=10./220.)])
    def OmegaP(self):
        return 0.
class mockFlatDehnenBarPotential(testMWPotential):
    def __init__(self):
        testMWPotential.__init__(self,
                                 potlist=[potential.LogarithmicHaloPotential(normalize=1.),
                                          potential.DehnenBarPotential()])
    def OmegaP(self):
        return self._potlist[1].OmegaP()
class mockSlowFlatDehnenBarPotential(testMWPotential):
    def __init__(self):
        testMWPotential.__init__(self,
                                 potlist=[potential.LogarithmicHaloPotential(normalize=1.),
                                          potential.DehnenBarPotential(tform=1.,tsteady=250.,rolr=2.5)])
    def OmegaP(self):
        return self._potlist[1].OmegaP()
class mockFlatSteadyLogSpiralPotential(testplanarMWPotential):
    def __init__(self):
        testplanarMWPotential.__init__(self,
                                       potlist=[potential.LogarithmicHaloPotential(normalize=1.),
                                                potential.SteadyLogSpiralPotential()])
    def OmegaP(self):
        return self._potlist[1].OmegaP()
class mockSlowFlatSteadyLogSpiralPotential(testplanarMWPotential):
    def __init__(self):
        testplanarMWPotential.__init__(self,
                                       potlist=[potential.LogarithmicHaloPotential(normalize=1.),
                                                potential.SteadyLogSpiralPotential(tform=.1,tsteady=25.)])
    def OmegaP(self):
        return self._potlist[1].OmegaP()
class mockFlatTransientLogSpiralPotential(testplanarMWPotential):
    def __init__(self):
        testplanarMWPotential.__init__(self,
                                       potlist=[potential.LogarithmicHaloPotential(normalize=1.),
                                                potential.TransientLogSpiralPotential(to=-10.)]) #this way, it's basically a steady spiral
    def OmegaP(self):
        return self._potlist[1].OmegaP()

#Class to test lists of linearPotentials
from galpy.potential import linearPotential, \
    evaluatelinearPotentials, evaluatelinearForces, \
    RZToverticalPotential
class testlinearMWPotential(linearPotential):
    """Initialize with potential in natural units"""
    def __init__(self,potlist=MWPotential):
        self._potlist= RZToverticalPotential(potlist,1.)
        linearPotential.__init__(self,amp=1.)
        return None
    def _evaluate(self,R,phi=0,t=0,dR=0,dphi=0):
        return evaluatelinearPotentials(self._potlist,R,t=t)
    def _force(self,R,t=0.):
        return evaluatelinearForces(self._potlist,R,t=t)
    def normalize(self,norm,t=0.):
        self._amp= norm

class mockCombLinearPotential(testlinearMWPotential):
    def __init__(self):
        testlinearMWPotential.__init__(self,
                                       potlist=[potential.MWPotential[0],
                                                potential.MWPotential[1].toVertical(1.),
                                                potential.MWPotential[2].toVertical(1.)])

class mockSimpleLinearPotential(testlinearMWPotential):
    def __init__(self):
        testlinearMWPotential.__init__(self,
                                       potlist=potential.MiyamotoNagaiPotential(normalize=1.).toVertical(1.))

class mockMovingObjectPotential(testMWPotential):
    def __init__(self,rc=0.75,maxt=1.,nt=50):
        from galpy.orbit import Orbit
        self._rc= rc
        o1= Orbit([self._rc,0.,1.,0.,0.,0.])
        o2= Orbit([self._rc,0.,1.,0.,0.,numpy.pi])
        lp= potential.LogarithmicHaloPotential(normalize=1.)
        times= numpy.linspace(0.,maxt,nt)
        o1.integrate(times,lp,method='dopr54_c')
        o2.integrate(times,lp,method='dopr54_c')
        self._o1p= potential.MovingObjectPotential(o1)
        self._o2p= potential.MovingObjectPotential(o2)
        testMWPotential.__init__(self,[self._o1p,self._o2p])
        self.isNonAxi= True
        return None
    def phi2deriv(self,R,z,phi=0.,t=0.):
        raise AttributeError
    def OmegaP(self):
        return 1./self._rc
from galpy.potential_src.ForceSoftening import PlummerSoftening
class mockMovingObjectExplSoftPotential(testMWPotential):
    def __init__(self,rc=0.75,maxt=1.,nt=50):
        from galpy.orbit import Orbit
        self._rc= rc
        o1= Orbit([self._rc,0.,1.,0.,0.,0.])
        o2= Orbit([self._rc,0.,1.,0.,0.,numpy.pi])
        lp= potential.LogarithmicHaloPotential(normalize=1.)
        times= numpy.linspace(0.,maxt,nt)
        o1.integrate(times,lp,method='dopr54_c')
        o2.integrate(times,lp,method='dopr54_c')
        self._o1p= potential.MovingObjectPotential(o1,
                                                   softening=PlummerSoftening(softening_length=0.05))
        self._o2p= potential.MovingObjectPotential(o2,
                                                   softening=PlummerSoftening(softening_length=0.05))
        testMWPotential.__init__(self,[self._o1p,self._o2p])
        self.isNonAxi= True
        return None
class mockMovingObjectLongIntPotential(mockMovingObjectPotential):
    def __init__(self,rc=0.75):
        mockMovingObjectPotential.__init__(self,rc=rc,maxt=15.,nt=3001)
        return None