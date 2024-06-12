import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import usePlanContext from "../hooks/use-plan-context";

export default function PlanDetail() {
  const [planName, setPlanName] = useState("");
  const { id } = useParams();
  const { getPlanByID } = usePlanContext();

  useEffect(() => {
    async function fetchPlan() {
      const plan = await getPlanByID(id);
      if (plan) {
        setPlanName(plan.name);
      }
    }
    fetchPlan();
  }, []);

  return (
    <form>
      <label htmlFor="planName">Plan:</label>
      <input
        name="planName"
        id="planName"
        type="planName"
        value={planName}
        onChange={(e) => {
          setPlanName(e.target.value);
        }}
      />
      <button>Save</button>
      <button>Delete</button>
    </form>
  );
}
