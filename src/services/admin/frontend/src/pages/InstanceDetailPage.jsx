import ResourceDetail from "../components/ResourceDetail";
import HomePage from "./HomePage";

export default function InstanceDetailPage({ match }) {
  // Call API to fetch the instance detail
  const instance = null;

  return (
    <div>
      <HomePage />
      <ResourceDetail resource={instance} type="instance" />
    </div>
  );
}
