import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div>
      <Link to="/plans"></Link>
      <Link to="/instances"></Link>
      <button>
        <Link to="/logout">Logout</Link>
      </button>
    </div>
  );
}
