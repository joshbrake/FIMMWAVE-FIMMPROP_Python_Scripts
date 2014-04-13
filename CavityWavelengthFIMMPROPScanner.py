from pdPythonLib import*
fimm = pdApp()
fimm.ConnectToApp()

# Initialization

# Initialization of variable call functions
variables = "app.subnodes[1].subnodes[1]"
scanner = "app.subnodes[1].subnodes[25]"

# Initialization of variables
li = 0.700               # Initial wavelength for scan
lf = 0.900              # Final wavelength for scan
steps = 2000                           # Number of steps for scanner
SLT = [0.000,0.006]                          # Sensing layer thickness (um)
CW = [4.00]                    # Intial Width of porous region (water) in cavity (um)
RIC = 1.33                          # Refractive index of the cavity
RISL = 1.5                          # Refractive index of the sensing layer
GW = [0.012]
#GW = 0.00653887                     # Gold film thickness (um)

# Set FIMMWAVE initial values
fimm.Exec("{variables}.setvariable(RI_cavity,{RIC})")
fimm.Exec("{variables}.setvariable(RI_SL,{RISL})")

fimm.Exec("{scanner}.nsteps={steps}")

# Set up scanner parameters
fimm.Exec("{scanner}.xstart={li}")    # Set the wavelength for the scanner. Since we are only scanning for one step, the starting x value is the only value which matters.
fimm.Exec("{scanner}.xend={lf}")
fimm.Exec("{scanner}.xlabel=lambda")

    
for i in range(0,len(CW)):

    for n in range(0,len(SLT)):
        
        for j in range(0,len(GW)):
            
            fimm.Exec("{variables}.setvariable(Gold_width,{GW[j]})")
            fimm.Exec("{variables}.setvariable(SL_thickness,{SLT[n]})")
            fimm.Exec("{variables}.setvariable(Cavity_width,{CW[i]-SLT[n]})")
            fimm.Exec("{scanner}.scan(0,0,1)")
        
            filename = "C:\Users\joshbrake.LETNET\Dropbox\LETU\LETU M.S.E. Stuff\FIMMWAVE-FIMMPROP Biosensors Stuff\Scripts\Simulation Data\FIMMPROP Wavelength Scanner\Wavelength Scanner " + str(li*1000)+ "-" + str(lf*1000) + " nm " + '%.2f' % CW[i] + " um CW " + '%.3f' % SLT[n] + " um SLT " + '%.3f' % GW[j] + " um GW " + str(steps) + " pts.txt"
            output = open(filename, 'w')

 # Saves results to a file
            for x in xrange(1,steps+1):
                outputpower = fimm.Exec("{scanner}.ydata[{x}].rhspower")        # Read the result
                outputlambda = fimm.Exec("{scanner}.xdata[{x}]")                   # Read in sensing layer thickness
                output.write(str(outputlambda) + ' ' + str(outputpower)+'\n')      # Write the result to the text file we opened

            output.close()  # Close the text file
    
del fimm    # Delete pdApp object