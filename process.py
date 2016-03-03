#!/usr/bin/env python

# Run a stabilization analysis pass and transcode to a youtube-friendly format.
# https://github.com/BrettDikeman/bikeopticon
# Copyright 2016, Brett Dikeman brett dikeman gmail com.

# Requires ffmpeg, with VidStab https://github.com/georgmartius/vid.stab
# Currently contains only limited error-checking; intended only for use on embedded, trusted systems.


import getopt, os, shlex, subprocess, sys
import utils
import config

def main(argv):

    input_file = ''
    output_file = ''

    if not 'enable-libvidstab' in subprocess.check_output([FFMPEG_BIN, '-version']):
	    print "You do not have vidstab installed for the specified ffmpeg binary."
	    sys.exit(2)

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["input=","output="])
    except getopt.GetoptError:
        print "Unrecognized options. process.py -i <input_file> -o <output_file>"
        sys.exit(2)
        

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'process.py -i <input_file> -o <output_file>'
            sys.exit()
            
        elif opt in ("-i", "--input"):
            input_file = arg

            try:
                f = open(input_file)
                f.close()
            except IOError as e:
                print('Input video %s unreadable or does not exist.') % input_file
                sys.exit(2)
            
            # split up the input filename for the transforms filename
            input_basename, input_file_extension = os.path.splitext(input_file)
            
            # set default output filename if none is given
            output_file = input_basename + EXTENSION + input_file_extension
            
            # set transform file name
            
            transform_file = input_basename + ".trf"
            
        elif opt in ("-o", "--output"):
            output_file = arg
    
    print 'Input file is', input_file, '; output file is', output_file
    
    # Start ffmpeg work
    
    save_trf = False
    try:
    	# Does the transform file already exist? If so, skip the first pass.   
        if os.path.isfile(transform_file):
            print "TRF file exists, not re-analyzing..."
        else:
            print "Calling ffmpeg vidstab analysis..."
            subprocess.call(shlex.split("%s -i %s -vf %s:result=%s.trf -f null -" % (FFMPEG_BIN, input_file, VIDSTAB_DETECTION_OPTIONS, input_basename)))
        
    except subprocess.CalledProcessError:
        print "ffmpeg analysis call failed."
        if os.path.isfile(transform_file): os.remove(transform_file)
        sys.exit(2)
        
    else:
    	# detection worked; mark the TRF file as valid and do the transform/transcode pass
    	save_trf = True
    	save_output = False
    	
    	print "Calling ffmpeg transform and transcode pass..."
        try:
            save_output = False
            subprocess.call(shlex.split("%s -i %s -vf %s:input=%s.trf %s %s" % (FFMPEG_BIN, input_file, VIDSTAB_TRANSFORM_OPTIONS, input_basename, FFMPEG_TRANSCODE_OPTIONS, output_file)))
        except subprocess.CalledProcessError:
            print "Transform and transcode pass failed."
            sys.exit(2) 
        else:
        	# Transform/transcode worked, transform file no longer needed, keep the output
        	save_trf = False
        	save_output = True
        	
    finally:
    	    if not save_trf:
    		    if os.path.isfile(transform_file): os.remove(transform_file)
    	    if not save_output:
    		    if os.path.isfile(output_file): os.remove(output_file)

    
if __name__ == '__main__':
    main(sys.argv[1:])
