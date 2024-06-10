import ResourceDetail from "../components/ResourceDetail";
import HomePage from "./HomePage";

export default function PlanDetailPage({ match }) {
  // Call API to fetch the plan details
  const plan = null;

  return (
    <div>
      <HomePage />
      <ResourceDetail resource={plan} type="plan" />
    </div>
  );
}
