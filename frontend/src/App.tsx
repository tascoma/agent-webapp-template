import { useEffect, useState } from "react";
import { api } from "./lib/api";

type Health = { status: string };

export default function App() {
  const [status, setStatus] = useState<string>("checking…");

  useEffect(() => {
    api
      .get<Health>("/health")
      .then((data) => setStatus(data.status))
      .catch((err) => setStatus(`error: ${err.message}`));
  }, []);

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: "2rem" }}>
      <h1>Agent Webapp Template</h1>
      <p>
        Backend health: <strong>{status}</strong>
      </p>
      <p style={{ color: "#666" }}>
        Edit <code>src/App.tsx</code> to start building. Run <code>/setup-frontend</code> to
        add routing and auth.
      </p>
    </main>
  );
}
