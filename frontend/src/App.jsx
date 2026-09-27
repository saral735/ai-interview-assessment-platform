import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import RecruiterDashboard from "./pages/recruiter/RecruiterDashboard";
import CandidateDashboard from "./pages/candidate/CandidateDashboard";
import Interview from "./pages/candidate/Interview";
import ProtectedRoute from "./components/ProtectedRoute";

function Home() {
  return (
    <div>
      <h1>AI Interview Assessment Platform</h1>
      <p>AI-powered interview assessment system</p>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/login" element={<Login />} />

        <Route
          path="/recruiter/dashboard"
          element={
            <ProtectedRoute allowedRole="recruiter">
              <RecruiterDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/candidate/dashboard"
          element={
            <ProtectedRoute allowedRole="candidate">
              <CandidateDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/candidate/interview/:interviewId"
          element={
            <ProtectedRoute allowedRole="candidate">
              <Interview />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;