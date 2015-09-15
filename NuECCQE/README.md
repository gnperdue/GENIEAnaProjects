
* First, you need to retrieve a copy of the MINERvA splines for GENIE 2.6.2.
* Go to 

    http://cdcvs.fnal.gov/cgi-bin/public-cvs/cvsweb-public.cgi/AnalysisFramework/MParamFiles/data/GENIE/spline_files/gxspl-nuclear-MINERVA_Full.xml.gz?cvsroot=mnvsoft

* Download a copy of Revision 1.2.
* Unzip the file and rename it `gxspl-nuclear-MINERVA_Full_2_6_2.xml`.
* Next, run:

        python add_cross_sections.py --splines gxspl-nuclear-MINERVA_Full_2_6_2.xml --target 1000060120
        python add_cross_sections.py --splines gxspl-nuclear-MINERVA_Full_2_6_2.xml --target 1000060120 --nc
        python add_cross_sections.py --splines gxspl-nuclear-MINERVA_Full_2_6_2.xml --target 1000010010
        python add_cross_sections.py --splines gxspl-nuclear-MINERVA_Full_2_6_2.xml --target 1000010010 --nc

* This will produce the files:

        Electron_Antineutrino_CC_Carbon.txt
        Electron_Antineutrino_CC_Hydrogen.txt
        Electron_Antineutrino_NC_Carbon.txt
        Electron_Antineutrino_NC_Hydrogen.txt
        Electron_Neutrino_CC_Carbon.txt
        Electron_Neutrino_CC_Hydrogen.txt
        Electron_Neutrino_NC_Carbon.txt
        Electron_Neutrino_NC_Hydrogen.txt
        Muon_Antineutrino_CC_Carbon.txt
        Muon_Antineutrino_CC_Hydrogen.txt
        Muon_Antineutrino_NC_Carbon.txt
        Muon_Antineutrino_NC_Hydrogen.txt
        Muon_Neutrino_CC_Carbon.txt
        Muon_Neutrino_CC_Hydrogen.txt
        Muon_Neutrino_NC_Carbon.txt
        Muon_Neutrino_NC_Hydrogen.txt

* Next, open the root files `/minerva/data/users/jwolcott/flux/*nu{e,mu}_flux_nueccqentuples_resurrection.root`
* For each file, in the appropriate file, run:

        flux_E_cvweighted->Print("all"); > electron_antinu_flux.txt
        flux_E_cvweighted->Print("all"); > muon_antinu_flux.txt
        flux_E_cvweighted->Print("all"); > electron_nu_flux.txt
        flux_E_cvweighted->Print("all"); > muon_nu_flux.txt

* Next, run `python print_splines.py --splines DFR_1000010010_splines.xml` to produce:

        ReinDFRPXSec_Electron_Antineutrino_CC_on_Hydrogen.txt
        ReinDFRPXSec_Electron_Antineutrino_NC_on_Hydrogen.txt
        ReinDFRPXSec_Electron_Neutrino_CC_on_Hydrogen.txt
        ReinDFRPXSec_Electron_Neutrino_NC_on_Hydrogen.txt
        ReinDFRPXSec_Muon_Antineutrino_CC_on_Hydrogen.txt
        ReinDFRPXSec_Muon_Antineutrino_NC_on_Hydrogen.txt
        ReinDFRPXSec_Muon_Neutrino_CC_on_Hydrogen.txt
        ReinDFRPXSec_Muon_Neutrino_NC_on_Hydrogen.txt

