import numpy as np
import pandas as pd

prim = lambda H: np.transpose(np.conj(H))
inv  = lambda H: np.linalg.inv(H)

def AMP( y,H,sigma2,sigmas2,iterAMP,m,n ) :
    r     = np.zeros(m).reshape(m,1);
    xhat  = np.zeros(n).reshape(n,1);
    alpha = sigmas2 ;                   # SIGNAL VARIANCE ESTIMATION
    for t in range( 1,iterAMP+1 ):
        r     = y - np.dot(H,xhat) + (n/m)*sigmas2/(sigmas2+alpha)*r;
        alpha = sigma2 + (n/m) * sigmas2 * alpha / ( sigmas2+alpha );
        xhat  = ( sigmas2/(sigmas2+alpha) ) * ( np.dot( prim(H),r) + xhat )
    return( np.sign(np.real(xhat))+1j*np.sign(np.imag(xhat)) )

if __name__ == '__main__' :
    print ( "APPROXIMATE MESSAGE PASSING" )
    m = 128 ; 	# NUMBER OF ANTENNAS
    n =  16 ; 	# NUMBERS OF USERS
    Nmonte = int(1e3);	# NUMBER OF MONTECARLO SWEEPS
    bVerbose = False

    SNRrange = [ n for n in range(1,21) ] # HOW MUCH ENERGY WE CRAM IN
    count    = 0;
    pm_r     = lambda n : 2*(np.random.rand(n)>0.5)-np.ones(n) # HOOMAN SIGNUL
    meta_errors = {'MMSE':[[],[]],'AMP1':[[],[]],'AMP2':[[],[]]}
    for s in SNRrange :
        SNRdb  = s ;
        errors = {'MMSE':[],'AMP1':[],'AMP2':[]}
        for MonteCarlo in range(1,Nmonte+1) :
            x = np.array(pm_r(n) + 1j*pm_r(n)).reshape(n,1)   # MESSAGE (COMPLEX)
            sigmas2 = 2. ;                                    # SIGNAL VARIANCE
            sigma2  = 2.* n/m * 10.**(-SNRdb/10.);            #  NOISE VARIANCE SNR IN LOG10 DB
            H = 1./np.sqrt(2*m) * np.random.randn(m,n) + 1.j/np.sqrt(2.*m) * np.random.randn(m,n) ; # TRANSMITION WITH RANDOM USERS
            w = ( np.sqrt(2*sigma2)*np.random.randn(m,1) + 1.j*np.sqrt(2.*sigma2)*np.random.randn(m,1) ); # NOISE
            y = np.dot(H,x) + w ;                             # THE CHANNEL

            iterAMP1 = 2 ;
            xhat1 = AMP(y,H,sigma2,sigmas2,iterAMP1,m,n);     # APPROXIMATE MESSAGE 1
            errors['AMP1'] .append( np.sum(x != xhat1) ) ;

            if bVerbose:
                print ( 'y:',y )
                print ( 'H:',H )
                print ( 'sigma2:',sigma2 )
                print ( 'sigmas2:',sigmas2 ) ;exit(1)

            iterAMP2 = 4 ;
            xhat2 = AMP(y,H,sigma2,sigmas2,iterAMP2,m,n);     # APPROXIMATE MESSAGE 2
            errors['AMP2'] .append( np.sum(x != xhat2) ) ;

            x_mmse = np.dot( inv( sigma2/sigmas2*np.eye(n) + np.dot(prim(H),H) ) , np.dot(prim(H),y) ) ;
            x_mmse = np.sign(np.real(x_mmse)) + 1.j*np.sign(np.imag(x_mmse));
            errors['MMSE'] .append( np.sum(x !=x_mmse) ) ;

        count = count + 1 ;

        meta_errors['AMP1'][0].append( np.mean(errors['AMP1']) ) ;
        meta_errors['AMP1'][1].append( np.std (errors['AMP1']) ) ;
        meta_errors['AMP2'][0].append( np.mean(errors['AMP2']) ) ;
        meta_errors['AMP2'][1].append( np.std (errors['AMP2']) ) ;

        meta_errors['MMSE'][0].append( np.mean(errors['MMSE']) ) ;
        meta_errors['MMSE'][1].append( np.std (errors['MMSE']) ) ;

import matplotlib.pyplot as plt
plt .semilogy( SNRrange,meta_errors['AMP1'][0],'r' )
plt .semilogy( SNRrange,meta_errors['AMP2'][0],'b' )
plt .semilogy( SNRrange,meta_errors['MMSE'][0],'k' )
plt .title ('Approximate Message Passing')
plt .xlabel('Signal to Noise [db]')
plt .ylabel('Mean meta error')
plt .show( )
