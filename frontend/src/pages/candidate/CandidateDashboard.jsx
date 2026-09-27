
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../../App.css";

import { getCandidateInterviews } from "../../services/api";

function CandidateDashboard() {
  const navigate = useNavigate();

  const [interviews, setInterviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setLoading(false);
      setError("Please login again.");
      return;
    }

    getCandidateInterviews(token)
      .then((data) => {
        setInterviews(data);
      })
      .catch((error) => {
        console.error(
          "Failed to load candidate interviews:",
          error
        );

        setError(
          error instanceof Error
            ? error.message
            : "Failed to load interviews"
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const availableInterviews = interviews.filter(
    (interview) =>
      interview.status === "READY" ||
      interview.status === "CREATED"
  );

  const completedInterviews = interviews.filter(
    (interview) =>
      interview.status === "COMPLETED"
  );

  const latestCompletedInterview =
    completedInterviews.length > 0
      ? completedInterviews[0]
      : null;

  const handleStartInterview = (interviewId) => {
    navigate(`/candidate/interview/${interviewId}`);
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("role");
    localStorage.removeItem("user_id");

    navigate("/login");
  };

  return (
    <div className="dashboard-layout">

      {/* Sidebar */}
      <aside className="sidebar">

        <div className="sidebar-logo">
          AI Interview
        </div>

        <nav>

          <div className="sidebar-item active">
            Dashboard
          </div>

          <div className="sidebar-item">
            Profile
          </div>

          <div className="sidebar-item">
            Resume
          </div>

          <div className="sidebar-item">
            Interviews
          </div>

          <div className="sidebar-item">
            Results
          </div>

        </nav>

      </aside>

      {/* Main Content */}
      <main className="dashboard-main">

        {/* Header */}
        <header className="dashboard-header">

          <div>
            <h1>
              Candidate Dashboard
            </h1>

            <p>
              Manage your profile, resume and AI interviews.
            </p>
          </div>

          <div className="dashboard-header-actions">

            <div className="recruiter-badge">
              Candidate
            </div>

            <button
              className="logout-button"
              onClick={handleLogout}
            >
              Logout
            </button>

          </div>

        </header>

        {/* Error */}
        {error && (
          <section className="dashboard-section">

            <div className="assessment-error">

              <strong>
                Dashboard Error
              </strong>

              <p>
                {error}
              </p>

            </div>

          </section>
        )}

        {/* Overview */}
        <section className="dashboard-section">

          <h2>
            Overview
          </h2>

          <div className="stats-grid">

            <div className="stat-card">

              <h3>
                Resume Status
              </h3>

              <p>
                Uploaded
              </p>

            </div>

            <div className="stat-card">

              <h3>
                Available Interviews
              </h3>

              <p>
                {loading
                  ? "..."
                  : availableInterviews.length}
              </p>

            </div>

            <div className="stat-card">

              <h3>
                Completed Interviews
              </h3>

              <p>
                {loading
                  ? "..."
                  : completedInterviews.length}
              </p>

            </div>

            <div className="stat-card">

              <h3>
                Latest Score
              </h3>

              <p>
                {loading
                  ? "..."
                  : latestCompletedInterview?.final_score !== null &&
                    latestCompletedInterview?.final_score !== undefined
                    ? `${Number(
                        latestCompletedInterview.final_score
                      ).toFixed(2)}%`
                    : "-"}
              </p>

            </div>

          </div>

        </section>

        {/* My Interviews */}
        <section className="dashboard-section">

          <div className="section-heading-row">

            <div>
              <h2>
                My Interviews
              </h2>

              <p className="section-description">
                View your available and completed AI interviews.
              </p>
            </div>

          </div>

          <div className="activity-card">

            {loading ? (

              <div className="empty-state">
                <p>
                  Loading interviews...
                </p>
              </div>

            ) : interviews.length === 0 ? (

              <div className="empty-state">
                <p>
                  No interviews available at the moment.
                </p>
              </div>

            ) : (

              interviews.map((interview) => (

                <div
                  className="interview-card"
                  key={interview.id}
                >

                  {/* Interview Information */}
                  <div className="interview-info">

                    <div className="interview-title-row">

                      <h3>
                        Interview #{interview.id}
                      </h3>

                      <span
                        className={`status-badge ${interview.status.toLowerCase()}`}
                      >
                        {interview.status}
                      </span>

                    </div>

                    <p>
                      <strong>
                        Job:
                      </strong>{" "}
                      {interview.job_title}
                    </p>

                    {/* Completed Interview Details */}
                    {interview.status === "COMPLETED" && (
                      <div className="interview-result-grid">

                        <p>
                          <strong>
                            Score:
                          </strong>{" "}

                          {interview.final_score !== null &&
                          interview.final_score !== undefined
                            ? `${Number(
                                interview.final_score
                              ).toFixed(2)}%`
                            : "-"}
                        </p>

                        <p>
                          <strong>
                            Passing Score:
                          </strong>{" "}

                          {interview.passing_score !== null &&
                          interview.passing_score !== undefined
                            ? `${Number(
                                interview.passing_score
                              ).toFixed(2)}%`
                            : "-"}
                        </p>

                        <p>
                          <strong>
                            Confidence:
                          </strong>{" "}

                          {interview.confidence !== null &&
                          interview.confidence !== undefined
                            ? `${Number(
                                interview.confidence
                              ).toFixed(0)}%`
                            : "-"}
                        </p>

                        <p>
                          <strong>
                            Result:
                          </strong>{" "}

                          {interview.assessment_result || "-"}
                        </p>

                      </div>
                    )}

                  </div>

                  {/* Actions */}
                  <div className="interview-actions">

                    {(interview.status === "READY" ||
                      interview.status === "CREATED") && (

                      <button
                        className="assessment-button"
                        onClick={() =>
                          handleStartInterview(
                            interview.id
                          )
                        }
                      >
                        Start Interview
                      </button>

                    )}

                    {interview.status === "COMPLETED" && (

                      <span className="candidate-completed">
                        Completed
                      </span>

                    )}

                  </div>

                </div>

              ))

            )}

          </div>

        </section>

      </main>

    </div>
  );
}

export default CandidateDashboard;

