from pdPythonLib import*
fimm = pdApp()
fimm.ConnectToApp()

# Initialization

# Initialization of variable call functions
variables = "app.subnodes[1].subnodes[1]"
scanner = "app.subnodes[1].subnodes[25]"

# Initialization of variables
li = 0.700               # Wavelength for scan
lf = 0.900
steps = 2000                           # Number of steps for scanner
SLT = 0.000                          # Sensing layer thickness (um)
CW = [3.40,3.69,3.99,4.28]                          # Intial Width of porous region (water) in cavity (um)
RIC = [1.00,1.33,1.40,1.41,1.42,1.43,1.44,1.45,1.46,1.47,1.48]                          # Refractive index of the cavity
RISL = 1.5                          # Refractive index of the sensing layer
GW = 0.00653887                     # Gold film thickness (um)    

# Set FIMMWAVE initial values

fimm.Exec("{variables}.setvariable(RI_SL,{RISL})")
fimm.Exec("{variables}.setvariable(Gold_width,{GW})")
fimm.Exec("{variables}.setvariable(SL_thickness,{SLT})")

fimm.Exec("{scanner}.nsteps={steps}")

# Set up scanner parameters
fimm.Exec("{scanner}.xstart={li}")
fimm.Exec("{scanner}.xend={lf}")
fimm.Exec("{scanner}.xlabel=lambda")

for i in range(0,len(CW)):
    fimm.Exec("{variables}.setvariable(Cavity_width,{CW[i]})")
    
    
    for n in range(0,len(RIC)):
        fimm.Exec("{variables}.setvariable(RI_cavity,{RIC[n]})")
    
        fimm.Exec("{scanner}.scan(0,0,1)")

        filename = "C:\Users\joshbrake.LETNET\Dropbox\LETU\LETU M.S.E. Stuff\FIMMWAVE-FIMMPROP Biosensors Stuff\Scripts\Simulation Data\FIMMPROP RI Scanner\RI Scanner " + str(li*1000)+ "-" + str(lf*1000) + " nm " + '%.2f' % CW[i] + " um CW " + '%.2f' % RIC[n] + " RI " + str(GW) + " um GW " + str(steps) + " pts.txt"
        output = open(filename, 'w')

 # Saves results to a file
        for x in xrange(1,steps+1):
            outputpower = fimm.Exec("{scanner}.ydata[{x}].rhspower")        # Read the result
            outputlambda = fimm.Exec("{scanner}.xdata[{x}]")                   # Read in sensing layer thickness
            output.write(str(outputlambda) + ' ' + str(outputpower)+'\n')      # Write the result to the text file we opened

        output.close()  # Close the text file
    
del fimm    # Delete pdApp object