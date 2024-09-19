# Art Timelapse Maker

# Purpose

This program takes videos files and creates a timelapse from them. It has the following capabilities:

- Video and Audio
  - Speed up (or slow down video): Can speed up or slow down videos.
  - Trim: It can trim the videos from the beginning and end.
  - Fade: Can fade the video from the beginning and end.

When processing video and audio it follows this order:

1. Trim the video: First the file will be trimmed.
2. Speed: Second the trimmed file will be sped up or slowed down.
3. Fade: Finally, the file will have fades applied to it.

The modified files will then be combined separately by type.

If you used both video and audio they will be combined together.

Then if you've added extra modifications (resizing and/or compressing the output) it will do that.

# Requirements

- Python
- FFmpeg
  - Including FFprobe which should be installed alongside it

# File Structure

This program uses the following 4 directories:

- video : The directory that stores the source video files.
- audio: The directory that stores the source audio files.
- temp : The directory that stores all the temporary files while creating the output.
- output : The directory that stores the output files.
- settings : The directory that stores the settings file.

You need to use video and/or audio files. If only using 1 of the two it will process it and combine the files. If using both it will process and combine both of them separately and then combine them together. The program will only resize and/or compress the output if you used video or both video and audio, but not if you only used audio.

You can also bypass the entire source processing stage and put files directly into the temp folder. You would do this if you want to combine a collection of video and/or audio, but don't need to modify every file separately. You will still be able to add a fade in and out to the output video and audio doing this option.

You can also bypass the temp processing stage by putting files directly into the output folder. However, would need to name the audio file "audio.wav" and the video file "timelapse.mp4", or if using a file already containing both "timelapse_audio.mp4". You would do this if you only want to resize and/or compress a video.

# Example Use

- python timelapse.py -p -ve -us -uco -th 0 -ovfi 5 -ovfo 5 -oafi 5 -oafo 5 -afi 2 -afo 2
  - Prompts the user to specify clips
  - Uses verbose outputs
  - Uses settings (custom speeds, clips, and fades)
  - Uses a custom order for the files
  - Uses the optimal amount of threads (according to FFmpeg)
  - Adds a 5 second fade in and out to the output combined video with audio
  - Adds a 2 seconds fade in and out to each individual audio track

# Notable Defaults

- Output FPS is 30
- Videos are sped up 30x
- Resolution is 1920 x 1080

# Command Line Arguments

- -h
  - --help
  - show this help message and exit
- -p
  - --prompt
  - Prompts the user about clipping, fading, and speed per file
- -th THREADS
  - --threads THREADS
  - How many threads for ffmpeg to use. If you're unsure what to use pass in 0. Default: -1 to disable
    - The speed of these arguments will depend on your CPU. 0 uses the option FFmpeg deems the best. The following is an example I ran on my computer.
      - -1: 306.6862787
      - 0: 96.3282931
      - 1: 292.42736859999997
      - 2: 131.7168447
      - 3: 116.39917910000001
      - 4: 110.0103064
      - 6: 104.01194459999999
      - 8: 101.6860101
      - 10: 98.0229897
      - 12: 96.73899949999999
      - 14: 95.8332582
      - 16: 94.6499448
- -il IMAGE_LENGTH
  - --image_length IMAGE_LENGTH
  - How many seconds you want images to be by default. Default: 10
- -us
  - --use_settings
  - If you're using any saved settings
- -uco
  - --use_custom_order
  - If you want to use a custom order for the files to be combined
- -ve
  - --verbose
  - Displays in detail the step the program is doing
- -fps OUTPUT_FPS
  - --output_fps OUTPUT_FPS
  - Defines the output video fps. Default: 30
- -sf SPEED_FACTOR
  - --speed_factor SPEED_FACTOR
  - How much do you want to speed up video for the timelapse by. Default: 30
- -asf AUDIO_SPEED_FACTOR
  - --audio_speed_factor AUDIO_SPEED_FACTOR
  - How much do you want to speed up the audio for the timelapse by. Default: 0 to disable
- -pa
  - --preserve_audio
  - Wont remove the audio tracks from the videos.
- -wi WIDTH
  - --width WIDTH
  - The desired output width. Default: 1920
- -he HEIGHT
  - --height HEIGHT
  - The desired output height. Default: 1080
- -v VIDEO_DIRECTORY
  - --video_directory VIDEO_DIRECTORY
  - Path to the video directory. Default: ./video
- -a AUDIO_DIRECTORY
  - --audio_directory AUDIO_DIRECTORY
  - Path to the audio directory. Default: ./audio
- -o OUTPUT_DIRECTORY
  - --output_directory OUTPUT_DIRECTORY
  - Path to the output directory. Default: ./output
- -t TEMP_DIRECTORY
  - --temp_directory TEMP_DIRECTORY
  - Path to the temp directory. Default: ./temp
- -s SETTINGS_DIRECTORY
  - --settings_directory SETTINGS_DIRECTORY
  - Path to the settings directory. Default: /settings
- -osp
  - --override_source_path
  - Will replace the existing source paths ("video" and "audio") in the settings to the current
    directory paths. Useful if you've moved the directories and don't want to update the settings
    file manually with prompts.
- -iac
  - --ignore_audio_check
  - Doesn't stop the process if the audio isn't longer than the video (and audio is used)
- -ktv
  - --keep_temp_video
  - Doesn't delete the temporary video files if passed
