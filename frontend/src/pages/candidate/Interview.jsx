import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "../../App.css";

function Interview() {
  const { interviewId } = useParams();
  const navigate = useNavigate();

  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const [isListening, setIsListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(true);

  const recognitionRef = useRef(null);

  const fetchNextQuestion = async () => {
    const response = await fetch(
      `http://127.0.0.1:8000/interviews/${interviewId}/next-question`
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : "Failed to load question"
      );
    }

    if (!data.question) {
      setQuestion(null);
      return;
    }

    setQuestion(data.question);
  };

  useEffect(() => {
    fetchNextQuestion()
      .catch((error) => {
        console.error(error);

        setError(
          error instanceof Error
            ? error.message
            : "Failed to load interview"
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }, [interviewId]);

  // =========================
  // SPEECH RECOGNITION SETUP
  // =========================

  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setSpeechSupported(false);
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-IN";
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      console.log("Speech recognition started");

      setIsListening(true);
      setError("");
      setMessage("Listening... Please speak your answer.");
    };

    recognition.onresult = (event) => {
      let transcript = "";

      for (
        let i = event.resultIndex;
        i < event.results.length;
        i++
      ) {
        transcript += event.results[i][0].transcript;
      }

      console.log("Speech transcript:", transcript);

      if (transcript.trim()) {
        setAnswer((previousAnswer) => {
          const cleanedPrevious = previousAnswer.trim();

          if (!cleanedPrevious) {
            return transcript.trim();
          }

          return `${cleanedPrevious} ${transcript.trim()}`;
        });
      }
    };

    recognition.onerror = (event) => {
      console.error(
        "Speech recognition error:",
        event.error
      );

      setIsListening(false);

      if (event.error === "not-allowed") {
        setError(
          "Microphone permission was denied. Please allow microphone access."
        );
      } else if (event.error === "no-speech") {
        setError(
          "No speech detected. Please speak clearly and try again."
        );
      } else if (event.error === "audio-capture") {
        setError(
          "Microphone could not be accessed. Please check your microphone."
        );
      } else if (event.error === "network") {
        setError(
          "Speech recognition network error. Please check your internet connection and try again."
        );
      } else {
        setError(
          `Speech recognition error: ${event.error}`
        );
      }
    };

    recognition.onend = () => {
      console.log("Speech recognition ended");
      setIsListening(false);
    };

    recognitionRef.current = recognition;

    return () => {
      try {
        recognition.stop();
      } catch (error) {
        console.error(error);
      }

      recognitionRef.current = null;
    };
  }, []);

  // =========================
  // START VOICE
  // =========================

  const handleStartListening = () => {
    if (!speechSupported) {
      setError(
        "Speech recognition is not supported in this browser."
      );
      return;
    }

    if (!recognitionRef.current) {
      setError(
        "Voice recognition is not available."
      );
      return;
    }

    try {
      setError("");
      setMessage(
        "Listening... Please speak your answer."
      );

      recognitionRef.current.start();
    } catch (error) {
      console.error(
        "Could not start speech recognition:",
        error
      );

      setError(
        "Could not start voice recognition. Please try again."
      );
    }
  };

  // =========================
  // STOP VOICE
  // =========================

  const handleStopListening = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (error) {
        console.error(error);
      }
    }

    setIsListening(false);
    setMessage("Voice input stopped.");
  };

  // =========================
  // SUBMIT ANSWER
  // =========================

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!answer.trim()) {
      setError(
        "Please enter or speak your answer."
      );
      return;
    }

    if (isListening) {
      handleStopListening();
    }

    setSubmitting(true);
    setError("");
    setMessage("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/interviews/${interviewId}/questions/${question.id}/answer?answer_text=${encodeURIComponent(
          answer
        )}`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Failed to submit answer"
        );
      }

      setMessage(
        "Answer submitted successfully."
      );

      setAnswer("");

      await fetchNextQuestion();
    } catch (error) {
      console.error(error);

      setError(
        error instanceof Error
          ? error.message
          : "Failed to submit answer"
      );
    } finally {
      setSubmitting(false);
    }
  };

  // =========================
  // COMPLETE INTERVIEW
  // =========================

  const handleCompleteInterview = async () => {
    setError("");
    setMessage("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/interviews/${interviewId}/complete`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Failed to complete interview"
        );
      }

      setMessage(
        "Interview completed successfully."
      );

      setTimeout(() => {
        navigate("/candidate/dashboard");
      }, 1000);
    } catch (error) {
      console.error(error);

      setError(
        error instanceof Error
          ? error.message
          : "Failed to complete interview"
      );
    }
  };

  // =========================
  // LOADING
  // =========================

  if (loading) {
    return (
      <div className="interview-page">
        <div className="interview-container">
          <h2>Loading Interview...</h2>
        </div>
      </div>
    );
  }

  // =========================
  // UI
  // =========================

  return (
    <div className="interview-page">
      <div className="interview-container">

        <header className="interview-header">
          <div>
            <h1>AI Interview</h1>

            <p>
              Interview #{interviewId}
            </p>
          </div>

          <div className="interview-badge">
            Candidate
          </div>
        </header>

        {error && (
          <div className="interview-error">
            {error}
          </div>
        )}

        {message && (
          <div className="interview-message">
            {message}
          </div>
        )}

        {question ? (
          <section className="question-card">

            <div className="question-top">
              <span>
                Question #{question.question_order}
              </span>

              <span>
                {question.question_type}
              </span>

              <span>
                {question.difficulty}
              </span>
            </div>

            <h2>
              {question.question_text}
            </h2>

            <form onSubmit={handleSubmit}>

              <label htmlFor="answer">
                Your Answer
              </label>

              <textarea
                id="answer"
                value={answer}
                onChange={(event) =>
                  setAnswer(event.target.value)
                }
                placeholder="Type your answer here or use the microphone..."
                rows="8"
                disabled={submitting}
              />

              {/* Voice Controls */}

              {speechSupported ? (
                <div className="voice-controls">

                  {!isListening ? (
                    <button
                      type="button"
                      className="voice-button"
                      onClick={handleStartListening}
                      disabled={submitting}
                    >
                      🎤 Start Voice
                    </button>
                  ) : (
                    <button
                      type="button"
                      className="voice-button listening"
                      onClick={handleStopListening}
                      disabled={submitting}
                    >
                      ⏹ Stop Voice
                    </button>
                  )}

                </div>
              ) : (
                <p className="voice-not-supported">
                  Voice input is not supported in this
                  browser. You can type your answer
                  instead.
                </p>
              )}

              <button
                type="submit"
                className="submit-answer-button"
                disabled={submitting}
              >
                {submitting
                  ? "Evaluating..."
                  : "Submit Answer"}
              </button>

            </form>

          </section>
        ) : (
          <section className="interview-complete-card">

            <h2>
              Interview Completed
            </h2>

            <p>
              You have answered all available questions.
            </p>

            <button
              className="complete-interview-button"
              onClick={handleCompleteInterview}
            >
              Complete Interview
            </button>

          </section>
        )}

      </div>
    </div>
  );
}

export default Interview;