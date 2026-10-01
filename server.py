"""
Módulo de servidor Flask para la aplicación de detección de emociones.
Proporciona endpoints para analizar texto utilizando IBM Watson NLP.
"""
from flask import Flask, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/emotionDetector")
def emotion_detector_handler():
    """
    Maneja las peticiones web para analizar las emociones de un texto.
    Retorna una cadena formateada con los puntajes o un error 400 si es vacío.
    """
    text_to_analyse = request.args.get("textToAnalyze")
    response = emotion_detector(text_to_analyse)

    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 400

    dominant_emotion = response["dominant_emotion"]

    pure_emotions = response.copy()
    del pure_emotions["dominant_emotion"]

    emotion_list = [f"'{key}': {value}" for key, value in pure_emotions.items()]

    first_part = ", ".join(emotion_list[:-1])
    last_part = emotion_list[-1]

    formatted_response = (
        f"For the given statement, the system response is {first_part} "
        f"and {last_part}. The dominant emotion is {dominant_emotion}."
    )
    return formatted_response, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
