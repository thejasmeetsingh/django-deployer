import ResourceList from "../components/ResourceList";
import HomePage from "./HomePage";

export default function InstancePage({ instances }) {
  return (
    <div>
      <HomePage />
      <ResourceList resources={instances} baseURL="instances" />
    </div>
  );
}
