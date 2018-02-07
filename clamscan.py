import os, pyclamd

def scan(filepath):
	if not os.path.exists(filepath):
		return 2, filepath + " not exist"
	
	cd = pyclamd.ClamdAgnostic()
	result = cd.scan_file(filepath)
	
	if (result is not None):
		return 1, result
	else:
		return 0, "No virus found"
