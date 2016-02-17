#!/usr/bin/env python

# Run a stabilization analysis pass and transcode to a youtube-friendly format.
# https://github.com/BrettDikeman/bikeopticon
# Copyright 2016, Brett Dikeman brett dikeman gmail com.

# Requires ffmpeg, with VidStab https://github.com/georgmartius/vid.stab
# Currently contains only limited error-checking; intended only for use on embedded, trusted systems.


import getopt, os, shlex, subprocess, sys

def main(argv):

    inputfile = ''
    outputfile = ''
    extension = 'stabyt'                            # suffix added to processed files (STABilized YouTube ready? Ugh...)
    ffmpeg_bin = '/usr/local/bin/ffmpeg'
    
    # Options to pass to vidstab on the analysis pass, with no leading/trailing spaces.
    vidstab_detection_options = 'vidstabdetect=shakiness=10:accuracy=15:stepsize=12'
    
    # Options for the transform pass, with no leading/trailing spaces.
    vidstab_transform_options = 'vidstabtransform=smoothing=30'
    
    # Transcoding options. By default, youtube-friendly with no audio (-an).
    # Thanks to Jernej Virag; see https://www.virag.si/2015/06/encoding-videos-for-youtube-with-ffmpeg/

    ffmpeg_transcode_options = "-codec:v libx264 -crf 21 -bf 2 -flags +cgop -pix_fmt yuv420p -an -movflags faststart" 

    if not "enable-libvidstab" in subprocess.check_output([ffmpeg_bin, '-version']):
	    print 'You do not have vidstab installed for the specified ffmpeg binary.'
	    sys.exit(2)

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["input=","output="])
    except getopt.GetoptError:
        print 'Unrecognized options. process.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
        

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'process.py -i <inputfile> -o <outputfile>'
            sys.exit()
            
        elif opt in ("-i", "--input"):
            inputfile = arg

            try:
                f = open(inputfile)
                f.close()
            except IOError as e:
                print('Input video %s unreadable or does not exist.') % inputfile
                sys.exit(2)
            
            # split up the input filename for the transforms filename
            input_filename, input_file_extension = os.path.splitext(inputfile)
            
            # set default output filename if none is given
            outputfile = input_filename + extension + input_file_extension
            
        elif opt in ("-o", "--output"):
            outputfile = arg
    
    print 'Input file is', inputfile, '; output file is', outputfile

    print 'Calling ffmpeg vidstab analysis...'
    
    
    try:
        subprocess.call(shlex.split("%s -i %s -vf %s:result=%s.trf -f null -" % (ffmpeg_bin, inputfile, vidstab_detection_options, input_filename)))
        
    except subprocess.CalledProcessError:
        print 'ffmpeg analysis call failed.'
        
    else:
    	# detection worked; do the transform/transcode pass
    	print 'Done. Calling second stage of vidstab processing and transcoding...'
        try:
            subprocess.call(shlex.split("%s -i %s -vf %s:input=%s.trf %s %s" % (ffmpeg_bin, inputfile, vidstab_transform_options, input_filename, ffmpeg_transcode_options, outputfile)))
        except subprocess.CalledProcessError:
            print 'Transform and transcode pass failed.'
            # Remove partially encoded file if it exists
            if os.path.isfile(outputfile): os.remove(outputfile)
            sys.exit(2) 
        else:
            # The transform/transcode worked. We no longer need the TRF file.
    		os.remove(input_filename + ".trf")

    
if __name__ == "__main__":
    main(sys.argv[1:])
