# CavitySLRefractiveIndexFIMMPROPScanner Python Script
# Joshua Brake
# 2/22/14
# The purpose of this scanner is to use the basic scanner set up in subnode 26 of the FIMMWAVE/FIMMPROP file "Multilaser FP Biosensor.prj" to simulate the resonance shift due to the adhesion of biomarkers on the rear surface of the cavity structure. This is simulated by using gold thin films as the mirrors for the Fabry-Perot etalon structure and then by simulating a distance between the mirrors to be composed of two layers of different refractive indices. One layer represents the fluid in the cavity (n=1.33) and the sensing layer is assumed to have a higher variable refractive index ranging from n=1.40-1.55 which represents different concentrations of adhered biomarkers. (This simulation assumes the variable RI, fixed height model.) The optical power of a specific wavelength is measured as the RI of the sensing layer is changed.

# FIMMWAVE's default units are um

# Required initialization of FIMMWAVE/FIMMPROP libaries and network connection. See FIMMWAVE/FIMMPROP documentation for details
from pdPythonLib import*
fimm = pdApp()
fimm.ConnectToApp()

# Initialization of variable call function shortcuts
# The numbers in the subnodes refer to the number of the object in the list the in FIMMWAVE program. subnodes[26] refers to the scanner object and subnodes[1] refers to the variables object where the parameters for the various devices and scanners are stored.
variables = "app.subnodes[1].subnodes[1]"
scanner = "app.subnodes[1].subnodes[26]"

# Initialization of variables
l = [0.780,0.830,0.850]                         # Wavelength(s) for scan (um)
steps = 2000                        # Number of steps for scanner. Determines resolution
SLT = 0.200                         # Sensing layer thickness (um)
CW = [3.96,3.97,3.98,3.99,4.00,4.01,4.02,4.03,4.04]                        # Intial Width(s) of porous region (water) in cavity (um)
RIC = 1.33                          # Refractive index of the cavity
RISLi = 1.40                        # Initial refractive index of the sensing layer
RISLf = 1.55                        # Final refractive index of the sensing layer
GW = [0.012]                        # Gold film thickness (um)

# Set FIMMWAVE initial values. All values are set by making a string and then sending it to FIMMWAVE by calling the Exec command on the fimm object initiated in the initialization.
fimm.Exec("{variables}.setvariable(Cavity_width,Complete_Cavity_Width-SL_thickness)")
fimm.Exec("{variables}.setvariable(RI_cavity,{RIC})")
fimm.Exec("{variables}.setvariable(SL_thickness,{SLT})")

# Set up scanner parameters
fimm.Exec("{scanner}.nsteps={steps}")


# Nested for loops to scan through all possible combinations of laser wavelength (l), gold thin film thickness (GW), and cavity width (CW).
for n in range(0,len(l)):
    
    for j in range(0,len(GW)):
        
        for i in range(0,len(CW)):
            
            # Set respective variables
            fimm.Exec("{variables}.setvariable(Complete_Cavity_Width,{CW[i]})")
            fimm.Exec("{variables}.setvariable(Gold_width,{GW[j]})")
            fimm.Exec("{variables}.setvariable(lambda,{l[n]})")
            
            # Set scanner parameters
            fimm.Exec("{scanner}.xstart={RISLi}")
            fimm.Exec("{scanner}.xend={RISLf}")
            fimm.Exec("{scanner}.xlabel=RI_SL")
            
            # Start scan
            fimm.Exec("{scanner}.scan(0,0,1)")
            
            # Variables for naming the files
            GWnm = GW[j]*1000
            lnm = l[n]*1000
            
            # Name file and open for writing results
            filename = "C:\Users\joshbrake.LETNET\Dropbox\LETU\LETU M.S.E. Stuff\FIMMWAVE-FIMMPROP Stuff\Scripts\Simulation\FIMMPROP SL Scanner\SL Scan RI " + '%.2f' % RISLi + "-" + '%.2f' % RISLf + " " + '%.2f' % CW[i] + " um CW " + '%.1f' % GWnm + " nm GW " + str(steps) + " pts " + '%.1f' % lnm + " nm.txt"
            output = open(filename, 'w')
            
            # Saves results to a file
            for x in xrange(1,steps):
                fimm.AddCmd("{scanner}.ydata[{x}].rhspower")        # Read the result
            outputpower = fimm.Exec("{scanner}.ydata[{steps}]")                   # Read in sensing layer thickness
            
            for x in xrange(1,steps):
                fimm.AddCmd("{scanner}.xdata[{x}].rhspower")        # Read the result
            outputSLT = fimm.Exec("{scanner}.xdata[{steps}]")                   # Read in sensing layer thickness
            
            for x in xrange(0,steps-1):
                output.write(str(outputSLT[x]) + ' ' + str(outputpower[x])+'\n')      # Write the result to the text file we opened
            
            output.close()  # Close the text file

del fimm    # Delete pdApp object