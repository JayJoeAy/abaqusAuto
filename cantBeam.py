from abaqus import *
from abaqusConstants import *
import regionToolset

session.viewports['ViewPort:1'].setValues(displayedObject=None)
#---------------
#Create the model
mdb.models.changeKey(fromName='Model-1',toName='Cantilever Beam')
beamModel=mdb.models['Cantilever Beam']
#---------
import sketch 
import part
beamProfileSketch=bemaModel.ConstrainedSketch(name='Beam CS profile',sheetSize=5)
beamProfileSketch = beamModel.ConstrainedSketch('Beam CS Profile', 5) 
beamProfileSketch.rectangle(point1=(0.1,0.1), point2=(0.3,-0.1)) 
beamProfileSketch.rectangle((0.1,0. 1), (0.3,-0.1)) 
beamPart=beamHodel.Part(name='Beam', dimensionality=THREE_D,type=DEFORMABLE_BODY) 
beamPart=beamModel.Part('Beam', THREE_D, DEFORMABLE_BODY)
beamPart.BaseSolidExtrude{sketch:beamProfileSketch, depth=5) 
beamPart.BaseSolidExtrude(beamProfileSketch, 5) 
 # Create material

import material
 # Create material AISI tees Steel by assigning mass density, youngs I # modulus and poissons ratio

beamMaterial = beamModel.Material(name='AISI tees Steel')
beamMaterial.Density(table=((7872, ), ))
beamMaterial.Elastic(table=((200e9,0.29),))
# Create solid section and assign the beam to it
import section
# create a section to assign to the beam
beamSection = beamModel.HomogeneousSolidSection(name='Beam Section',
material='AISI 1ees Steel')
# Assign the beam to this section
beam_region = (beamPart.cells,) 
beamPart .SectionAssignment(beam_region, 'Beam Section' ) 
# Create the assembly
import assembly
# Create the part instance
beamAssembly = beamModel.rootAssembly
beaminstance = beamAssembly.Instance(name='Beam Instance', part=beamPart, dependent=ON)
# Create the step
import step
# Create a static general step
beamModel.StaticStep(name='Apply Load', previous= 'Initial',description='Load is applied during this step') 

# Create the field output request
#Change the name of field output request 'F-Output-1' to 'Selected Field Outputs'
beamModel.fieldOutputRequests.changeKey(fromName='F-Output-1',
toName='Selected Field Outputs')
# Since F-Output-1 is applied at the 'Apply Load' step by default, 'Selected Field
#Outputs' will be too
# We only need to set the required variables
beamModel.fieldOutputRequests['Selected Field Outputs'].setValues(variables=('S','E', 'PEMAG', 'U', 'RF' , 'CF')) 

# Create the history output request
I # We try a slightly different method from that used in field output request #Create a new history output request called 'Default History Outputs' and assign
# both the step and the variables
beamModel.HistoryOutputRequest(name=' Default History Outputs',
createStepName=' Apply Load ' , variables=PRESELECT)
#Now delete the original history output request 'H-Output-1' 
del beamModel. historyOutputRequests['H-Output-1'] 


# Apply pressure load to top surface
I
# First we need to locate and select the top surface
# We place a point somewhere on the top surface based on our knowledge of the
# geometry
top_face_pt_x = 0.2
top_face_pt_y = 0.1
top_face_pt_z = 2. 5
top_face_pt = (top_face_pt_x.top_face_pt_y,top_face_pt_z)
# The face on which that point lies is the face we are looking for
top_face = beamlnstance.faces.findAt((top_face_pt,))
# We extract the region of the face choosing which direction its normal points in
top_face_region=regionToolset.Region(sidelFaces=top_face)
#Apply the pressure load on this region in the 'Apply Load' step
beamModel.Pressure(name='Uniform Applied Pressure', createStepName='Apply Load',region=top_face_region, distributionType=UNIFORM,magnitude=le. amplitude=UNSET) 


# ------------------------------------------------------------ - - ----------
# Apply encastre (fixed) boundary condition to one end to make it cantilever I
I # First we need to locate and select the top surface
# We place a point somewhere on the top surface based on our knowledge of the
# geometry
fixed_end_face_pt_x = 0.2
fixed_end_face_pt_y = 0
fixed_end_face_pt_z = 0
fixed_end_face_pt = (fixed_end_face_pt_x,fixed_end_face_pt_y,fixed_end_face_pt_z) 

fixed_end_face = beaminstance.faces.findAt((fixed_end_face_pt,))
 # we extract the region of the face choosing which direction its normal points in
fixed_end_face_region=regionToolset.Region(faces=fixed_end_face)
beamModel.EncastreBC(name='Encaster one end', createStepName='Initial',region=fixed_end_face_region)

import mesh 

beam_inside_xcoord=0.2
beam_inside_ycoord=0
beam_inside_zcoord=2.5
elemlypel = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD,
kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF,
hourglassControl=DEFAULT, distortionControl=DEFAULT)
beamCells=beamPart.cells
selectedBeamCells=beamCells.findAt((beam_inside_xcoord,beam_inside_ycoord,
beam_inside_zcoord),)
beamMeshRegion=(selectedBeamCells,)
beamPart.setElementType(regions=beamMeshRegion, elemTypes=(elemTypel,))
I beamPart.seedPart(size=e.l, deviationFactor=e.l)
beamPart.generateMesh()


# Create and run the job
import job
# Create the job
mdb.Job(name='CantileverBeamJob', model='Cantilever Beam', type=ANALYSIS,
explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE,
description='Job simulates a loaded cantilever beam',
parallelizationMethodExplicit=DOMAIN, multiprocessingMode=DEFAULT,
numDomains=l, userSubroutine=' ', numCpus=l, memory=Se,
memoryUnits=PERCENTAGE, scratch='', echoPrint=OFF, modelPrint=OFF,
contactPrint=OFF, historyPrint=OFF)
# Run the job
mdb.jobs['CantileverBeamJob').submit(consistencyChecking=OFF)
# Do not return control till job is finished running
mdb.jobs('CantileverBeamJob'].waitForCompletion()
# End of run job 



