- -kta
  - --keep_temp_audio
  - Doesn't delete the temporary audio files if passed
- -vci VIDEO_CLIP_IN
  - --video_clip_in VIDEO_CLIP_IN
  - How many seconds you want to clip from the start of the video by default. Default: 0
- -vco VIDEO_CLIP_OUT
  - --video_clip_out VIDEO_CLIP_OUT
  - How many seconds you want to clip from the end of the video by default. Default: 0
- -vfi VIDEO_FADE_IN
  - --video_fade_in VIDEO_FADE_IN
  - How many seconds you want fade in to the video by default. Default: 0
- -vfo VIDEO_FADE_OUT
  - --video_fade_out VIDEO_FADE_OUT
  - How many seconds you want fade out of the video by default. Default: 0
- -ovfi OUTPUT_VIDEO_FADE_IN
  - --output_video_fade_in OUTPUT_VIDEO_FADE_IN
  - How many seconds you want fade in to the output video. Default: 0
- -ovfo OUTPUT_VIDEO_FADE_OUT
  - --output_video_fade_out OUTPUT_VIDEO_FADE_OUT
  - How many seconds you want fade out of the output video. Default: 0
- -movfi MODIFIED_OUTPUT_VIDEO_FADE_IN
  - --modified_output_video_fade_in MODIFIED_OUTPUT_VIDEO_FADE_IN
  - How many seconds you want fade in to the modified output video. Default: 0
- -movfo MODIFIED_OUTPUT_VIDEO_FADE_OUT
  - --modified_output_video_fade_out MODIFIED_OUTPUT_VIDEO_FADE_OUT
  - How many seconds you want fade out of the modified output video. Default: 0
- -aci AUDIO_CLIP_IN
  - --audio_clip_in AUDIO_CLIP_IN
  - How many seconds you want to clip from the start of the audio by default. Default: 0
- -aco AUDIO_CLIP_OUT
  - --audio_clip_out AUDIO_CLIP_OUT
  - How many seconds you want to clip from the end of the audio by default. Default: 0
- -afi AUDIO_FADE_IN
  - --audio_fade_in AUDIO_FADE_IN
  - How many seconds you want fade in to the audio by default. Default: 0
- -afo AUDIO_FADE_OUT
  - --audio_fade_out AUDIO_FADE_OUT
  - How many seconds you want fade out of the audio by default. Default: 0
- -oafi OUTPUT_AUDIO_FADE_IN
  - --output_audio_fade_in OUTPUT_AUDIO_FADE_IN
  - How many seconds you want fade in to the output audio. Default: 0
- -oafo OUTPUT_AUDIO_FADE_OUT
  - --output_audio_fade_out OUTPUT_AUDIO_FADE_OUT
  - How many seconds you want fade out of the output audio. Default: 0
- -moafi MODIFIED_OUTPUT_AUDIO_FADE_IN
  - --modified_output_audio_fade_in MODIFIED_OUTPUT_AUDIO_FADE_IN
  - How many seconds you want fade in to the modified output audio. Default: 0
- -moafo MODIFIED_OUTPUT_AUDIO_FADE_OUT
  - --modified_output_audio_fade_out MODIFIED_OUTPUT_AUDIO_FADE_OUT
  - How many seconds you want fade out of the modified output audio. Default: 0
- -cl COMPRESSION_LEVEL
  - --compression_level COMPRESSION_LEVEL
  - How compressed do you want the output. Must be from -1 to 52. 0 is the best quality. Default:
    -1 to disable
- -rs RESIZE
  - --resize RESIZE
  - What scale do you want to resize the output. Default: 0 to disable
- -otv
  - --override_temp_video
  - Overrides the temporary video files if passed
- -ota
  - --override_temp_audio
  - Overrides the temporary audio files if passed
- -oo
  - --override_output
  - Overrides the output if passed
- -os
  - --override_settings
  - If you're going to change the settings with a prompt
- -oco
  - --override_custom_order
  - If you're going to change the custom order with a prompt. If the files aren't the exact same
    you will have to override the file regardless.
- -dv
  - --delete_source_video
  - Deletes the source video files if passed
- -da
  - --delete_source_audio
  - Deletes the source audio files if passed
- -ds
  - --delete_settings
  - Deletes the settings file if passed
- -dco
  - --delete_custom_order
  - Deletes the custom order file if passed
- -ctv
  - --clear_temp_video
  - Deletes all the existing temporary video files before creating new files if passed
- -cta
  - --clear_temp_audio
  - Deletes all the existing temporary audio files before creating new files if passed
- -co
  - --clear_output
  - Deletes all the existing output files before creating new files if passed
- -cs
  - --clear_settings
  - Deletes the existing settings before creating new settings if passed
- -cco
  - --clear_custom_order
  - Deletes the existing custom order before creating new settings if passed
- -kuv
  - --keep_unfaded_video
  - Keep the unfaded output video
- -kua
  - --keep_unfaded_audio
  - Keep the unfaded output audio
- -ra
  - --randomize_audio
  - Randomizes the order that audio is combined (to reuse the same audio files for multiple
    timelapses without it getting old)
- -rv
  - --randomize_video
  - Randomizes the order that video is combined (not sure why you would ever want this, but why
    not)
- -dss
  - --dont_save_settings
  - Doesn't save the settings if passed
- -dsco
  - --dont_save_custom_order
  - Doesn't save the custom order if passed
