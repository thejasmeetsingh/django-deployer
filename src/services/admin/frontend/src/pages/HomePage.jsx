import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div>
      <div>
        <Link to="/plan">Plans</Link>
      </div>
      <div>
        <Link to="/instance">Instances</Link>
      </div>
      <button>
        <Link to="/logout">Logout</Link>
      </button>
    </div>
  );
}