* Finally, run `python flux_convolution.py`. Note that this procedure normalizes
the flux files to unity.

        CC Carbon
        Anti-electron neutrino CC on Carbon total xsec = 37.6117856754 x 10^(-38) cm2
        Electron neutrino CC on Carbon total xsec = 52.1966912346 x 10^(-38) cm2
        Anti-muon neutrino CC on Carbon total xsec = 25.8769441087 x 10^(-38) cm2
        Muon neutrino CC on Carbon total xsec = 43.3498216643 x 10^(-38) cm2
            
        NC Carbon
        Anti-electron neutrino NC on Carbon total xsec = 12.9854974675 x 10^(-38) cm2
        Electron neutrino NC on Carbon total xsec = 15.0445508063 x 10^(-38) cm2
        Anti-muon neutrino NC on Carbon total xsec = 9.10849358775 x 10^(-38) cm2
        Muon neutrino NC on Carbon total xsec = 12.7416035042 x 10^(-38) cm2
            
        CC Hydrogen
        Anti-electron neutrino CC on Hydrogen total xsec = 3.85481054572 x 10^(-38) cm2
        Electron neutrino CC on Hydrogen total xsec = 2.93087063056 x 10^(-38) cm2
        Anti-muon neutrino CC on Hydrogen total xsec = 2.72637755554 x 10^(-38) cm2
        Muon neutrino CC on Hydrogen total xsec = 2.38741078524 x 10^(-38) cm2
        
        NC Hydrogen
        Anti-electron neutrino NC on Hydrogen total xsec = 1.05600940717 x 10^(-38) cm2
        Electron neutrino NC on Hydrogen total xsec = 1.18138326314 x 10^(-38) cm2
        Anti-muon neutrino NC on Hydrogen total xsec = 0.741623447796 x 10^(-38) cm2
        Muon neutrino NC on Hydrogen total xsec = 1.00236725871 x 10^(-38) cm2
        
        Rein CC Hydrogen
        Anti-electron neutrino CC on Hydrogen total xsec = 0.205262943845 x 10^(-38) cm2
        Electron neutrino CC on Hydrogen total xsec = 0.165770285792 x 10^(-38) cm2
        Anti-muon neutrino CC on Hydrogen total xsec = 0.180177491493 x 10^(-38) cm2
        Muon neutrino CC on Hydrogen total xsec = 0.158374593581 x 10^(-38) cm2
        
        Rein NC Hydrogen
        Anti-electron neutrino NC on Hydrogen total xsec = 0.205227989755 x 10^(-38) cm2
        Electron neutrino NC on Hydrogen total xsec = 0.165837208051 x 10^(-38) cm2
        Anti-muon neutrino NC on Hydrogen total xsec = 0.180168358819 x 10^(-38) cm2
        Muon neutrino NC on Hydrogen total xsec = 0.158331666016 x 10^(-38) cm2
    
