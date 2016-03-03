EXTENSION = 'stabyt'                            # suffix added to processed files (STABilized YouTube ready? Ugh...)
FFMPEG_BIN = '/usr/local/bin/ffmpeg'

# Filenames to process when handling a directory
VALID_EXTENSIONS = ('.mov','.MOV','.mp4','.MP4','.avi','.AVI');

# Options to pass to vidstab on the analysis pass, with no leading/trailing spaces.
VIDSTAB_DETECTION_OPTIONS = "vidstabdetect=shakiness=10:accuracy=15:stepsize=12"

# Options for the transform pass, with no leading/trailing spaces.
VIDSTAB_TRANSFORM_OPTIONS = "vidstabtransform=smoothing=30"

# Transcoding options. By default, youtube-friendly with no audio (-an).
# Thanks to Jernej Virag; see https://www.virag.si/2015/06/encoding-videos-for-youtube-with-ffmpeg/

FFMPEG_TRANSCODE_OPTIONS = "-codec:v libx264 -crf 21 -bf 2 -flags +cgop -pix_fmt yuv420p -an -movflags faststart"
