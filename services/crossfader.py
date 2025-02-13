import librosa
import soundfile as sf
import numpy as np

def create_seamless_loop(input_file, output_file, loop_duration=8.0, crossfade_duration=0.5):
    """
    Creates a seamless loop from an audio file with crossfading.
    
    Parameters:
    input_file (str): Path to input audio file
    output_file (str): Path to save the looped audio
    loop_duration (float): Desired duration of the loop in seconds
    crossfade_duration (float): Duration of the crossfade in seconds
    """
    # Load the audio file
    audio, sr = librosa.load(input_file)
    
    # Convert durations to samples
    loop_samples = int(loop_duration * sr)
    fade_samples = int(crossfade_duration * sr)
    
    # Find the best loop point using RMS energy
    hop_length = 512
    rms = librosa.feature.rms(y=audio, hop_length=hop_length)
    
    # Get segments with similar energy levels
    threshold = np.mean(rms)
    similar_segments = np.where(np.abs(rms[0, :-1] - rms[0, 1:]) < threshold)[0]
    
    # Find the best loop point that's close to our desired duration
    target_frame = int((loop_duration * sr) / hop_length)
    loop_point = similar_segments[np.argmin(np.abs(similar_segments - target_frame))] * hop_length
    
    # Extract the loop segment
    loop_segment = audio[:loop_point + fade_samples]
    
    # Apply crossfade
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    
    loop_segment[-fade_samples:] *= fade_out
    loop_segment[:fade_samples] *= fade_in
    
    # Save the result
    sf.write(output_file, loop_segment, sr)
    
    return loop_segment, sr

def create_extended_loop(loop_segment, sr, duration=30.0, output_file="extended_loop.wav"):
    """
    Creates an extended version of the loop for the specified duration.
    
    Parameters:
    loop_segment (np.array): The basic loop segment
    sr (int): Sample rate
    duration (float): Desired duration in seconds
    output_file (str): Output file path
    """
    # Calculate how many times to repeat the loop
    num_repeats = int(np.ceil(duration * sr / len(loop_segment)))
    
    # Create the extended loop
    extended_loop = np.tile(loop_segment, num_repeats)
    
    # Trim to exact duration
    final_samples = int(duration * sr)
    extended_loop = extended_loop[:final_samples]
    
    # Save the result
    sf.write(output_file, extended_loop, sr)
    
    return extended_loop

def extract_and_crossfade(input_file, start_time, end_time, output_file, crossfade_duration=0.5):
    """
    Extracts a region from an audio file, applies crossfading, and exports it.
    
    Parameters:
    input_file (str): Path to input audio file
    start_time (float): Start time in seconds
    end_time (float): End time in seconds
    output_file (str): Path to save the processed audio
    crossfade_duration (float): Duration of crossfade in seconds
    
    Returns:
    tuple: (processed_audio, sample_rate)
    """
    # Load the audio file
    print("Loading audio...")
    audio, sr = librosa.load(input_file)
    
    # Convert times to samples
    start_sample = int(start_time * sr)
    end_sample = int(end_time * sr)
    fade_samples = int(crossfade_duration * sr)
    
    # Extract the region
    print("Extracting region...")
    region = audio[start_sample:end_sample]
    
    # Create crossfade envelopes
    print("Applying crossfade...")
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    
    # Apply crossfade
    region[:fade_samples] *= fade_in
    region[-fade_samples:] *= fade_out
    
    # Save the result
    print("Saving output...")
    sf.write(output_file, region, sr)
    
    return region, sr