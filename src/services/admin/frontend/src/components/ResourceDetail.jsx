import InstanceDetail from "./InstanceDetail";
import PlanDetail from "./PlanDetail";

export default function ResourceDetail({ type }) {
  if (type === "plan") {
    return <PlanDetail />;
  }
  return <InstanceDetail />;
}
