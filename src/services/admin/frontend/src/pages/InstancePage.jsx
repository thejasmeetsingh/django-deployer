import ResourceList from "../components/resourceList";
import HomePage from "./HomePage";

export default function InstancePage({ instances }) {
  return (
    <div>
      <HomePage />
      <ResourceList resources={instances} baseURL="instances" />
    </div>
  );
}