* We may cut on energy ranges: `python flux_convolution.py --min 2 --max 20` Note
that this **renormalizes the flux**, so the weighted cross section does not always
go down. For example:

        $ python flux_convolution.py --min 2 --max 20
        CC Carbon
        Anti-electron neutrino CC on Carbon total xsec = 34.7262554542 x 10^(-38) cm2
        Electron neutrino CC on Carbon total xsec = 55.1347955989 x 10^(-38) cm2
        Anti-muon neutrino CC on Carbon total xsec = 28.8476148138 x 10^(-38) cm2
        Muon neutrino CC on Carbon total xsec = 45.0533208676 x 10^(-38) cm2
        
        NC Carbon
        Anti-electron neutrino NC on Carbon total xsec = 12.0651515123 x 10^(-38) cm2
        Electron neutrino NC on Carbon total xsec = 15.8775665109 x 10^(-38) cm2
        Anti-muon neutrino NC on Carbon total xsec = 10.1722369861 x 10^(-38) cm2
        Muon neutrino NC on Carbon total xsec = 13.3871631409 x 10^(-38) cm2
        
        CC Hydrogen
        Anti-electron neutrino CC on Hydrogen total xsec = 3.55957267536 x 10^(-38) cm2
        Electron neutrino CC on Hydrogen total xsec = 3.04769030792 x 10^(-38) cm2
        Anti-muon neutrino CC on Hydrogen total xsec = 3.0363323642 x 10^(-38) cm2
        Muon neutrino CC on Hydrogen total xsec = 2.47392299834 x 10^(-38) cm2
        
        NC Hydrogen
        Anti-electron neutrino NC on Hydrogen total xsec = 0.978184718406 x 10^(-38) cm2
        Electron neutrino NC on Hydrogen total xsec = 1.24258684125 x 10^(-38) cm2
        Anti-muon neutrino NC on Hydrogen total xsec = 0.825475779287 x 10^(-38) cm2
        Muon neutrino NC on Hydrogen total xsec = 1.05008299944 x 10^(-38) cm2
        
        Rein CC Hydrogen
        Anti-electron neutrino CC on Hydrogen total xsec = 0.21792418187 x 10^(-38) cm2
        Electron neutrino CC on Hydrogen total xsec = 0.18252868106 x 10^(-38) cm2
        Anti-muon neutrino CC on Hydrogen total xsec = 0.204143776234 x 10^(-38) cm2
        Muon neutrino CC on Hydrogen total xsec = 0.169733162643 x 10^(-38) cm2
        
        Rein NC Hydrogen
        Anti-electron neutrino NC on Hydrogen total xsec = 0.217896344508 x 10^(-38) cm2
        Electron neutrino NC on Hydrogen total xsec = 0.182670625462 x 10^(-38) cm2
        Anti-muon neutrino NC on Hydrogen total xsec = 0.203822436951 x 10^(-38) cm2
        Muon neutrino NC on Hydrogen total xsec = 0.169556329885 x 10^(-38) cm2
        
        $ python run flux_convolution.py --min 20 --max 21
        CC Carbon
        Anti-electron neutrino CC on Carbon total xsec = 75.8352626597 x 10^(-38) cm2
        Electron neutrino CC on Carbon total xsec = 168.196236945 x 10^(-38) cm2
        Anti-muon neutrino CC on Carbon total xsec = 76.1599516586 x 10^(-38) cm2
        Muon neutrino CC on Carbon total xsec = 166.120734658 x 10^(-38) cm2
        
        NC Carbon
        Anti-electron neutrino NC on Carbon total xsec = 25.5110350726 x 10^(-38) cm2
        Electron neutrino NC on Carbon total xsec = 48.5573246189 x 10^(-38) cm2
        Anti-muon neutrino NC on Carbon total xsec = 26.1246793997 x 10^(-38) cm2
        Muon neutrino NC on Carbon total xsec = 48.7675840846 x 10^(-38) cm2
        
        CC Hydrogen
        Anti-electron neutrino CC on Hydrogen total xsec = 7.80069119552 x 10^(-38) cm2
        Electron neutrino CC on Hydrogen total xsec = 9.39150431197 x 10^(-38) cm2
        Anti-muon neutrino CC on Hydrogen total xsec = 7.88085090842 x 10^(-38) cm2
        Muon neutrino CC on Hydrogen total xsec = 9.28917509816 x 10^(-38) cm2
        
        NC Hydrogen
        Anti-electron neutrino NC on Hydrogen total xsec = 2.07348967763 x 10^(-38) cm2
        Electron neutrino NC on Hydrogen total xsec = 3.79254113717 x 10^(-38) cm2
        Anti-muon neutrino NC on Hydrogen total xsec = 2.12388047144 x 10^(-38) cm2
        Muon neutrino NC on Hydrogen total xsec = 3.80960599363 x 10^(-38) cm2
        
        Rein CC Hydrogen
        Anti-electron neutrino CC on Hydrogen total xsec = 0.277102628344 x 10^(-38) cm2
        Electron neutrino CC on Hydrogen total xsec = 0.280278758118 x 10^(-38) cm2
        Anti-muon neutrino CC on Hydrogen total xsec = 0.286155071379 x 10^(-38) cm2
        Muon neutrino CC on Hydrogen total xsec = 0.283783136309 x 10^(-38) cm2
        
        Rein NC Hydrogen
        Anti-electron neutrino NC on Hydrogen total xsec = 0.277017209929 x 10^(-38) cm2
        Electron neutrino NC on Hydrogen total xsec = 0.280192360643 x 10^(-38) cm2
        Anti-muon neutrino NC on Hydrogen total xsec = 0.283798338772 x 10^(-38) cm2
        Muon neutrino NC on Hydrogen total xsec = 0.281445938623 x 10^(-38) cm2
    
* For a quick smell test, the total CC cross section at 20 GeV on Carbon is about

        In [49]: 166.120734658 / 20 / 12   # x 10^(-38) cm^2 / GeV
        Out[49]: 0.6921697277416667

