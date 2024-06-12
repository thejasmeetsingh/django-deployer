import { Link } from "react-router-dom";

export default function ResourceList({ resources, baseURL }) {
  const renderResource = resources.map((resource, _) => {
    return (
      <div key={resource.id}>
        <Link key={resource.id} to={`/${baseURL}/${resource.id}`}>
          {resource.name}
        </Link>
      </div>
    );
  });

  return <div>{renderResource}</div>;
}
