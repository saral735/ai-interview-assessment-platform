
import { useEffect, useState } from "react";
import "../../App.css";

import {
  getJobs,
  getCandidates,
  getInterviews,
  getAssessment,
} from "../../services/api";

function RecruiterDashboard() {
  const [candidates, setCandidates] = useState([]);
  const [interviews, setInterviews] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  const [assessment, setAssessment] = useState(null);
  const [assessmentLoading, setAssessmentLoading] = useState(false);
  const [assessmentError, setAssessmentError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setLoading(false);
      return;
    }

    Promise.all([
      getJobs(token),
      getCandidates(token),
      getInterviews(token),
    ])
      .then(([jobsData, candidatesData, interviewsData]) => {
        setJobs(jobsData);
        setCandidates(candidatesData);
        setInterviews(interviewsData);
      })
      .catch((error) => {
        console.error(
          "Failed to fetch dashboard data:",
          error
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const handleAssessment = async (interviewId) => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      return;
    }

    setAssessmentLoading(true);
    setAssessmentError("");
    setAssessment(null);

    try {
      const data = await getAssessment(
        interviewId,
        token
      );

      setAssessment(data);
    } catch (error) {
      console.error(
        "Assessment error:",
        error
      );

      setAssessmentError(
        error instanceof Error
          ? error.message
          : "Failed to generate assessment"
      );
    } finally {
      setAssessmentLoading(false);
    }
  };

  const getResultClass = (result) => {
    if (result === "PASS") {
      return "assessment-result pass";
    }

    if (result === "FAIL") {
      return "assessment-result fail";
    }

    return "assessment-result review";
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
            Jobs
          </div>

          <div className="sidebar-item">
            Candidates
          </div>

          <div className="sidebar-item">
            Interviews
          </div>

          <div className="sidebar-item">
            Assessments
          </div>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="dashboard-main">

        {/* Header */}
        <header className="dashboard-header">
          <div>
            <h1>Recruiter Dashboard</h1>
            <p>
              Manage jobs, candidates and AI interviews.
            </p>
          </div>

          <div className="recruiter-badge">
            Recruiter
          </div>
        </header>

        {/* Overview */}
        <section className="dashboard-section">
          <h2>Overview</h2>

          <div className="stats-grid">

            <div className="stat-card">
              <h3>Total Jobs</h3>
              <p>
                {loading ? "..." : jobs.length}
              </p>
            </div>

            <div className="stat-card">
              <h3>Total Candidates</h3>
              <p>
                {loading ? "..." : candidates.length}
              </p>
            </div>

            <div className="stat-card">
              <h3>Interviews</h3>
              <p>
                {loading ? "..." : interviews.length}
              </p>
            </div>

            <div className="stat-card">
              <h3>Completed</h3>
              <p>
                {loading
                  ? "..."
                  : interviews.filter(
                      (interview) =>
                        interview.status === "COMPLETED"
                    ).length}
              </p>
            </div>

          </div>
        </section>

        {/* Recent Interviews */}
        <section className="dashboard-section">
          <h2>Recent Interviews</h2>

          <div className="activity-card">

            {loading ? (
              <p>Loading interviews...</p>
            ) : interviews.length === 0 ? (
              <p>No interviews available.</p>
            ) : (
              interviews.map((interview) => (
                <div
                  className="interview-card"
                  key={interview.id}
                >
                  <div className="interview-info">
                    <h3>
                      Interview #{interview.id}
                    </h3>

                    <p>
                      <strong>Candidate:</strong>{" "}
                      {interview.candidate_name}
                    </p>

                    <p>
                      <strong>Job:</strong>{" "}
                      {interview.job_title}
                    </p>

                    <p>
                      <strong>Status:</strong>{" "}
                      <span
                        className={`status-badge ${interview.status.toLowerCase()}`}
                      >
                        {interview.status}
                      </span>
                    </p>
                  </div>

                  <button
                    className="assessment-button"
                    onClick={() =>
                      handleAssessment(interview.id)
                    }
                    disabled={assessmentLoading}
                  >
                    {assessmentLoading
                      ? "Generating..."
                      : "View Assessment"}
                  </button>
                </div>
              ))
            )}

          </div>
        </section>

        {/* Assessment Error */}
        {assessmentError && (
          <section className="dashboard-section">
            <div className="assessment-error">
              <strong>Assessment Error</strong>
              <p>{assessmentError}</p>
            </div>
          </section>
        )}

        {/* Assessment Report */}
        {assessment && (
          <section className="dashboard-section">

            <div className="assessment-header">
              <div>
                <h2>Assessment Report</h2>
                <p>
                  Final interview assessment for Interview #
                  {assessment.interview_id}
                </p>
              </div>

              <div
                className={getResultClass(
                  assessment.result
                )}
              >
                {assessment.result}
              </div>
            </div>

            {/* Score Overview */}
            <div className="assessment-grid">

              <div className="assessment-card primary-score">
                <span>Final Score</span>
                <strong>
                  {assessment.final_score}
                </strong>
                <small>
                  out of 100
                </small>
              </div>

              <div className="assessment-card">
                <span>Passing Score</span>
                <strong>
                  {assessment.passing_score}
                </strong>
                <small>
                  required
                </small>
              </div>

              <div className="assessment-card">
                <span>Confidence</span>
                <strong>
                  {assessment.confidence}%
                </strong>
                <small>
                  assessment confidence
                </small>
              </div>

              <div className="assessment-card">
                <span>Evaluated Answers</span>
                <strong>
                  {assessment.evaluated_answers}
                </strong>
                <small>
                  completed evaluations
                </small>
              </div>

            </div>

            {/* Assessment Summary */}
            <div className="assessment-summary">

              <div>
                <h3>Candidate</h3>
                <p>
                  Candidate #{assessment.candidate_id}
                </p>
              </div>

              <div>
                <h3>Job</h3>
                <p>
                  Job #{assessment.job_id}
                </p>
              </div>

              <div>
                <h3>Total Questions</h3>
                <p>
                  {assessment.total_questions}
                </p>
              </div>

              <div>
                <h3>Assessment Status</h3>
                <p className="assessment-status-text">
                  {assessment.result}
                </p>
              </div>

            </div>

          </section>
        )}

        {/* Recent Jobs */}
        <section className="dashboard-section">
          <h2>Recent Jobs</h2>

          <div className="activity-card">

            {loading ? (
              <p>Loading jobs...</p>
            ) : jobs.length === 0 ? (
              <p>No jobs available.</p>
            ) : (
              jobs.map((job) => (
                <div
                  className="job-card"
                  key={job.id}
                >
                  <div>
                    <h3>{job.title}</h3>

                    <p>
                      {job.description}
                    </p>
                  </div>

                  <div className="job-meta">
                    <span>
                      Passing Score:{" "}
                      {job.passing_score}
                    </span>
                  </div>
                </div>
              ))
            )}

          </div>
        </section>

        {/* Candidates */}
        <section className="dashboard-section">
          <h2>Candidates</h2>

          <div className="activity-card">

            {loading ? (
              <p>Loading candidates...</p>
            ) : candidates.length === 0 ? (
              <p>No candidates available.</p>
            ) : (
              candidates.map((candidate) => (
                <div
                  className="candidate-card"
                  key={candidate.id}
                >
                  <div>
                    <h3>{candidate.name}</h3>

                    <p>
                      {candidate.email}
                    </p>
                  </div>

                  <div className="candidate-meta">
                    <span>
                      Candidate #{candidate.id}
                    </span>
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

export default RecruiterDashboard;
