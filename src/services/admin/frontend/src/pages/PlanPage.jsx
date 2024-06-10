import ResourceList from "../components/resourceList";
import HomePage from "./HomePage";

export default function PlanPage({ plans }) {
  return (
    <div>
      <HomePage />
      <ResourceList resources={plans} baseURL="plans" />
    </div>
  );
}
