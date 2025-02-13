# audio-services
Various functions to work with audios.

## Cut and Crossfade Audio
*Documentation will be provided later*

## Speech-To-Text with Whisper (Require OpenAI API Key)
Add a .env file with your API Key as a param 

```
OPENAI_API_KEY=<your key>
``` 

 - Use flag `--stt`.
 - Specify input path by `--input <your path>`, else default to `./input/input.mp3`
 - Specify output path by `--output <your path>`, else default to `./output/output.txt`