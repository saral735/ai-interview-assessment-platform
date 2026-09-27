const API_BASE_URL = "http://127.0.0.1:8000";

export async function getJobs(token) {
  const response = await fetch(`${API_BASE_URL}/jobs/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch jobs");
  }

  return response.json();
}
export async function getCandidates(token) {
  const response = await fetch(
    `${API_BASE_URL}/candidates/`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch candidates");
  }

  return response.json();
}

export async function getInterviews(token) {
  const response = await fetch(
    `${API_BASE_URL}/interviews/`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch interviews");
  }

  return response.json();
}
export async function getAssessment(interviewId, token) {
  const response = await fetch(
    `${API_BASE_URL}/interviews/${interviewId}/assessment`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    const data = await response.json();

    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Failed to generate assessment"
    );
  }

  return response.json();
}

export async function getCandidateInterviews(token) {
  const response = await fetch(
    `${API_BASE_URL}/interviews/candidate/my-interviews`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    const data = await response.json();

    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Failed to fetch candidate interviews"
    );
  }

  return response.json();
}