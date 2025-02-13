import os
from services.crossfader import extract_and_crossfade
from services.speech_to_text import speech_to_text
import sys

def service(args):
    service_name = args[0]
    if service_name == "--crossfade":
        extract_and_crossfade(input_file = "./input/test.mp3", 
                          start_time = 8, 
                          end_time = 40, 
                          output_file = "./output/output.mp3", 
                          crossfade_duration=0.5)
    elif service_name == "--stt":
        
        if "--input" in args:
            if len(args) > args.index("--input") + 1:
                audio_file = args[args.index("--input") + 1]
                if not os.path.isfile(audio_file):
                    raise ValueError(f"Invalid input path: {audio_file}")
        else:
            audio_file = "./input/input.mp3"

        result = speech_to_text(audio_file=audio_file)

        if "--output" in args:
            output_path = args[args.index("--output") + 1] if len(args) > args.index("--output") + 1 else None
            if output_path:
                if not os.path.isdir(os.path.dirname(output_path)):
                    raise ValueError(f"Invalid output path: {output_path}")
                with open(output_path, 'w') as f:
                    f.write(result)
            else:
                raise ValueError("Output path not provided for --output flag")
        else:
            with open("./output/output.txt", 'w') as f:
                f.write(result)
            print(result)
    else:
        raise ValueError("Invalid service name")

if __name__ == "__main__":
    args = sys.argv[1:]
    service(args)