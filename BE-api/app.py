from flask import Flask, jsonify, request
from flask_cors import CORS
from pydub import AudioSegment
import numpy as np
import io
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
CORS(app)
logger = logging.getLogger(__name__)

def calculate_average_db(audio_segment):
    """
    Calculate the average decibel level of the audio segment.
    :param audio_segment: pydub.AudioSegment object
    :return: Average decibel level
    """
    try:
        samples = np.array(audio_segment.get_array_of_samples())
        
        # Handle stereo audio by taking the first channel if needed
        if len(samples.shape) > 1:
            samples = samples[:, 0]
        
        # Ensure we have samples
        if len(samples) == 0:
            logger.warning("No audio samples found")
            return -100  # Return a reasonable default for silence
            
        # Convert to float and normalize to [-1, 1] range
        samples = samples.astype(np.float32)
        max_val = 2**(audio_segment.sample_width * 8 - 1)
        samples = samples / max_val
        
        # Calculate RMS (Root Mean Square) for better loudness representation
        rms = np.sqrt(np.mean(samples**2))
        
        # Avoid log(0) by setting a minimum RMS value
        rms = max(rms, 1e-10)
        
        # Convert RMS to dB (reference: 1.0 = 0dB)
        db_value = 20 * np.log10(rms)
        
        logger.debug(f"RMS: {rms}, Calculated dB: {db_value}")
        return db_value
    except Exception as e:
        logger.error(f"Error calculating average dB: {str(e)}")
        raise

def normalize_db(db_value, original_min=-60, original_max=0, new_min=0, new_max=100):
    """
    Normalize the db_value from original range to new range.
    Default ranges: -60dB to 0dB → 0 to 100 (percentage scale)
    Note: -60dB is a more realistic minimum for typical audio recordings
    """
    try:
        # Clamp the input value to the original range
        db_value = max(min(db_value, original_max), original_min)
        
        # Normalize the db_value from original range to new range
        normalized_value = (db_value - original_min) / (original_max - original_min) * (new_max - new_min) + new_min
        
        # Ensure the value is within the new range
        result = max(min(normalized_value, new_max), new_min)
        logger.debug(f"Normalized {db_value}dB to {result}")
        return result
    except Exception as e:
        logger.error(f"Error normalizing dB value: {str(e)}")
        raise

def calculate_normalized_average_db(audio_segment):
    """
    Calculate and normalize the average dB level of an audio segment.
    Returns a value between 0-100 representing the audio loudness level.
    """
    try:
        average_db = calculate_average_db(audio_segment)
        # Normalize to a 0-100 scale (more meaningful than 0-500)
        normalized_db = normalize_db(average_db)
        logger.debug(f"Normalized average dB: {normalized_db}")
        return normalized_db
    except Exception as e:
        logger.error(f"Error calculating normalized average dB: {str(e)}")
        raise

@app.route('/process-data', methods=['POST'])
def process_data():
    try:
        if 'file' not in request.files:
            logger.warning("No file part in request")
            return jsonify(error='No file part'), 400
            
        file = request.files['file']
        if file.filename == '':
            logger.warning("No file selected")
            return jsonify(error='No selected file'), 400
            
        audio_data = file.read()

        # Log audio data details for debugging
        logger.debug(f"Received audio data type: {type(audio_data)}")
        logger.debug(f"Received audio data length: {len(audio_data)}")
        logger.debug(f"File content type: {file.content_type}")

        # Validate audio data
        if len(audio_data) == 0:
            logger.error("Received empty audio file")
            return jsonify(error='Empty audio file'), 400

        # Process audio with error handling
        try:
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format='wav')
            logger.debug(f"Audio segment created: duration={len(audio_segment)}ms, channels={audio_segment.channels}, sample_rate={audio_segment.frame_rate}, sample_width={audio_segment.sample_width}")
            
            # Additional validation
            if len(audio_segment) == 0:
                logger.error("Audio segment has zero duration")
                return jsonify(error='Audio segment has zero duration'), 400
            
            # Calculate normalized average dB
            average_db = calculate_normalized_average_db(audio_segment)
            logger.info(f"Successfully processed audio, normalized dB: {average_db}")
            
            return jsonify(average_db=average_db, status='success')
            
        except Exception as audio_error:
            logger.error(f"Audio processing error: {str(audio_error)}")
            return jsonify(error=f'Audio processing failed: {str(audio_error)}'), 500
            
    except Exception as e:
        logger.error(f"General processing error: {str(e)}")
        return jsonify(error=f'Processing failed: {str(e)}'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')