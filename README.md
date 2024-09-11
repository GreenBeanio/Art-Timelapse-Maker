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

# File Structure

This program uses the following 4 directories:

- video : The directory that stores the source video files.
- audio: The directory that stores the source audio files.
- temp : The directory that stores all the temporary files while creating the output.
- output : The directory that stores the output files.
- settings : The directory that stores the settings file.

You need to use video and/or audio files. If only using 1 of the two it will process and combine them. If using both it will process and combine both of them separately and then combine them together. The program will only resize and/or compress the output if you used video or both video and audio, but not if you only used audio.

You can also bypass the entire source processing stage and put files directly into the temp folder if all you want to do is combine files. You would do this if you want to combine a collection of video and/or audio, but don't need to modify every file separately. You will still be able to add a fade in and out to the output audio and video doing this option.

You could also bypass the temp processing stage by putting files directly into the output folder. However, would need to name the audio file "audio.wav" and the video file "timelapse.mp4", or if using a file already containing both "timelapse_audio.mp4". You would do this if you only want to resize and/or compress a video. However, you wont be able to add a fade in and out to the video and/or audio this way. If that's your use case put your video file with audio in the temp folder alongside the cli argument to preserve audio.

# Command Line Arguments

----
