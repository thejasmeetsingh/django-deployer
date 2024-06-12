import { useEffect } from "react";
import ResourceList from "../components/ResourceList";
import usePlanContext from "../hooks/use-plan-context";

export default function PlanPage() {
  const { plans, fetchPlans } = usePlanContext();

  useEffect(() => {
    fetchPlans();
  }, []);

  return (
    <div>
      <ResourceList resources={plans} baseURL="plan" />
    </div>
  );
}
