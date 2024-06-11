import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div>
      <div>
        <Link to="/plans">Plans</Link>
      </div>
      <div>
        <Link to="/instances">Instances</Link>
      </div>
      <button>
        <Link to="/logout">Logout</Link>
      </button>
    </div>
  );
}
